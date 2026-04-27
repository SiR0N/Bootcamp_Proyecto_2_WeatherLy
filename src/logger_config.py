import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Rotación para trazabilidad profesional
    handler = RotatingFileHandler('logs/app.log', maxBytes=5*1024*1024, backupCount=3)
    handler.setFormatter(logging.Formatter(format_str))
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    # Salida por consola para ver el progreso
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(format_str))
    logger.addHandler(console)
    
    return logger