import os
from datetime import datetime
import shutil
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QHeaderView,
    QAbstractItemView, QProgressBar,
    QFrame
)
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QSizePolicy

class CircularProgress(QWidget):
    def __init__(self, porcentaje=0):
        super().__init__()
        self.porcentaje = porcentaje
        self.setMinimumSize(180, 180)

    def setValue(self, valor):
        self.porcentaje = valor
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        margen = 12
        rect = QRectF(
    margen,
    margen,
    self.width() - margen * 2,
    self.height() - margen * 2
        )

        # Fondo gris
        pen = QPen(QColor("#e5e7eb"), 14)
        painter.setPen(pen)
        painter.drawArc(rect, 0, 360 * 16)

        # Color según porcentaje
        if self.porcentaje < 60:
            color = QColor("#22c55e")
        elif self.porcentaje < 85:
            color = QColor("#eab308")
        else:
            color = QColor("#ef4444")

        # Arco de progreso
        pen = QPen(color, 14)
        painter.setPen(pen)

        angulo = int((self.porcentaje / 100) * 360 * 16)
        painter.drawArc(rect, 90 * 16, -angulo)

        # Texto central
        painter.setPen(QColor("#111827"))
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        painter.setFont(font)

        painter.drawText(
            self.rect(),
            Qt.AlignmentFlag.AlignCenter,
            f"{self.porcentaje}%"
        )

        
