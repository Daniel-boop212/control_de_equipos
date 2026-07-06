from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QPushButton,
    QDateEdit, QFileDialog, QLabel, QHBoxLayout
)
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QFileDialog

class MantenimientoForm(QDialog):
    def __init__(self, categoria=None):
        super().__init__()
        self.categoria = categoria
        self.setWindowTitle("Registrar mantenimiento")
        self.resize(400, 300)
        self.pdf_mantenimiento = ""
        self.pdf_calibracion = ""

        layout = QVBoxLayout()
        self.setLayout(layout)

        form = QFormLayout()
        layout.addLayout(form)

        # Fecha mantenimiento
        self.fecha = QDateEdit()
        self.fecha.setCalendarPopup(True)
        self.fecha.setDate(QDate.currentDate())
        form.addRow("Fecha mantenimiento", self.fecha)

        # Tipo
        self.tipo = QComboBox()
        self.tipo.addItems([
            "Preventivo",
            "Correctivo",
            "Calibración",
            "Otro"
        ])
        form.addRow("Tipo", self.tipo)

        # Descripción
        self.descripcion = QLineEdit()
        form.addRow("Descripción", self.descripcion)

        # Responsable
        self.responsable = QLineEdit()
        form.addRow("Responsable", self.responsable)

        # Documento responsable
        self.documento = QLineEdit()
        form.addRow("Documento responsable", self.documento)

        # Fecha próximo mantenimiento
        self.fecha_proxima = QDateEdit()
        self.fecha_proxima.setCalendarPopup(True)
        self.fecha_proxima.setDate(QDate.currentDate())
        form.addRow("Próximo mantenimiento", self.fecha_proxima)

        self.pdf_mantenimiento = None
        self.pdf_calibracion = None

        if self.categoria == "Biomédico":
            self.btn_pdf_mant = QPushButton("Cargar PDF mantenimiento")
            self.btn_pdf_mant.clicked.connect(self.cargar_pdf_mantenimiento)
            layout.addWidget(self.btn_pdf_mant)

            self.btn_pdf_cal = QPushButton("Cargar PDF calibración")
            self.btn_pdf_cal.clicked.connect(self.cargar_pdf_calibracion)
            layout.addWidget(self.btn_pdf_cal)

        # Guardar
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.guardar)
        layout.addWidget(self.btn_guardar)

    def cargar_pdf_mantenimiento(self):
        archivo, _ = QFileDialog.getOpenFileName(
        self,
        "Seleccionar PDF",
        "",
        "PDF Files (*.pdf)"
        )

        if archivo:
            self.pdf_mantenimiento = archivo


    def cargar_pdf_calibracion(self):
        archivo, _ = QFileDialog.getOpenFileName(
        self,
        "Seleccionar PDF",
        "",
        "PDF Files (*.pdf)"
        )

        if archivo:
            self.pdf_calibracion = archivo

    def guardar(self):
        self.datos = {
        "fecha": self.fecha.date().toString("yyyy-MM-dd"),
        "tipo": self.tipo.currentText(),
        "descripcion": self.descripcion.text(),
        "responsable": self.responsable.text(),
        "documento_responsable": self.documento.text(),
        "fecha_proxima": self.fecha_proxima.date().toString("yyyy-MM-dd"),
        "pdf_mantenimiento": self.pdf_mantenimiento,
        "pdf_calibracion": self.pdf_calibracion
        }
        self.accept()