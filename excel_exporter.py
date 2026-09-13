import os
import zipfile
from datetime import datetime
from xml.sax.saxutils import escape


BASE_HEADERS = [
    "nombre",
    "categoria",
    "servicio",
    "estado",
    "marca",
    "modelo",
    "serie",
    "ubicacion",
    "tipo",
    "tipo_equipo",
    "fecha_compra",
    "fecha_adquisicion",
    "proveedor",
    "garantia",
    "cantidad_mantenimientos",
    "ultimo_mantenimiento_fecha",
    "ultimo_mantenimiento_tipo",
    "ultimo_mantenimiento_proxima",
    "ultimo_mantenimiento_responsable",
    "ultimo_mantenimiento_descripcion",
    "ultimo_pdf_mantenimiento",
    "ultimo_pdf_calibracion",
]


def exportar_equipos_excel(equipos, ruta):
    if not ruta.lower().endswith(".xlsx"):
        ruta += ".xlsx"

    filas = [_normalizar_equipo(equipo) for equipo in equipos]
    headers = _headers(filas)
    rows = [headers] + [[fila.get(h, "") for h in headers] for fila in filas]

    os.makedirs(os.path.dirname(os.path.abspath(ruta)), exist_ok=True)

    with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as xlsx:
        xlsx.writestr("[Content_Types].xml", _content_types())
        xlsx.writestr("_rels/.rels", _rels())
        xlsx.writestr("xl/workbook.xml", _workbook())
        xlsx.writestr("xl/_rels/workbook.xml.rels", _workbook_rels())
        xlsx.writestr("xl/styles.xml", _styles())
        xlsx.writestr("xl/worksheets/sheet1.xml", _sheet(rows))

    return ruta


def _normalizar_equipo(equipo):
    fila = {}

    for clave, valor in equipo.items():
        if clave == "mantenimientos":
            continue
        fila[clave] = _texto(valor)

    mantenimientos = equipo.get("mantenimientos", [])
    fila["cantidad_mantenimientos"] = len(mantenimientos)

    if mantenimientos:
        ultimo = mantenimientos[-1]
        fila["ultimo_mantenimiento_fecha"] = _texto(ultimo.get("fecha", ""))
        fila["ultimo_mantenimiento_tipo"] = _texto(ultimo.get("tipo", ""))
        fila["ultimo_mantenimiento_proxima"] = _texto(ultimo.get("fecha_proxima", ""))
        fila["ultimo_mantenimiento_responsable"] = _texto(ultimo.get("responsable", ""))
        fila["ultimo_mantenimiento_descripcion"] = _texto(ultimo.get("descripcion", ""))
        fila["ultimo_pdf_mantenimiento"] = _texto(ultimo.get("pdf_mantenimiento", ""))
        fila["ultimo_pdf_calibracion"] = _texto(ultimo.get("pdf_calibracion", ""))

    return fila


def _headers(filas):
    vistos = set()
    headers = []

    for clave in BASE_HEADERS:
        if any(clave in fila for fila in filas):
            headers.append(clave)
            vistos.add(clave)

    for fila in filas:
        for clave in fila:
            if clave not in vistos:
                headers.append(clave)
                vistos.add(clave)

    return headers


def _sheet(rows):
    xml_rows = []
    widths = _column_widths(rows)

    for row_index, row in enumerate(rows, start=1):
        cells = []
        style = ' s="1"' if row_index == 1 else ""
        for col_index, value in enumerate(row, start=1):
            cell_ref = f"{_columna(col_index)}{row_index}"
            cells.append(
                f'<c r="{cell_ref}"{style} t="inlineStr"><is><t>{escape(_texto(value))}</t></is></c>'
            )
        xml_rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')

    cols = "".join(
        f'<col min="{i}" max="{i}" width="{width}" customWidth="1"/>'
        for i, width in enumerate(widths, start=1)
    )

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
        f'<cols>{cols}</cols>'
        f'<sheetData>{"".join(xml_rows)}</sheetData>'
        '<autoFilter ref="A1:XFD1"/>'
        '</worksheet>'
    )


def _column_widths(rows):
    if not rows:
        return []

    widths = []
    for col_index in range(len(rows[0])):
        max_len = 10
        for row in rows[:200]:
            if col_index < len(row):
                max_len = max(max_len, len(_texto(row[col_index])))
        widths.append(min(max_len + 2, 45))
    return widths


def _columna(numero):
    letras = ""
    while numero:
        numero, resto = divmod(numero - 1, 26)
        letras = chr(65 + resto) + letras
    return letras


def _texto(valor):
    if valor is None:
        return ""
    if isinstance(valor, (dict, list)):
        valor = str(valor)
    else:
        valor = str(valor)

    return "".join(
        caracter
        for caracter in valor
        if caracter in "\t\n\r" or ord(caracter) >= 32
    )


def _content_types():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>"""


def _rels():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""


def _workbook():
    fecha = escape(datetime.now().strftime("%Y-%m-%d"))
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="Equipos {fecha}" sheetId="1" r:id="rId1"/></sheets>
</workbook>"""


def _workbook_rels():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""


def _styles():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><color rgb="FFFFFFFF"/><sz val="11"/><name val="Calibri"/></font></fonts>
<fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF2563EB"/><bgColor indexed="64"/></patternFill></fill></fills>
<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/></cellXfs>
</styleSheet>"""