class StorageWindow(QDialog):
    def __init__(self, equipos):
        super().__init__()

        self.equipos = equipos
        self.capacidad_recomendada_gb = 100

        self.setWindowTitle("Almacenamiento")
        self.resize(900, 650)

        # ===== ESTILO GENERAL =====
        self.setStyleSheet("""
    QDialog {
        background-color: white;
    }

    QLabel {
        color: #111827;
    }

    QTableWidget {
        background: white;
        color: #111827;
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

    QPushButton {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #1d4ed8;
    }

    QPushButton:disabled {
        background-color: #9ca3af;
    }

    QProgressBar {
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        text-align: center;
        height: 28px;
        background: #f3f4f6;
        font-weight: bold;
    }
        """)

        # ===== SCROLL AREA =====
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: white;")

        # ===== CONTENEDOR CENTRAL =====
        self.container = QWidget()
        self.container.setStyleSheet("background: white;")

        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.scroll.setWidget(self.container)
        

        # ===== LAYOUT PRINCIPAL =====
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.scroll)

        # ===== DATOS =====
        self.datos = self.calcular_almacenamiento()

        # ===== UI (contenido scrolleable) =====
        self.crear_header()
        self.crear_cards()
        self.crear_barra()
        self.crear_tabla()
        self.crear_diagnostico()
        self.crear_historial_backups()

        # ===== PIE FIJO (siempre visible, fuera del scroll) =====
        self.crear_botones()
        layout.addWidget(self.pie_botones)

    def crear_header(self):
        titulo = QLabel("💾 Uso de almacenamiento")
        titulo.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #1e3a8a;
            padding: 8px;
        """)
        self.main_layout.addWidget(titulo)

        resumen = QLabel(
            f"Total usado: {self.formatear_bytes(self.datos['total'])} | "
            f"Capacidad recomendada: {self.capacidad_recomendada_gb} GB"
        )
        resumen.setStyleSheet("font-size: 14px; padding: 4px;")
        self.main_layout.addWidget(resumen)

    def crear_cards(self):
        cards_layout = QHBoxLayout()

        cards_layout.addWidget(
            self.crear_tarjeta(
                "JSON",
                self.formatear_bytes(self.datos["json"]),
                "#2563eb"
            )
        )

        cards_layout.addWidget(
            self.crear_tarjeta(
                "Imágenes",
                self.formatear_bytes(self.datos["imagenes"]),
                "#16a34a"
            )
        )

        cards_layout.addWidget(
            self.crear_tarjeta(
                "PDFs",
                self.formatear_bytes(self.datos["pdfs"]),
                "#f59e0b"
            )
        )

        cards_layout.addWidget(
            self.crear_tarjeta(
                "Total",
                self.formatear_bytes(self.datos["total"]),
                "#7c3aed"
            )
        )

        self.main_layout.addLayout(cards_layout)

    def crear_barra(self):
        total_gb = self.datos["total"] / (1024 ** 3)

        porcentaje_real = (
            total_gb / self.capacidad_recomendada_gb
        ) * 100

        porcentaje_uso = (
            max(1, int(porcentaje_real))
            if self.datos["total"] > 0
            else 0
        )
        contenedor = QHBoxLayout()

        # ===== Círculo =====
        circulo = CircularProgress(min(porcentaje_uso, 100))
        contenedor.addWidget(circulo)

        # ===== Parte derecha =====
        derecha = QVBoxLayout()

        lbl = QLabel("Uso total del almacenamiento")
        lbl.setStyleSheet("""
        font-size: 15px;
        font-weight: bold;
        color: #1e3a8a;
    """)
        derecha.addWidget(lbl)

        barra = QProgressBar()
        barra.setMaximum(100)
        barra.setValue(min(porcentaje_uso, 100))
        barra.setFormat(f"{porcentaje_uso}%")

        barra.setStyleSheet("""
    QProgressBar {
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        text-align: center;
        height: 28px;
        background: #f3f4f6;
        font-weight: bold;
    }

    QProgressBar::chunk {
        border-radius: 9px;
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 #22c55e,
            stop:0.6 #eab308,
            stop:1 #ef4444
        );
    }
    """)

        derecha.addWidget(barra)

        info = QLabel(
        f"{self.formatear_bytes(self.datos['total'])} usados "
        f"de {self.capacidad_recomendada_gb} GB"
        )
        info.setStyleSheet("color:#6b7280;")
        derecha.addWidget(info)

        contenedor.addLayout(derecha)
        self.main_layout.addLayout(contenedor)

    def crear_tabla(self):
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels([
            "Tipo", "Tamaño", "% del total"
        ])
        self.tabla.setRowCount(4)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.configurar_tabla(self.tabla)
        self.tabla.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        filas = [
            (
                "JSON",
                self.formatear_bytes(self.datos["json"]),
                self.porcentaje(
                    self.datos["json"],
                    self.datos["total"]
                )
            ),
            (
                "Imágenes",
                self.formatear_bytes(self.datos["imagenes"]),
                self.porcentaje(
                    self.datos["imagenes"],
                    self.datos["total"]
                )
            ),
            (
                "PDFs",
                self.formatear_bytes(self.datos["pdfs"]),
                self.porcentaje(
                    self.datos["pdfs"],
                    self.datos["total"]
                )
            ),
            (
                "TOTAL",
                self.formatear_bytes(self.datos["total"]),
                "100%"
            )
        ]

        for fila, (tipo, tamaño, porcentaje_texto) in enumerate(filas):
            item_tipo = QTableWidgetItem(tipo)
            item_tamaño = QTableWidgetItem(tamaño)
            item_porcentaje = QTableWidgetItem(porcentaje_texto)

            if tipo == "TOTAL":
                color_fila = QColor(220, 240, 255)
            else:
                color_fila = QColor(245, 248, 252)

            item_tipo.setBackground(color_fila)
            item_tamaño.setBackground(color_fila)
            item_porcentaje.setBackground(color_fila)

            self.tabla.setItem(fila, 0, item_tipo)
            self.tabla.setItem(fila, 1, item_tamaño)
            self.tabla.setItem(fila, 2, item_porcentaje)

        self.main_layout.addWidget(self.tabla)

    def crear_diagnostico(self):
        diagnostico = QLabel(self.obtener_diagnostico(self.datos))
        diagnostico.setWordWrap(True)
        diagnostico.setStyleSheet("""
            background: #eff6ff;
            padding: 12px;
            border-radius: 10px;
            color: #1e3a8a;
            font-weight: bold;
        """)
        self.main_layout.addWidget(diagnostico)

    def crear_botones(self):
        # Pie fijo, FUERA del área de scroll, para que siempre sea visible.
        self.pie_botones = QFrame()
        self.pie_botones.setStyleSheet("""
            QFrame {
                background: white;
                border-top: 1px solid #dbe3ee;
            }
        """)

        layout = QHBoxLayout(self.pie_botones)
        layout.setContentsMargins(20, 12, 20, 12)

        self.btn_restaurar = QPushButton("Restaurar seleccionado")
        self.btn_restaurar.clicked.connect(self.restaurar_backup)
        self.btn_restaurar.setEnabled(bool(self.obtener_backups()))

        layout.addWidget(self.btn_restaurar)
        layout.addStretch()

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.close)
        layout.addWidget(btn_cerrar)

    def calcular_almacenamiento(self):
        total_json = 0
        total_imagenes = 0
        total_pdfs = 0

        for archivo in [
            "data/equipos.json",
            "data/servicios.json"
        ]:
            if os.path.exists(archivo):
                total_json += os.path.getsize(archivo)

        for equipo in self.equipos:
            imagen = equipo.get("imagen")

            if imagen and os.path.exists(imagen):
                total_imagenes += os.path.getsize(imagen)

            for m in equipo.get("mantenimientos", []):
                pdf1 = m.get("pdf_mantenimiento")
                pdf2 = m.get("pdf_calibracion")

                if pdf1 and os.path.exists(pdf1):
                    total_pdfs += os.path.getsize(pdf1)

                if pdf2 and os.path.exists(pdf2):
                    total_pdfs += os.path.getsize(pdf2)

        total = total_json + total_imagenes + total_pdfs

        return {
            "json": total_json,
            "imagenes": total_imagenes,
            "pdfs": total_pdfs,
            "total": total
        }

    def formatear_bytes(self, bytes_):
        kb = 1024
        mb = kb * 1024
        gb = mb * 1024

        if bytes_ >= gb:
            return f"{bytes_ / gb:.2f} GB"
        elif bytes_ >= mb:
            return f"{bytes_ / mb:.2f} MB"
        elif bytes_ >= kb:
            return f"{bytes_ / kb:.2f} KB"
        else:
            return f"{bytes_} B"

    def crear_tarjeta(self, titulo, valor, color="#2563eb"):
        card = QFrame()
        card.setStyleSheet(f"""
        QFrame {{
            background: white;
            border: 2px solid {color};
            border-radius: 12px;
            padding: 8px;
        }}
        """)

        layout = QVBoxLayout(card)

        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet("""
            font-size: 12px;
            color: #6b7280;
            font-weight: bold;
        """)

        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet(f"""
            font-size: 18px;
            color: {color};
            font-weight: bold;
        """)

        layout.addWidget(lbl_titulo)
        layout.addWidget(lbl_valor)

        return card

    def porcentaje(self, valor, total):
        if total == 0:
            return "0%"
        return f"{(valor / total) * 100:.1f}%"

    def obtener_diagnostico(self, datos):
        total = datos["total"]

        if total == 0:
            return "Sin datos almacenados."

        porcentaje_imagenes = datos["imagenes"] / total

        if total > 80 * 1024 ** 3:
            return "Almacenamiento alto. Considera liberar espacio."

        if porcentaje_imagenes > 0.8:
            return "Las imágenes ocupan la mayor parte del almacenamiento."

        return "Almacenamiento saludable."
    
    def crear_historial_backups(self):
        titulo = QLabel("🕒 Historial de backups")
        titulo.setStyleSheet("""
        font-size: 16px;
        font-weight: bold;
        color: #1e3a8a;
        padding-top: 10px;
        """)
        self.main_layout.addWidget(titulo)

        backups = self.obtener_backups()

        # ===== CONTENEDOR =====
        contenedor = QFrame()
        layout_cont = QVBoxLayout(contenedor)
        layout_cont.setContentsMargins(0, 0, 0, 0)
        layout_cont.setSpacing(10)

        if not backups:
            # Sin backups: mostramos un mensaje en vez de la tabla,
            # pero seguimos creando los botones más abajo.
            self.tabla_backups = None

            vacio = QLabel("No hay backups disponibles.")
            vacio.setStyleSheet("""
            color: #6b7280;
            padding: 8px;
            """)
            layout_cont.addWidget(vacio)
        else:
            # ===== TABLA =====
            self.tabla_backups = QTableWidget()
            self.tabla_backups.setColumnCount(3)
            self.tabla_backups.setHorizontalHeaderLabels(["Archivo", "Fecha", "Tamaño"])

            self.tabla_backups.setRowCount(len(backups))

            self.tabla_backups.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            self.tabla_backups.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Minimum
            )

            self.tabla_backups.verticalHeader().setVisible(False)
            self.tabla_backups.setEditTriggers(
                QAbstractItemView.EditTrigger.NoEditTriggers
            )
            self.tabla_backups.setSelectionBehavior(
                QAbstractItemView.SelectionBehavior.SelectRows
            )

            self.configurar_tabla(self.tabla_backups)
            self.tabla_backups.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            # Expandir correctamente
            self.tabla_backups.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding
            )

            header = self.tabla_backups.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            # Llenar tabla
            for fila, backup in enumerate(backups):
                self.tabla_backups.setItem(
                    fila, 0, QTableWidgetItem(backup["archivo"])
                )
                self.tabla_backups.setItem(
                    fila, 1, QTableWidgetItem(backup["fecha"])
                )
                self.tabla_backups.setItem(
                    fila, 2, QTableWidgetItem(backup["tamano"])
                )

            layout_cont.addWidget(self.tabla_backups)

        self.main_layout.addWidget(contenedor)

    def obtener_backups(self):
        carpeta = "backups"

        if not os.path.exists(carpeta):
            return []

        backups = []

        for archivo in os.listdir(carpeta):
            ruta = os.path.join(carpeta, archivo)

            if not os.path.isfile(ruta):
                continue

            tamaño = os.path.getsize(ruta)
            fecha_ts = os.path.getmtime(ruta)

            if archivo.startswith("equipos_"):
                nombre_mostrar = "Equipos"
            elif archivo.startswith("servicios_"):
                nombre_mostrar = "Servicios"
            else:
                nombre_mostrar = archivo

            backups.append({
            "archivo": nombre_mostrar,
            "archivo_real": archivo,
            "fecha": datetime.fromtimestamp(
                fecha_ts
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "tamano": self.formatear_bytes(tamaño),
            "ruta": ruta
            })

        backups.sort(
        key=lambda x: os.path.getmtime(x["ruta"]),
        reverse=True
        )

        return backups
    
    def restaurar_backup(self):
        if self.tabla_backups is None:
            return

        fila = self.tabla_backups.currentRow()

        if fila == -1:
            QMessageBox.warning(
            self,
            "Sin selección",
            "Selecciona un backup primero."
            )
            return

        backups = self.obtener_backups()
        backup = backups[fila]

        respuesta = QMessageBox.question(
            self,
            "Confirmar restauración",
            "¿Seguro que deseas restaurar este backup?\n"
            "El archivo actual será reemplazado.",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if respuesta != QMessageBox.StandardButton.Yes:
            return

        nombre = backup["archivo_real"]

        if nombre.startswith("equipos_"):
            destino = "data/equipos.json"
        elif nombre.startswith("servicios_"):
            destino = "data/servicios.json"
        else:
            return

        shutil.copy2(backup["ruta"], destino)

        QMessageBox.information(
            self,
            "Restaurado",
            "Backup restaurado correctamente."
        )

    def configurar_tabla(self, tabla):
        tabla.setSizePolicy(
        QSizePolicy.Policy.Expanding,
        QSizePolicy.Policy.Minimum
        )

        tabla.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        tabla.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        tabla.setWordWrap(False)
        tabla.resizeRowsToContents()