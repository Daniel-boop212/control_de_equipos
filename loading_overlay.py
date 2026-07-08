from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout,
    QProgressBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMovie


class LoadingOverlay(QWidget):
    def __init__(self, parent=None, texto="Cargando..."):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
        QWidget {
            background-color: rgba(0, 0, 0, 140);
        }

        QLabel {
            color: white;
            font-size: 18px;
            font-weight: bold;
        }

        QProgressBar {
            border: 1px solid white;
            border-radius: 8px;
            text-align: center;
            color: white;
            min-height: 20px;
        }

        QProgressBar::chunk {
            background-color: #2563eb;
            border-radius: 8px;
        }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel(texto)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Barra indeterminada (animada)
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # animación infinita
        self.progress.setFixedWidth(300)

        layout.addWidget(self.label)
        layout.addSpacing(20)
        layout.addWidget(self.progress)

        self.hide()

    def mostrar(self, texto="Cargando..."):
        self.label.setText(texto)
        self.resize(self.parent().size())
        self.show()
        self.raise_()

    def ocultar(self):
        self.hide()