import json
import os
import logging

log = logging.getLogger(__name__)   # Logger del módulo
class Storage:
    def __init__(self, file_path="data/weather.json"):
        self.file_path = file_path


    def load_data(self):
        """Lee el archivo JSON y devuelve la lista de registros."""
        if not os.path.exists(self.file_path):
            log.warning(f"Archivo {self.file_path} no encontrado. Devolviendo lista vacía.")
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list):
                log.info(f"{len(data)} registros cargados desde {self.file_path}.")
                return data
            else:
                log.error(f"Formato inválido en {self.file_path}. Se esperaba una lista.")
                return []

        except json.JSONDecodeError:
            log.error(f"JSON mal formado en {self.file_path}.")
            return []

        except Exception as e:
            log.exception(f"Error inesperado al leer {self.file_path}: {e}")
            return []


    def save_data(self, data):
        """Guarda la lista completa de registros en el archivo JSON."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            log.info(f"Datos guardados correctamente en {self.file_path}. Total registros: {len(data)}")

        except Exception as e:
            log.exception(f"Error guardando datos en {self.file_path}: {e}")


    def is_duplicate(self, new_record, existing_data):
        """
        Comprueba si un registro es duplicado por date + city.
        """
        for record in existing_data:
            if record["date"] == new_record["date"] and record["city"] == new_record["city"]:
                log.warning(f"Registro duplicado detectado: {new_record}")
                return True

        return False


    def add_record(self, new_record):
        """
        Añade un registro si no es duplicado.
        """
        data = self.load_data()

        if self.is_duplicate(new_record, data):
            log.info("Registro no guardado por duplicado.")
            return "Duplicate record. Not saved."

        data.append(new_record)
        self.save_data(data)

        log.info(f"Nuevo registro añadido: {new_record}")
        return "Record saved successfully."




