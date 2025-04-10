# interface/main_window.py
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from interface.scanner_window import ScannerWindow  # ← Importamos el módulo

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
            "Análisis de Procesos": self.ventana_no_disponible,
            "Verificar Red WiFi": self.ventana_no_disponible,
            "Comprobar Contraseñas": self.ventana_no_disponible,
            "Activar VPN Segura": self.ventana_no_disponible,
            "Generar Reporte de Seguridad": self.ventana_no_disponible
        }

        for texto, accion in botones.items():
            btn = QPushButton(texto)
            btn.setStyleSheet("padding: 10px; font-size: 14px;")
            btn.clicked.connect(accion)
            layout.addWidget(btn)

        self.setLayout(layout)

        # Guardamos referencia para que no se cierre la ventana secundaria
        self.ventanas_secundarias = []

    def abrir_ventana_escaner(self):
        ventana = ScannerWindow()
        ventana.show()
        self.ventanas_secundarias.append(ventana)  # evitar que se cierre

    def ventana_no_disponible(self):
        print("🔧 Esta función aún no está disponible.")  # opcional: QMessageBox más adelante
