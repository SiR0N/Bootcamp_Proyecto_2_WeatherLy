import pytest
import sys
import os

# Añadimos 'src' al path para que los imports internos de los archivos funcionen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api_client import WeatherAPIClient

@pytest.fixture
def client():
    """Instancia el cliente de la API para las pruebas"""
    return WeatherAPIClient()

def test_normalization_toledo(client):
    """Verifica que Toledo se mapea correctamente con las nuevas coordenadas"""
    mock_api_response = {
        "current": {
            "time": "2026-04-28T12:00",
            "temperature_2m": 21.5,
            "relative_humidity_2m": 45,
            "wind_speed_10m": 10.0
        }
    }
    # Coordenadas exactas según el nuevo cities.py
    lat_toledo, lon_toledo = 39.8581, -4.0226
    
    result = client.normalize_data(mock_api_response, lat_toledo, lon_toledo, "Open Meteo")
    
    assert result["city"] == "Toledo"
    assert result["temp"] == 21.5
    assert result["source"] == "Open Meteo"

def test_duplicate_detection(client):
    """Comprueba la lógica de duplicados"""
    historical = [{"date": "2026-04-28T10:00", "city": "Albacete"}]
    new_rec = {"date": "2026-04-28T10:00", "city": "Albacete"}
    
    assert client.is_duplicate(new_rec, historical) is True

def test_unknown_city(client):
    """Verifica que coordenadas no registradas devuelven Unknown City"""
    mock_api_response = {
        "current": {"time": "2026-04-28T12:00", "temperature_2m": 20, "relative_humidity_2m": 50, "wind_speed_10m": 5}
    }
    # Coordenadas de prueba (el Polo Norte, por ejemplo)
    result = client.normalize_data(mock_api_response, 90.0, 0.0, "Test")
    assert result["city"] == "Unknown City"