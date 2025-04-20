from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from modules.process_monitor import obtener_procesos_clasificados, guardar_log_sospechosos

class ProcessWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitoreo de Procesos")
        self.resize(800, 500)

        layout = QVBoxLayout()
        self.label_info = QLabel("Procesos analizados con clasificación de comportamiento.")
        layout.addWidget(self.label_info)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["PID", "Nombre", "Ruta", "Clasificación", "Score"])
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.cargar_datos()

    def cargar_datos(self):
        procesos = obtener_procesos_clasificados()
        guardar_log_sospechosos(procesos)

        self.table.setRowCount(len(procesos))

        for fila, proc in enumerate(procesos):
            self.table.setItem(fila, 0, QTableWidgetItem(str(proc["pid"])))
            self.table.setItem(fila, 1, QTableWidgetItem(proc["nombre"]))
            self.table.setItem(fila, 2, QTableWidgetItem(proc["ruta"]))
            self.table.setItem(fila, 3, QTableWidgetItem(proc["clasificacion"]))
            self.table.setItem(fila, 4, QTableWidgetItem(str(proc["score"])))

            # Resaltar la fila según clasificación
            if proc["clasificacion"] == "Sospechoso":
                self.colorear_fila(fila, QColor(255, 102, 102))  # rojo suave
            elif proc["clasificacion"] == "Alto Consumo":
                self.colorear_fila(fila, QColor(255, 255, 153))  # amarillo
            else:
                self.colorear_fila(fila, QColor(204, 255, 204))  # verde suave

    def colorear_fila(self, fila, color):
        for col in range(self.table.columnCount()):
            self.table.item(fila, col).setBackground(color)
            self.table.item(fila, col).setTextAlignment(Qt.AlignCenter)
