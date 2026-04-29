import logging
from apscheduler.schedulers.background import BackgroundScheduler

log = logging.getLogger(__name__)

class Scheduler:
    def __init__(self):
        # Usamos BackgroundScheduler para que el menú de main.py siga funcionando
        self._scheduler = BackgroundScheduler()
        self._scheduler.start()
        self._current_job = None

    def schedule_job(self, func, minutes):
        """Programa o actualiza la tarea repetitiva."""
        self.cancel_all() # Limpiamos tareas previas antes de poner una nueva
        
        self._current_job = self._scheduler.add_job(
            func, 
            "interval", 
            minutes=minutes,
            id="weather_update"
        )
        log.info(f"Tarea programada cada {minutes} minutos.")

    def cancel_all(self):
        """Detiene todas las tareas programadas."""
        self._scheduler.remove_all_jobs()
        self._current_job = None
        log.info("Todas las tareas automáticas han sido canceladas.")

    def shutdown(self):
        """Apaga el scheduler por completo."""
        self._scheduler.shutdown()