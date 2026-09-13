from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from paths import resource_path
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(650, 420)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
        )

        self.setStyleSheet("""
        QWidget {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #eff6ff,
                stop:1 #dbeafe
            );
            border: 2px solid #93c5fd;
            border-radius: 20px;
        }

        QLabel {
            border: none;
        }

        QProgressBar {
            border: none;
            border-radius: 10px;
            background: #dbeafe;
            height: 18px;
            text-align: center;
            font-weight: bold;
        }

        QProgressBar::chunk {
            border-radius: 10px;
            background: #2563eb;
        }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        # Logo
        self.logo = QLabel()
        pixmap = QPixmap(resource_path("assets/logo_clinica.jpg"))
        self.logo.setPixmap(
            pixmap.scaled(
                220,
                140,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título
        self.titulo = QLabel("Gestión Clínica")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo.setStyleSheet("""
            font-size: 34px;
            font-weight: bold;
            color: #1e3a8a;
        """)

        # Subtítulo
        self.subtitulo = QLabel("Sistema")
        self.subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitulo.setStyleSheet("""
            font-size: 16px;
            color: #475569;
        """)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        self.progress.setFixedWidth(400)

        # Texto carga
        self.loading_text = QLabel("Inicializando...")
        self.loading_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_text.setStyleSheet("""
            font-size: 14px;
            color: #334155;
        """)

        # Autor
        self.autor = QLabel("Desarrollado por Daniel Andrade • v1.3")
        self.autor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.autor.setStyleSheet("""
            font-size: 12px;
            color: #64748b;
        """)

        layout.addStretch()
        layout.addWidget(self.logo)
        layout.addSpacing(15)
        layout.addWidget(self.titulo)
        layout.addWidget(self.subtitulo)
        layout.addSpacing(25)
        layout.addWidget(self.progress)
        layout.addWidget(self.loading_text)
        layout.addStretch()
        layout.addWidget(self.autor)

        self.valor = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar)
        self.timer.start(25)

    def actualizar(self):
        self.valor += 1
        self.progress.setValue(self.valor)

        if self.valor < 25:
            self.loading_text.setText("Cargando módulos...")
        elif self.valor < 50:
            self.loading_text.setText("Leyendo equipos...")
        elif self.valor < 75:
            self.loading_text.setText("Preparando interfaz...")
        else:
            self.loading_text.setText("Finalizando...")

        if self.valor >= 100:
            self.timer.stop()
            self.close()