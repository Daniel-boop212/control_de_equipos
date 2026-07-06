import json
import os
import sys
import subprocess

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QFont, QColor, QDesktopServices
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QFrame,
    QHBoxLayout, QVBoxLayout,
    QComboBox, QPushButton, QLabel,
    QListWidget, QTableWidget, QTableWidgetItem,
    QTabWidget, QTextEdit, QTextBrowser,
    QInputDialog, QMessageBox,
    QFileDialog,
    QTreeWidget, QTreeWidgetItem,
    QHeaderView, QAbstractItemView,
    QSpacerItem, QSizePolicy
)
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMenu
from datetime import datetime
from biomedico_form import BiomedicoForm
from computo_form import ComputoForm
from refrigeracion_form import RefrigeracionForm
from muebles_form import MueblesForm
from mantenimiento_form import MantenimientoForm
from alertas_window import AlertasWindow
from models.mantenimiento import Mantenimiento
from ayuda_window import AyudaWindow
from utils.pdf_generator import generar_pdf_hoja_vida

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
    background: #f5f8fc;
}

QWidget {
    font-size: 13px;
    color: #1f2937;
}

QLabel {
    font-weight: bold;
}

QPushButton {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1d4ed8;
}

QPushButton:pressed {
    background-color: #1e40af;
}

QComboBox {
    background: white;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 8px;
}

QListWidget {
    background: white;
    border: 1px solid #dbe3ee;
    border-radius: 12px;
    padding: 6px;
}

QListWidget::item {
    padding: 12px;
    border-radius: 8px;
}

QListWidget::item:selected {
    background: #dbeafe;
    color: #2563eb;
    font-weight: bold;
}

QTableWidget {
    background: white;
    border: 1px solid #dbe3ee;
    border-radius: 12px;
    gridline-color: #e5e7eb;
}

QHeaderView::section {
    background: #eff6ff;
    color: #1e3a8a;
    padding: 10px;
    border: none;
    font-weight: bold;
}

QTextEdit {
    background: white;
    border: 1px solid #dbe3ee;
    border-radius: 12px;
    padding: 12px;
}

QTabWidget::pane {
    border: 1px solid #dbe3ee;
    background: white;
    border-radius: 12px;
}

QTabBar::tab {
    background: #e5e7eb;
    padding: 10px 18px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}

QTabBar::tab:selected {
    background: #2563eb;
    color: white;
}

QTableWidget::item {
    padding: 10px;
}

QTableWidget::item:selected {
    background: #dbeafe;
    color: #1d4ed8;
}       

QMessageBox {
    background-color: white;
}

QMessageBox QLabel {
    color: black;
}      

QInputDialog {
    background-color: white;
}

QInputDialog QLabel {
    color: black;
}

