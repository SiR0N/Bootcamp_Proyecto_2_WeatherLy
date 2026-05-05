import json

def user_registration_flow(components):
    """Sistema de aceptación de términos y registro."""
    path = os.path.join(DATA_DIR, "users_consent.json")
    
    # 1. Verificar si ya existe consentimiento
    if os.path.exists(path):
        with open(path, 'r') as f:
            consents = json.load(f)
            if consents: # Si hay alguien, asumimos que ya pasó el filtro inicial
                return True

    # 2. Formulario de términos
    print("\n" + "="*40)
    print("      TÉRMINOS Y CONDICIONES DE WEATHERLY")
    print("="*40)
    print("1. Aceptas el uso de tus datos para análisis meteorológico.")
    print("2. Los datos se guardarán localmente en formato JSON.")
    print("3. No garantizamos que no llueva aunque la app diga sol.")
    
    confirm = input("\n¿Aceptas estos términos para continuar? (S/N): ").strip().upper()
    
    if confirm == "S":
        user_data = {
            "user_id": "default_user",
            "accepted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "terms_version": "1.0"
        }
        # Guardar en la carpeta data
        with open(path, 'w') as f:
            json.dump([user_data], f, indent=4)
        
        print("\n[✓] Registro completado. ¡Bienvenido a Weatherly!")
        time.sleep(1)
        return True
    else:
        print("\n[!] Debes aceptar los términos para usar la aplicación.")
        sys.exit() # Cerramos la app si no acepta
