from importlib.metadata import files
import json
import os
import logging
import shutil
from datetime import datetime

log = logging.getLogger(__name__)   # Logger del módulo
class Storage:
    def __init__(self, file_path="data/weather.json"):
        self.file_path = file_path
        self.ensure_file_exists()
        self.backup_created = False

    def ensure_file_exists(self):
        """Asegura que el archivo JSON exista."""

        folder = os.path.dirname(self.file_path)

        # Solo crear carpeta si existe nombre de carpeta
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4, ensure_ascii=False)

            log.info(f"Archivo creado automáticamente: {self.file_path}")

    def create_backup(self):
        """
        Crea una copia de seguridad con fecha.
        """
        if not os.path.exists(self.file_path):
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        backup_path = self.file_path.replace(
            ".json",
            f"_{timestamp}.json"
        )

        shutil.copy(self.file_path, backup_path)

        log.info(f"Backup creado: {backup_path}")

    def clean_old_backups(self, max_backups=5):
        """
        Mantiene solo los últimos N backups y borra los antiguos.
        """
        folder = os.path.dirname(self.file_path)

        # Obtener archivos backup
        files = [
            f for f in os.listdir(folder)
            if f.startswith("weather_") and f.endswith(".json")
        ]

        # Ordenarlos por nombre (ya incluye fecha)
        files.sort()

        # Si hay más de los permitidos → borrar los más antiguos
        if len(files) > max_backups:
            to_delete = files[:len(files) - max_backups]

            for f in to_delete:
                path = os.path.join(folder, f)
                os.remove(path)
                log.info(f"Backup antiguo eliminado: {path}")   
    
    
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
            
            #Hacer Backup antes de sobrescribir. Crear solo 1 backup por ejecución para evitar demasiados archivos. Solo si el archivo ya existe (no tiene sentido hacer backup de un archivo vacío).
            if not self.backup_created and os.path.exists(self.file_path):
                self.create_backup()
                self.clean_old_backups() 
                self.backup_created = True

             #  Asegurar archivo antes de guardar
            self.ensure_file_exists()

            #Guardar datos nuevos
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

    def get_last_record(self):
        """Devuelve el último registro guardado o None si está vacío."""
        data = self.load_data()
        if data:
            return data[-1]  # Retorna el último elemento de la lista
        return None



