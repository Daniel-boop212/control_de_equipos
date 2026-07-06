from base_form import BaseForm
from PyQt6.QtWidgets import QDateEdit
from PyQt6.QtCore import QDate


class MueblesForm(BaseForm):
    def __init__(self, datos_existentes=None):
        super().__init__("Agregar mueble o enser")
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
        self.agregar_input("Tipo de elemento")
        self.agregar_input("Marca")
        self.agregar_input("Modelo")
        self.agregar_input("Color")
        self.agregar_input("Material")
        self.agregar_input("Cantidad")
        self.agregar_input("Estado")   # <- extra para evitar fila impar

        self.agregar_seccion("Compra y proveedor")

        self.agregar_fecha("Fecha de compra")
        self.agregar_input("Garantía")
        self.agregar_input("Proveedor")
        self.agregar_input("Teléfono del proveedor")

    def guardar_datos(self):
        datos = {}

        for nombre, widget in self.inputs.items():
            if isinstance(widget, QDateEdit):
                datos[nombre] = widget.date().toString("dd/MM/yyyy")
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
                else:
                    widget.setText(str(valor))