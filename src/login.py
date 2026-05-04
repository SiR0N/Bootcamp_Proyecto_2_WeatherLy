import hashlib
import getpass
import logging
from storage import Storage

log = logging.getLogger(__name__)

# Definimos la ruta del archivo JSON que almacena los usuarios
ARCHIVO_USUARIOS = "usuarios.json"

# Inicializamos el storage para la base de datos de usuarios
usuarios_storage = Storage(ARCHIVO_USUARIOS)

def hash_password(password):
    """Encripta la contraseña utilizando el algoritmo SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def cargar_usuarios():
    """Carga los usuarios desde el archivo JSON utilizando Storage."""
    try:
        data = usuarios_storage.load_data()
        if isinstance(data, list):
            # Adaptamos por si hay una lista de diccionarios
            usuarios = {}
            for d in data:
                if isinstance(d, dict):
                    usuarios.update(d)
            return usuarios
        elif isinstance(data, dict):
            return data
        return {}
    except Exception:
        return {}

def guardar_usuarios(usuarios):
    """Guarda los usuarios en el archivo JSON utilizando Storage."""
    usuarios_storage.save_data(usuarios)

def registrar_interno(usuario, password):
    """Lógica de registro de usuario."""
    usuarios = cargar_usuarios()
    
    if usuario in usuarios:
        log.warning(f"Intento de registro fallido: el usuario '{usuario}' ya existe.")
        return False

    # Guardamos la contraseña encriptada
    usuarios[usuario] = hash_password(password)
    guardar_usuarios(usuarios)
    log.info(f"Usuario {usuario} registrado correctamente.")
    return True

def registrar():
    """Interacción con el usuario por consola para registro."""
    print("\n=== REGISTRO ===")
    usuario = input("Usuario: ")
    password = getpass.getpass("Contraseña: ")

    resultado = registrar_interno(usuario, password)
    if resultado:
        print("Usuario registrado correctamente.")
    else:
        print("Ese usuario ya existe.")
    return resultado

def login_interno(usuario, password):
    """Lógica interna de verificación de login."""
    usuarios = cargar_usuarios()
    
    if usuario not in usuarios:
        log.warning(f"Intento de login fallido: el usuario '{usuario}' no existe.")
        return False

    # Comparamos el hash de la contraseña ingresada con el hash guardado
    return usuarios[usuario] == hash_password(password)

def login():
    """Interacción con el usuario por consola para login."""
    print("\n=== LOGIN ===")
    usuario = input("Usuario: ")
    password = getpass.getpass("Contraseña: ")

    resultado = login_interno(usuario, password)
    if resultado:
        print("Login exitoso 🎉")
    else:
        print("Usuario o contraseña incorrectos.")
    return resultado

def menu():
    """Menú de selección principal."""
    while True:
        print("\n1. Registrar")
        print("2. Login")
        print("3. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            registrar()
        elif opcion == "2":
            if login():
                return True
        elif opcion == "3":
            print("Saliendo...")
            log.info("Saliendo de la aplicación.")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    menu()