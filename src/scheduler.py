import logging
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from api_client import WeatherAPIClient
from cities import CITY_MAP

# INTEGRACIÓN CON VANESSA Y GEMA
from validator import validate_record
from alerts import generate_alerts
from storage import Storage

# Configuración para ver los logs en la terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

log = logging.getLogger(__name__)
client = WeatherAPIClient()
storage = Storage() # Instancia de Gema

def job_update_weather():
    log.info("=== INICIANDO ACTUALIZACIÓN PROGRAMADA ===")

    # AJUSTE PARA CITY_MAP: coords es la llave, city es el valor
    for coords, city in CITY_MAP.items():
        try:
            lat, lon = coords # Ahora sí son 2 valores exactos
            log.info(f"Procesando {city} (lat={lat}, lon={lon})")

            # 1. API (Luis)
            data = client.get_weather_data(lat, lon)

            if data:
                data['city'] = city # Necesario para validación y storage

                # 2. VALIDACIÓN (Vanessa)
                if not validate_record(data):
                    log.error(f"Datos inválidos para {city}. Saltando...")
                    continue

                # 3. ALERTAS (Vanessa)
                alerts = generate_alerts(data)
                log.info(f"Datos recibidos: Temp={data['temp']}°C, Hum={data['hum']}%")

                for alert in alerts:
                    if alert["level"] != "INFO":
                        log.warning(f"¡ALERTA! [{city}] {alert['metric'].upper()}: {alert['message']}")

                # 4. STORAGE (Gema)
                result = storage.add_record(data)
                log.info(f"Guardado: {result}")

            else:
                log.warning(f"Sin respuesta de API para {city}")

        except Exception as e:
            log.error(f"Error inesperado en {city}: {e}")

def start_automation():
    scheduler = BlockingScheduler()
    scheduler.add_job(job_update_weather, "interval", minutes=15)
    
    log.info("Sistema de automatización en marcha (cada 15 min).")
    job_update_weather() # Prueba inicial

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.warning("Automatización detenida.")

if __name__ == "__main__":
    start_automation()