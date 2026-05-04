import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def train_and_evaluate_model():
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sensor_telemetry.csv")
    
    if not os.path.exists(data_path):
        print(f"Error: No se encontró el archivo de datos en {data_path}")
        return

    df = pd.read_csv(data_path)
    
    # Preprocesamiento básico (usar sólo variables numéricas)
    features = ['temperature', 'humidity']
    X = df[features].copy()
    
    # Configurar modelo Isolation Forest
    # contamination = 0.03 ya que inyectamos aprox 3% de anomalías
    model = IsolationForest(n_estimators=100, contamination=0.03, random_state=42)
    
    print("Entrenando el modelo Isolation Forest...")
    model.fit(X)
    
    # Predecir anomalías (-1 significa anomalía, 1 significa normal)
    df['anomaly_prediction'] = model.predict(X)
    
    # Calcular métricas básicas 
    # Consideramos 'anomalía real' si la temp > 40 o temp == -999 o humedad < 10
    df['real_anomaly'] = ((df['temperature'] > 40) | (df['temperature'] == -999) | (df['humidity'] < 10)).astype(int)
    # Convertir predicción a 1 (anomalía) y 0 (normal)
    df['pred_anomaly'] = (df['anomaly_prediction'] == -1).astype(int)
    
    # Verdaderos positivos, falsos positivos...
    tp = len(df[(df['real_anomaly'] == 1) & (df['pred_anomaly'] == 1)])
    fp = len(df[(df['real_anomaly'] == 0) & (df['pred_anomaly'] == 1)])
    fn = len(df[(df['real_anomaly'] == 1) & (df['pred_anomaly'] == 0)])
    tn = len(df[(df['real_anomaly'] == 0) & (df['pred_anomaly'] == 0)])
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print("\nResultados de Detección de Anomalías:")
    print(f"Total Registros: {len(df)}")
    print(f"Verdaderos Positivos (Anomalías correctas): {tp}")
    print(f"Falsos Positivos (Falsas alarmas): {fp}")
    print(f"Falsos Negativos (Anomalías no detectadas): {fn}")
    print(f"Verdaderos Negativos (Normales correctos): {tn}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall (TPR): {recall:.4f}")
    print(f"F1-Score: {f1_score:.4f}")
    
    # Guardar el modelo
    model_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "isolation_forest.pkl")
    joblib.dump(model, model_path)
    print(f"\nModelo guardado en: {model_path}")
    
    # Graficar y guardar imagen de resultados
    plt.figure(figsize=(12, 6))
    normal_data = df[df['pred_anomaly'] == 0]
    anomaly_data = df[df['pred_anomaly'] == 1]
    
    plt.scatter(normal_data['temperature'], normal_data['humidity'], c='blue', label='Normal', alpha=0.5, s=10)
    plt.scatter(anomaly_data['temperature'], anomaly_data['humidity'], c='red', label='Anomalía Detectada', alpha=0.8, s=20)
    plt.xlabel('Temperatura')
    plt.ylabel('Humedad')
    plt.title('Detección de Anomalías (Isolation Forest)')
    plt.legend()
    
    plot_path = os.path.join(model_dir, "anomalies_plot.png")
    plt.savefig(plot_path)
    print(f"Gráfico guardado en: {plot_path}")

if __name__ == "__main__":
    train_and_evaluate_model()
