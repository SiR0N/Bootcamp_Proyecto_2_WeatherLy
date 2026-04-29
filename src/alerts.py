class AlertEngine:
    def __init__(self):
        # Mapeo de métricas a sus métodos de evaluación
        self._rules = {
            "temp": self._temperature_alert,
            "wind": self._wind_alert,
            "hum": self._humidity_alert
        }

    def _temperature_alert(self, value):
        if value < -15 or value > 50:
            return "CRITICAL", "Extreme temperature"
        elif value < -8 or value > 40:
            return "WARNING", "Abnormal temperature"
        return "INFO", "Normal temperature"

    def _wind_alert(self, value):
        if value <= 0 or value > 130:
            return "CRITICAL", "Invalid wind"
        elif value > 70:
            return "WARNING", "High wind"
        return "INFO", "Normal wind"

    def _humidity_alert(self, value):
        if value < 0 or value > 100:
            return "CRITICAL", "Invalid humidity"
        elif value <= 20 or value >= 70:
            return "WARNING", "Uncomfortable humidity"
        return "INFO", "Normal humidity"

    def generate_alerts(self, data):
        """
        Procesa un diccionario de datos y devuelve una lista de alertas.
        """
        alerts = []
        
        for metric, evaluate_func in self._rules.items():
            if metric in data:
                level, message = evaluate_func(data[metric])
                alerts.append({
                    "level": level,
                    "metric": metric,
                    "value": data[metric],
                    "message": message
                })
        
        return alerts