import json
import os

from PyQt6.QtWidgets import QFrame, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QComboBox, QPushButton, QLabel,
    QListWidget, QTableWidget, QTableWidgetItem,
    QTabWidget, QTextEdit, QInputDialog,
    QMessageBox
)
from PyQt6.QtGui import QColor
from biomedico_form import BiomedicoForm
from computo_form import ComputoForm
from refrigeracion_form import RefrigeracionForm
from muebles_form import MueblesForm
from models.mantenimiento import Mantenimiento
from mantenimiento_form import MantenimientoForm

FORMULARIOS = {
    "Biomédico": BiomedicoForm,
    "Cómputo": ComputoForm,
    "Refrigeración": RefrigeracionForm,
    "Muebles y enseres": MueblesForm
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión Clínica")
        self.resize(1200, 700)
        self.setStyleSheet("""
QMainWindow {
    background-color: #1e1e2f;
    color: #eaeaea;
}

QPushButton {
    background-color: #2b2b3c;
    border: 1px solid #3d3d55;
    padding: 8px;
    border-radius: 8px;
    color: white;
}

QPushButton:hover {
    background-color: #3a3a55;
}

QTableWidget {
    background-color: #252536;
    border: none;
    gridline-color: #3a3a55;
}

QHeaderView::section {
    background-color: #2b2b3c;
    color: white;
    padding: 6px;
    border: none;
}

QTextEdit {
    background-color: #252536;
    border-radius: 6px;
    padding: 8px;
}
""")
        self.equipos_visibles = []

        # ================= WIDGET CENTRAL =================
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # ================= PANEL IZQUIERDO =================
        self.lista_servicios = QListWidget()
        self.cargar_servicios_json()
        self.actualizar_servicios()
        self.lista_servicios.setMaximumWidth(250)
        self.lista_servicios.itemClicked.connect(self.filtrar_por_servicio)

        main_layout.addWidget(self.lista_servicios)
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        self.btn_agregar_servicio = QPushButton("Agregar servicio")
        self.btn_borrar_servicio = QPushButton("Borrar servicio")

        left_layout.addWidget(self.btn_agregar_servicio)
        left_layout.addWidget(self.btn_borrar_servicio)

        self.btn_agregar_servicio.clicked.connect(self.agregar_servicio)
        self.btn_borrar_servicio.clicked.connect(self.borrar_servicio)

        # ================= PANEL DERECHO =================
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout)

        # ---------- Parte superior ----------
        right_layout.addWidget(QLabel("Categoría"))

        self.combo_categoria = QComboBox()
        self.combo_categoria.addItems([
            "Biomédico",
            "Cómputo",
            "Refrigeración",
            "Muebles y enseres"
        ])
        right_layout.addWidget(self.combo_categoria)

        toolbar = QFrame()
        toolbar_layout = QHBoxLayout()
        toolbar.setLayout(toolbar_layout)
        toolbar.setStyleSheet("border: none;")

        self.btn_agregar = QPushButton("＋ Agregar")
        self.btn_editar = QPushButton("✎ Editar")
        self.btn_mantenimiento = QPushButton("🛠 Mantenimiento")
        self.btn_borrar = QPushButton("🗑 Borrar")

        self.btn_agregar.clicked.connect(self.abrir_formulario)
        self.btn_editar.clicked.connect(self.editar_equipo)
        self.btn_mantenimiento.clicked.connect(self.registrar_mantenimiento)
        self.btn_borrar.clicked.connect(self.borrar_equipo)

        toolbar_layout.addWidget(self.btn_agregar)
        toolbar_layout.addWidget(self.btn_editar)
        toolbar_layout.addWidget(self.btn_mantenimiento)
        toolbar_layout.addWidget(self.btn_borrar)
        toolbar_layout.addStretch()

        right_layout.addWidget(toolbar)

        # ---------- Tabla de equipos ----------
        right_layout.addWidget(QLabel("Equipos del servicio"))

        self.tabla_equipos = QTableWidget()
        self.tabla_equipos.setColumnCount(3)
        self.tabla_equipos.setHorizontalHeaderLabels([
            "Equipo", "Categoría", "Estado"
        ])

        right_layout.addWidget(self.tabla_equipos)

        # ---------- Panel inferior ----------
        self.tabs = QTabWidget()

        # Pestaña hoja de vida
        self.tab_hoja_vida = QTextEdit()
        self.tab_hoja_vida.setReadOnly(True)
        self.tab_hoja_vida.setText("Aquí aparecerá la hoja de vida del equipo.")

        # Pestaña mantenimientos
        self.tab_mantenimientos = QTextEdit()
        self.tab_mantenimientos.setReadOnly(True)
        self.tab_mantenimientos.setText("Aquí aparecerá el historial de mantenimientos.")

        self.tabs.addTab(self.tab_hoja_vida, "Hoja de vida")
        self.tabs.addTab(self.tab_mantenimientos, "Documentos")

        right_layout.addWidget(self.tabs)

        # Cargar datos de prueba

        self.cargar_equipos_json()
        self.actualizar_tabla()
        self.actualizar_servicios()
        self.filtrar_por_servicio()
        self.tabla_equipos.cellClicked.connect(self.mostrar_equipo)

    def abrir_formulario(self):
        categoria = self.combo_categoria.currentText()

        if categoria == "Biomédico":
            ventana = BiomedicoForm()
            resultado = ventana.exec()

            if resultado:
                datos = ventana.datos_guardados

                servicio = self.lista_servicios.currentItem()
                if servicio:
                    datos["servicio"] = servicio.text()
                else:
                    datos["servicio"] = "Sin asignar"

                datos["categoria"] = "Biomédico"
                datos["estado"] = self.obtener_estado_equipo(datos)

                self.guardar_equipo_json(datos)
                print("Equipo guardado")

        elif categoria == "Cómputo":
            ventana = ComputoForm()
            resultado = ventana.exec()

            if resultado:
                datos = ventana.datos_guardados

                servicio = self.lista_servicios.currentItem()
                if servicio:
                    datos["servicio"] = servicio.text()
                else:
                    datos["servicio"] = "Sin asignar"

                datos["categoria"] = "Cómputo"
                datos["estado"] = "🔵"

                self.guardar_equipo_json(datos)

        elif categoria == "Refrigeración":
            ventana = RefrigeracionForm()
            resultado = ventana.exec()

            if resultado:
                datos = ventana.datos_guardados

                servicio = self.lista_servicios.currentItem()
                if servicio:
                    datos["servicio"] = servicio.text()
                else:
                    datos["servicio"] = "Sin asignar"

                datos["categoria"] = "Refrigeración"
                datos["estado"] = "🔵"

                self.guardar_equipo_json(datos)

        elif categoria == "Muebles y enseres":
            ventana = MueblesForm()
            resultado = ventana.exec()

            if resultado:
                datos = ventana.datos_guardados

                servicio = self.lista_servicios.currentItem()
                if servicio:
                    datos["servicio"] = servicio.text()
                else:
                    datos["servicio"] = "Sin asignar"

                datos["categoria"] = "Muebles y enseres"
                datos["estado"] = "🔵"

                self.guardar_equipo_json(datos)

    def cargar_equipos_json(self):
        ruta = "data/equipos.json"

        if not os.path.exists(ruta):
            self.equipos = []
            return

        with open(ruta, "r", encoding="utf-8") as archivo:
            self.equipos = json.load(archivo)
            for equipo in self.equipos:
                equipo["estado"] = self.obtener_estado_equipo(equipo)

            for equipo in self.equipos:
                if "mantenimientos" not in equipo:
                    equipo["mantenimientos"] = []

    def actualizar_tabla(self, lista=None):
        if lista is None:
            lista = self.equipos

        self.tabla_equipos.setRowCount(len(lista))
        self.equipos_visibles = lista

        for fila, equipo in enumerate(lista):
            nombre = equipo.get(
            "nombre_equipo",
            equipo.get("nombre", "Sin nombre")
            )
            categoria = equipo.get("categoria", "")
            estado = equipo.get("estado", "")

            if estado == "🔴":
                color = QColor(255, 120, 120, 120)
            elif estado == "🟡":
                color = QColor(255, 230, 120, 120)
            elif estado == "🟢":
                color = QColor(120, 255, 160, 120)
            elif estado == "🔵":
                color = QColor(120, 180, 255, 120)
            else:
                color = QColor(220, 220, 220, 80)

            item_nombre = QTableWidgetItem(nombre)
            item_categoria = QTableWidgetItem(categoria)
            item_estado = QTableWidgetItem(estado)

            item_nombre.setBackground(color)
            item_categoria.setBackground(color)
            item_estado.setBackground(color)

            self.tabla_equipos.setItem(fila, 0, item_nombre)
            self.tabla_equipos.setItem(fila, 1, item_categoria)
            self.tabla_equipos.setItem(fila, 2, item_estado)

    def mostrar_equipo(self, fila, columna):
        equipo = self.equipos_visibles[fila]

        # ================= HOJA DE VIDA =================
        texto_hoja = "HOJA DE VIDA DEL EQUIPO\n"
        texto_hoja += "────────────────────────────\n\n"

        for clave, valor in equipo.items():
            if clave in [
            "mantenimientos",
            "pdf_mantenimiento",
            "pdf_calibracion"
            ]:
                continue

            texto_hoja += (
            f"{clave.replace('_', ' ').title()}:\n"
            f"{valor}\n\n"
            )

        self.tab_hoja_vida.setText(texto_hoja.strip())

        # ================= MANTENIMIENTOS =================
        texto_mant = "HISTORIAL DE MANTENIMIENTOS\n"
        texto_mant += "────────────────────────────\n\n"

        mantenimientos = equipo.get("mantenimientos", [])

        if not mantenimientos:
            texto_mant += "No hay mantenimientos registrados."
        else:
            for m in mantenimientos:
                texto_mant += (
                f"📅 {m.get('fecha','')}\n"
                f"🔧 {m.get('tipo','')}\n"
                f"👤 {m.get('responsable','')} ({m.get('documento_responsable','')})\n"
                f"📝 {m.get('descripcion','')}\n"
                f"➡ Próximo: {m.get('fecha_proxima','')}\n"
                "────────────────────────────\n\n"
                )

        # ================= DOCUMENTOS =================
        texto_mant += "\nPDFs de mantenimiento:\n"
        pdfs_mant = equipo.get("pdf_mantenimiento", [])

        if pdfs_mant:
            for pdf in pdfs_mant:
                texto_mant += f"📄 {pdf}\n"
        else:
            texto_mant += "Ninguno\n"

        texto_mant += "\nPDFs de calibración:\n"
        pdfs_cal = equipo.get("pdf_calibracion", [])

        if pdfs_cal:
            for pdf in pdfs_cal:
                texto_mant += f"📄 {pdf}\n"
        else:
            texto_mant += "Ninguno\n"

        self.tab_mantenimientos.setText(texto_mant.strip())

    def cargar_servicios_json(self):
        ruta = "data/servicios.json"

        if not os.path.exists(ruta):
            self.servicios = []
            return

        with open(ruta, "r", encoding="utf-8") as archivo:
            self.servicios = json.load(archivo)

    def actualizar_servicios(self):
        self.lista_servicios.clear()
        self.lista_servicios.addItems(self.servicios)

    def agregar_servicio(self):
        nombre, ok = QInputDialog.getText(
        self,
        "Nuevo servicio",
        "Nombre del servicio:"
        )
        if not nombre:
            self.mostrar_warning("Dato inválido","Debes escribir un nombre.")
        if ok and nombre:
            self.servicios.append(nombre)
            self.guardar_servicios_json()
            self.actualizar_servicios()
            self.mostrar_info("Servicio agregado",f"Se agregó el servicio: {nombre}")

    def guardar_servicios_json(self):
        with open("data/servicios.json", "w", encoding="utf-8") as archivo:
            json.dump(self.servicios, archivo, indent=4, ensure_ascii=False)

    def borrar_servicio(self):
        item = self.lista_servicios.currentItem()

        if not item:
            self.mostrar_warning(
            "Sin selección",
            "Selecciona un servicio para borrarlo."
            )
            return

        nombre = item.text()

        equipos_del_servicio = [
        equipo for equipo in self.equipos
        if equipo.get("servicio") == nombre
        ]

        cantidad = len(equipos_del_servicio)

        mensaje = (
        f"¿Seguro que deseas borrar el servicio '{nombre}'?\n\n"
        f"También se eliminarán {cantidad} equipos asociados."
        )

        respuesta = QMessageBox.question(
        self,
        "Confirmar borrado",
        mensaje,
        QMessageBox.StandardButton.Yes |
        QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.No:
            return

        self.servicios.remove(nombre)

        self.equipos = [
        equipo for equipo in self.equipos
        if equipo.get("servicio") != nombre
        ]

        self.guardar_servicios_json()

        with open("data/equipos.json", "w", encoding="utf-8") as archivo:
            json.dump(
            self.equipos,
            archivo,
            indent=4,
            ensure_ascii=False
            )

        self.actualizar_servicios()
        self.actualizar_tabla()

        self.mostrar_info(
        "Servicio eliminado",
        f"Se eliminó el servicio '{nombre}' y {cantidad} equipos asociados."
        )

    def guardar_equipo_json(self, equipo):
        ruta = "data/equipos.json"

        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as archivo:
                equipos = json.load(archivo)
        else:
            equipos = []

        equipos.append(equipo)

        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(equipos, archivo, indent=4, ensure_ascii=False)

        self.equipos = equipos
        self.mostrar_info("Equipo guardado","El equipo fue guardado correctamente.")
        self.actualizar_tabla()

    def borrar_equipo(self):
        fila = self.tabla_equipos.currentRow()

        if fila == -1:
            self.mostrar_warning("Sin selección","Selecciona un equipo para borrarlo.")
            return

        equipo_a_borrar = self.equipos_visibles[fila]
        respuesta = QMessageBox.question(
            self,
            "Confirmar borrado",
            "¿Seguro que deseas borrar este equipo?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        if respuesta == QMessageBox.StandardButton.No:
            return
        self.equipos.remove(equipo_a_borrar)
        
        with open("data/equipos.json", "w", encoding="utf-8") as archivo:
            json.dump(self.equipos, archivo, indent=4, ensure_ascii=False)

        item = self.lista_servicios.currentItem()

        if item:
            self.filtrar_por_servicio()
        else:
            self.actualizar_tabla()
        self.mostrar_info("Equipo eliminado","El equipo fue eliminado correctamente.")

    def filtrar_por_servicio(self):
        item = self.lista_servicios.currentItem()

        if not item:
            self.actualizar_tabla()
            return

        servicio = item.text()

        equipos_filtrados = [
            equipo for equipo in self.equipos
            if equipo.get("servicio") == servicio
        ]

        self.actualizar_tabla(equipos_filtrados)

    def mostrar_info(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_error(self, titulo, mensaje):
        QMessageBox.critical(self, titulo, mensaje)

    def mostrar_warning(self, titulo, mensaje):
        QMessageBox.warning(self, titulo, mensaje)

    def editar_equipo(self):
        fila = self.tabla_equipos.currentRow()

        if fila == -1:
            self.mostrar_warning(
            "Sin selección",
            "Selecciona un equipo para editar."
            )
            return

        equipo = self.equipos_visibles[fila]
        categoria = equipo.get("categoria")

        if categoria not in FORMULARIOS:
            self.mostrar_error(
            "Error",
            f"No existe formulario para la categoría: {categoria}"
            )
            return

        Formulario = FORMULARIOS[categoria]
        ventana = Formulario(datos_existentes=equipo)
        resultado = ventana.exec()

        if not resultado:
            return

        nuevos_datos = ventana.datos_guardados

        nuevos_datos["servicio"] = equipo.get("servicio")
        nuevos_datos["categoria"] = equipo.get("categoria")
        nuevos_datos["estado"] = self.obtener_estado_equipo(nuevos_datos)

        if "pdf_mantenimiento" in equipo:
            nuevos_datos["pdf_mantenimiento"] = equipo["pdf_mantenimiento"]

        if "pdf_calibracion" in equipo:
            nuevos_datos["pdf_calibracion"] = equipo["pdf_calibracion"]

        indice_real = self.equipos.index(equipo)
        self.equipos[indice_real] = nuevos_datos

        with open("data/equipos.json", "w", encoding="utf-8") as archivo:
            json.dump(
            self.equipos,
            archivo,
            indent=4,
            ensure_ascii=False
            )

        item = self.lista_servicios.currentItem()

        if item:
            self.filtrar_por_servicio()
        else:
            self.actualizar_tabla()

        self.mostrar_info(
        "Equipo editado",
        "Los cambios fueron guardados correctamente."
        )

    def obtener_estado_equipo(self, equipo):
        fecha = equipo.get("fecha_proximo_mantenimiento")

        if not fecha:
            return "⚪"

        return Mantenimiento.calcular_estado(fecha)
    
    def registrar_mantenimiento(self):
        fila = self.tabla_equipos.currentRow()

        if fila == -1:
            self.mostrar_warning(
            "Sin selección",
            "Selecciona un equipo primero."
            )
            return

        equipo = self.equipos_visibles[fila]

        ventana = MantenimientoForm()
        resultado = ventana.exec()

        if not resultado:
            return

        datos = ventana.datos

        # asegurar lista de mantenimientos
        if "mantenimientos" not in equipo:
            equipo["mantenimientos"] = []

        # agregar historial
        equipo["mantenimientos"].append(datos)

        # actualizar campos principales del equipo
        equipo["fecha_mantenimiento"] = datos["fecha"]
        equipo["descripcion_mantenimiento"] = datos["descripcion"]
        equipo["responsable"] = datos["responsable"]
        equipo["documento_responsable"] = datos["documento_responsable"]
        equipo["fecha_proximo_mantenimiento"] = datos["fecha_proxima"]

        # recalcular estado
        equipo["estado"] = self.obtener_estado_equipo(equipo)

        # guardar JSON
        with open("data/equipos.json", "w", encoding="utf-8") as archivo:
            json.dump(self.equipos, archivo, indent=4, ensure_ascii=False)

        # refrescar UI
        self.filtrar_por_servicio()

        self.mostrar_info(
        "Mantenimiento registrado",
        "El mantenimiento fue guardado correctamente."
        )