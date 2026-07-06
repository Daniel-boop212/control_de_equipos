from base_form import BaseForm
from PyQt6.QtWidgets import QDateEdit, QComboBox
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QLineEdit, QDateEdit, QComboBox
from PyQt6.QtWidgets import QMessageBox

MAPEO_CAMPOS = {
    "imagen_equipo": "imagen",

    # Información general
    "Código del equipo": "codigo_equipo",
    "R.S.": "rs",
    "Código del prestador": "codigo_prestador",
    "Registro de importación": "registro_importacion",
    "Nombre del equipo": "nombre",
    "Marca": "marca",
    "Modelo": "modelo",
    "Serie": "serie",
    "Ubicación": "ubicacion",

    # Adquisición y proveedor
    "Fecha de adquisición": "fecha_adquisicion",
    "N° de factura": "numero_factura",
    "Fecha de instalación": "fecha_instalacion",
    "Vencimiento de garantía": "vencimiento_garantia",
    "Costo": "costo",
    "Vida útil": "vida_util",
    "Proveedor": "proveedor",
    "Teléfono del proveedor": "telefono_proveedor",
    "Contacto del proveedor": "contacto_proveedor",

    # Especificaciones técnicas
    "Voltaje": "voltaje",
    "Corriente": "corriente",
    "Potencia": "potencia",
    "Frecuencia (Hz)": "frecuencia_hz",
    "Presión": "presion",
    "Velocidad": "velocidad",
    "Temperatura": "temperatura",
    "Peso": "peso",
    "Humedad": "humedad",

    # Configuración
    "Tipo de equipo": "tipo_equipo",
    "Forma de adquisición": "forma_adquisicion",
    "Fuente de alimentación": "fuente_alimentacion",
    "Frecuencia de mantenimiento": "frecuencia_mantenimiento",
    "Requiere calibración": "requiere_calibracion",

    # Recomendaciones
    "Recomendaciones del fabricante": "recomendaciones"
}


class BiomedicoForm(BaseForm):
    def __init__(self, datos_existentes=None):
        super().__init__("Agregar equipo biomédico")

        self.datos_existentes = datos_existentes
        self.crear_campos()

        if self.datos_existentes:
            self.cargar_datos_existentes()

        self.btn_guardar.clicked.connect(self.guardar_datos)

    def crear_campos(self):
        self.agregar_seccion("Imagen")
        self.agregar_selector_imagen("imagen_equipo")

        self.agregar_seccion("Información general")

        self.agregar_input("Código del equipo", obligatorio=True)
        self.agregar_input("R.S.")
        self.agregar_input("Código del prestador")
        self.agregar_input("Registro de importación")
        self.agregar_input("Nombre del equipo", obligatorio=True)
        self.agregar_input("Marca", obligatorio=True)
        self.agregar_input("Modelo", obligatorio=True)
        self.agregar_input("Serie", obligatorio=True)
        self.agregar_input("Ubicación")

        self.agregar_seccion("Adquisición y proveedor")

        self.agregar_fecha("Fecha de adquisición")
        self.agregar_input("N° de factura")
        self.agregar_fecha("Fecha de instalación")
        self.agregar_fecha("Vencimiento de garantía")
        self.agregar_input("Costo")
        self.agregar_input("Vida útil")
        self.agregar_input("Proveedor")
        self.agregar_input("Teléfono del proveedor")
        self.agregar_input("Contacto del proveedor")

        self.agregar_seccion("Especificaciones técnicas")

        for campo in [
            "Voltaje",
            "Corriente",
            "Potencia",
            "Frecuencia (Hz)",
            "Presión",
            "Velocidad",
            "Temperatura",
            "Peso",
            "Humedad"
        ]:
            self.agregar_input(campo)

        self.agregar_seccion("Configuración")

        self.agregar_combo("Tipo de equipo", ["Móvil", "Fijo"])
        self.agregar_combo(
            "Forma de adquisición",
            ["Compra", "Alquiler", "Donación", "Otro"]
        )
        self.agregar_combo(
            "Fuente de alimentación",
            ["Corriente", "Batería", "Otro"]
        )
        self.agregar_combo(
            "Frecuencia de mantenimiento",
            ["Trimestral", "Semestral", "Anual"]
        )
        self.agregar_combo(
            "Requiere calibración",
            ["Sí", "No"]
        )

        self.agregar_seccion("Recomendaciones")
        self.agregar_input("Recomendaciones del fabricante")

    def guardar_datos(self):
        faltante = self.validar_campos_obligatorios([
    "Código del equipo",
    "Nombre del equipo",
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

            # 📅 fecha
            if isinstance(widget, QDateEdit):
                datos[clave] = widget.date().toString("dd/MM/yyyy")

            # 🔽 combo
            elif isinstance(widget, QComboBox):
                datos[clave] = widget.currentText()

            # 📝 texto
            elif isinstance(widget, QLineEdit):
                datos[clave] = widget.text()

            # 🖼 imagen (IMPORTANTE)
            elif isinstance(widget, dict) and widget.get("tipo") == "imagen":
                datos[clave] = widget.get("valor")

            else:
                # fallback seguro
                try:
                    datos[clave] = widget.text()
                except:
                    datos[clave] = ""

        self.datos_guardados = datos
        self.accept()

    def cargar_datos_existentes(self):
        for nombre, widget in self.inputs.items():
            clave = MAPEO_CAMPOS[nombre]

            if clave in self.datos_existentes:
                valor = self.datos_existentes[clave]

                if isinstance(widget, QDateEdit):
                    fecha = QDate.fromString(str(valor), "dd/MM/yyyy")
                    if fecha.isValid():
                        widget.setDate(fecha)

                elif isinstance(widget, QComboBox):
                    widget.setCurrentText(str(valor))

                elif isinstance(self.inputs[nombre], dict):
                    if self.inputs[nombre].get("tipo") == "imagen":
                        if valor:
                            self.inputs[nombre]["valor"] = valor
                            self.inputs[nombre]["widget"].setText("Imagen cargada ✓")

                else:
                    widget.setText(str(valor))