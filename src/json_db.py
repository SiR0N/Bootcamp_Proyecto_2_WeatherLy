import json
import os
import logging

log = logging.getLogger(__name__)

class JsonDB:
    def __init__(self, path, default=None):
        self.path = path
        self.default = default if default is not None else {}
        self.data = self._load()

    def _ensure_exists(self):
        """Asegura que el archivo y el directorio existan."""
        folder = os.path.dirname(self.path)

        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.default, f, indent=4)
            log.info(f"Archivo creado automáticamente: {self.path}")

    def _load(self):
        """Carga los datos del archivo JSON o crea uno si no existe."""
        self._ensure_exists()
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
                log.info(f"Archivo {self.path} cargado correctamente.")
                return data
        except json.JSONDecodeError:
            log.error(f"Error al leer {self.path}. JSON corrupto. Restaurando a default.")
            self.data = self.default
            self.save()
            return self.data

    def save(self):
        """Guarda los datos en el archivo JSON."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        log.info(f"Datos guardados en {self.path}")

    def set(self, key, value):
        """Guarda un valor asociado a una clave (para diccionarios)."""
        if not isinstance(self.data, dict):
            log.error("Intento de usar set() en un JSON que no es diccionario.")
            raise TypeError("Este JSON no es un diccionario")

        self.data[key] = value
        log.info(f"Set: {key} = {value} en {self.path}")
        self.save()

    def get(self, key, default=None):
        """Obtiene el valor de una clave."""
        if not isinstance(self.data, dict):
            log.error("Intento de usar get() en un JSON que no es diccionario.")
            raise TypeError("Este JSON no es un diccionario")

        return self.data.get(key, default)

    def exists(self, key):
        """Comprueba si existe la clave en los datos."""
        if not isinstance(self.data, dict):
            log.error("Intento de usar exists() en un JSON que no es diccionario.")
            raise TypeError("Este JSON no es un diccionario")

        return key in self.data