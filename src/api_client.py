import requests
import logging
from cities import CITY_MAP

log = logging.getLogger(__name__)   # Logger del módulo


class WeatherAPIClient:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"

        self.city_map = CITY_MAP

    def get_weather_data(self, lat, lon):
        """
        Obtiene los datos de la API. Fuente: 'Open Meteo'.
        """
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
            "timezone": "auto"
        }

        log.info(f"Solicitando datos meteorológicos para lat={lat}, lon={lon}")
        log.debug(f"Parámetros enviados a la API: {params}")

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            raw_data = response.json()
            log.debug(f"Respuesta cruda de la API: {raw_data}")

            normalized = self.normalize_data(raw_data, lat, lon, source_name="Open Meteo")
            log.info(f"Datos normalizados correctamente para {normalized['city']}")

            return normalized

        except requests.exceptions.HTTPError as e:
            log.error(f"Error HTTP al llamar a la API: {e}")
            return self.get_error_fallback(lat, lon)

        except requests.exceptions.Timeout:
            log.error("Timeout al llamar a la API")
            return self.get_error_fallback(lat, lon)

        except Exception as error:
            log.exception(f"Error inesperado al obtener datos: {error}")
            return self.get_error_fallback(lat, lon)

    def normalize_data(self, data, lat, lon, source_name):
        """
        Normaliza los datos a inglés, con decimales de punto.
        """
        current = data.get("current", {})
        city_name = self.city_map.get((lat, lon), "Unknown City")

        log.debug(f"Normalizando datos para {city_name}")

        return {
            "date": current.get("time"),
            "city": city_name,
            "temp": float(current.get("temperature_2m")),
            "hum": int(current.get("relative_humidity_2m")),
            "wind": float(current.get("wind_speed_10m")),
            "source": source_name
        }

    #is_dupicated duplicada?
    def is_duplicate(self, new_record, existing_records):
        """
        Comprueba si el registro ya existe (misma fecha/hora y ciudad).
        """
        for record in existing_records:
            if record["date"] == new_record["date"] and record["city"] == new_record["city"]:
                log.warning(f"Registro duplicado detectado: {new_record}")
                return True
        return False

    def get_error_fallback(self, lat, lon):
        """
        Caso de FALLO de red o API. Fuente: 'Error'.
        """
        city_name = self.city_map.get((lat, lon), "Unknown City")
        log.warning(f"Usando fallback por error de API para {city_name}")

        return {
            "date": "N/A",
            "city": city_name,
            "temp": 0.0,
            "hum": 0,
            "wind": 0.0,
            "source": "Error"
        }