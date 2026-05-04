import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_telemetry_data(num_devices=5, num_records_per_device=1000):
    """
    Genera datos de telemetría simulados para dispositivos IoT.
    Incluye datos normales y la inyección intencional de anomalías 
    para poder probar posteriormente el modelo de IA.
    """
    data = []
    start_time = datetime.now() - timedelta(days=7) # Datos de la última semana
    
    for device_id in range(1, num_devices + 1):
        device_name = f"ESP32_Edge_{device_id}"
        
        # Temperatura base normal: media 25C, desv 2
        # Humedad base normal: media 50%, desv 5
        
        for i in range(num_records_per_device):
            timestamp = start_time + timedelta(minutes=10 * i) # Una lectura cada 10 minutos
            
            # Generar datos normales
            temp = np.random.normal(25, 2)
            humidity = np.random.normal(50, 5)
            status = "OK"
            
            # Inyectar anomalías (aprox 3% de los datos)
            if np.random.rand() < 0.03:
                anomaly_type = np.random.choice(["temp_spike", "humidity_drop", "sensor_error"])
                
                if anomaly_type == "temp_spike":
                    temp = np.random.normal(65, 5) # Fuego o sobrecalentamiento extremo
                elif anomaly_type == "humidity_drop":
                    humidity = np.random.normal(5, 2) # Caída brusca de humedad
                elif anomaly_type == "sensor_error":
                    temp = -999 # Valor anómalo indicando falla en el hardware
                    status = "ERROR"
            
            data.append({
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "device_id": device_name,
                "temperature": round(temp, 2),
                "humidity": round(humidity, 2),
                "sensor_status": status
            })
            
    df = pd.DataFrame(data)
    
    # Ordenar por tiempo de forma cronológica
    df = df.sort_values(by="timestamp").reset_index(drop=True)
    
    # Asegurar que el directorio exista
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sensor_telemetry.csv")
    df.to_csv(output_path, index=False)
    print(f"Datos de telemetría generados exitosamente en: {output_path}")
    print(f"Total de registros generados: {len(df)}")
    
    # Imprimir un breve resumen para validar que hay anomalías
    print("\nMuestra de anomalías generadas:")
    anomalies = df[(df['temperature'] > 40) | (df['temperature'] == -999) | (df['humidity'] < 10)]
    print(anomalies.head())

if __name__ == "__main__":
    np.random.seed(42) # Semilla para reproducibilidad
    generate_telemetry_data()
