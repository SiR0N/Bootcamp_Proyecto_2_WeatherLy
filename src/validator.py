import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class WeatherValidator:
    def __init__(self):
        # Definimos los campos obligatorios
        self.required_fields = ["date", "city", "temp", "wind", "hum", "source"]

    def _is_numeric(self, value):
        """Helper para verificar si el valor es un número."""
        return isinstance(value, (int, float))

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
            return True
        except (ValueError, TypeError):
            return False

    def validate_temperature(self, value):
        return self._is_numeric(value) and -15 <= value <= 50

    def validate_wind(self, value):
        return self._is_numeric(value) and 0 < value <= 130

    def validate_humidity(self, value):
        return self._is_numeric(value) and 0 <= value <= 100

    def validate_record(self, data):
        """
        Retorna (True, []) si es válido.
        Retorna (False, [lista_de_errores]) si no.
        """
        errors = []

        # 1. Verificar campos faltantes
        for field in self.required_fields:
            if field not in data:
                msg = f"Missing field: {field}"
                logger.critical(msg, extra={"data": data})
                errors.append(msg)
        
        # Si faltan campos, mejor no seguir validando valores para evitar KeyErrors
        if errors:
            return False, errors

        # 2. Validaciones de contenido
        checks = [
            (self.validate_date(data["date"]), "Invalid date format"),
            (self.validate_temperature(data["temp"]), f"Temperature out of range: {data.get('temp')}"),
            (self.validate_wind(data["wind"]), f"Wind out of range: {data.get('wind')}"),
            (self.validate_humidity(data["hum"]), f"Humidity out of range: {data.get('hum')}")
        ]

        for is_valid, error_msg in checks:
            if not is_valid:
                logger.critical(error_msg, extra={"data": data})
                errors.append(error_msg)

        return (len(errors) == 0), errors