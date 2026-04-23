import requests
import logging

class WeatherAPIClient:
    def __init__(self):
        # URL base de la API Open-Meteo
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def get_weather_data(self, lat, lon):
        """
        Request data from the API and return it normalized.
        """
        # Parámetros de la API según el acuerdo del grupo
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
            "timezone": "auto"
        }

        try:
            # Petición GET con timeout de seguridad
            response = requests.get(self.base_url, params=params, timeout=10)
            
            # Verificación de errores HTTP
            response.raise_for_status() 
            
            raw_data = response.json()
            return self.normalize_data(raw_data, lat, lon)

        except Exception as error:
            # Registro de errores en el log
            logging.error(f"Error fetching data: {error}")
            return None

    def normalize_data(self, data, lat, lon):
        """
        Normalize data to the agreed schema: temp, hum, wind.
        """
        current = data.get("current", {})
        
        return {
            "fecha": current.get("time"),      # Formato YYYY-MM-DDTHH:mm
            "zona": f"{lat},{lon}",
            "temp": float(current.get("temperature_2m")),      # Grados Celsius
            "hum": int(current.get("relative_humidity_2m")),    # Porcentaje
            "wind": float(current.get("wind_speed_10m")),       # km/h
            "fuente": "Open Meteo"
        }