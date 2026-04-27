# main.py
import json
from datetime import datetime

from api_client import WeatherAPIClient
from storage import Storage
from Bootcamp_Proyecto_2_WeatherLy.src.validator import WeatherValidator
from Bootcamp_Proyecto_2_WeatherLy.src.alerts import AlertEngine
from scheduler import Scheduler
from logger_config import setup_logging   # ← AQUÍ EL CAMBIO

log = setup_logging()


def init_components():
    return {
        "api": WeatherAPIClient(),
        "storage": Storage("weather.json"),
        "validator": WeatherValidator(),
        "alerts": AlertEngine(),
        "scheduler": Scheduler(),
    }


def fetch_and_process(components):
    api = components["api"]
    storage = components["storage"]
    validator = components["validator"]
    alerts = components["alerts"]

    log.info("Solicitando datos meteorológicos...")

    # 1. Obtener datos
    try:
        data = api.get_current_weather()
        log.debug(f"Datos recibidos: {data}")
    except Exception:
        log.exception("Error al obtener datos de la API")
        return

    # 2. Validar
    ok, errors = validator.validate(data)
    if not ok:
        log.warning(f"Datos inválidos: {errors}")
        return

    # 3. Guardar
    record = {
        "date": datetime.utcnow().isoformat(timespec="minutes"),
        "city": data["city"],
        "temp": data["temp"],
        "hum": data["hum"],
        "wind": data["wind"],
        "source": "API"
    }

    try:
        storage.append_record(record)
        log.info("Registro guardado correctamente")
    except Exception:
        log.exception("Error al guardar en weather.json")
        return

    # 4. Alertas
    triggered = alerts.evaluate(data)
    for alert in triggered:
        log.warning(f"ALERTA: {alert.message}")


def show_menu():
    print("\n=== Weather App ===")
    print("1. Actualizar datos ahora")
    print("2. Ver último registro")
    print("3. Configurar tareas automáticas")
    print("4. Salir")


def view_last(components):
    storage = components["storage"]
    last = storage.get_last_record()

    if not last:
        print("No hay registros todavía.")
        return

    print("\n--- Último registro ---")
    for k, v in last.items():
        print(f"{k}: {v}")


def setup_scheduler(components):
    scheduler = components["scheduler"]

    print("\nTareas automáticas:")
    print("1. Cada 5 minutos")
    print("2. Cada 30 minutos")
    print("3. Desactivar")

    op = input("Opción: ").strip()

    if op == "1":
        scheduler.schedule_job(lambda: fetch_and_process(components), 5)
        print("Programado cada 5 minutos.")
    elif op == "2":
        scheduler.schedule_job(lambda: fetch_and_process(components), 30)
        print("Programado cada 30 minutos.")
    elif op == "3":
        scheduler.cancel_all()
        print("Tareas desactivadas.")
    else:
        print("Opción no válida.")


def main():
    components = init_components()
    log.info("Aplicación iniciada")

    while True:
        show_menu()
        op = input("Selecciona una opción: ").strip()

        if op == "1":
            fetch_and_process(components)
        elif op == "2":
            view_last(components)
        elif op == "3":
            setup_scheduler(components)
        elif op == "4":
            log.info("Saliendo de la aplicación")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
