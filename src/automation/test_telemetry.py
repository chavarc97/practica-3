import pandas as pd
import pytest
import os

@pytest.fixture
def telemetry_data():
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sensor_telemetry.csv")
    if not os.path.exists(data_path):
        pytest.skip(f"El archivo {data_path} no existe. Por favor, genere los datos primero.")
    return pd.read_csv(data_path)

def test_data_format(telemetry_data):
    """Verifica que el dataset contenga las columnas esperadas."""
    expected_columns = ["timestamp", "device_id", "temperature", "humidity", "sensor_status"]
    for col in expected_columns:
        assert col in telemetry_data.columns, f"Falta la columna esperada: {col}"

def test_no_missing_values(telemetry_data):
    """Verifica que no haya valores nulos en el dataset base."""
    assert telemetry_data.isnull().sum().sum() == 0, "Se encontraron valores nulos en el dataset."

def test_anomalies_present(telemetry_data):
    """Verifica que el dataset tenga casos límite/anomalías inyectadas para la IA."""
    high_temps = telemetry_data[telemetry_data['temperature'] > 40]
    errors = telemetry_data[telemetry_data['sensor_status'] == 'ERROR']
    low_humidity = telemetry_data[telemetry_data['humidity'] < 10]
    
    assert len(high_temps) > 0 or len(errors) > 0 or len(low_humidity) > 0, "No se encontraron anomalías en los datos. El modelo de IA no podrá ser probado adecuadamente."

def test_sensor_bounds(telemetry_data):
    """Verifica que las lecturas de humedad estén en rangos realistas (0-100%)."""
    # Nota: la temperatura puede ser negativa (ej. -999 para errores) pero la humedad no debería.
    assert (telemetry_data['humidity'] >= 0).all(), "Humedad negativa detectada."
    assert (telemetry_data['humidity'] <= 100).all(), "Humedad mayor a 100% detectada."
