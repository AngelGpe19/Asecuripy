# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
from modules.password_audit import obtener_contraseñas_navegadores, evaluar_contraseñas

class PasswordAuditWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auditoría de Contraseñas")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        self.label_info = QLabel("Haz clic en 'Analizar' para revisar las contraseñas almacenadas en tus navegadores.")
        layout.addWidget(self.label_info)

        self.boton_analizar = QPushButton("Analizar")
        self.boton_analizar.clicked.connect(self.analizar_contrasenas)
        layout.addWidget(self.boton_analizar)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def analizar_contrasenas(self):
        try:
            contrasenas = obtener_contraseñas_navegadores()
            if not contrasenas:
                self.resultado.setText("No se encontraron contraseñas almacenadas o no se pudo acceder a ellas.")
                return

            # ✅ Evaluar TODAS las contraseñas de una vez
            evaluaciones = evaluar_contraseñas(contrasenas)

            resultados = []
            for evaluacion in evaluaciones:
                resultado = f"""
🌐 Sitio: {evaluacion.get('sitio', 'Desconocido')}
👤 Usuario: {evaluacion.get('usuario', 'N/A')}
🔐 Seguridad: {'✅ Segura' if evaluacion['es_segura'] else '❌ Insegura'}
🧪 Detalles: {evaluacion['motivo']}
--------------------------------------
"""
                resultados.append(resultado)

            self.resultado.setText("\n".join(resultados))

        except Exception as e:
            self.resultado.setText(f"❌ Ocurrió un error durante el análisis: {str(e)}")
