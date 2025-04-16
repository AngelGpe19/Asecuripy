# interface/process_window.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from modules.process_monitor import obtener_procesos_sospechosos, info_sistema


class ProcessWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 Monitor de Procesos Sospechosos")
        self.setFixedSize(900, 600)

        layout = QVBoxLayout()

        titulo = QLabel("🧪 Análisis de Procesos en Tiempo Real")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(titulo)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "PID", "Nombre", "Usuario", "Ruta", "Comando", "Inicio"
        ])
        layout.addWidget(self.tabla)

        self.btn_actualizar = QPushButton("🔁 Actualizar Lista de Procesos")
        self.btn_actualizar.clicked.connect(self.actualizar_procesos)
        layout.addWidget(self.btn_actualizar)

        self.setLayout(layout)
        self.actualizar_procesos()

    def actualizar_procesos(self):
        procesos = obtener_procesos_sospechosos()
        self.tabla.setRowCount(len(procesos))

        for fila, proc in enumerate(procesos):
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(proc['pid'])))
            self.tabla.setItem(fila, 1, QTableWidgetItem(proc['nombre']))
            self.tabla.setItem(fila, 2, QTableWidgetItem(proc['usuario']))
            self.tabla.setItem(fila, 3, QTableWidgetItem(str(proc['ruta'])))
            self.tabla.setItem(fila, 4, QTableWidgetItem(proc['comando']))
            self.tabla.setItem(fila, 5, QTableWidgetItem(proc['inicio']))

            if proc['sospechoso']:
                for col in range(6):
                    self.tabla.item(fila, col).setBackground(Qt.red)

        QMessageBox.information(self, "✔️ Proceso Completado", f"Se analizaron {len(procesos)} procesos.")

