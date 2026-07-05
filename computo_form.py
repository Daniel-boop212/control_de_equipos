from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QScrollArea, QComboBox
)


class ComputoForm(QDialog):
    def __init__(self, datos_existentes=None):
        super().__init__()
        self.datos_existentes = datos_existentes
        self.setWindowTitle("Agregar equipo de cómputo")
        self.resize(700, 700)

        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        layout_principal.addWidget(scroll)

        contenido = QWidget()
        scroll.setWidget(contenido)

        self.form = QFormLayout()
        contenido.setLayout(self.form)

        self.inputs = {}
        self.crear_campos()
        if self.datos_existentes:
            self.cargar_datos_existentes()

        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.guardar_datos)
        layout_principal.addWidget(self.btn_guardar)

    def agregar_input(self, nombre):
        campo = QLineEdit()
        self.form.addRow(nombre, campo)
        self.inputs[nombre] = campo

    def crear_campos(self):
        campos = [
            "nombre",
            "marca",
            "proveedor",
            "modelo",
            "serie",
            "fecha_compra",
            "tiempo_garantia",
            "marca_monitor",
            "serie_monitor",
            "marca_teclado",
            "serie_teclado",
            "marca_mouse",
            "serie_mouse",
            "procesador",
            "fecha_mantenimiento",
            "descripcion_mantenimiento",
            "fecha_proximo_mantenimiento",
            "responsable",
            "documento_responsable"
        ]

        for campo in campos:
            self.agregar_input(campo)

        self.tipo = QComboBox()
        self.tipo.addItems([
            "Computador",
            "Televisor",
            "Impresora",
            "Scanner",
            "Servidor",
            "Otro"
        ])
        self.form.addRow("tipo", self.tipo)

    def guardar_datos(self):
        datos = {}

        for nombre, widget in self.inputs.items():
            datos[nombre] = widget.text()

        datos["tipo"] = self.tipo.currentText()

        self.datos_guardados = datos
        self.accept()

    def cargar_datos_existentes(self):
        for nombre, widget in self.inputs.items():
            if nombre in self.datos_existentes:
                widget.setText(str(self.datos_existentes[nombre]))

        if "tipo" in self.datos_existentes:
            self.tipo.setCurrentText(
                self.datos_existentes["tipo"]
            )