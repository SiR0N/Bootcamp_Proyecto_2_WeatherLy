import json
import os
import logging

log = logging.getLogger(__name__)   # Logger del módulo

FILE_PATH = "data/weather.json"


def load_data():
    """Lee el archivo JSON y devuelve la lista de registros."""
    if not os.path.exists(FILE_PATH):
        log.warning(f"Archivo {FILE_PATH} no encontrado. Devolviendo lista vacía.")
        return []

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            log.info(f"{len(data)} registros cargados desde {FILE_PATH}.")
            return data

        log.error(f"Formato inválido en {FILE_PATH}. Se esperaba una lista.")
        return []

    except json.JSONDecodeError:
        log.error(f"JSON mal formado en {FILE_PATH}.")
        return []

    except Exception as e:
        log.exception(f"Error inesperado al leer {FILE_PATH}: {e}")
        return []


def save_data(data):
    """Guarda la lista completa de registros en el archivo JSON."""
    try:
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        log.info(f"Datos guardados correctamente en {FILE_PATH}. Total registros: {len(data)}")

    except Exception as e:
        log.exception(f"Error guardando datos en {FILE_PATH}: {e}")


def is_duplicate(new_record, existing_data):
    """
    Comprueba si un registro es duplicado por date + city.
    """
    for record in existing_data:
        if record["date"] == new_record["date"] and record["city"] == new_record["city"]:
            log.warning(f"Registro duplicado detectado: {new_record}")
            return True

    return False


def add_record(new_record):
    """
    Añade un registro si no es duplicado.
    """
    data = load_data()

    if is_duplicate(new_record, data):
        log.info("Registro no guardado por duplicado.")
        return "Duplicate record. Not saved."

    data.append(new_record)
    save_data(data)

    log.info(f"Nuevo registro añadido: {new_record}")
    return "Record saved successfully."
