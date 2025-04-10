from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt
from utils.nmap_checker import get_nmap_path
from modules.port_scanner import run_scan

class ScannerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Escáner de Puertos")
        self.setMinimumSize(500, 600)

        layout = QVBoxLayout()

        # Título
        title = QLabel("🔍 Escáner de Puertos")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        # Mostrar ruta de Nmap
        self.nmap_path_label = QLabel()
        self.nmap_path_label.setStyleSheet("color: green; font-size: 12px;")
        self.update_nmap_path_label()
        layout.addWidget(self.nmap_path_label)

        # Campo para ingresar IP
        self.input_ip = QLineEdit()
        self.input_ip.setPlaceholderText("Introduce la IP o dominio objetivo")
        layout.addWidget(self.input_ip)

        # Combo de tipo de escaneo
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Rápido", "Completo", "Agresivo"])
        layout.addWidget(self.combo_tipo)

        # Botón para escanear
        btn_scan = QPushButton("Iniciar Escaneo")
        btn_scan.clicked.connect(self.ejecutar_escaneo)
        layout.addWidget(btn_scan)

        # Área de resultados
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def update_nmap_path_label(self):
        nmap_path = get_nmap_path()
        if nmap_path:
            self.nmap_path_label.setText(f"✔️ Nmap detectado en: {nmap_path}")
        else:
            self.nmap_path_label.setText("❌ Nmap no detectado. Algunas funciones no estarán disponibles.")
            self.nmap_path_label.setStyleSheet("color: red; font-size: 12px;")

    def ejecutar_escaneo(self):
        objetivo = self.input_ip.text().strip()
        if not objetivo:
            QMessageBox.warning(self, "Campo vacío", "Por favor ingresa una IP o dominio.")
            return

        tipo = self.combo_tipo.currentText().lower()
        tipo_mapeado = {
            "rápido": "fast",
            "completo": "full",
            "agresivo": "aggressive"
        }.get(tipo, "fast")

        self.resultado.setText("⏳ Ejecutando escaneo, por favor espera...")
        salida, error = run_scan(objetivo, tipo_mapeado)

        if error:
            self.resultado.setStyleSheet("color: red;")
            self.resultado.setText(error)
        else:
            self.resultado.setStyleSheet("color: black;")
            self.resultado.setText(salida)
