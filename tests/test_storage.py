#Archivo de pruebas temporal para Storage. No forma parte de la aplicación final.


from src.storage import Storage

storage = Storage("data/weather.json")

registro_1 = {
    "date": "2026-04-27T14:30",
    "city": "Madrid",
    "temp": 25,
    "hum": 60,
    "wind": 15,
    "source": "test"
}

registro_2 = {
    "date": "2026-04-27T15:00",
    "city": "Toledo",
    "temp": 28,
    "hum": 55,
    "wind": 10,
    "source": "test"
}

print(storage.add_record(registro_1))
print(storage.add_record(registro_2))

print(storage.load_data())

from src.storage import Storage

storage = Storage("data/weather.json")

# Registro duplicado (NO debería guardarse)
registro_1 = {
    "date": "2026-04-27T14:30",
    "city": "Madrid",
    "temp": 25,
    "hum": 60,
    "wind": 15,
    "source": "test"
}

# Registro duplicado (NO debería guardarse)
registro_2 = {
    "date": "2026-04-27T15:00",
    "city": "Toledo",
    "temp": 28,
    "hum": 55,
    "wind": 10,
    "source": "test"
}

# 🔥 NUEVO registro (SÍ debería guardarse)
registro_3 = {
    "date": "2026-04-27T16:00",
    "city": "Sevilla",
    "temp": 30,
    "hum": 50,
    "wind": 12,
    "source": "test"
}

print(storage.add_record(registro_1))
print(storage.add_record(registro_2))
print(storage.add_record(registro_3))

print("\nDatos finales:")
print(storage.load_data())