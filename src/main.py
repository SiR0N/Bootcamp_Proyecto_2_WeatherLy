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

import login 

import time
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
PROJECT_ROOT = os.path.dirname(BASE_DIR)               

LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

data_storage_path = os.path.join(DATA_DIR, "weather.json")
alerts_storage_path = os.path.join(DATA_DIR, "alerts.json")
log_storage_path = os.path.join(LOGS_DIR, "app.log") 

log = setup_logging(log_storage_path)


import statistics
import plotext as plt

def view_stats_graph(components):
    storage = components["storage"]
    cities = list(CITY_MAP.values())

    temps = []
    hums = []
    winds = []

    for city in cities:
        records = storage.get_last_records_by_city(city, limit=200)
        if not records:
            temps.append(None)
            hums.append(None)
            winds.append(None)
            continue

        stats = compute_stats(records)
        temps.append(stats["temp_mean"])
        hums.append(stats["hum_mean"])
        winds.append(stats["wind_mean"])

    plt.clear_figure()
    plt.clear_data()
    
    indices = list(range(len(cities)))

    plt.title("Medias por Ciudad")
    plt.xlabel("Ciudad")
    plt.ylabel("Valor")

    plt.plot(indices, temps, label="Temp (°C)")
    plt.plot(indices, hums, label="Humedad (%)")
    plt.plot(indices, winds, label="Viento (km/h)")

    plt.xticks(indices, cities)

    plt.canvas_color("default")
    plt.axes_color("default")
    plt.ticks_color("white")


    plt.show()

def compute_stats(records):

    temps = [r["temp"] for r in records if "temp" in r]
    hums = [r["hum"] for r in records if "hum" in r]
    winds = [r["wind"] for r in records if "wind" in r]

    return {
        "temp_mean": round(statistics.mean(temps), 2) if temps else None,
        "temp_median": round(statistics.median(temps), 2) if temps else None,
        "hum_mean": round(statistics.mean(hums), 2) if hums else None,
        "hum_median": round(statistics.median(hums), 2) if hums else None,
        "wind_mean": round(statistics.mean(winds), 2) if winds else None,
        "wind_median": round(statistics.median(winds), 2) if winds else None,
    }

def view_stats(components):
    show_logo_super_small()
    type_effect("Calculando estadísticas...", 0.02)

    storage = components["storage"]
    cities = list(CITY_MAP.values())

    print("\n--- ESTADÍSTICAS POR CIUDAD ---")
    for city in cities:
        records = storage.get_last_records_by_city(city, limit=200)

        if not records:
            print(f"\n{city}: sin datos suficientes.")
            continue

        stats = compute_stats(records)

        print(f"\n{city}:")
        print(f"  Temp → media: {stats['temp_mean']}°C | mediana: {stats['temp_median']}°C")
        print(f"  Hum  → media: {stats['hum_mean']}% | mediana: {stats['hum_median']}%")
        print(f"  Viento → media: {stats['wind_mean']} kmh | mediana: {stats['wind_median']} kmh")


