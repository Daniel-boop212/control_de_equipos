from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QScrollArea,
    QLabel, QComboBox, QDateEdit
)
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QFileDialog

class BaseForm(QDialog):
    def __init__(self, titulo, width=1100, height=750):
        super().__init__()

        self.inputs = {}
        self.fila_actual = 0
        self.col_actual = 0

        self.setWindowTitle(titulo)
        self.resize(width, height)

        self.setStyleSheet("""
QDialog {
    background: white;
}

QScrollArea, QWidget {
    background: white;
}

QLabel {
    color: #1f2937;
    font-weight: bold;
    font-size: 13px;
}

QLineEdit, QComboBox, QDateEdit {
    background: white;
    color: black;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 8px;
    min-height: 20px;
}

QComboBox QAbstractItemView {
    background: white;
    color: black;
    selection-background-color: #2563eb;
    selection-color: white;
}

QCalendarWidget QWidget {
    background: white;
    color: black;
}

QCalendarWidget QToolButton {
    color: black;
    background: white;
    font-weight: bold;
}

QCalendarWidget QMenu {
    background: white;
    color: black;
}

QCalendarWidget QSpinBox {
    background: white;
    color: black;
}

QCalendarWidget QAbstractItemView {
    background: white;
    color: black;
    selection-background-color: #2563eb;
    selection-color: white;
}

QPushButton {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px;
    font-weight: bold;
}
                           
QTextEdit {
    background: white;
    color: black;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 8px;
}

QPushButton:hover {
    background-color: #1d4ed8;
}
""")

        layout = QVBoxLayout()
        self.setLayout(layout)

        titulo_label = QLabel(titulo)
        titulo_label.setStyleSheet("""
    font-size: 30px;
    font-weight: bold;
    color: #1e3a8a;
    padding: 15px;
""")
        layout.addWidget(titulo_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        contenido = QWidget()
        scroll.setWidget(contenido)

        self.form = QGridLayout()
        self.form.setHorizontalSpacing(20)
        self.form.setVerticalSpacing(12)
        contenido.setLayout(self.form)

        botones = QHBoxLayout()

        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_guardar = QPushButton("Guardar")

        botones.addWidget(self.btn_cancelar)
        botones.addWidget(self.btn_guardar)

        layout.addLayout(botones)
        self.btn_cancelar.clicked.connect(self.reject)
        self.btn_cancelar.setStyleSheet("""
    QPushButton {
        background-color: #ef4444;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #dc2626;
    }
""")

    def agregar_textarea(self, nombre):
        from PyQt6.QtWidgets import QTextEdit

        label = QLabel(nombre)
        area = QTextEdit()
        area.setMinimumHeight(120)

        self.form.addWidget(label, self.fila_actual, 0)
        self.form.addWidget(area, self.fila_actual, 1, 1, 3)

        self.inputs[nombre] = area
        self.fila_actual += 1
        self.col_actual = 0

    def agregar_boton(self, texto, callback):
        btn = QPushButton(texto)
        btn.clicked.connect(callback)

        self.form.addWidget(btn, self.fila_actual, 0, 1, 2)
        self.fila_actual += 1

        return btn
    
    def agregar_selector_imagen(self, nombre, obligatorio=False):
        contenedor = QWidget()
        layout = QHBoxLayout()
        contenedor.setLayout(layout)

        label_archivo = QLabel("Sin imagen")
        boton = QPushButton("Seleccionar imagen")

        self.inputs[nombre] = {
        "tipo": "imagen",
        "widget": label_archivo,
        "valor": None
        }

        def seleccionar():
            archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar imagen",
            "",
            "Imágenes (*.png *.jpg *.jpeg)"
            )

            if archivo:
                label_archivo.setText("Imagen cargada ✓")
                self.inputs[nombre]["valor"] = archivo

        boton.clicked.connect(seleccionar)

        layout.addWidget(boton)
        layout.addWidget(label_archivo)

        label = self.crear_label(nombre, obligatorio)
        self.form.addWidget(label, self.fila_actual, 0)
        self.form.addWidget(contenedor, self.fila_actual, self.col_actual * 2 + 1)

        self._siguiente_posicion()

    def agregar_seccion(self, texto):
        if self.col_actual == 1:
            self.col_actual = 0
            self.fila_actual += 1

        titulo = QLabel(texto)
        titulo.setStyleSheet("""
        font-size: 20px;
        font-weight: bold;
        color: #1e3a8a;
        padding-top: 20px;
        padding-bottom: 10px;
        """)

        self.form.addWidget(titulo, self.fila_actual, 0, 1, 4)
        self.fila_actual += 1

    def _siguiente_posicion(self):
        if self.col_actual == 0:
            self.col_actual = 1
        else:
            self.col_actual = 0
            self.fila_actual += 1

    def agregar_input(self, nombre, obligatorio=False):
        label = self.crear_label(nombre, obligatorio)
        campo = QLineEdit()

        self.form.addWidget(label, self.fila_actual, self.col_actual * 2)
        self.form.addWidget(campo, self.fila_actual, self.col_actual * 2 + 1)

        self.inputs[nombre] = campo
        self._siguiente_posicion()


    def agregar_fecha(self, nombre, obligatorio=False):
        label = self.crear_label(nombre, obligatorio)
        campo = QDateEdit()
        campo.setCalendarPopup(True)
        campo.setDate(QDate.currentDate())
        campo.setDisplayFormat("dd/MM/yyyy")

        self.form.addWidget(label, self.fila_actual, self.col_actual * 2)
        self.form.addWidget(campo, self.fila_actual, self.col_actual * 2 + 1)

        self.inputs[nombre] = campo
        self._siguiente_posicion()

    def agregar_combo(self, nombre, opciones, obligatorio=False):
        label = self.crear_label(nombre, obligatorio)
        combo = QComboBox()
        combo.addItems(opciones)

        self.form.addWidget(label, self.fila_actual, self.col_actual * 2)
        self.form.addWidget(combo, self.fila_actual, self.col_actual * 2 + 1)

        self.inputs[nombre] = combo
        self._siguiente_posicion()

    def cargar_datos_existentes(self, datos):
        for nombre, widget in self.inputs.items():
            if nombre not in datos:
                continue

            valor = datos[nombre]

            if isinstance(widget, QLineEdit):
                widget.setText(str(valor))

            elif isinstance(widget, QComboBox):
                widget.setCurrentText(str(valor))

            elif isinstance(widget, QDateEdit):
                fecha = QDate.fromString(str(valor), "dd/MM/yyyy")
                if fecha.isValid():
                    widget.setDate(fecha)

            elif isinstance(widget, QTextEdit):
                widget.setPlainText(str(valor))

    def obtener_datos(self):
        datos = {}

        for nombre, obj in self.inputs.items():

            # 🔥 caso imagen
            if isinstance(obj, dict) and obj.get("tipo") == "imagen":
                datos[nombre] = obj.get("valor")
                continue

            # widgets normales
            if isinstance(obj, QLineEdit):
                datos[nombre] = obj.text()

            elif isinstance(obj, QComboBox):
                datos[nombre] = obj.currentText()

            elif isinstance(obj, QDateEdit):
                datos[nombre] = obj.date().toString("dd/MM/yyyy")

            elif isinstance(obj, QTextEdit):
                datos[nombre] = obj.toPlainText()

        return datos
    
    def validar_campos_obligatorios(self, campos):
        faltante = None

        estilo_normal = """
        background: white;
        color: black;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 8px;
        min-height: 20px;
    """

        estilo_error = """
        background: #fef2f2;
        color: black;
        border: 2px solid #dc2626;
        border-radius: 8px;
        padding: 8px;
        min-height: 20px;
    """

        for nombre in campos:
            widget = self.inputs[nombre]

            vacio = False

            if isinstance(widget, dict):  # imagen
                vacio = not widget["valor"]
                widget_real = widget["widget"]
            elif hasattr(widget, "text"):
                vacio = widget.text().strip() == ""
                widget_real = widget
            else:
                widget_real = widget

            if vacio:
                if faltante is None:
                    faltante = nombre

                # Pintar rojo
                if hasattr(widget_real, "setStyleSheet"):
                    widget_real.setStyleSheet(estilo_error)
            else:
                # Restaurar estilo normal
                if hasattr(widget_real, "setStyleSheet"):
                    widget_real.setStyleSheet(estilo_normal)

        return faltante
    
    def crear_label(self, nombre, obligatorio=False):
        label = QLabel()

        if obligatorio:
            label.setText(f"{nombre} <span style='color:#dc2626;'>*</span>")
        else:
            label.setText(nombre)

        return label