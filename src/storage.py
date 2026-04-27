import json  # Librería para trabajar con archivos JSON
import os    # Librería para trabajar con archivos y rutas del sistema

# Ruta donde está el archivo JSON
FILE_PATH = "data/weather.json"


def load_data():   #Función para leer el histórico guardado en el archivo JSON
    # Comprobar si el archivo NO existe
    if not os.path.exists(FILE_PATH):
        # Si no existe, devolvemos una lista vacía, sin romper el programa
        return []

    try:
        # Abrimos el archivo en modo lectura
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            # Cargamos el contenido del JSON y lo convertimos a un objeto de Python
            data = json.load(file)

        # Comprobamos que lo que hemos leído es una lista
        if isinstance(data, list):
            # Si es lista, la devolvemos
            return data

        # Si no es lista, devolvemos lista vacía (evitamos errores)
        return []

    except (json.JSONDecodeError, FileNotFoundError):
        # Si el JSON está mal formado o hay algún error al leerlo
        # devolvemos una lista vacía para no romper el programa
        return []

  
def save_data(data):
    try:
        # Abrimos el archivo en modo escritura (borra lo anterior y escribe nuevo)
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            # Guardamos los datos en formato JSON
            json.dump(data, file, indent=4, ensure_ascii=False)

    except Exception as e:
        # Si hay error, lo mostramos
        print(f"Error saving data: {e}")
    

def is_duplicate(new_record, existing_data):
    """
    Comprueba si un registro es duplicado.
    Un duplicado es aquel que tiene el mismo 'date' y 'city'.
    """

    # Recorremos todos los registros ya guardados
    for record in existing_data:

        # Comprobamos si coinciden date y city
        if record["date"] == new_record["date"] and record["city"] == new_record["city"]:
            return True  # Es duplicado

    return False  # No es duplicado


def add_record(new_record):
    """
    Añade un nuevo registro al archivo JSON si no está duplicado.
    Si ya existe un registro con la misma date y city, no lo guarda.
    """

    # Cargamos los datos que ya existen en weather.json
    data = load_data()

    # Comprobamos si el nuevo registro ya existe
    if is_duplicate(new_record, data):
        return "Duplicate record. Not saved."

    # Si no es duplicado, lo añadimos a la lista
    data.append(new_record)

    # Guardamos la lista actualizada en el JSON
    save_data(data)

    return "Record saved successfully."

