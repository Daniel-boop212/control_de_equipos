from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Image, Table, TableStyle
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from datetime import datetime
import os


LOGO_PATH = "assets/logo_clinica.jpg"


def generar_pdf_hoja_vida(equipo, ruta):
    doc = SimpleDocTemplate(
        ruta,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    estilos = getSampleStyleSheet()
    elementos = []

    # ================= HEADER =================
    if os.path.exists(LOGO_PATH):
        logo = Image(LOGO_PATH, width=4*cm, height=2*cm)
        elementos.append(logo)

    elementos.append(Spacer(1, 10))

    titulo = Paragraph(
        "<b>HOJA DE VIDA DEL EQUIPO</b>",
        estilos["Title"]
    )
    elementos.append(titulo)
    elementos.append(Spacer(1, 20))

    # ================= IMAGEN EQUIPO =================
    imagen = equipo.get("imagen")

    if imagen and os.path.exists(imagen):
        img = Image(imagen, width=10*cm, height=7*cm)
        elementos.append(img)
        elementos.append(Spacer(1, 20))

    # ================= TABLA INFO =================
    datos = [["Campo", "Valor"]]

    ignorar = {
        "mantenimientos",
        "pdf_mantenimiento",
        "pdf_calibracion",
        "imagen"
    }

    for k, v in equipo.items():
        if k in ignorar:
            continue

        datos.append([
            k.replace("_", " ").title(),
            str(v)
        ])

    tabla = Table(datos, colWidths=[6*cm, 9*cm])

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563eb")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 25))

    # ================= MANTENIMIENTOS =================
    mantenimientos = equipo.get("mantenimientos", [])

    elementos.append(
        Paragraph("<b>HISTORIAL DE MANTENIMIENTOS</b>", estilos["Heading2"])
    )
    elementos.append(Spacer(1, 10))

    if not mantenimientos:
        elementos.append(
            Paragraph("No hay mantenimientos registrados.", estilos["Normal"])
        )
    else:
        for i, m in enumerate(mantenimientos, 1):

            datos_tarjeta = [
        ["Mantenimiento", f"#{i}"],
        ["Fecha", m.get("fecha", "")],
        ["Tipo", m.get("tipo", "")],
        ["Responsable", m.get("responsable", "")],
        ["Documento", m.get("documento_responsable", "")],
        ["Descripción", m.get("descripcion", "")],
        ["Próximo", m.get("fecha_proxima", "")]
            ]

            tarjeta = Table(datos_tarjeta, colWidths=[4*cm, 11*cm])

            tarjeta.setStyle(TableStyle([
            # borde general
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#2563eb")),

        # líneas internas suaves
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),

        # encabezado de cada fila
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),

        # estilo general
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),

        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 6),
            ]))

        elementos.append(tarjeta)
        elementos.append(Spacer(1, 15))

    # ================= FOOTER =================
    elementos.append(Spacer(1, 20))

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    footer = Paragraph(
        f"<i>Documento generado el {fecha}</i>",
        estilos["Italic"]
    )

    elementos.append(footer)

    # ================= GENERAR =================
    doc.build(elementos)

    import sys
    import subprocess

    try:
        if sys.platform.startswith("win"):
            os.startfile(ruta)
        elif sys.platform.startswith("darwin"):
            subprocess.run(["open", ruta])
        else:
            subprocess.run(["xdg-open", ruta])
    except Exception as e:
        print("No se pudo abrir el PDF:", e)