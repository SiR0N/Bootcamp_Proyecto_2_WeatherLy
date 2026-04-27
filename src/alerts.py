def temperature_alert(value):
    if value < -15 or value > 50:
        return "CRITICAL", "Extreme temperature"
    elif value < -8 or value > 40:
        return "WARNING", "Abnormal temperature"
    return "INFO", "Normal temperature"


def wind_alert(value):
    if value <= 0 or value > 130:
        return "CRITICAL", "Invalid wind"
    elif value > 70:
        return "WARNING", "High wind"
    return "INFO", "Normal wind"


def humidity_alert(value):
    if value < 0 or value > 100:
        return "CRITICAL", "Invalid humidity"
    elif value <= 20 or value >= 70:
        return "WARNING", "Uncomfortable humidity"
    return "INFO", "Normal humidity"


def generate_alerts(data):
    alerts = []

    for metric, func in {
        "temp": temperature_alert,
        "wind": wind_alert,
        "hum": humidity_alert
    }.items():
        level, message = func(data[metric])

        alerts.append({
            "level": level,
            "metric": metric,
            "value": data[metric],
            "message": message
        })

    return alerts
