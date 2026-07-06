from base_form import BaseForm
from PyQt6.QtWidgets import QDateEdit, QComboBox, QLineEdit
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMessageBox

MAPEO = {
    "Nombre": "nombre",
    "Marca": "marca",
    "Modelo": "modelo",
    "Serie": "serie",
    "Fecha compra": "fecha_compra",
    "Garantía": "garantia",
    "Proveedor": "proveedor",
    "Procesador": "procesador",
    "Marca monitor": "marca_monitor",
    "Serie monitor": "serie_monitor",
    "Tipo": "tipo",
    "imagen_equipo": "imagen"
}

class ComputoForm(BaseForm):
    def __init__(self, datos_existentes=None):
        super().__init__("Equipo de cómputo")
        self.agregar_seccion("Imagen")
        self.agregar_selector_imagen("imagen_equipo")

        self.agregar_seccion("Información general")
        self.agregar_input("Nombre", obligatorio=True)
        self.agregar_input("Marca", obligatorio=True)
        self.agregar_input("Modelo", obligatorio=True)
        self.agregar_input("Serie", obligatorio=True)

        self.agregar_seccion("Compra")
        self.agregar_fecha("Fecha compra")
        self.agregar_input("Garantía")
        self.agregar_input("Proveedor")

        self.agregar_seccion("Hardware")
        self.agregar_input("Procesador")
        self.agregar_input("Marca monitor")
        self.agregar_input("Serie monitor")

        self.agregar_combo("Tipo", [
            "Computador",
            "Televisor",
            "Impresora",
            "Scanner",
            "Servidor"
        ])

        self.btn_guardar.clicked.connect(self.guardar)

        if datos_existentes:
            self.cargar_datos_existentes(datos_existentes)

    def guardar(self):
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
            clave = MAPEO.get(nombre)

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

    def cargar_datos_existentes(self, datos):
        for nombre, widget in self.inputs.items():
            clave = MAPEO.get(nombre)

            if not clave or clave not in datos:
                continue

            valor = datos[clave]

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