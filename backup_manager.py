import os
import sys
import shutil
from datetime import datetime
import json

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def app_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class BackupManager:
    MAX_BACKUPS_POR_ARCHIVO = 20

    @staticmethod
    def crear_backup(ruta_archivo):
        if not os.path.exists(ruta_archivo):
            return None

        carpeta_backup = app_path("backups")
        os.makedirs(carpeta_backup, exist_ok=True)

        nombre_original = os.path.basename(ruta_archivo)
        nombre_sin_extension = os.path.splitext(nombre_original)[0]
        extension = os.path.splitext(nombre_original)[1]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        nombre_backup = (
            f"{nombre_sin_extension}_{timestamp}{extension}"
        )

        ruta_backup = os.path.join(
            carpeta_backup,
            nombre_backup
        )

        shutil.copy2(ruta_archivo, ruta_backup)

        BackupManager.limpiar_backups(nombre_sin_extension)

        return ruta_backup

    @staticmethod
    def limpiar_backups(nombre_archivo):
        carpeta_backup = app_path("backups")

        if not os.path.exists(carpeta_backup):
            return

        archivos_relacionados = []

        for archivo in os.listdir(carpeta_backup):
            ruta = os.path.join(carpeta_backup, archivo)

            if not os.path.isfile(ruta):
                continue

            if archivo.startswith(nombre_archivo + "_"):
                archivos_relacionados.append(ruta)

        archivos_relacionados.sort(
            key=lambda x: os.path.getmtime(x),
            reverse=True
        )

        if (
            len(archivos_relacionados)
            <= BackupManager.MAX_BACKUPS_POR_ARCHIVO
        ):
            return

        archivos_a_borrar = archivos_relacionados[
            BackupManager.MAX_BACKUPS_POR_ARCHIVO:
        ]

        for archivo in archivos_a_borrar:
            try:
                os.remove(archivo)
            except Exception as e:
                print(
                    f"No se pudo borrar backup {archivo}: {e}"
                )
    
    @staticmethod
    def restaurar_ultimo_backup(nombre_archivo):
        carpeta_backup = app_path("backups")

        if not os.path.exists(carpeta_backup):
            return False

        backups = []

        for archivo in os.listdir(carpeta_backup):
            ruta = os.path.join(carpeta_backup, archivo)

            if not os.path.isfile(ruta):
                continue

            if archivo.startswith(nombre_archivo + "_"):
                backups.append(ruta)

        if not backups:
            return False

        backups.sort(
        key=lambda x: os.path.getmtime(x),
        reverse=True
        )

        ultimo_backup = backups[0]
        destino = app_path(os.path.join("data", f"{nombre_archivo}.json"))

        shutil.copy2(ultimo_backup, destino)
        return True
    
    @staticmethod
    def cargar_json_seguro(ruta_archivo):
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                return json.load(archivo)

        except (json.JSONDecodeError, OSError, ValueError):
            nombre = os.path.splitext(
                os.path.basename(ruta_archivo)
            )[0]

            restaurado = BackupManager.restaurar_ultimo_backup(
                nombre
            )

            if not restaurado:
                raise Exception(
                    f"{ruta_archivo} corrupto y sin backup."
                )

            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                try:
                    return json.load(archivo)
                except:
                    raise Exception(
            f"Backup restaurado pero también está corrupto: {ruta_archivo}"
                 )
                
    @staticmethod
    def obtener_historial_backups():
        carpeta_backup = app_path("backups")

        if not os.path.exists(carpeta_backup):
            return []

        backups = []

        for archivo in os.listdir(carpeta_backup):
            ruta = os.path.join(carpeta_backup, archivo)

            if not os.path.isfile(ruta):
                continue

            fecha = datetime.fromtimestamp(
            os.path.getmtime(ruta)
            ).strftime("%Y-%m-%d %H:%M:%S")

            backups.append({
            "nombre": archivo,
            "ruta": ruta,
            "fecha": fecha,
            "tamano": os.path.getsize(ruta)
            })

        backups.sort(
        key=lambda x: os.path.getmtime(x["ruta"]),
        reverse=True
        )

        return backups
    
    @staticmethod
    def restaurar_backup_especifico(ruta_backup):
        if not os.path.exists(ruta_backup):
            return False

        nombre = os.path.basename(ruta_backup)

        if nombre.startswith("equipos_"):
            destino = app_path("data/equipos.json")
        elif nombre.startswith("servicios_"):
            destino = app_path("data/servicios.json")
        else:
            return False

        shutil.copy2(ruta_backup, destino)
        return True