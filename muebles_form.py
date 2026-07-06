from base_form import BaseForm
from PyQt6.QtWidgets import QDateEdit, QLineEdit
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMessageBox

MAPEO_CAMPOS = {
    "imagen_equipo": "imagen",
    "Nombre": "nombre",
    "Tipo de elemento": "tipo_elemento",
    "Marca": "marca",
    "Modelo": "modelo",
    "Color": "color",
    "Material": "material",
    "Cantidad": "cantidad",
    "Estado": "estado_mueble",
    "Fecha de compra": "fecha_compra",
    "Garantía": "garantia",
    "Proveedor": "proveedor",
    "Teléfono del proveedor": "telefono_proveedor"
}


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
        self.agregar_input("Nombre", obligatorio=True)
        self.agregar_input("Tipo de elemento", obligatorio=True)
        self.agregar_input("Marca")
        self.agregar_input("Modelo")
        self.agregar_input("Color")
        self.agregar_input("Material")
        self.agregar_input("Cantidad")
        self.agregar_input("Estado")

        self.agregar_seccion("Compra y proveedor")
        self.agregar_fecha("Fecha de compra")
        self.agregar_input("Garantía")
        self.agregar_input("Proveedor")
        self.agregar_input("Teléfono del proveedor")

    def guardar_datos(self):
        faltante = self.validar_campos_obligatorios([
    "Nombre",
    "Tipo de elemento"
        ])

        if faltante:
            QMessageBox.warning(
    self,
    "Campo obligatorio",
    f"Falta llenar: {faltante}"
)
            return
        datos = {}

        for nombre, widget in self.inputs.items():
            clave = MAPEO_CAMPOS.get(nombre)

            if not clave:
                continue

            if isinstance(widget, dict) and widget.get("tipo") == "imagen":
                datos[clave] = widget["valor"]

            elif isinstance(widget, QDateEdit):
                datos[clave] = widget.date().toString("dd/MM/yyyy")

            elif isinstance(widget, QLineEdit):
                datos[clave] = widget.text()

        self.datos_guardados = datos
        self.accept()

    def cargar_datos_existentes(self):
        for nombre, widget in self.inputs.items():
            clave = MAPEO_CAMPOS.get(nombre)

            if not clave or clave not in self.datos_existentes:
                continue

            valor = self.datos_existentes[clave]

            if isinstance(widget, dict) and widget.get("tipo") == "imagen":
                widget["valor"] = valor
                widget["widget"].setText("Imagen cargada ✓")

            elif isinstance(widget, QDateEdit):
                fecha = QDate.fromString(str(valor), "dd/MM/yyyy")
                if fecha.isValid():
                    widget.setDate(fecha)

            elif isinstance(widget, QLineEdit):
                widget.setText(str(valor))