from PyQt6.QtWidgets import QFileDialog
from base_form import BaseForm


class MantenimientoForm(BaseForm):
    def __init__(self, categoria=None, datos_existentes=None):
        super().__init__("Registrar mantenimiento", 1000, 700)

        self.categoria = categoria
        self.datos_existentes = datos_existentes
        self.pdf_mantenimiento = None
        self.pdf_calibracion = None

        self.crear_campos()

        if datos_existentes:
            self.cargar_datos_existentes(datos_existentes)

            self.pdf_mantenimiento = datos_existentes.get("pdf_mantenimiento")
            self.pdf_calibracion = datos_existentes.get("pdf_calibracion")

        self.btn_guardar.clicked.connect(self.guardar)

    def crear_campos(self):
        # ================= INFO =================
        self.agregar_seccion("Información del mantenimiento")

        self.agregar_fecha("fecha")
        self.agregar_combo("tipo", [
            "Preventivo",
            "Correctivo",
            "Calibración",
            "Otro"
        ])
        self.agregar_fecha("fecha_proxima")

        # ================= RESPONSABLE =================
        self.agregar_seccion("Responsable")

        self.agregar_input("responsable")
        self.agregar_input("documento_responsable")

        # ================= DESCRIPCIÓN =================
        self.agregar_seccion("Descripción")
        self.agregar_textarea("descripcion")

        # ================= PDFs BIOMÉDICO =================
        if self.categoria == "Biomédico":
            self.agregar_seccion("Documentos adjuntos")

            self.btn_pdf_mant = self.agregar_boton(
                "Cargar PDF mantenimiento",
                self.cargar_pdf_mantenimiento
            )

            self.btn_pdf_cal = self.agregar_boton(
                "Cargar PDF calibración",
                self.cargar_pdf_calibracion
            )

    def cargar_pdf_mantenimiento(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar PDF",
            "",
            "PDF Files (*.pdf)"
        )

        if archivo:
            self.pdf_mantenimiento = archivo
            self.btn_pdf_mant.setText(
                f"PDF mantenimiento ✓"
            )

    def cargar_pdf_calibracion(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar PDF",
            "",
            "PDF Files (*.pdf)"
        )

        if archivo:
            self.pdf_calibracion = archivo
            self.btn_pdf_cal.setText(
                f"PDF calibración ✓"
            )

    def guardar(self):
        datos = self.obtener_datos()

        datos["pdf_mantenimiento"] = self.pdf_mantenimiento
        datos["pdf_calibracion"] = self.pdf_calibracion

        self.datos = datos
        self.accept()