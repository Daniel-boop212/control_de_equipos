from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QPushButton, QDateEdit
)
from PyQt6.QtCore import QDate


class MantenimientoForm(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registrar mantenimiento")
        self.resize(400, 300)

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

        # Guardar
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.guardar)
        layout.addWidget(self.btn_guardar)

    def guardar(self):
        self.datos = {
            "fecha": self.fecha.date().toString("yyyy-MM-dd"),
            "tipo": self.tipo.currentText(),
            "descripcion": self.descripcion.text(),
            "responsable": self.responsable.text(),
            "documento_responsable": self.documento.text(),
            "fecha_proxima": self.fecha_proxima.date().toString("yyyy-MM-dd")
        }
        self.accept()