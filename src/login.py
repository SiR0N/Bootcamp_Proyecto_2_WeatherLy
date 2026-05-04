import hashlib
import getpass
import logging

log = logging.getLogger(__name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def registrar_interno(usuario, password, storage):
    """Recibe el objeto storage desde el main."""
    usuarios = storage.load_data()
    
    if usuario in usuarios:
        log.warning(f"El usuario '{usuario}' ya existe.")
        return False

    usuarios[usuario] = hash_password(password)
    storage.save_data(usuarios)
    return True

def login_interno(usuario, password, storage):
    usuarios = storage.load_data()
    if usuario not in usuarios:
        return False
    return usuarios[usuario] == hash_password(password)

def login(storage):
    print("\n=== LOGIN ===")
    usuario = input("Usuario: ")
    password = getpass.getpass("Contraseña: ")

    if login_interno(usuario, password, storage):
        print("Login exitoso 🎉")
        return True
    else:
        print("Usuario o contraseña incorrectos.")
        return False

def registrar(storage):
    print("\n=== REGISTRO ===")
    usuario = input("Usuario: ")
    password = getpass.getpass("Contraseña: ")

    if registrar_interno(usuario, password, storage):
        print("Usuario registrado correctamente.")
        return True
    else:
        print("Ese usuario ya existe.")
        return False

def menu_autenticacion(storage):
    """Menú principal que recibe el storage configurado."""
    while True:
        print("\n1. Registrar")
        print("2. Login")
        print("3. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            registrar(storage)
        elif opcion == "2":
            if login(storage):
                return True
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")
    return False