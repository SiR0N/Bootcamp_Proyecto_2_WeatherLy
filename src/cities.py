# cities.py
"""
Listado oficial de ciudades y coordenadas para la aplicación meteorológica.
Fuente única de verdad para evitar duplicación en api_client y scheduler.
"""

CITIES = {
    "Toledo": (39.8581, -4.0226),
    "Ciudad Real": (38.9863, -3.9274),
    "Albacete": (38.9942, -1.8585),
    "Guadalajara": (40.6333, -3.1667),
    "Cuenca": (40.0714, -2.1348)
}

# Mapa inverso: (lat, lon) → nombre de ciudad
CITY_MAP = {coords: name for name, coords in CITIES.items()}
