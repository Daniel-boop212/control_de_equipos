from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTextBrowser, QPushButton
)


class AyudaWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ayuda")
        self.resize(800, 500)

        self.setStyleSheet("""
        QDialog {
            background: white;
        }

        QTextBrowser {
            background: white;
            border: 1px solid #dbe3ee;
            border-radius: 12px;
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

        texto = QTextBrowser()
        texto.setHtml("""
        <h1>Manual de uso</h1>

        <h2>1. Servicios</h2>
        <p>
        En el panel izquierdo puedes crear o eliminar servicios
        (Ej: UCI, Laboratorio, Radiología).
        </p>

        <h2>2. Equipos</h2>
        <p>
        Selecciona un servicio y agrega equipos usando el botón
        <b>Agregar</b>.
        </p>

        <h2>3. Categorías</h2>
        <ul>
            <li>Biomédico</li>
            <li>Cómputo</li>
            <li>Refrigeración</li>
            <li>Muebles y enseres</li>
        </ul>

        <h2>4. Mantenimientos</h2>
        <p>
        Selecciona un equipo y presiona <b>Mantenimiento</b>
        para registrar uno nuevo.
        </p>

        <h2>5. Estados</h2>
        <ul>
            <li>🔵 Recién mantenido</li>
            <li>🟢 Al día</li>
            <li>🟡 Próximo a vencer (30 días o menos)</li>
            <li>🔴 Vencido</li>
            <li>⚪ Sin mantenimiento programado</li>
        </ul>

        <h2>6. Alertas</h2>
        <p>
        El botón Alertas muestra equipos próximos a vencer
        o con mantenimiento vencido.
        </p>

        <h2>7. PDF</h2>
        <p>
        Puedes exportar la hoja de vida completa de un equipo
        en formato PDF.
        </p>

        <h2>Consejos</h2>
        <ul>
            <li>Registra mantenimientos apenas se realicen.</li>
            <li>Adjunta documentos cuando sea posible.</li>
            <li>Revisa alertas periódicamente.</li>
        </ul>
        """)

        layout.addWidget(texto)

        btn = QPushButton("Cerrar")
        btn.clicked.connect(self.close)
        layout.addWidget(btn)