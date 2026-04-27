from Bootcamp_Proyecto_2_WeatherLy.src.validator import validate_record
from Bootcamp_Proyecto_2_WeatherLy.src.alerts import generate_alerts


def process_weather_data(data):
    if not validate_record(data):
        return {
            "status": "invalid",
            "data": data,
            "alerts": []
        }

    alerts = generate_alerts(data)

    return {
        "status": "ok",
        "data": data,
        "alerts": alerts
    }