# main.py
from datetime import datetime

# Importación de Configuración y Datos
from cities import CITY_MAP 
from logger_config import setup_logging 


from api_client import WeatherAPIClient
from storage import Storage
from validator import WeatherValidator
from alerts import AlertEngine
from scheduler import Scheduler

log = setup_logging()

def init_components():
    """Inicializa todas las clases y las guarda en un diccionario."""
    return {
        "api": WeatherAPIClient(),
        "storage": Storage("data/weather.json"),
        "validator": WeatherValidator(),
        "alerts": AlertEngine(),
        "scheduler": Scheduler(),
    }

def fetch_and_process(components):
    """
    Orquesta el flujo completo para todas las ciudades.
    Esta es la lógica que antes tenías en job_update_weather.
    """
    api = components["api"]
    storage = components["storage"]
    validator = components["validator"]
    alerts_engine = components["alerts"]

    log.info("=== INICIANDO CICLO DE ACTUALIZACIÓN ===")

    for coords, city in CITY_MAP.items():
        try:
            lat, lon = coords 
            log.info(f"Procesando {city} (lat={lat}, lon={lon})")

            # 1. Obtener datos (Luis)
            data = api.get_weather_data(lat, lon)

            if data:
                data['city'] = city # Inyectamos el nombre para validación y storage

                # 2. Validar (Vanessa - Validator)
                is_ok, errors = validator.validate_record(data)
                if not is_ok:
                    log.error(f"Datos inválidos para {city}: {errors}")
                    continue

                # 3. Alertas (Vanessa - AlertEngine)
                triggered_alerts = alerts_engine.generate_alerts(data)
                log.info(f"Datos recibidos en {city}: Temp={data.get('temp')}°C")

                for alert in triggered_alerts:
                    if alert["level"] != "INFO":
                        log.warning(f"¡ALERTA! [{city}] {alert['metric'].upper()}: {alert['message']}")

                # 4. Guardar (Gema - Storage)
                # Añadimos metadatos antes de guardar
                data["date"] = datetime.now().strftime("%Y-%m-%dT%H:%M")
                data["source"] = "API_Weather_System"
                
                result = storage.add_record(data)
                log.info(f"Guardado exitoso para {city}: {result}")

            else:
                log.warning(f"Sin respuesta de API para {city}")

        except Exception as e:
            # log.exception incluye el rastreo del error para debuggear mejor
            log.exception(f"Error inesperado procesando {city}: {e}")

    log.info("=== CICLO DE ACTUALIZACIÓN FINALIZADO ===")

def show_menu():
    print("\n" + "="*25)
    print("   WEATHER DASHBOARD")
    print("="*25)
    print("1. Actualizar ciudades ahora")
    print("2. Ver último registro guardado")
    print("3. Configurar automatización")
    print("4. Salir")

def view_last(components):
    storage = components["storage"]
    last = storage.get_last_record()

    if not last:
        print("\n[!] No hay datos en weather.json.")
        return

    print("\n--- ÚLTIMO REGISTRO ENCONTRADO ---")
    for key, value in last.items():
        print(f"{key.capitalize()}: {value}")

def setup_scheduler(components):
    scheduler = components["scheduler"]

    print("\n--- CONFIGURACIÓN DE AUTOMATIZACIÓN ---")
    print("1. Ejecutar cada 15 minutos")
    print("2. Ejecutar cada 60 minutos")
    print("3. Desactivar tareas automáticas")

    op = input("Seleccione opción: ").strip()

    if op == "1":
        scheduler.schedule_job(lambda: fetch_and_process(components), 15)
        print("[+] Programado cada 15 minutos.")
    elif op == "2":
        scheduler.schedule_job(lambda: fetch_and_process(components), 60)
        print("[+] Programado cada 60 minutos.")
    elif op == "3":
        scheduler.cancel_all()
        print("[-] Tareas automáticas desactivadas.")
    else:
        print("[!] Opción no válida.")

def main():
    components = init_components()
    log.info("Aplicación iniciada. Menú interactivo listo.")

    try:
        while True:
            show_menu()
            op = input(">> ").strip()

            if op == "1":
                fetch_and_process(components)
            elif op == "2":
                view_last(components)
            elif op == "3":
                setup_scheduler(components)
            elif op == "4":
                log.info("Cerrando aplicación...")
                components["scheduler"].shutdown()
                break
            else:
                print("Opción no válida, intente de nuevo.")
                
    except KeyboardInterrupt:
        log.info("Interrupción detectada. Apagando sistema...")
        components["scheduler"].shutdown()

if __name__ == "__main__":
    main()