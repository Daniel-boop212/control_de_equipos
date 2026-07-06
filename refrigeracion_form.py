from base_form import BaseForm
from PyQt6.QtWidgets import QDateEdit, QComboBox
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDateEdit, QComboBox, QLineEdit
from PyQt6.QtWidgets import QMessageBox

MAPEO_CAMPOS = {
    "imagen_equipo": "imagen",
    "Nombre": "nombre",
    "Marca": "marca",
    "Modelo": "modelo",
    "Serie": "serie",
    "Tipo": "tipo",
    "Capacidad": "capacidad",
    "Fecha de compra": "fecha_compra",
    "Proveedor": "proveedor",
    "Garantía": "garantia",
    "Vida útil": "vida_util",
    "Teléfono del proveedor": "telefono_proveedor",
    "Ubicación": "ubicacion"
}

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

        self.agregar_input("Nombre", obligatorio=True)
        self.agregar_input("Marca", obligatorio=True)
        self.agregar_input("Modelo", obligatorio=True)
        self.agregar_input("Serie", obligatorio=True)

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
        faltante = self.validar_campos_obligatorios([
    "Nombre",
    "Marca",
    "Modelo",
    "Serie"
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

            elif isinstance(widget, QComboBox):
                datos[clave] = widget.currentText()

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

            elif isinstance(widget, QComboBox):
                widget.setCurrentText(str(valor))

            elif isinstance(widget, QLineEdit):
                widget.setText(str(valor))