# ============================
# LOGOS
# ============================
def type_effect(text, delay=0.02):
    """Imprime texto con efecto de escritura."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

import itertools

def loader(duration=2):
    """Loader circular animado."""
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    end_time = time.time() + duration

    while time.time() < end_time:
        sys.stdout.write("\rCargando " + next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)

    sys.stdout.write("\rCargando ✓\n")

def show_logo():
    logo = [
        "           .--.",
        "        .-(    ).",
        "       (___.__)__)   ☁️",
        "",
        "██     ██ ██      ",
        "██     ██ ██      ",
        "██  █  ██ ██      ",
        "██ ███ ██ ██      ",
        " ███ ███  ███████ ",
        "",
        "        WEATHERLY",
        ""
    ]

    for line in logo:
        type_effect(line, delay=0.02)
    time.sleep(0.5)
def weather_loader(duration=3):
    """Animación cíclica de iconos meteorológicos."""
    
    """
    frames1 = [
        "   .--.      \n  (    ) ☁   \n (__.__)     ",
        "   .--.      \n  (    ) 🌧   \n (__.__)     ",
        "   .--.      \n  ( ⚡ )      \n (__.__)     ",
        "    \\ | /    \n  --  ☀  --   \n    / | \\     ",
        "    ~ ~ ~     \n  🌬 viento    \n    ~ ~ ~     "
    ]"""
    frames = [
        "☁️  Nube",
        "🌧️  Lluvia",
        "⚡  Tormenta",
        "☀️  Sol",
        "🌬️  Viento"
    ]

    cycle_frames = itertools.cycle(frames)
    end_time = time.time() + duration
    print("Cargando...")
    while time.time() < end_time:
        frame = next(cycle_frames)
        sys.stdout.write("\r" + frame + "      ")
        sys.stdout.flush()
        time.sleep(0.4)

    print("\n")

weather_icons = itertools.cycle(["☀", "🌧", "⚡", "🌬", "☁"])

def show_logo_small():
    icon = next(weather_icons)
    print(rf"""
  .--.
 ( {icon} )  WL
