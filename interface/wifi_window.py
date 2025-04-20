from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QProgressBar, QApplication, QTextEdit
)
from PyQt5.QtCore import QThread, pyqtSignal
import sys

from modules.wifi_analyzer import (
    obtener_gateway,
    obtener_ip_local,
    obtener_interfaces_activas,
    obtener_redes_disponibles,
    verificar_cifrado_red,
    detectar_spoofing_arp,
    escanear_dispositivos_red,
    analizar_canal_wifi
)

class WifiAnalyzerThread(QThread):
    update_signal = pyqtSignal(str)

    def run(self):
        try:
            self.update_signal.emit("🔄 Iniciando análisis de red...\n")

            gateway = obtener_gateway()
            self.update_signal.emit(f"📍 Gateway: {gateway if gateway else 'No disponible'}\n")

            ip_local = obtener_ip_local()
            self.update_signal.emit(f"🌐 IP Local: {ip_local if ip_local else 'No disponible'}\n")

            interfaces = obtener_interfaces_activas()
            if interfaces:
                for interfaz in interfaces:
                    self.update_signal.emit(f"📡 Interfaz: {interfaz['nombre']} | IP: {interfaz['ip']}\n")
            else:
                self.update_signal.emit("📡 No se detectaron interfaces activas.\n")

            self.update_signal.emit("🔎 Escaneando redes WiFi disponibles...\n")
            redes_wifi = obtener_redes_disponibles()
            self.update_signal.emit(f"🛰️ Resultado crudo: \n{redes_wifi[:500]}...\n")

            cifrados = verificar_cifrado_red()
            self.update_signal.emit(f"🔐 Cifrados detectados: {dict(cifrados)}\n")

            spoofing = detectar_spoofing_arp()
            if spoofing:
                self.update_signal.emit(f"⚠️ Posible ARP Spoofing detectado - MACs duplicadas: {', '.join(spoofing)}\n")
            else:
                self.update_signal.emit("✅ No se detectaron duplicaciones de MAC sospechosas.\n")

            dispositivos = escanear_dispositivos_red()
            self.update_signal.emit(f"💻 Dispositivos activos en la red: {len(dispositivos)} encontrados\n")
            if dispositivos:
                self.update_signal.emit(f"📋 IPs: {', '.join(dispositivos)}\n")

            canales = analizar_canal_wifi()
            self.update_signal.emit(f"📡 Canales WiFi detectados: {dict(canales)}\n")

            self.update_signal.emit("✅ Análisis de red completado exitosamente.\n")
        except Exception as e:
            self.update_signal.emit(f"[❌] Error durante el análisis: {str(e)}\n")

class WifiAnalyzerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔍 Analizador de Red WiFi")
        self.setGeometry(100, 100, 800, 500)

        self.layout = QVBoxLayout()

        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setPlaceholderText("Los resultados del análisis aparecerán aquí...")

        self.start_button = QPushButton("🚀 Iniciar Análisis WiFi")
        self.start_button.clicked.connect(self.start_wifi_analysis)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminado

        self.layout.addWidget(self.status_text)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)

    def start_wifi_analysis(self):
        self.status_text.clear()
        self.thread = WifiAnalyzerThread()
        self.thread.update_signal.connect(self.update_ui)
        self.thread.finished.connect(self.analysis_finished)
        self.thread.start()

    def update_ui(self, message):
        print(f"[LOG] {message.strip()}")
        self.status_text.append(message)

    def analysis_finished(self):
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        self.status_text.append("🎉 Análisis finalizado.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WifiAnalyzerWindow()
    window.show()
    sys.exit(app.exec_())
