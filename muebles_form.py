from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QScrollArea
)


class MueblesForm(QDialog):
    def __init__(self, datos_existentes=None):
        super().__init__()
        self.datos_existentes = datos_existentes
        self.setWindowTitle("Agregar mueble o enser")
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
            "tipo_elemento",
            "marca",
            "modelo",
            "color",
            "material",
            "cantidad",
            "fecha_compra",
            "garantia",
            "proveedor",
            "telefono_proveedor",
            "fecha_mantenimiento",
            "fecha_proximo_mantenimiento",
            "responsable",
            "documento_responsable"
        ]

        for campo in campos:
            self.agregar_input(campo)

    def guardar_datos(self):
        datos = {}

        for nombre, widget in self.inputs.items():
            datos[nombre] = widget.text()

        self.datos_guardados = datos
        self.accept()

    def cargar_datos_existentes(self):
        for nombre, widget in self.inputs.items():
            if nombre in self.datos_existentes:
                widget.setText(str(self.datos_existentes[nombre]))