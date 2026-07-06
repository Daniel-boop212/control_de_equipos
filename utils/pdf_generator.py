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
import sys
import subprocess

LOGO_PATH = "assets/logo_clinica.jpg"


def estado_legible(estado):
    mapa = {
        "🔴": "Vencido",
        "🟡": "Próximo a vencer",
        "🟢": "Al día",
        "🔵": "Recién mantenido",
        "⚪": "Sin mantenimiento"
    }
    return mapa.get(estado, estado)


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
    logo = ""
    if os.path.exists(LOGO_PATH):
        logo = Image(LOGO_PATH, width=4 * cm, height=2 * cm)

    header = Table([
        [
            logo,
            Paragraph(
                "<b>HOJA DE VIDA DEL EQUIPO</b><br/>Sistema de Gestión Clínica",
                estilos["Title"]
            )
        ]
    ], colWidths=[4.5 * cm, 10.5 * cm])

    header.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -1), 2, colors.HexColor("#2563eb"))
    ]))

    elementos.append(header)
    elementos.append(Spacer(1, 20))

    # ================= RESUMEN =================
    nombre = equipo.get("nombre", equipo.get("nombre_equipo", "Sin nombre"))
    categoria = equipo.get("categoria", "N/A")
    servicio = equipo.get("servicio", "N/A")
    estado = estado_legible(equipo.get("estado", "⚪"))

    resumen = Table([
        ["Equipo", nombre],
        ["Categoría", categoria],
        ["Servicio", servicio],
        ["Estado", estado]
    ], colWidths=[4 * cm, 11 * cm])

    resumen.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#dbeafe")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6)
    ]))

    elementos.append(resumen)
    elementos.append(Spacer(1, 20))

    # ================= IMAGEN =================
    imagen = equipo.get("imagen")

    if imagen and os.path.exists(imagen):
        img = Image(imagen)
        img._restrictSize(12 * cm, 8 * cm)
        elementos.append(img)
        elementos.append(Spacer(1, 20))

    # ================= TABLA INFO =================
    elementos.append(
        Paragraph("<b>INFORMACIÓN DETALLADA</b>", estilos["Heading2"])
    )
    elementos.append(Spacer(1, 10))

    ignorar = {
        "mantenimientos",
        "pdf_mantenimiento",
        "pdf_calibracion",
        "imagen",
        "categoria",
        "servicio",
        "estado"
    }

    datos = [["Campo", "Valor"]]

    orden_preferido = [
        "codigo_equipo",
        "nombre",
        "marca",
        "modelo",
        "serie",
        "ubicacion",
        "proveedor",
        "fecha_compra",
        "fecha_adquisicion",
        "garantia",
        "vencimiento_garantia"
    ]

    agregados = set()

    for campo in orden_preferido:
        if campo in equipo and campo not in ignorar:
            datos.append([
                campo.replace("_", " ").title(),
                str(equipo[campo])
            ])
            agregados.add(campo)

    for k, v in equipo.items():
        if k in ignorar or k in agregados:
            continue

        datos.append([
            k.replace("_", " ").title(),
            str(v)
        ])

    tabla = Table(datos, colWidths=[6 * cm, 9 * cm])

    estilo = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563eb")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]

    for i in range(1, len(datos)):
        color = colors.whitesmoke if i % 2 == 0 else colors.white
        estilo.append(("BACKGROUND", (0, i), (-1, i), color))

    tabla.setStyle(TableStyle(estilo))

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

            tarjeta = Table(datos_tarjeta, colWidths=[4 * cm, 11 * cm])

            tarjeta.setStyle(TableStyle([
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#2563eb")),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
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

    try:
        if sys.platform.startswith("win"):
            os.startfile(ruta)
        elif sys.platform.startswith("darwin"):
            subprocess.run(["open", ruta])
        else:
            subprocess.run(["xdg-open", ruta])
    except Exception as e:
        print("No se pudo abrir el PDF:", e)