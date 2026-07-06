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

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from biomedico_form import BiomedicoForm
from computo_form import ComputoForm
from refrigeracion_form import RefrigeracionForm
from muebles_form import MueblesForm
from mantenimiento_form import MantenimientoForm
from models.mantenimiento import Mantenimiento

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
        self.lista_servicios.itemClicked.connect(self.filtrar_por_servicio)

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

        right_layout.addLayout(top_bar)

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
        self.btn_pdf.clicked.connect(self.generar_pdf_hoja_vida)

        toolbar_layout.addWidget(self.btn_agregar)
        toolbar_layout.addWidget(self.btn_editar)
        toolbar_layout.addWidget(self.btn_mantenimiento)
        toolbar_layout.addWidget(self.btn_borrar)
        toolbar_layout.addWidget(self.btn_pdf)
        toolbar_layout.addStretch()

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

        self.tabs.addTab(self.tab_hoja_vida, "Hoja de vida")
        self.tabs.addTab(self.tab_mantenimientos, "Documentos")

        right_layout.addWidget(self.tabs)

        # Cargar datos de prueba

        self.cargar_equipos_json()
        self.actualizar_tabla()
        self.actualizar_servicios()
        self.filtrar_por_servicio()
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
            "pdf_calibracion"
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

        for m in mantenimientos:
            titulo = f"{m.get('fecha', '')} — {m.get('tipo', '')}"
            padre = QTreeWidgetItem([titulo])

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

            # PDFs solo para biomédico
            if equipo.get("categoria") == "Biomédico":
                pdf_m = m.get("pdf_mantenimiento", "")
                pdf_c = m.get("pdf_calibracion", "")

                if pdf_m:
                    pdf_item = QTreeWidgetItem([
                    f"PDF mantenimiento: {os.path.basename(pdf_m)}"
                    ])
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
        self.actualizar_tabla()
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
            self.filtrar_por_servicio()
        else:
            self.actualizar_tabla()
        self.mostrar_info("Equipo eliminado","El equipo fue eliminado correctamente.")
        self.actualizar_boton_alertas()

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
        self.actualizar_boton_alertas()

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

        self.filtrar_por_servicio()

        self.mostrar_info(
        "Mantenimiento registrado",
        "El mantenimiento fue guardado correctamente."
        )
        self.actualizar_boton_alertas()

    def generar_pdf_hoja_vida(self):
        fila = self.tabla_equipos.currentRow()

        if fila == -1:
            self.mostrar_warning(
            "Sin selección",
            "Selecciona un equipo primero."
            )
            return

        equipo = self.equipos_visibles[fila]

        nombre = equipo.get(
        "nombre_equipo",
        equipo.get("nombre", "equipo")
        )

        ruta, _ = QFileDialog.getSaveFileName(
    self,
    "Guardar hoja de vida",
    f"hoja_vida_{nombre}.pdf",
    "PDF Files (*.pdf)"
        )

        if not ruta:
            return

        doc = SimpleDocTemplate(ruta, pagesize=A4)
        estilos = getSampleStyleSheet()
        elementos = []

        elementos.append(
            Paragraph("HOJA DE VIDA DEL EQUIPO", estilos["Title"])
        )
        elementos.append(Spacer(1, 20))

        for clave, valor in equipo.items():
            if clave == "mantenimientos":
                continue

            texto = f"<b>{clave.replace('_', ' ').title()}:</b> {valor}"
            elementos.append(Paragraph(texto, estilos["BodyText"]))
            elementos.append(Spacer(1, 8))

        elementos.append(Spacer(1, 20))
        elementos.append(
        Paragraph("Historial de mantenimientos", estilos["Heading2"])
        )

        mantenimientos = equipo.get("mantenimientos", [])

        if not mantenimientos:
            elementos.append(
            Paragraph("No hay mantenimientos.", estilos["BodyText"])
            )
        else:
            for m in mantenimientos:
                texto = (
                f"Fecha: {m.get('fecha','')}<br/>"
                f"Tipo: {m.get('tipo','')}<br/>"
                f"Responsable: {m.get('responsable','')}<br/>"
                f"Documento: {m.get('documento_responsable','')}<br/>"
                f"Descripción: {m.get('descripcion','')}<br/>"
                f"Próximo: {m.get('fecha_proxima','')}"
                )

                elementos.append(
                Paragraph(texto, estilos["BodyText"])
                )
                elementos.append(Spacer(1, 15))

        doc.build(elementos)
        QDesktopServices.openUrl(QUrl.fromLocalFile(ruta))
        self.mostrar_info(
        "PDF generado",
        f"Se creó: {ruta}"
        )
    
    def obtener_alertas_mantenimiento(self):
        alertas = []

        for equipo in self.equipos:
            estado = equipo.get("estado", "⚪")

            if estado in ["🔴", "🟡"]:
                nombre = equipo.get(
                "nombre_equipo",
                equipo.get("nombre", "Sin nombre")
                )

                servicio = equipo.get("servicio", "Sin servicio")
                fecha = equipo.get("fecha_proximo_mantenimiento", "Sin fecha")

                alertas.append({
                "nombre": nombre,
                "servicio": servicio,
                "estado": estado,
                "fecha": fecha
                })

        return alertas
    
    def mostrar_alertas_inicio(self):
        alertas = self.obtener_alertas_mantenimiento()

        if not alertas:
            return

        mensaje = "Equipos con mantenimiento próximo o vencido:\n\n"

        for alerta in alertas:
            mensaje += (
            f"{alerta['estado']} "
            f"{alerta['nombre']} "
            f"({alerta['servicio']})\n"
            f"Fecha: {alerta['fecha']}\n\n"
            )

        QMessageBox.warning(
        self,
        "Alertas de mantenimiento",
        mensaje
        )

    def mostrar_alertas_manual(self):
        alertas = self.obtener_alertas_mantenimiento()

        if not alertas:
            self.mostrar_info(
            "Alertas",
            "No hay equipos próximos a vencer."
            )
            return

        mensaje = ""

        for alerta in alertas:
            mensaje += (
            f"{alerta['estado']} "
            f"{alerta['nombre']}\n"
            f"Servicio: {alerta['servicio']}\n"
            f"Fecha: {alerta['fecha']}\n\n"
            )

        self.mostrar_warning(
        "Próximos mantenimientos",
        mensaje
        )

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