QInputDialog QLineEdit {
    background-color: white;
    color: black;
    border: 1px solid #cbd5e1;
    padding: 6px;
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
        left_panel = QWidget()
        left_panel.setMaximumWidth(280)

        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        # Logo
        logo = QLabel()
        pixmap = QPixmap("assets/logo_clinica.jpg")  # ruta del logo
        logo.setPixmap(
        pixmap.scaled(
        220, 120,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
        )
        )
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        left_layout.addWidget(logo)

        # Lista de servicios
        self.lista_servicios = QListWidget()
        self.cargar_servicios_json()
        self.actualizar_servicios()
        self.lista_servicios.itemClicked.connect(self.aplicar_filtros)

        # Botones
        self.btn_agregar_servicio = QPushButton("Agregar servicio")
        self.btn_borrar_servicio = QPushButton("Borrar servicio")

        self.btn_agregar_servicio.clicked.connect(self.agregar_servicio)
        self.btn_borrar_servicio.clicked.connect(self.borrar_servicio)

        # Agregar al layout
        left_layout.addWidget(self.lista_servicios, 1)  # <- ocupa el espacio libre
        left_layout.addWidget(self.btn_agregar_servicio)
        left_layout.addWidget(self.btn_borrar_servicio)

        main_layout.addWidget(left_panel)

        # ================= PANEL DERECHO =================
        right_panel = QFrame()
        right_panel.setStyleSheet("""
        QFrame {
            background: white;
        border-radius: 18px;
        border: 1px solid #dbe3ee;
        }
        """)

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(16)

        main_layout.addWidget(right_panel)

        # ---------- Parte superior ----------
        top_bar = QHBoxLayout()

        top_bar.addWidget(QLabel("Categoría"))

        self.combo_categoria = QComboBox()
        self.combo_categoria.addItems([
    "Biomédico",
    "Cómputo",
    "Refrigeración",
    "Muebles y enseres"
        ])

        top_bar.addWidget(self.combo_categoria)
        top_bar.addStretch()

        self.btn_alertas = QPushButton("⚠ Alertas")
        self.btn_alertas.clicked.connect(self.mostrar_alertas_manual)
        top_bar.addWidget(self.btn_alertas)

        self.btn_ayuda = QPushButton("❓ Ayuda")
        self.btn_ayuda.clicked.connect(self.mostrar_ayuda)
        top_bar.addWidget(self.btn_ayuda)

        right_layout.addLayout(top_bar)

        filtros_layout = QHBoxLayout()

        filtros_layout.addWidget(QLabel("Buscar"))

        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Nombre del equipo...")
        filtros_layout.addWidget(self.input_busqueda)

        self.combo_filtro_categoria = QComboBox()
        self.combo_filtro_categoria.addItems([
    "Todas",
    "Biomédico",
    "Cómputo",
    "Refrigeración",
    "Muebles y enseres"
        ])
        filtros_layout.addWidget(self.combo_filtro_categoria)

        self.input_busqueda.textChanged.connect(self.aplicar_filtros)
        self.combo_filtro_categoria.currentTextChanged.connect(self.aplicar_filtros)

        right_layout.addLayout(filtros_layout)

        # ---------- Parte inferior ----------
        toolbar = QFrame()
        toolbar_layout = QHBoxLayout()
        toolbar.setLayout(toolbar_layout)
        toolbar.setStyleSheet("border: none;")

        self.btn_agregar = QPushButton("＋ Agregar")
        self.btn_editar = QPushButton("✎ Editar")
        self.btn_mantenimiento = QPushButton("🛠 Mantenimiento")
        self.btn_borrar = QPushButton("🗑 Borrar")
        self.btn_pdf = QPushButton("📄 Exportar PDF")
        
        self.btn_agregar.clicked.connect(self.abrir_formulario)
        self.btn_editar.clicked.connect(self.editar_equipo)
        self.btn_mantenimiento.clicked.connect(self.registrar_mantenimiento)
        self.btn_borrar.clicked.connect(self.borrar_equipo)
        self.btn_pdf.clicked.connect(self.exportar_pdf)

        toolbar_layout.addWidget(self.btn_agregar)
        toolbar_layout.addWidget(self.btn_editar)
        toolbar_layout.addWidget(self.btn_mantenimiento)
        toolbar_layout.addWidget(self.btn_borrar)
        toolbar_layout.addWidget(self.btn_pdf)
        toolbar_layout.addStretch()

        self.input_busqueda.textChanged.connect(self.aplicar_filtros)
        self.combo_filtro_categoria.currentTextChanged.connect(self.aplicar_filtros)
        self.lista_servicios.itemClicked.connect(self.aplicar_filtros)


        right_layout.addWidget(toolbar)

        # ---------- Tabla de equipos ----------
        right_layout.addWidget(QLabel("Equipos del servicio"))

        self.tabla_equipos = QTableWidget()
        self.tabla_equipos.setColumnCount(3)
        self.tabla_equipos.setHorizontalHeaderLabels([
            "Equipo", "Categoría", "Estado"
        ])
        self.tabla_equipos.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla_equipos.horizontalHeader().setStretchLastSection(True)
        self.tabla_equipos.verticalHeader().setVisible(False)
        self.tabla_equipos.setShowGrid(False)
        self.tabla_equipos.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla_equipos.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        header = self.tabla_equipos.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        right_layout.addWidget(self.tabla_equipos)

        # ---------- Panel inferior ----------
        self.tabs = QTabWidget()

        # Pestaña hoja de vida
        self.tab_hoja_vida = QTextBrowser()
        self.tab_hoja_vida.setText("Aquí aparecerá la hoja de vida del equipo.")

        # Pestaña mantenimientos
        self.tab_mantenimientos = QTreeWidget()
        self.tab_mantenimientos.setHeaderHidden(True)
        self.tab_mantenimientos.itemDoubleClicked.connect(self.abrir_item_arbol)

        self.tab_mantenimientos.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tab_mantenimientos.customContextMenuRequested.connect(
    self.menu_mantenimiento
)

        self.tabs.addTab(self.tab_hoja_vida, "Hoja de vida")
        self.tabs.addTab(self.tab_mantenimientos, "Historial de mantenimientos")

        right_layout.addWidget(self.tabs)

        # Cargar datos de prueba

        self.cargar_equipos_json()
        self.actualizar_servicios()
        self.actualizar_tabla([])   # vacía
        self.actualizar_boton_alertas() 
        self.tabla_equipos.cellClicked.connect(self.mostrar_equipo)
        QTimer.singleShot(300, self.mostrar_alertas_inicio)

    def abrir_item_arbol(self, item, columna):
        ruta = item.data(0, Qt.ItemDataRole.UserRole)

        if not ruta:
            return

        if not os.path.exists(ruta):
            self.mostrar_error("Archivo no encontrado", ruta)
            return

        QDesktopServices.openUrl(QUrl.fromLocalFile(ruta))

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
            nombre = equipo.get("nombre", "Sin nombre")
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
        self.equipo_actual = equipo

        # ================= HOJA DE VIDA =================
        texto_hoja = """
        <h2>Hoja de Vida del Equipo</h2>
        <hr>
        """

        for clave, valor in equipo.items():
            if clave in [
            "mantenimientos",
            "pdf_mantenimiento",
            "pdf_calibracion",
            "imagen"
            ]:
                continue

            texto_hoja += f"""
            <p>
            <b>{clave.replace('_', ' ').title()}:</b><br>
            {valor}
            </p>
            """

        self.tab_hoja_vida.setHtml(texto_hoja)

        # ================= MANTENIMIENTOS =================
        self.tab_mantenimientos.clear()

        mantenimientos = equipo.get("mantenimientos", [])

        if not mantenimientos:
            item = QTreeWidgetItem(["No hay mantenimientos"])
            self.tab_mantenimientos.addTopLevelItem(item)
            return

        for i, m in enumerate(mantenimientos):
            titulo = f"{m.get('fecha', '')} — {m.get('tipo', '')}"
            padre = QTreeWidgetItem([titulo])

            # Guardar índice del mantenimiento (para editar/borrar)
            padre.setData(0, Qt.ItemDataRole.UserRole + 1, i)

            padre.addChild(QTreeWidgetItem([
            f"Responsable: {m.get('responsable', '')}"
            ]))

            padre.addChild(QTreeWidgetItem([
            f"Documento: {m.get('documento_responsable', '')}"
            ]))

            padre.addChild(QTreeWidgetItem([
            f"Descripción: {m.get('descripcion', '')}"
            ]))

            padre.addChild(QTreeWidgetItem([
            f"Próximo mantenimiento: {m.get('fecha_proxima', '')}"
            ]))

            # PDFs solo biomédico
            if equipo.get("categoria") == "Biomédico":
                pdf_m = m.get("pdf_mantenimiento", "")
                pdf_c = m.get("pdf_calibracion", "")

                if pdf_m:
                    pdf_item = QTreeWidgetItem([
                    f"PDF mantenimiento: {os.path.basename(pdf_m)}"
                    ])
                    # UserRole normal = ruta PDF
                    pdf_item.setData(0, Qt.ItemDataRole.UserRole, pdf_m)
                else:
                    pdf_item = QTreeWidgetItem([
                    "PDF mantenimiento: No adjunto"
                    ])

                padre.addChild(pdf_item)

                if pdf_c:
                    pdf_item2 = QTreeWidgetItem([
                    f"PDF calibración: {os.path.basename(pdf_c)}"
                    ])
                    pdf_item2.setData(0, Qt.ItemDataRole.UserRole, pdf_c)
                else:
                    pdf_item2 = QTreeWidgetItem([
                    "PDF calibración: No adjunto"
                    ])

                padre.addChild(pdf_item2)

            self.tab_mantenimientos.addTopLevelItem(padre)

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
        self.aplicar_filtros()
        self.actualizar_boton_alertas()

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
            self.aplicar_filtros()
        else:
            self.actualizar_tabla()
        self.mostrar_info("Equipo eliminado","El equipo fue eliminado correctamente.")
        self.actualizar_boton_alertas()

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
            self.aplicar_filtros()
        else:
            self.actualizar_tabla()

        self.mostrar_info(
        "Equipo editado",
        "Los cambios fueron guardados correctamente."
        )
        self.actualizar_boton_alertas()

    def obtener_estado_equipo(self, equipo):
        mantenimientos = equipo.get("mantenimientos", [])

        if not mantenimientos:
            return "🔵"   # o ⚪ si prefieres

        ultimo = mantenimientos[-1]
        fecha = ultimo.get("fecha_proxima")

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

        categoria = equipo.get("categoria")
        ventana = MantenimientoForm(categoria)
        resultado = ventana.exec()

        if not resultado:
            return

        datos = ventana.datos

        if "mantenimientos" not in equipo:
            equipo["mantenimientos"] = []

        equipo["mantenimientos"].append(datos)

        equipo["fecha_mantenimiento"] = datos["fecha"]
        equipo["descripcion_mantenimiento"] = datos["descripcion"]
        equipo["responsable"] = datos["responsable"]
        equipo["documento_responsable"] = datos["documento_responsable"]
        equipo["fecha_proximo_mantenimiento"] = datos["fecha_proxima"]

        equipo["estado"] = self.obtener_estado_equipo(equipo)

        with open("data/equipos.json", "w", encoding="utf-8") as archivo:
            json.dump(self.equipos, archivo, indent=4, ensure_ascii=False)

        self.aplicar_filtros()

        self.mostrar_info(
        "Mantenimiento registrado",
        "El mantenimiento fue guardado correctamente."
        )
        self.actualizar_boton_alertas()
    
    def obtener_alertas_mantenimiento(self):
        alertas = []

        for equipo in self.equipos:
            estado = equipo.get("estado", "⚪")

            if estado not in ["🔴", "🟡"]:
                continue

            nombre = equipo.get(
            "nombre_equipo",
            equipo.get("nombre", "Sin nombre")
            )

            servicio = equipo.get("servicio", "Sin servicio")
            fecha = equipo.get("fecha_proximo_mantenimiento", "Sin fecha")

            dias_restantes = None

            try:
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
                hoy = datetime.now().date()
                dias_restantes = (fecha_obj - hoy).days
            except:
                pass

            alertas.append({
            "nombre": nombre,
            "servicio": servicio,
            "estado": estado,
            "fecha": fecha,
            "dias_restantes": dias_restantes
            })

        return alertas
    
    def mostrar_alertas_inicio(self):
        cantidad = len(self.obtener_alertas_mantenimiento())

        if cantidad > 0:
            self.mostrar_info(
            "Alertas",
            f"Hay {cantidad} alertas de mantenimiento.\n"
            "Presiona el botón ⚠ Alertas para ver detalles."
            )

    def mostrar_alertas_manual(self):
        alertas = self.obtener_alertas_mantenimiento()

        if not alertas:
            self.mostrar_info(
            "Alertas",
            "No hay equipos próximos a vencer."
            )
            return

        ventana = AlertasWindow(alertas)
        ventana.exec()

    def actualizar_boton_alertas(self):
        cantidad = len(self.obtener_alertas_mantenimiento())
        self.btn_alertas.setText(f"⚠ {cantidad} alertas")

        if cantidad == 0:
            self.btn_alertas.setStyleSheet("""
            QPushButton {
                background-color: #16a34a;
                color: white;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }
            """)
        else:
            self.btn_alertas.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }
            """)

    def aplicar_filtros(self):
        item = self.lista_servicios.currentItem()

        if not item:
            self.actualizar_tabla([])
            return

        servicio = item.text()
        categoria = self.combo_filtro_categoria.currentText()
        busqueda = self.input_busqueda.text().lower().strip()

        filtrados = []

        for equipo in self.equipos:
            if equipo.get("servicio") != servicio:
                continue

            if categoria != "Todas":
                if equipo.get("categoria") != categoria:
                    continue

            nombre = equipo.get(
            "nombre_equipo",
            equipo.get("nombre", "")
            ).lower()

            if busqueda and busqueda not in nombre:
                continue

            filtrados.append(equipo)

        self.actualizar_tabla(filtrados)

    def menu_mantenimiento(self, posicion):
        item = self.tab_mantenimientos.itemAt(posicion)

        if not item:
            return

        # Solo permitir en items principales (mantenimientos)
        if item.parent() is not None:
            item = item.parent()

        menu = QMenu()
        menu.setStyleSheet("""
    QMenu {
        background-color: white;
        color: black;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 6px;
    }

    QMenu::item {
        padding: 8px 25px 8px 20px;
        border-radius: 6px;
    }

    QMenu::item:selected {
        background-color: #2563eb;
        color: white;
    }
    """)
        
        editar = menu.addAction("✏ Editar mantenimiento")
        borrar = menu.addAction("🗑 Borrar mantenimiento")

        accion = menu.exec(self.tab_mantenimientos.viewport().mapToGlobal(posicion))

        if accion == editar:
            self.editar_mantenimiento(item)

        elif accion == borrar:
            self.borrar_mantenimiento(item)

    def borrar_mantenimiento(self, item):
        indice = item.data(0, Qt.ItemDataRole.UserRole + 1)

        respuesta = QMessageBox.question(
        self,
        "Confirmar",
        "¿Eliminar mantenimiento?",
        QMessageBox.StandardButton.Yes |
        QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.No:
            return

        if indice is None:
            self.mostrar_warning(
            "Error",
            "No se pudo identificar el mantenimiento.")
            return
        
        del self.equipo_actual["mantenimientos"][indice]
        self.actualizar_estado_mantenimientos(self.equipo_actual)
        self.aplicar_filtros()
        self.actualizar_boton_alertas()

        with open("data/equipos.json", "w", encoding="utf-8") as archivo:
            json.dump(self.equipos, archivo, indent=4, ensure_ascii=False)

        self.mostrar_equipo(
        self.tabla_equipos.currentRow(),
        0
        )

    def editar_mantenimiento(self, item):
        indice = item.data(0, Qt.ItemDataRole.UserRole + 1)

        if indice is None:
            self.mostrar_warning(
            "Error",
            "No se pudo identificar el mantenimiento.")
            return
    
        mantenimiento = self.equipo_actual["mantenimientos"][indice]

        ventana = MantenimientoForm(
        self.equipo_actual["categoria"],
        datos_existentes=mantenimiento
        )

        resultado = ventana.exec()

        if not resultado:
            return

        self.equipo_actual["mantenimientos"][indice] = ventana.datos
        self.actualizar_estado_mantenimientos(self.equipo_actual)
        self.aplicar_filtros()      
        self.actualizar_boton_alertas()

        with open("data/equipos.json", "w", encoding="utf-8") as archivo:
            json.dump(self.equipos, archivo, indent=4, ensure_ascii=False)

        self.mostrar_equipo(
        self.tabla_equipos.currentRow(),
        0
        )

    def exportar_pdf(self):
        fila = self.tabla_equipos.currentRow()

        if fila == -1:
            self.mostrar_warning(
            "Sin selección",
            "Selecciona un equipo"
            )
            return

        equipo = self.equipos_visibles[fila]

        ruta, _ = QFileDialog.getSaveFileName(
        self,
        "Guardar PDF",
        "hoja_vida.pdf",
        "PDF Files (*.pdf)"
        )

        if not ruta:
            return

        generar_pdf_hoja_vida(equipo, ruta)

    def actualizar_estado_mantenimientos(self, equipo):
        mantenimientos = equipo.get("mantenimientos", [])

        if not mantenimientos:
            equipo.pop("fecha_proximo_mantenimiento", None)
            equipo["estado"] = "⚪"
            return

        ultimo = mantenimientos[-1]

        equipo["fecha_proximo_mantenimiento"] = ultimo.get(
        "fecha_proxima", ""
        )

        equipo["estado"] = self.obtener_estado_equipo(equipo)

    def mostrar_ayuda(self):
        ventana = AyudaWindow()
        ventana.exec()