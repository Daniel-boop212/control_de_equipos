import os

from paths import data_path, resource_path


DEFAULT_CLINIC_NAME = "Clinica"
LOGO_CONFIG_PATH = data_path("assets/logo_actual.txt")
CLINIC_NAME_CONFIG_PATH = data_path("assets/nombre_clinica.txt")


def get_clinic_logo_path():
    ruta = _leer_texto(LOGO_CONFIG_PATH)

    if ruta:
        candidatos = [ruta]
        if not os.path.isabs(ruta):
            candidatos.append(data_path(ruta))

        for candidato in candidatos:
            if os.path.exists(candidato):
                return candidato

    return resource_path("assets/logo_clinica.jpg")


def save_clinic_logo_path(ruta):
    _guardar_texto(LOGO_CONFIG_PATH, ruta)


def get_clinic_name():
    return _leer_texto(CLINIC_NAME_CONFIG_PATH) or DEFAULT_CLINIC_NAME


def save_clinic_name(nombre):
    _guardar_texto(CLINIC_NAME_CONFIG_PATH, nombre.strip())


def _leer_texto(ruta):
    if not os.path.exists(ruta):
        return None

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
    except OSError:
        return None

    return contenido or None


def _guardar_texto(ruta, contenido):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)
