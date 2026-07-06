from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QScrollArea, QComboBox,
    QListWidget, QFileDialog, QLabel
)

MAPEO_CAMPOS = {
    "Código del equipo": "codigo_equipo",
    "R.S.": "rs",
    "Código del prestador": "codigo_prestador",
    "Registro de importación": "registro_importacion",
    "Nombre del equipo": "nombre_equipo",
    "Marca": "marca",
    "Modelo": "modelo",
    "Serie": "serie",
    "Ubicación": "ubicacion",
    "Fecha de adquisición": "fecha_adquisicion",
    "N° de factura": "numero_factura",
    "Fecha de instalación": "fecha_instalacion",
    "Vencimiento de garantía": "vencimiento_garantia",
    "Costo": "costo",
    "Vida útil": "vida_util",
    "Proveedor": "proveedor",
    "Teléfono del proveedor": "telefono_proveedor",
    "Contacto del proveedor": "contacto_proveedor",
    "Voltaje": "voltaje",
    "Corriente": "corriente",
    "Potencia": "potencia",
    "Frecuencia (Hz)": "frecuencia_hz",
    "Presión": "presion",
    "Velocidad": "velocidad",
    "Temperatura": "temperatura",
    "Peso": "peso",
    "Humedad": "humedad",
    "Recomendaciones del fabricante": "recomendaciones",
    "fecha mantenimiento" : "fecha_mantenimiento",
    "fecha proximo mantenimiento" : "fecha_proximo_mantenimiento",
    "responsable": "responsable",
    "documento responsable": "documento_responsable",
    "descripcion mantenimiento": "descripcion_mantenimiento",
}

class BiomedicoForm(QDialog):
    def __init__(self, datos_existentes=None):
        super().__init__()
        self.datos_existentes = datos_existentes

        self.setWindowTitle("Agregar equipo biomédico")
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

    def guardar_datos(self):
        datos = {}

        for nombre_visual, widget in self.inputs.items():
            clave_interna = MAPEO_CAMPOS[nombre_visual]
            datos[clave_interna] = widget.text()

        datos["tipo_equipo"] = self.tipo_equipo.currentText()
        datos["forma_adquisicion"] = self.forma_adquisicion.currentText()
        datos["fuente_alimentacion"] = self.fuente.currentText()
        datos["frecuencia_mantenimiento"] = self.mantenimiento.currentText()
        datos["requiere_calibracion"] = self.calibracion.currentText()

        self.datos_guardados = datos
        self.accept()

    def crear_campos(self):
        campos_texto = [
            "Código del equipo",
            "R.S.",
            "Código del prestador",
            "Registro de importación",
            "Nombre del equipo",
            "Marca",
            "Modelo",
            "Serie",
            "Ubicación",
            "Fecha de adquisición",
            "N° de factura",
            "Fecha de instalación",
            "Vencimiento de garantía",
            "Costo",
            "Vida útil",
            "Proveedor",
            "Teléfono del proveedor",
            "Contacto del proveedor",
            "Voltaje",
            "Corriente",
            "Potencia",
            "Frecuencia (Hz)",
            "Presión",
            "Velocidad",
            "Temperatura",
            "Peso",
            "Humedad",
            "Recomendaciones del fabricante"
        ]

        for campo in campos_texto:
            self.agregar_input(campo)
        self.tipo_equipo = QComboBox()
        self.tipo_equipo.addItems(["Móvil", "Fijo"])
        self.form.addRow("Tipo de equipo", self.tipo_equipo)

        self.forma_adquisicion = QComboBox()
        self.forma_adquisicion.addItems([
            "Compra",
            "Alquiler",
            "Donación",
            "Otro"
        ])
        self.form.addRow("Forma de adquisición", self.forma_adquisicion)

        self.fuente = QComboBox()
        self.fuente.addItems([
            "Corriente",
            "Batería",
            "Otro"
        ])
        self.form.addRow("Fuente de alimentación", self.fuente)

        self.mantenimiento = QComboBox()
        self.mantenimiento.addItems([
            "Trimestral",
            "Semestral",
            "Anual"
        ])
        self.form.addRow("Mantenimiento", self.mantenimiento)

        self.calibracion = QComboBox()
        self.calibracion.addItems(["Sí", "No"])
        self.form.addRow("Requiere calibración", self.calibracion)


    def cargar_datos_existentes(self):
        for nombre_visual, widget in self.inputs.items():
            clave_json = MAPEO_CAMPOS[nombre_visual]

            if clave_json in self.datos_existentes:
                valor = self.datos_existentes[clave_json]
                widget.setText(str(valor))

        if "tipo_equipo" in self.datos_existentes:
            self.tipo_equipo.setCurrentText(
                self.datos_existentes["tipo_equipo"]
            )

        if "forma_adquisicion" in self.datos_existentes:
            self.forma_adquisicion.setCurrentText(
                self.datos_existentes["forma_adquisicion"]
            )

        if "fuente_alimentacion" in self.datos_existentes:
            self.fuente.setCurrentText(
                self.datos_existentes["fuente_alimentacion"]
            )

        if "frecuencia_mantenimiento" in self.datos_existentes:
            self.mantenimiento.setCurrentText(
                self.datos_existentes["frecuencia_mantenimiento"]
            )

        if "requiere_calibracion" in self.datos_existentes:
            self.calibracion.setCurrentText(
             self.datos_existentes["requiere_calibracion"]
            )