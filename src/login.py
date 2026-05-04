import hashlib
import getpass
import logging
from json_db import JsonDB

log = logging.getLogger(__name__)

# Definimos la ruta del archivo JSON que almacena los usuarios
ARCHIVO_USUARIOS = "data/usuarios.json"

# Base de datos de usuarios en disco
usuarios_db = JsonDB(ARCHIVO_USUARIOS, default={})

def hash_password(password):
    """Encripta la contraseña utilizando el algoritmo SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def registrar_interno(usuario, password):
    """Lógica de registro de usuario."""
    if usuarios_db.exists(usuario):
        log.warning(f"Intento de registro fallido: el usuario '{usuario}' ya existe.")
        return False

    # Guardamos la contraseña encriptada en la base de datos
    usuarios_db.set(usuario, hash_password(password))
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
    if not usuarios_db.exists(usuario):
        log.warning(f"Intento de login fallido: el usuario '{usuario}' no existe.")
        return False

    # Comparamos el hash de la contraseña ingresada con el hash guardado
    return usuarios_db.get(usuario) == hash_password(password)

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
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    menu()