import requests
import logging

class WeatherAPIClient:
    def __init__(self):
        # URL base de la API Open-Meteo
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        
        # Mapeo de las 5 capitales de Castilla-La Mancha
        self.city_map = {
            (40.63, -3.16): "Guadalajara",
            (39.86, -4.02): "Toledo",
            (38.99, -3.92): "Ciudad Real",
            (38.99, -1.86): "Albacete",
            (40.07, -2.13): "Cuenca"
        }

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

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status() 
            raw_data = response.json()
            
            return self.normalize_data(raw_data, lat, lon, source_name="Open Meteo")

        except Exception as error:
            logging.error(f"Error fetching data: {error}")
            # Si falla la API, la fuente debe indicar ERROR, no Console
            return self.get_error_fallback(lat, lon)

    def normalize_data(self, data, lat, lon, source_name):
        """
        Normaliza los datos a inglés, con decimales de punto.
        """
        current = data.get("current", {})
        city_name = self.city_map.get((lat, lon), "Unknown City")
        
        return {
            "date": current.get("time"),
            "city": city_name,
            "temp": float(current.get("temperature_2m")),
            "hum": int(current.get("relative_humidity_2m")),
            "wind": float(current.get("wind_speed_10m")),
            "source": source_name
        }

    def is_duplicate(self, new_record, existing_records):
        """
        Comprueba si el registro ya existe (misma fecha/hora y ciudad).
        """
        for record in existing_records:
            if record["date"] == new_record["date"] and record["city"] == new_record["city"]:
                return True
        return False

    def get_error_fallback(self, lat, lon):
        """
        Caso de FALLO de red o API. Fuente: 'Error'.
        """
        city_name = self.city_map.get((lat, lon), "Unknown City")
        return {
            "date": "N/A",
            "city": city_name,
            "temp": 0.0,
            "hum": 0,
            "wind": 0.0,
            "source": "Error"
        }

    def get_manual_input(self, lat, lon, date, temp, hum, wind):
        """
        Para cuando se introducen datos MANUALMENTE. Fuente: 'Console'.
        """
        city_name = self.city_map.get((lat, lon), "Unknown City")
        return {
            "date": date,
            "city": city_name,
            "temp": float(temp),
            "hum": int(hum),
            "wind": float(wind),
            "source": "Console"
        }