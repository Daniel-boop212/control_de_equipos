import json
import os
import shutil
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path, PurePosixPath

from backup_manager import BackupManager
from paths import data_path


class DataTransferError(Exception):
    pass


class DataTransferManager:
    JSON_FILES = (
        "data/servicios.json",
        "data/equipos.json",
    )
    DATA_DIRS = (
        "storage",
        "backups",
    )
    IMAGE_DIR = os.path.join("storage", "imagenes")
    FILE_KEYS = {
        "imagen",
        "pdf_mantenimiento",
        "pdf_calibracion",
    }
    MANIFEST_NAME = "gestion_clinica_export.json"

    @classmethod
    def exportar(cls, destino_zip):
        destino_zip = os.path.abspath(destino_zip)
        if not destino_zip.lower().endswith(".zip"):
            destino_zip += ".zip"

        app_root = cls.app_root()
        carpeta_destino = os.path.dirname(destino_zip)
        if carpeta_destino:
            os.makedirs(carpeta_destino, exist_ok=True)

        equipos = cls._cargar_json(
            os.path.join(app_root, "data", "equipos.json"),
            default=[],
        )

        manifest = {
            "formato": "gestion_clinica_export",
            "version": 1,
            "creado": datetime.now().isoformat(timespec="seconds"),
            "referencias": {},
            "logo_actual": None,
            "nombre_clinica": None,
        }

        agregados = set()

        with zipfile.ZipFile(
            destino_zip,
            "w",
            compression=zipfile.ZIP_DEFLATED,
        ) as zipf:
            for ruta_relativa in cls.JSON_FILES:
                ruta = os.path.join(app_root, ruta_relativa)
                cls._agregar_si_existe(zipf, ruta, ruta_relativa, agregados)

            for carpeta_relativa in cls.DATA_DIRS:
                cls._agregar_carpeta(
                    zipf,
                    os.path.join(app_root, carpeta_relativa),
                    carpeta_relativa,
                    agregados,
                )

            logo_txt = os.path.join(app_root, "assets", "logo_actual.txt")
            cls._agregar_si_existe(zipf, logo_txt, "assets/logo_actual.txt", agregados)

            nombre_clinica_txt = os.path.join(app_root, "assets", "nombre_clinica.txt")
            cls._agregar_si_existe(
                zipf,
                nombre_clinica_txt,
                "assets/nombre_clinica.txt",
                agregados,
            )

            for valor in cls._iterar_referencias(equipos):
                cls._agregar_referencia(
                    zipf,
                    app_root,
                    valor,
                    manifest["referencias"],
                    agregados,
                )

            logo_actual = cls._leer_texto(logo_txt)
            if logo_actual:
                manifest["logo_actual"] = logo_actual
                cls._agregar_referencia(
                    zipf,
                    app_root,
                    logo_actual,
                    manifest["referencias"],
                    agregados,
                )

            nombre_clinica = cls._leer_texto(nombre_clinica_txt)
            if nombre_clinica:
                manifest["nombre_clinica"] = nombre_clinica

            zipf.writestr(
                cls.MANIFEST_NAME,
                json.dumps(manifest, indent=4, ensure_ascii=False),
            )

        return destino_zip

    @classmethod
    def importar(cls, origen):
        origen = os.path.abspath(origen)

        if not os.path.exists(origen):
            raise DataTransferError("La ruta seleccionada no existe.")

        if os.path.isfile(origen):
            if not zipfile.is_zipfile(origen):
                raise DataTransferError("Selecciona un archivo ZIP valido.")

            with tempfile.TemporaryDirectory() as tmp:
                cls._extraer_zip_seguro(origen, tmp)
                return cls._importar_desde_carpeta(tmp)

        return cls._importar_desde_carpeta(origen)

    @classmethod
    def app_root(cls):
        return os.path.abspath(data_path(""))

    @classmethod
    def _importar_desde_carpeta(cls, carpeta):
        source_root = cls._encontrar_raiz_datos(carpeta)
        app_root = cls.app_root()

        servicios_ruta = os.path.join(source_root, "data", "servicios.json")
        equipos_ruta = os.path.join(source_root, "data", "equipos.json")

        servicios = cls._cargar_json(servicios_ruta, default=None)
        equipos = cls._cargar_json(equipos_ruta, default=None)

        if not isinstance(servicios, list):
            raise DataTransferError("servicios.json no tiene el formato esperado.")
        if not isinstance(equipos, list):
            raise DataTransferError("equipos.json no tiene el formato esperado.")

        manifest = cls._cargar_manifest(source_root)
        referencias = dict(manifest.get("referencias", {}))

        cls._preparar_destino(app_root)

        cls._respaldar_actuales()

        cls._copiar_carpeta_merge(
            os.path.join(source_root, "storage"),
            os.path.join(app_root, "storage"),
            sobrescribir=True,
        )
        cls._copiar_carpeta_merge(
            os.path.join(source_root, "backups"),
            os.path.join(app_root, "backups"),
            sobrescribir=False,
        )
        cls._copiar_carpeta_merge(
            os.path.join(source_root, "assets"),
            os.path.join(app_root, "assets"),
            sobrescribir=True,
        )

        reemplazos = cls._copiar_referencias(
            source_root,
            app_root,
            equipos,
            referencias,
        )

        if reemplazos:
            cls._reemplazar_referencias(equipos, reemplazos)

        logo_actual = manifest.get("logo_actual")
        if not logo_actual:
            logo_actual = cls._leer_texto(
                os.path.join(source_root, "assets", "logo_actual.txt")
            )

        if logo_actual:
            nuevo_logo = reemplazos.get(logo_actual)
            if not nuevo_logo:
                nuevo_logo = cls._copiar_logo_antiguo(source_root, app_root, logo_actual)

            if nuevo_logo:
                os.makedirs(os.path.join(app_root, "assets"), exist_ok=True)
                with open(
                    os.path.join(app_root, "assets", "logo_actual.txt"),
                    "w",
                    encoding="utf-8",
                ) as archivo:
                    archivo.write(nuevo_logo)

        nombre_clinica = manifest.get("nombre_clinica")
        if not nombre_clinica:
            nombre_clinica = cls._leer_texto(
                os.path.join(source_root, "assets", "nombre_clinica.txt")
            )

        if nombre_clinica:
            os.makedirs(os.path.join(app_root, "assets"), exist_ok=True)
            with open(
                os.path.join(app_root, "assets", "nombre_clinica.txt"),
                "w",
                encoding="utf-8",
            ) as archivo:
                archivo.write(nombre_clinica)

        with open(
            os.path.join(app_root, "data", "servicios.json"),
            "w",
            encoding="utf-8",
        ) as archivo:
            json.dump(servicios, archivo, indent=4, ensure_ascii=False)

        with open(
            os.path.join(app_root, "data", "equipos.json"),
            "w",
            encoding="utf-8",
        ) as archivo:
            json.dump(equipos, archivo, indent=4, ensure_ascii=False)

        return {
            "servicios": len(servicios),
            "equipos": len(equipos),
            "archivos_reubicados": len(reemplazos),
        }

    @classmethod
    def _preparar_destino(cls, app_root):
        os.makedirs(os.path.join(app_root, "data"), exist_ok=True)
        os.makedirs(os.path.join(app_root, "storage"), exist_ok=True)
        os.makedirs(os.path.join(app_root, cls.IMAGE_DIR), exist_ok=True)
        os.makedirs(os.path.join(app_root, "backups"), exist_ok=True)

    @classmethod
    def _respaldar_actuales(cls):
        for ruta_relativa in cls.JSON_FILES:
            BackupManager.crear_backup(data_path(ruta_relativa))

    @classmethod
    def _cargar_json(cls, ruta, default):
        if not os.path.exists(ruta):
            if default is None:
                raise DataTransferError(f"No se encontro {os.path.basename(ruta)}.")
            return default

        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, OSError) as error:
            raise DataTransferError(f"No se pudo leer {ruta}: {error}") from error

    @classmethod
    def _cargar_manifest(cls, source_root):
        ruta = os.path.join(source_root, cls.MANIFEST_NAME)
        if not os.path.exists(ruta):
            return {}

        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                manifest = json.load(archivo)
        except (json.JSONDecodeError, OSError):
            return {}

        if not isinstance(manifest, dict):
            return {}

        return manifest

    @classmethod
    def _encontrar_raiz_datos(cls, carpeta):
        carpeta = os.path.abspath(carpeta)

        candidatos = [carpeta]
        try:
            for raiz, dirs, _ in os.walk(carpeta):
                if "data" in dirs:
                    candidatos.append(raiz)
        except OSError as error:
            raise DataTransferError(f"No se pudo revisar la carpeta: {error}") from error

        for candidato in candidatos:
            if all(os.path.exists(os.path.join(candidato, p)) for p in cls.JSON_FILES):
                return candidato

        raise DataTransferError(
            "No se encontro una instalacion valida con data/servicios.json y data/equipos.json."
        )

    @classmethod
    def _extraer_zip_seguro(cls, zip_path, destino):
        destino_path = Path(destino).resolve()

        with zipfile.ZipFile(zip_path) as zipf:
            for info in zipf.infolist():
                ruta_destino = (destino_path / info.filename).resolve()
                try:
                    if os.path.commonpath(
                        [str(ruta_destino), str(destino_path)]
                    ) != str(destino_path):
                        raise DataTransferError("El ZIP contiene rutas no seguras.")
                except ValueError as error:
                    raise DataTransferError("El ZIP contiene rutas no seguras.")
            zipf.extractall(destino)

    @classmethod
    def _agregar_si_existe(cls, zipf, ruta, arcname, agregados):
        if not os.path.isfile(ruta):
            return

        arcname = cls._zip_name(arcname)
        if arcname in agregados:
            return

        zipf.write(ruta, arcname)
        agregados.add(arcname)

    @classmethod
    def _agregar_carpeta(cls, zipf, carpeta, arcbase, agregados):
        if not os.path.isdir(carpeta):
            return

        for raiz, _, archivos in os.walk(carpeta):
            for nombre in archivos:
                ruta = os.path.join(raiz, nombre)
                rel = os.path.relpath(ruta, carpeta)
                arcname = os.path.join(arcbase, rel)
                cls._agregar_si_existe(zipf, ruta, arcname, agregados)

    @classmethod
    def _agregar_referencia(cls, zipf, app_root, valor, referencias, agregados):
        ruta = cls._resolver_ruta(valor, app_root)
        if not ruta or not os.path.isfile(ruta):
            return

        rel_app = cls._relativa_si_esta_dentro(ruta, app_root)
        if rel_app:
            arcname = rel_app
        else:
            arcname = os.path.join(
                "external_files",
                f"{abs(hash(os.path.abspath(ruta)))}_{os.path.basename(ruta)}",
            )

        cls._agregar_si_existe(zipf, ruta, arcname, agregados)
        referencias[valor] = cls._zip_name(arcname)

    @classmethod
    def _copiar_referencias(cls, source_root, app_root, equipos, referencias):
        reemplazos = {}

        valores = set(cls._iterar_referencias(equipos))
        valores.update(referencias.keys())

        for valor in valores:
            origen = None
            if valor in referencias:
                origen = os.path.join(source_root, *PurePosixPath(referencias[valor]).parts)

            if not origen or not os.path.isfile(origen):
                origen = cls._resolver_ruta(valor, source_root)

            if not origen or not os.path.isfile(origen):
                continue

            destino, nuevo_valor = cls._destino_referencia(
                valor,
                origen,
                app_root,
                source_root,
            )

            os.makedirs(os.path.dirname(destino), exist_ok=True)
            cls._copiar_archivo(origen, destino)

            if nuevo_valor != valor:
                reemplazos[valor] = nuevo_valor

        return reemplazos

    @classmethod
    def _copiar_logo_antiguo(cls, source_root, app_root, valor):
        origen = cls._resolver_ruta(valor, source_root)
        if not origen or not os.path.isfile(origen):
            return None

        destino = os.path.join(
            app_root,
            "assets",
            f"logo_importado_{os.path.basename(origen)}",
        )
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        cls._copiar_archivo(origen, destino)
        return destino

    @classmethod
    def _destino_referencia(cls, valor, origen, app_root, source_root):
        if cls._parece_imagen(origen):
            return cls._destino_imagen(origen, app_root, source_root)

        if not os.path.isabs(valor):
            destino = cls._safe_join(app_root, valor)
            if destino:
                return destino, valor

        rel_source = cls._relativa_si_esta_dentro(valor, source_root)
        if rel_source:
            destino = cls._safe_join(app_root, rel_source)
            if destino:
                return destino, destino

        rel_origen = cls._relativa_si_esta_dentro(origen, source_root)
        if rel_origen and rel_origen.split(os.sep)[0] != "external_files":
            destino = cls._safe_join(app_root, rel_origen)
            if destino:
                return destino, destino

        carpeta = "imagenes" if cls._parece_imagen(origen) else "archivos"
        destino = os.path.join(
            app_root,
            "storage",
            carpeta,
            f"{abs(hash(os.path.abspath(origen)))}_{os.path.basename(origen)}",
        )
        return destino, destino

    @classmethod
    def _destino_imagen(cls, origen, app_root, source_root):
        rel_origen = cls._relativa_si_esta_dentro(origen, source_root)
        if rel_origen:
            partes = rel_origen.replace("\\", os.sep).split(os.sep)
            if len(partes) >= 2 and partes[0] == "storage" and partes[1] == "imagenes":
                destino = cls._safe_join(app_root, rel_origen)
                if destino:
                    return destino, rel_origen

        nombre = os.path.basename(origen)
        destino = os.path.join(app_root, cls.IMAGE_DIR, nombre)

        if os.path.exists(destino) and os.path.abspath(origen) != os.path.abspath(destino):
            destino = cls._ruta_unica(destino)

        return destino, os.path.relpath(destino, app_root)

    @classmethod
    def _resolver_ruta(cls, valor, base_root):
        if not valor or not isinstance(valor, str):
            return None

        valor = valor.strip()
        if not valor:
            return None

        if os.path.isabs(valor):
            if os.path.exists(valor):
                return valor
            return None

        ruta = os.path.join(base_root, valor)
        if os.path.exists(ruta):
            return ruta

        ruta_normalizada = os.path.join(base_root, valor.replace("\\", os.sep))
        if os.path.exists(ruta_normalizada):
            return ruta_normalizada

        return None

    @classmethod
    def _iterar_referencias(cls, datos):
        if isinstance(datos, dict):
            for clave, valor in datos.items():
                if clave in cls.FILE_KEYS and isinstance(valor, str) and valor.strip():
                    yield valor
                else:
                    yield from cls._iterar_referencias(valor)
        elif isinstance(datos, list):
            for item in datos:
                yield from cls._iterar_referencias(item)

    @classmethod
    def _reemplazar_referencias(cls, datos, reemplazos):
        if isinstance(datos, dict):
            for clave, valor in list(datos.items()):
                if clave in cls.FILE_KEYS and valor in reemplazos:
                    datos[clave] = reemplazos[valor]
                else:
                    cls._reemplazar_referencias(valor, reemplazos)
        elif isinstance(datos, list):
            for item in datos:
                cls._reemplazar_referencias(item, reemplazos)

    @classmethod
    def _copiar_carpeta_merge(cls, origen, destino, sobrescribir):
        if not os.path.isdir(origen):
            return
        if os.path.abspath(origen) == os.path.abspath(destino):
            return

        for raiz, _, archivos in os.walk(origen):
            rel = os.path.relpath(raiz, origen)
            destino_raiz = destino if rel == "." else os.path.join(destino, rel)
            os.makedirs(destino_raiz, exist_ok=True)

            for archivo in archivos:
                src = os.path.join(raiz, archivo)
                dst = os.path.join(destino_raiz, archivo)

                if not sobrescribir and os.path.exists(dst):
                    dst = cls._ruta_unica(dst)

                cls._copiar_archivo(src, dst)

    @classmethod
    def _copiar_archivo(cls, origen, destino):
        if os.path.abspath(origen) == os.path.abspath(destino):
            return

        shutil.copy2(origen, destino)

    @classmethod
    def _ruta_unica(cls, ruta):
        base, extension = os.path.splitext(ruta)
        contador = 1
        nueva = ruta

        while os.path.exists(nueva):
            nueva = f"{base}_{contador}{extension}"
            contador += 1

        return nueva

    @classmethod
    def _relativa_si_esta_dentro(cls, ruta, base):
        if not ruta or not os.path.isabs(ruta):
            return None

        try:
            ruta_abs = os.path.abspath(ruta)
            base_abs = os.path.abspath(base)
            if os.path.commonpath([ruta_abs, base_abs]) != base_abs:
                return None
        except ValueError:
            return None

        return os.path.relpath(ruta_abs, base_abs)

    @classmethod
    def _safe_join(cls, base, ruta_relativa):
        ruta_relativa = ruta_relativa.replace("\\", os.sep)
        destino = os.path.abspath(os.path.join(base, ruta_relativa))
        base_abs = os.path.abspath(base)

        try:
            if os.path.commonpath([destino, base_abs]) != base_abs:
                return None
        except ValueError:
            return None

        return destino

    @classmethod
    def _leer_texto(cls, ruta):
        if not os.path.exists(ruta):
            return None

        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                contenido = archivo.read().strip()
        except OSError:
            return None

        return contenido or None

    @classmethod
    def _parece_imagen(cls, ruta):
        return os.path.splitext(ruta)[1].lower() in {
            ".png",
            ".jpg",
            ".jpeg",
            ".bmp",
            ".gif",
            ".webp",
        }

    @classmethod
    def _zip_name(cls, ruta):
        return PurePosixPath(*Path(ruta).parts).as_posix()
