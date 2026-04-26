from apscheduler.schedulers.blocking import BlockingScheduler
from logger_config import setup_logging
from api_client import WeatherAPIClient

# Iniciamos tus herramientas
log = setup_logging()
client = WeatherAPIClient()

# Coordenadas de las 5 capitales de Castilla-La Mancha
CITIES = {
    "Toledo": (39.8581, -4.0226),
    "Ciudad Real": (38.9863, -3.9274),
    "Albacete": (38.9942, -1.8585),
    "Guadalajara": (40.6333, -3.1667),
    "Cuenca": (40.0714, -2.1348)
}

def job_update_weather():
    log.info("--- STARTING SCHEDULED UPDATE---")
    
    for city, coords in CITIES.items():
        lat, lon = coords
        
        # CORRECCIÓN AQUÍ: 
        # Quitamos 'city_name' porque la función de tu compañero NO lo acepta.
        # Solo le pasamos lat y lon como él definió en su archivo.
        data = client.get_weather_data(lat, lon)
        
        if data:
            # Aunque el código de tu compañero usa nombres en español (temp, hum),
            # tu Logger los registra correctamente para la trazabilidad.
            # Nota: usamos data['temp'] porque así lo llamó él.
            log.info(f"Data received for {city}: Temp {data['temp']}°C, Hum {data['hum']}%")
        else:
            log.warning(f"Could not retrieve data for {city}")

def start_automation():
    scheduler = BlockingScheduler()
    
    # Programado cada 15 minutos (Requisito del Ayuntamiento)
    scheduler.add_job(job_update_weather, 'interval', minutes=15)
    
    log.info("Automation system started. Next execution in 15 min.")
    
    # Ejecutamos una vez al inicio para verificar que todo funciona
    job_update_weather()
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.warning("Automation stopped manually by user.")

if __name__ == "__main__":
    start_automation()