(__.__)
""")

def show_logo_super_small():
    icon = next(weather_icons)
    print(rf"[ W  L ] {icon}")


# ============================
# COMPONENTES
# ============================

def init_components():
    return {
        "api": WeatherAPIClient(),
        "storage": Storage(data_storage_path),
        "alerts_storage": Storage(alerts_storage_path),

        "validator": WeatherValidator(),
        "alerts": AlertEngine(),
        "scheduler": Scheduler(),
    }

def get_manual_input(city):
    """Permite introducir datos manualmente si la API falla."""
    print(f"\n[!] CONTROL MANUAL PARA: {city.upper()}")
    try:
        temp = float(input(f"  > Temperatura en {city} (°C): "))
        hum = int(input(f"  > Humedad en {city} (%): "))
        wind = float(input(f"  > Velocidad del viento (km/h): "))
        
        return {
            "date": datetime.now().strftime("%Y-%m-%dT%H:%M"),
            "city": city,
            "temp": temp,
            "hum": hum,
            "wind": wind,
            "source": "Console"
        }
    except ValueError:
        print("\n[!] Error: Solo se admiten números. Se aborta la entrada manual.")
        return None

# ============================
# PROCESAMIENTO PRINCIPAL
# ============================

def fetch_and_process(components):
    api = components["api"]
    storage = components["storage"]
    validator = components["validator"]
    alerts_engine = components["alerts"]
    alerts_storage = components["alerts_storage"]

    log.info("=== INICIANDO CICLO DE ACTUALIZACIÓN ===")

    for coords, city in CITY_MAP.items():
        try:
            lat, lon = coords 
            log.info(f"Procesando {city} (lat={lat}, lon={lon})")

            data = api.get_weather_data(lat, lon)
            if data:
                data['city'] = city

                is_ok, errors = validator.validate_record(data)
                if not is_ok:
                    log.error(f"Datos inválidos para {city}: {errors}")
                    continue

                triggered_alerts = alerts_engine.generate_alerts(data)
                log.info(f"Datos recibidos en {city}: Temp={data.get('temp')}°C")

                for alert in triggered_alerts:
                    if alert["level"] != "INFO":
                        log.warning(f"¡ALERTA! [{city}] {alert['metric'].upper()}: {alert['message']}")



                    alert_record = {
                        "date": datetime.now().strftime("%Y-%m-%dT%H:%M"),
                        "city": city,
                        "level": alert["level"],
                        "metric": alert["metric"],
                        "value": alert["value"],
                        "message": alert["message"],
                        "source": "API_Weather_System"
                    }
                    alerts_storage.add_record(alert_record)

                # 4. Guardar 
                # Añadimos metadatos antes de guardar
                data["date"] = datetime.now().strftime("%Y-%m-%dT%H:%M")
                data["source"] = "API_Weather_System"
                
            
                result = storage.add_record(data)
                log.info(f"Guardado exitoso para {city}: {result}")

            else:
                log.warning(f"Sin respuesta de API para {city}")
                manual_data = get_manual_input(city)
                
                if manual_data:
                   is_ok, errors = validator.validate_record(manual_data)
                   
                   if not is_ok:
                       log.error(f"Datos manuales inválidos para {city}: {errors}")
                       continue
                   manual_data["date"] = datetime.now().strftime("%Y-%m-%dT%H:%M")
                   manual_data["source"] = "Console"
                   
                   result = storage.add_record(manual_data)
                   log.info(f"Guardado manual exitoso para {city}: {result}")
                   
                    
        except Exception as e:
            log.exception(f"Error inesperado procesando {city}: {e}")

    log.info("=== CICLO DE ACTUALIZACIÓN FINALIZADO ===")

def get_last_record_by_city(storage, city):
    """Devuelve el último registro de una ciudad."""
    data = storage.load_data()
    filtered = [r for r in data if r.get("city") == city]

    if not filtered:
        return None

    filtered.sort(key=lambda x: x.get("date", ""), reverse=True)
    return filtered[0]


def show_city_summaries(storage):
    print("\n--- Últimos registros por ciudad ---")

    for city in CITY_MAP.values():
        last = get_last_record_by_city(storage, city)

        if not last:
            print(f"{city}: sin datos")
            continue

        temp = last.get("temp", "?")
        hum = last.get("hum", "?")
        wind = last.get("wind", "?")
        date = last.get("date", "?")

        print(f"{city}: {temp}°C / {hum}% / {wind} kmh / {date}")
def view_city_evolution_graph(components):
    show_logo_super_small()
    storage = components["storage"]
    cities = list(CITY_MAP.values())

    # 1. Selección de ciudad
    print("\n--- EVOLUCIÓN HISTÓRICA ---")
    for i, city in enumerate(cities, start=1):
        print(f"{i}. {city}")
    
    op = input("Seleccione ciudad para ver evolución: ").strip()
    if not op.isdigit() or not (1 <= int(op) <= len(cities)):
        print("[!] Opción no válida.")
        return

    selected_city = cities[int(op) - 1]
    
    # 2. Obtener datos
    records = storage.get_last_records_by_city(selected_city, limit=20)
    if not records or len(records) < 2:
        print(f"\n[!] Datos insuficientes para {selected_city}.")
        return

    records.reverse()

    # 3. Preparar datos
    times = [r["date"].split('T')[1] if 'T' in r["date"] else r["date"] for r in records]
    temps = [r["temp"] for r in records]
    hums = [r["hum"] for r in records]
    winds = [r["wind"] for r in records]
    indices = list(range(len(records)))

    # 4. Configurar Subtramas (3 filas, 1 columna)
    plt.clear_figure()
    plt.subplots(3, 1) # Creamos la rejilla

    # --- Gráfica 1: Temperatura ---
    plt.subplot(1, 1)
    plt.plot(indices, temps, label="Temp (°C)", color="red", marker="dot")
    plt.title(f"Evolución en {selected_city}") # Título general arriba
    plt.ylabel("Temp")
    plt.xticks(indices, [""] * len(times)) # Ocultamos horas para no amontonar

    # --- Gráfica 2: Humedad ---
    plt.subplot(2, 1)
    plt.plot(indices, hums, label="Hum (%)", color="blue", marker="dot")
    plt.ylabel("Hum")
    plt.xticks(indices, [""] * len(times)) # Ocultamos horas

    # --- Gráfica 3: Viento ---
    plt.subplot(3, 1)
    plt.plot(indices, winds, label="Viento (km/h)", color="green", marker="dot")
    plt.ylabel("Viento")
    plt.xlabel("Hora del registro")
    plt.xticks(indices, times) # Mostramos las horas solo en la gráfica de abajo

    # Ajustes finales para todas
    plt.theme("dark")
    plt.show()
# ============================
# MENÚS
# ============================


def show_menu(storage):
    show_logo_small()
    show_city_summaries(storage)
    print("\n" + "="*25)
    print("   WEATHER DASHBOARD")
    print("="*25)
    print("1. Actualizar ciudades ahora")
    print("2. Ver últimos registros por ciudad")
    print("3. Configurar automatización")
    print("4. Ver estadísticas por ciudad")
    print("5. Ver graficos por ciudad")
    print("6. Ver graficos de ciudad")
    print("7. Salir")
def view_last(components):
    show_logo_super_small()
    type_effect("Cargando registros...", 0.02)
    storage = components["storage"]

    cities = list(CITY_MAP.values())

    print("\n--- SELECCIONAR CIUDAD ---")
    for i, city in enumerate(cities, start=1):
        print(f"{i}. {city}")

    op = input("Seleccione ciudad: ").strip()

    if not op.isdigit() or not (1 <= int(op) <= len(cities)):
        print("[!] Opción no válida.")
        return

    selected_city = cities[int(op) - 1]

    records = storage.get_last_records_by_city(selected_city, limit=10)

    if not records:
        print(f"\n[!] No hay registros para {selected_city}.")
        return

    print(f"\n--- ÚLTIMOS REGISTROS DE {selected_city} ---")
    for idx, record in enumerate(records, start=1):
        print(f"\n[{idx}] ----------------------")
        for key, value in record.items():
            print(f"{key.capitalize()}: {value}")


def view_alerts(components):
    alerts_storage = components["alerts_storage"]
    alerts = alerts_storage.load_data()

    if not alerts:
        print("\n[!] No hay alertas registradas.")
        return

    city_filter = input("Ciudad (deja vacío para ver todas): ").strip().lower()
    date_filter = input("Fecha YYYY-MM-DD (deja vacío para ver todas): ").strip()

    filtered_alerts = []

    for alert in alerts:
        city_matches = not city_filter or alert.get("city", "").lower() == city_filter
        date_matches = not date_filter or alert.get("date", "").startswith(date_filter)

        if city_matches and date_matches:
            filtered_alerts.append(alert)

    if not filtered_alerts:
        print("\n[!] No hay alertas con esos filtros.")
        return

    print("\n--- ALERTAS FILTRADAS ---")

    for alert in filtered_alerts:
        print(f"Fecha: {alert.get('date')}")
        print(f"Ciudad: {alert.get('city')}")
        print(f"Nivel: {alert.get('level')}")
        print(f"Métrica: {alert.get('metric')}")
        print(f"Valor: {alert.get('value')}")
        print(f"Mensaje: {alert.get('message')}")
        print("---------------------------")

def setup_scheduler(components):
    show_logo_super_small()
    type_effect("Configurando automatización...", 0.02)
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


# ============================
# MAIN
# ============================

def main():
    components = init_components()
    log.info("Aplicación iniciada. Menú interactivo listo.")

    

    #loader(2)
    weather_loader(3)
    try:
        while True:
            show_menu(components["storage"])
            op = input(">> ").strip()

            if op == "1":
                fetch_and_process(components)
            elif op == "2":
                view_last(components)
            elif op == "3":
                view_alerts(components)
            elif op == "4":
                view_stats(components)
            elif op == "5":
                view_stats_graph(components)
            elif op == "6":
                view_city_evolution_graph(components)   
            elif op == "7":
                log.info("Cerrando aplicación...")
                components["scheduler"].shutdown()
                break
            else:
                print("Opción no válida, intente de nuevo.")
                
    except KeyboardInterrupt:
        log.info("Interrupción detectada. Apagando sistema...")
        components["scheduler"].shutdown()


if __name__ == "__main__":
    show_logo()
    main()
