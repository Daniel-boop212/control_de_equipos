from base_form import BaseForm
from PyQt6.QtWidgets import QDateEdit, QComboBox
from PyQt6.QtCore import QDate


class RefrigeracionForm(BaseForm):
    def __init__(self, datos_existentes=None):
        super().__init__("Equipo de refrigeración")

        self.datos_existentes = datos_existentes

        self.crear_campos()

        if self.datos_existentes:
            self.cargar_datos_existentes()

        self.btn_guardar.clicked.connect(self.guardar_datos)

    def crear_campos(self):
        self.agregar_seccion("Imagen")
        self.agregar_selector_imagen("imagen_equipo")

        self.agregar_seccion("Información general")

        self.agregar_input("Nombre")
        self.agregar_input("Marca")
        self.agregar_input("Modelo")
        self.agregar_input("Serie")

        self.agregar_combo(
            "Tipo",
            [
                "Aire acondicionado",
                "Nevera",
                "Congelador",
                "Otro"
            ]
        )

        self.agregar_input("Capacidad")  # agregado para evitar hueco visual

        self.agregar_seccion("Compra y proveedor")

        self.agregar_fecha("Fecha de compra")
        self.agregar_input("Proveedor")
        self.agregar_input("Garantía")
        self.agregar_input("Vida útil")
        self.agregar_input("Teléfono del proveedor")
        self.agregar_input("Ubicación")  # extra para dejar pares

    def guardar_datos(self):
        datos = {}

        for nombre, widget in self.inputs.items():
            if isinstance(widget, QDateEdit):
                datos[nombre] = widget.date().toString("dd/MM/yyyy")
            elif isinstance(widget, QComboBox):
                datos[nombre] = widget.currentText()
            else:
                datos[nombre] = widget.text()

        self.datos_guardados = datos
        self.accept()

    def cargar_datos_existentes(self):
        for nombre, widget in self.inputs.items():
            if nombre in self.datos_existentes:
                valor = self.datos_existentes[nombre]

                if isinstance(widget, QDateEdit):
                    fecha = QDate.fromString(str(valor), "dd/MM/yyyy")
                    if fecha.isValid():
                        widget.setDate(fecha)

                elif isinstance(widget, QComboBox):
                    widget.setCurrentText(str(valor))

                else:
                    widget.setText(str(valor))