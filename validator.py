import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
        return True
    except:
        return False


def validate_temperature(value):
    return isinstance(value, (int, float)) and -15 <= value <= 50


def validate_wind(value):
    return isinstance(value, (int, float)) and 0 < value <= 130


def validate_humidity(value):
    return isinstance(value, (int, float)) and 0 <= value <= 100


def validate_record(data):
    required = ["date", "city", "temp", "wind", "hum", "source"]

    for field in required:
        if field not in data:
            logger.critical("Missing field", extra={"data": data})
            return False

    if not validate_date(data["date"]):
        logger.critical("Invalid date", extra={"data": data})
        return False

    if not validate_temperature(data["temp"]):
        logger.critical("Invalid temp", extra={"data": data})
        return False

    if not validate_wind(data["wind"]):
        logger.critical("Invalid wind", extra={"data": data})
        return False

    if not validate_humidity(data["hum"]):
        logger.critical("Invalid hum", extra={"data": data})
        return False

    return True
