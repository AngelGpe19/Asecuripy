import socket
import nmap
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QRadioButton, QLineEdit, QHBoxLayout
)


class ScannerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Escáner de Puertos")
        self.setFixedSize(600, 500)

        layout = QVBoxLayout()

        # Título
        titulo = QLabel("🔍 Escaneo de Puertos")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(titulo)

        # Radios para elegir el tipo de escaneo
        radio_layout = QHBoxLayout()
        self.radio_auto = QRadioButton("Escaneo automático (localhost)")
        self.radio_manual = QRadioButton("Escaneo manual")
        self.radio_auto.setChecked(True)

        radio_layout.addWidget(self.radio_auto)
        radio_layout.addWidget(self.radio_manual)
        layout.addLayout(radio_layout)

        # Campo de entrada para IP manual
        self.entrada_ip = QLineEdit()
        self.entrada_ip.setPlaceholderText("Introduce una IP o dominio (ej. 192.168.1.1)")
        self.entrada_ip.setEnabled(False)
        layout.addWidget(self.entrada_ip)

        self.radio_auto.toggled.connect(lambda: self.entrada_ip.setEnabled(not self.radio_auto.isChecked()))

        # Botón para iniciar escaneo
        self.boton_escanear = QPushButton("Iniciar Escaneo")
        self.boton_escanear.setStyleSheet("padding: 10px; font-size: 14px;")
        self.boton_escanear.clicked.connect(self.ejecutar_escaneo)
        layout.addWidget(self.boton_escanear)

        # Tabla de resultados
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Puerto", "Estado", "Servicio"])
        layout.addWidget(self.tabla)

        self.setLayout(layout)

    def ejecutar_escaneo(self):
        # Obtener IP objetivo
        if self.radio_auto.isChecked():
            objetivo = "127.0.0.1"
        else:
            objetivo = self.entrada_ip.text().strip()
            if not objetivo:
                QMessageBox.warning(self, "Falta IP", "Introduce una dirección IP válida.")
                return

        # Verificar si nmap está accesible
        try:
            escaner = nmap.PortScanner()
        except nmap.PortScannerError:
            QMessageBox.critical(self, "Error", "Nmap no está disponible o no se encuentra en el PATH.")
            return

        try:
            # Escaneo básico, puedes escalar con más opciones después
            escaner.scan(hosts=objetivo, arguments='-T4 -F')

            if objetivo not in escaner.all_hosts():
                QMessageBox.warning(self, "Sin respuesta", "No se recibió respuesta del host objetivo.")
                return

            puertos = escaner[objetivo].all_protocols()
            self.tabla.setRowCount(0)

            for protocolo in puertos:
                lport = escaner[objetivo][protocolo].keys()
                for puerto in sorted(lport):
                    estado = escaner[objetivo][protocolo][puerto]['state']
                    servicio = escaner[objetivo][protocolo][puerto].get('name', 'Desconocido')

                    fila = self.tabla.rowCount()
                    self.tabla.insertRow(fila)
                    self.tabla.setItem(fila, 0, QTableWidgetItem(str(puerto)))
                    self.tabla.setItem(fila, 1, QTableWidgetItem(estado.capitalize()))
                    self.tabla.setItem(fila, 2, QTableWidgetItem(servicio.capitalize()))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error inesperado:\n{str(e)}")
