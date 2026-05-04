<p align="center">
  <img src="docs/weatherly_logo.png" width="200" alt="Weatherly Logo">
</p>

<h1 align="center">🌦️ Weatherly</h1>

<p align="center">
  <b>Sistema Inteligente de Monitorización Climática</b>
</p>

<p align="center">
  🌍 Monitoriza · 📊 Analiza · 🚨 Detecta alertas en tiempo real
</p>

<br>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/API-Open%20Meteo-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Storage-JSON-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Testing-Pytest-brightgreen?style=for-the-badge&logo=pytest">
  <img src="https://img.shields.io/badge/Scheduler-APScheduler-purple?style=for-the-badge">
  <img src="https://img.shields.io/badge/Graphs-Plotext-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/Git-Version%20Control-black?style=for-the-badge&logo=git">
</p>

---

## ✨ Introducción

🌦️ **WeatherLy** es una aplicación en Python diseñada para la monitorización meteorológica en tiempo real.

Permite:
- 📡 Obtener datos desde API
- ✅ Validarlos
- 💾 Guardarlos
- 🚨 Generar alertas
- 📊 Analizarlos

Este sistema simula un entorno backend real, aplicando principios de arquitectura modular y separación de responsabilidades.

💡 **Caso de uso real:**  
WeatherLy podría ser utilizado por ayuntamientos o empresas para detectar condiciones meteorológicas adversas (olas de calor, vientos fuertes, humedad extrema) y tomar decisiones preventivas.

🎯 **Objetivo del proyecto:**  
Construir una base sólida de procesamiento de datos que integre API, validación, almacenamiento, análisis y automatización en un único sistema coherente.

---

## 🚀 Funcionalidades principales

- 🌍 **Monitorización climática en tiempo real**  
  Obtiene datos meteorológicos actualizados desde una API externa para múltiples ciudades.

- 🏙️ **Gestión de múltiples ciudades**  
  Permite trabajar simultáneamente con distintas ubicaciones definidas en el sistema.

- ✅ **Validación automática de datos**  
  Verifica que los datos recibidos cumplen formato y rangos válidos antes de procesarlos.

- 🚨 **Sistema de alertas inteligentes**  
  Detecta condiciones meteorológicas críticas y genera avisos según umbrales definidos.

- 💾 **Persistencia en JSON**  
  Guarda los datos de forma estructurada en archivos JSON para su consulta posterior.

- 🔁 **Control de duplicados**  
  Evita almacenar registros repetidos mediante validación por fecha y ciudad.

- 📊 **Estadísticas por ciudad**  
  Calcula métricas como media y mediana de temperatura, humedad y viento.

- 📈 **Gráficos en terminal**  
  Visualiza la evolución de los datos mediante gráficos directamente en consola.

- ⏱️ **Automatización de tareas**  
  Permite programar ejecuciones periódicas para actualizar datos automáticamente.

- 📝 **Logging profesional**  
  Registra eventos, errores y operaciones del sistema para facilitar debugging y trazabilidad.

- 🧪 **Tests con pytest**  
  Incluye pruebas automatizadas para garantizar el correcto funcionamiento del sistema.

---

## 🛠️ Arquitectura del sistema

