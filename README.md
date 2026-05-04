# Práctica 3: Validación y Pruebas en Sistema IoT con IA

Este repositorio contiene la implementación y los entregables correspondientes a la validación de un ecosistema IoT simulado. Incluye la inyección intencional de fallos y la utilización de un modelo de Inteligencia Artificial (*Isolation Forest*) para la detección de anomalías en la telemetría.

## Estructura del Proyecto

```text
.
├── practica-3.md            # Entregable completo documentado (Plan, Casos, Matriz de Riesgos)
├── README.md                # Instrucciones de ejecución
├── instructions.md          # Instrucciones originales formateadas
└── src/                     # Código fuente
    ├── requirements.txt     # Dependencias de Python
    ├── data/
    │   └── generate_data.py # Simulador que genera telemetría de dispositivos IoT (CSV)
    ├── ai_models/
    │   ├── anomaly_detector.py # Entrena y evalúa la IA (Isolation Forest)
    │   ├── isolation_forest.pkl# Modelo exportado (generado al correr la IA)
    │   └── anomalies_plot.png  # Gráfico de resultados (generado al correr la IA)
    └── automation/
        ├── test_telemetry.py # Pruebas funcionales de datos usando pytest
        └── test_mqtt_mock.py # Simulación y validación de conexión y payloads MQTT
```

## Requisitos Previos
- Python 3.9 o superior instalado en tu sistema.

## Instrucciones de Ejecución

Sigue estos pasos en tu terminal para replicar el entorno de pruebas, generar la data sintética y correr la IA:

### 1. Preparar el Entorno Virtual
Se recomienda utilizar un entorno virtual de Python (`venv`) para aislar las dependencias:

**En Mac/Linux:**
```bash
cd src/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**En Windows:**
```bash
cd src\
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Generar Datos Simulados (Sensores IoT)
Ejecuta el script que simulará los dispositivos enviando temperatura y humedad. Este código inyecta un pequeño porcentaje de anomalías:
```bash
python data/generate_data.py
```
> **Resultado:** Se generará el archivo `sensor_telemetry.csv` dentro de la carpeta `data/` con miles de registros históricos.

### 3. Entrenar y Evaluar el Modelo de IA
Ejecuta el modelo de Machine Learning que buscará aislar los datos atípicos:
```bash
python ai_models/anomaly_detector.py
```
> **Resultado:** Verás las métricas del modelo (como *Precision* y *Recall*) en consola. Además se crearán automáticamente los archivos `isolation_forest.pkl` y la gráfica visual `anomalies_plot.png`.

### 4. Correr la Suite de Pruebas Automatizadas
Para verificar que los mockups de MQTT, validaciones de esquema y las aserciones de robustez pasen correctamente, usa `pytest`:
```bash
pytest automation/
```
> **Resultado:** Verás una salida verde indicando que los 8 casos de prueba simulados (Telemetría y MQTT) se ejecutaron con éxito.
