import json
import os
import logging
import shutil
from datetime import datetime

log = logging.getLogger(__name__)

class Storage:
    def __init__(self, file_path, default_type=list):
        """
        :param file_path: Ruta al archivo JSON.
        :param default_type: list o dict (tipo de dato inicial si el archivo no existe).
        """
        self.file_path = file_path
        self.default_type = default_type
        self.backup_created = False
        self.ensure_file_exists()

    def ensure_file_exists(self):
        folder = os.path.dirname(self.file_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        if not os.path.exists(self.file_path):
            try:
                with open(self.file_path, "w", encoding="utf-8") as file:
                    # Inicializa según el tipo ( [] para lista, {} para diccionario )
                    initial_data = [] if self.default_type is list else {}
                    json.dump(initial_data, file, indent=4, ensure_ascii=False)
                log.info(f"Archivo creado: {self.file_path}")
            except Exception as e:
                log.error(f"Error al crear el archivo: {e}")

    def load_data(self):
        if not os.path.exists(self.file_path):
            return [] if self.default_type is list else {}

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, Exception) as e:
            log.error(f"Error al cargar {self.file_path}: {e}")
            return [] if self.default_type is list else {}

    def save_data(self, data):
        """Guarda datos y gestiona un único backup por sesión."""
        try:
            if not self.backup_created and os.path.exists(self.file_path):
                self.create_backup()
                self.clean_old_backups()
                self.backup_created = True

            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            log.error(f"Error al guardar en {self.file_path}: {e}")

    # --- Métodos para Listas (Historial de Clima) ---

    def add_record(self, new_record):
        """Añade un registro a una lista si no es idéntico al último."""
        data = self.load_data()
        if not isinstance(data, list):
            log.error("Intentando usar add_record en un archivo que no es una lista.")
            return False

        # Verificación básica de duplicados (evita guardar lo mismo dos veces seguidas)
        if data and data[-1] == new_record:
            return "Duplicate"

        data.append(new_record)
        self.save_data(data)
        return "Success"

    def get_last_records_by_city(self, city, limit=10):
        data = self.load_data()
        if not isinstance(data, list): return []
        
        filtered = [r for r in data if r.get("city") == city]
        # Ordenar por fecha si existe el campo
        filtered.sort(key=lambda x: x.get("date", ""), reverse=True)
        return filtered[:limit]


    def create_backup(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre_base, extension = os.path.splitext(self.file_path)
        backup_path = f"{nombre_base}_{timestamp}{extension}"
        try:
            shutil.copy(self.file_path, backup_path)
        except Exception:
            pass

    def clean_old_backups(self, max_backups=5):
        folder = os.path.dirname(self.file_path) or "."
        nombre_base = os.path.basename(self.file_path).replace(".json", "")
        files = sorted([
            f for f in os.listdir(folder)
            if f.startswith(nombre_base) and f.endswith(".json") and f != os.path.basename(self.file_path)
        ])
        if len(files) > max_backups:
            for f in files[:-max_backups]:
                os.remove(os.path.join(folder, f))