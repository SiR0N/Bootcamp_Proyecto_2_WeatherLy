from apscheduler.schedulers.blocking import BlockingScheduler
from api_client import WeatherAPIClient
import logging
from cities import CITY_MAP

log = logging.getLogger(__name__)   # Logger del módulo
client = WeatherAPIClient()

def job_update_weather():
    log.info("=== STARTING SCHEDULED UPDATE ===")

    for city, coords in CITY_MAP.items():
        lat, lon = coords

        log.info(f"Solicitando datos para {city} (lat={lat}, lon={lon})")

        try:
            data = client.get_weather_data(lat, lon)

            if data:
                log.info(
                    f"Datos recibidos para {city}: "
                    f"Temp={data['temp']}°C, Hum={data['hum']}%, Wind={data['wind']} km/h"
                )
            else:
                log.warning(f"No se pudieron obtener datos para {city}")

        except Exception:
            log.exception(f"Error inesperado procesando datos para {city}")


def start_automation():
    scheduler = BlockingScheduler()

    log.info("Iniciando sistema de automatización (cada 15 minutos)")

    # Programación oficial
    scheduler.add_job(job_update_weather, "interval", minutes=15)

    # Ejecutar una vez al inicio
    log.info("Ejecutando actualización inicial...")
    job_update_weather()

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.warning("Automatización detenida manualmente por el usuario.")
