from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTextBrowser,
    QPushButton, QLabel, QTabWidget
)


class AyudaWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ayuda")
        self.resize(900, 650)

        self.setStyleSheet("""
        QDialog {
            background: white;
        }

        QLabel {
            color: #111827;
        }

        QTabWidget::pane {
            border: 1px solid #dbe3ee;
            border-radius: 10px;
            background: white;
        }

        QTabBar::tab {
            background: #eff6ff;
            color: #1e3a8a;
            padding: 10px 18px;
            margin: 2px;
            border-radius: 8px;
            font-weight: bold;
        }

        QTabBar::tab:selected {
            background: #2563eb;
            color: white;
        }

        QTextBrowser {
            background: white;
            border: none;
            padding: 12px;
            color: #111827;
            font-size: 13px;
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
        """)

        layout = QVBoxLayout()
        self.setLayout(layout)

        titulo = QLabel("❓ Centro de ayuda")
        titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #1e3a8a;
            padding: 8px;
        """)
        layout.addWidget(titulo)

        subtitulo = QLabel(
            "Guía rápida para usar el sistema de inventario y mantenimientos"
        )
        subtitulo.setStyleSheet("""
            font-size: 13px;
            color: #6b7280;
            padding-left: 8px;
            padding-bottom: 8px;
        """)
        layout.addWidget(subtitulo)

        bienvenida = QLabel("""
        💡 <b>Tip:</b> Si eres nuevo, empieza por la pestaña
        <b>General</b> y sigue el orden recomendado.
        """)
        bienvenida.setStyleSheet("""
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 10px;
            padding: 12px;
            color: #1e3a8a;
            font-size: 13px;
        """)
        layout.addWidget(bienvenida)

        tabs = QTabWidget()
        layout.addWidget(tabs)

        tabs.addTab(
            self.crear_tab("""
            <h2>🚀 Primeros pasos</h2>
            <ol>
                <li>Crea un servicio.</li>
                <li>Selecciona el servicio.</li>
                <li>Agrega equipos.</li>
                <li>Registra mantenimientos.</li>
                <li>Consulta alertas.</li>
            </ol>

            <h2>🏥 Servicios</h2>
            <p>
            En el panel izquierdo puedes crear y eliminar servicios.
            Ejemplo: UCI, Urgencias, Radiología.
            </p>
            """),
            "🏠 General"
        )

        tabs.addTab(
            self.crear_tab("""
            <h2>🖥 Equipos</h2>
            <p>
            Selecciona un servicio y usa <b>Agregar</b>.
            </p>

            <h2>📂 Categorías</h2>
            <ul>
                <li>Biomédico</li>
                <li>Cómputo</li>
                <li>Refrigeración</li>
                <li>Muebles y enseres</li>
            </ul>

            <p>
            Cada categoría tiene su propio formulario.
            </p>
            """),
            "🖥 Equipos"
        )

        tabs.addTab(
            self.crear_tab("""
            <h2>🔧 Mantenimientos</h2>

            <p>
            Selecciona un equipo y presiona
            <b>Mantenimiento</b>.
            </p>

            <ul>
                <li>Preventivo</li>
                <li>Correctivo</li>
                <li>Calibración</li>
                <li>Otro</li>
            </ul>

            <p>
            Registra fecha, responsable y próxima revisión.
            </p>
            """),
            "🔧 Mantenimientos"
        )

        tabs.addTab(
            self.crear_tab("""
            <h2>🎨 Estados</h2>
            <ul>
                <li>🔵 Recién mantenido</li>
                <li>🟢 Al día</li>
                <li>🟡 Próximo a vencer</li>
                <li>🔴 Vencido</li>
                <li>⚪ Sin programación</li>
            </ul>

            <h2>⚠ Alertas</h2>
            <p>
            El botón Alertas muestra equipos en amarillo o rojo.
            </p>
            """),
            "⚠ Alertas"
        )

        tabs.addTab(
            self.crear_tab("""
            <h2>📄 PDF</h2>
            <p>
            Puedes exportar la hoja de vida del equipo.
            </p>

            <p>
            Equipos biomédicos permiten adjuntar:
            </p>

            <ul>
                <li>PDF mantenimiento</li>
                <li>PDF calibración</li>
            </ul>
            """),
            "📄 PDF"
        )

        tabs.addTab(
    self.crear_tab("""
    <h2>💾 Almacenamiento</h2>

    <p>
    Esta sección te permite ver cuánto espacio usan tus datos.
    </p>

    <ul>
        <li>JSON del sistema</li>
        <li>Imágenes de equipos</li>
        <li>PDFs de mantenimiento</li>
    </ul>

    <p>
    También puedes ver el porcentaje de uso total y recomendaciones.
    </p>
    """),
    "💾 Almacenamiento"
        )

        tabs.addTab(
    self.crear_tab("""
    <h2>🕒 Backups</h2>

    <p>
    El sistema guarda copias automáticas de seguridad.
    </p>

    <h3>📂 Tipos de backup</h3>
    <ul>
        <li>Equipos</li>
        <li>Servicios</li>
    </ul>

    <h3>🔄 Restauración</h3>
    <p>
    Selecciona un backup y presiona <b>Restaurar</b>.
    El archivo actual será reemplazado.
    </p>

    <h3>⚠ Recomendación</h3>
    <p>
    Haz backups antes de cambios grandes.
    </p>
    """),
    "🕒 Backups"
        )
        
        tabs.addTab(
            self.crear_tab("""
            <h2>💡 Consejos</h2>
            <ul>
                <li>Registra mantenimientos al realizarlos.</li>
                <li>Adjunta PDFs cuando existan.</li>
                <li>Revisa alertas periódicamente.</li>
                <li>Haz copias de seguridad del JSON.</li>
                <li>Monitorea almacenamiento.</li>
            </ul>
            """),
            "💡 Tips"
        )

        footer = QLabel("Versión 1.3 • Sistema de gestión biomédica")
        footer.setStyleSheet("""
            color: #9ca3af;
            font-size: 11px;
            padding-top: 4px;
        """)
        layout.addWidget(footer)

        btn = QPushButton("Cerrar")
        btn.clicked.connect(self.close)
        layout.addWidget(btn)



    def crear_tab(self, html):
        texto = QTextBrowser()
        texto.setHtml(html)
        return texto