from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton,
    QHBoxLayout, QLabel, QHeaderView,
    QAbstractItemView
)
from PyQt6.QtGui import QColor
from datetime import datetime


class AlertasWindow(QDialog):
    def __init__(self, alertas):
        super().__init__()

        self.setWindowTitle("Alertas de mantenimiento")
        self.resize(850, 420)

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

        QTableWidget::item {
            padding: 8px;
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
        """)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # ===== Título =====
        titulo = QLabel("⚠ Equipos con alertas de mantenimiento")
        titulo.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #b91c1c;
            padding: 8px;
        """)
        layout.addWidget(titulo)

        # ===== Tabla =====
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels([
            "Estado", "Equipo", "Servicio", "Fecha", "Restante"
        ])
        self.tabla.setRowCount(len(alertas))
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for fila, alerta in enumerate(alertas):
            estado = alerta["estado"]
            fecha = alerta["fecha"]

            # Calcular días restantes
            texto_dias = self.calcular_dias_restantes(fecha)

            item_estado = QTableWidgetItem(estado)
            item_nombre = QTableWidgetItem(alerta["nombre"])
            item_servicio = QTableWidgetItem(alerta["servicio"])
            item_fecha = QTableWidgetItem(fecha)
            item_dias = QTableWidgetItem(texto_dias)

            # Color por severidad
            if estado == "🔴":
                color = QColor(255, 220, 220)
            elif estado == "🟡":
                color = QColor(255, 245, 200)
            else:
                color = QColor(220, 240, 255)

            for item in [
                item_estado,
                item_nombre,
                item_servicio,
                item_fecha,
                item_dias
            ]:
                item.setBackground(color)

            self.tabla.setItem(fila, 0, item_estado)
            self.tabla.setItem(fila, 1, item_nombre)
            self.tabla.setItem(fila, 2, item_servicio)
            self.tabla.setItem(fila, 3, item_fecha)
            self.tabla.setItem(fila, 4, item_dias)

        layout.addWidget(self.tabla)

        # ===== Botón cerrar =====
        botones = QHBoxLayout()
        botones.addStretch()

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.close)
        botones.addWidget(btn_cerrar)

        layout.addLayout(botones)

    def calcular_dias_restantes(self, fecha):
        formatos = ["%Y-%m-%d", "%d/%m/%Y"]

        for formato in formatos:
            try:
                fecha_obj = datetime.strptime(fecha, formato).date()
                hoy = datetime.now().date()
                dias = (fecha_obj - hoy).days

                if dias < 0:
                    return f"Vencido hace {abs(dias)} días"
                elif dias == 0:
                    return "Vence hoy"
                elif dias == 1:
                    return "1 día"
                else:
                    return f"{dias} días"

            except ValueError:
                continue

        return "N/A"