```text
Bootcamp_Proyecto_2_WeatherLy/
│
├─ src/
│  ├─ main.py          🧠 Orquestador principal
│  ├─ api_client.py    🌐 API externa
│  ├─ storage.py       💾 Persistencia JSON
│  ├─ validator.py     ✅ Validaciones
│  ├─ alerts.py        🚨 Alertas
│  ├─ scheduler.py     ⏱️ Automatización
│  ├─ logger_config.py 📝 Logs
│  ├─ cities.py        🏙️ Ciudades
│
├─ data/               📂 Datos
├─ logs/               📜 Logs
├─ tests/              🧪 Tests

---

## 🧠 Componentes del sistema

### 🧠 main.py
Orquesta toda la aplicación y gestiona el menú interactivo.

### 🌐 api_client.py
- Conexión con la API Open-Meteo  
- Normalización de datos  
- Manejo de errores  

### 💾 storage.py
- Guarda datos en JSON  
- Evita duplicados (fecha + ciudad)  
- Crea backups automáticos  

### ✅ validator.py
- Valida formato de fecha  
- Valida rangos de temperatura, humedad y viento  

### 🚨 alerts.py
Genera alertas automáticas según condiciones climáticas.

### ⏱️ scheduler.py
Permite ejecutar tareas automáticamente cada X minutos.

### 📝 logger_config.py
Gestiona los logs del sistema (errores, eventos, etc.)

### 🏙️ cities.py
Define las ciudades disponibles y sus coordenadas


---

## 📊 Flujo de datos

```text
API → Normalización → Validación → Alertas → Almacenamiento → Visualización
```

### 🔎 Descripción del flujo

1. **📡 Obtención de datos (API)**  
   Se consumen datos meteorológicos en tiempo real desde la API Open-Meteo para cada ciudad.

2. **🔄 Normalización**  
   Los datos se transforman a un formato estándar (fecha, ciudad, temperatura, humedad, viento).

3. **✅ Validación**  
   Se comprueba que los datos cumplen los formatos y rangos definidos para evitar errores.

4. **🚨 Generación de alertas**  
   Se analizan los valores y se generan alertas en caso de condiciones críticas.

5. **💾 Almacenamiento**  
   Los datos válidos se guardan en archivos JSON, evitando duplicados.

6. **📊 Visualización y análisis**  
   Se muestran estadísticas y gráficos en terminal para interpretar la información.


## 🚀 Instalación y ejecución

```bash
git clone TU_REPO
cd Bootcamp_Proyecto_2_WeatherLy

python -m venv venv
# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt

python src/main.py
```

---

## 🧪 Testing

```bash
pytest
```

El proyecto incluye una suite de tests automatizados desarrollados con **pytest** para garantizar la fiabilidad del sistema.

### 🔎 ¿Qué se valida?

- 💾 **Persistencia de datos**  
  Verifica que los registros se guardan correctamente en JSON.

- 🔁 **Control de duplicados**  
  Asegura que no se almacenan registros repetidos (misma fecha y ciudad).

- 🌐 **Normalización de datos de API**  
  Comprueba que los datos recibidos se transforman correctamente al formato interno.

- 🚨 **Gestión de alertas**  
  Valida que las alertas se generan y almacenan correctamente.

### 🎯 Objetivo

Garantizar que cada módulo funciona de forma independiente y que los cambios futuros no rompan funcionalidades existentes.
---


## 📂 Ejemplo de datos

### 🌦️ Registro meteorológico

```json
{
  "date": "2026-05-02T10:00",
  "city": "Toledo",
  "temp": 22.5,
  "hum": 60,
  "wind": 15.2,
  "source": "Open Meteo"
}
```

### 🚨 Registro de alerta

```json
{
  "date": "2026-05-02T10:00",
  "city": "Toledo",
  "level": "WARNING",
  "metric": "temp",
  "value": 42,
  "message": "Abnormal temperature"
}
```

---

## 🛡️ Calidad del sistema
El sistema está diseñado siguiendo buenas prácticas de desarrollo para garantizar robustez y mantenibilidad:

- ✅ Validación de datos antes del guardado  
- 🔁 Control de duplicados por fecha y ciudad  
- 💾 Persistencia en JSON  
- 📝 Sistema de logs  
- 🧪 Tests automatizados  
- ⏱️ Automatización de tareas  
- 📊 Estadísticas y gráficos en terminal  

---

## 🔮 Mejoras futuras

- 🌐 Interfaz web con Streamlit  
- 🗄️ Base de datos PostgreSQL  
- 📊 Dashboard visual avanzado  
- 🔔 Notificaciones por email o Telegram  
- ☁️ Despliegue en la nube  

---

## 👩‍💻 Proyecto Bootcamp

Proyecto desarrollado como práctica de arquitectura backend, integrando consumo de APIs, validación de datos, persistencia, testing y automatización en un sistema modular real.

---

## 👥 Equipo

- 👩‍💻 SiRON
- 👨‍💻 luiselallali18-hub
- 👩‍💻 MariaIsaDurango 
- 👨‍💻 garciaguadalupevanessa-bit  
- 👨‍💻 Gema-Villanueva

