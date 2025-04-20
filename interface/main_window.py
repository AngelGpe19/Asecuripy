# interface/main_window.py
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from interface.scanner_window import ScannerWindow  # ← Importamos el módulo
from interface.process_window import ProcessWindow  # Importar ventana de procesos
from interface.wifi_window import WifiAnalyzerWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asecuripy - Centro de Seguridad")
        self.setFixedSize(400, 500)

        layout = QVBoxLayout()

        title = QLabel("🛡️ ASECURIPY")
        title.setFont(QFont("Arial", 20))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 30px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Diccionario de botones y sus acciones
        botones = {
            "Escáner de Puertos": self.abrir_ventana_escaner,
            "Análisis de Procesos":self.abrir_ventana_procesos,
            "Verificar Red WiFi": self.abrir_ventana_wifi,
            "Comprobar Contraseñas": self.ventana_no_disponible,
            "Activar VPN Segura": self.ventana_no_disponible,
            "Generar Reporte de Seguridad": self.ventana_no_disponible
        }

        for texto, accion in botones.items():
            btn = QPushButton(texto)
            btn.setStyleSheet("padding: 10px; font-size: 14px;")
            btn.clicked.connect(accion)
            layout.addWidget(btn)

            
        creditos = QLabel()
        creditos.setTextFormat(Qt.RichText)
        creditos.setTextInteractionFlags(Qt.TextBrowserInteraction)
        creditos.setOpenExternalLinks(True)
        creditos.setAlignment(Qt.AlignCenter)
        creditos.setStyleSheet("""
            QLabel {
                color: #34495e;
                font-size: 12px;
                margin-top: 30px;
            }
            QLabel:hover {
                text-decoration: underline;
            }
        """)
        creditos.setText('© 2025 Angel Guadalupe • <a href="https://github.com/AngelGpe19">github.com/AngelGpe19</a>')
        layout.addWidget(creditos)



        self.setLayout(layout)

        # Guardamos referencia para que no se cierre la ventana secundaria
        self.ventanas_secundarias = []

    def abrir_ventana_escaner(self):
        ventana = ScannerWindow()
        ventana.show()
        self.ventanas_secundarias.append(ventana)  # evitar que se cierre
    
    def abrir_ventana_procesos(self):
        ventana = ProcessWindow()
        ventana.show()
        self.ventanas_secundarias.append(ventana)
    
    def abrir_ventana_wifi (self):
        ventana = WifiAnalyzerWindow ()
        ventana.show ()
        self.ventanas_secundarias.append(ventana)
    
    def ventana_no_disponible(self):
        print("🔧 Esta función aún no está disponible.")  # opcional: QMessageBox más adelante
