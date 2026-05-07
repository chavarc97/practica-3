"""Genera gráfico de matriz de confusión del modelo Isolation Forest."""

import pandas as pd
import numpy as np
import joblib
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "sensor_telemetry.csv")
MODEL_PATH = os.path.join(BASE_DIR, "ai_models", "isolation_forest.pkl")
EVIDENCIAS_DIR = os.path.join(BASE_DIR, "evidencias")


def main():
    df = pd.read_csv(DATA_PATH)
    model = joblib.load(MODEL_PATH)

    X = df[["temperature", "humidity"]].copy()
    df["pred_anomaly"] = (model.predict(X) == -1).astype(int)
    df["real_anomaly"] = (
        (df["temperature"] > 40) | (df["temperature"] == -999) | (df["humidity"] < 10)
    ).astype(int)

    tp = len(df[(df["real_anomaly"] == 1) & (df["pred_anomaly"] == 1)])
    fp = len(df[(df["real_anomaly"] == 0) & (df["pred_anomaly"] == 1)])
    fn = len(df[(df["real_anomaly"] == 1) & (df["pred_anomaly"] == 0)])
    tn = len(df[(df["real_anomaly"] == 0) & (df["pred_anomaly"] == 0)])

    cm = np.array([[tn, fp], [fn, tp]])
    labels = [["TN", "FP"], ["FN", "TP"]]

    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.colorbar(im, ax=ax)

    classes = ["Normal", "Anomalía"]
    ax.set(
        xticks=[0, 1], yticks=[0, 1],
        xticklabels=classes, yticklabels=classes,
        xlabel="Predicción del Modelo",
        ylabel="Etiqueta Real",
        title="Matriz de Confusión — Isolation Forest (IoT Telemetría)",
    )

    for i in range(2):
        for j in range(2):
            color = "white" if cm[i, j] > cm.max() / 2 else "black"
            ax.text(j, i, f"{labels[i][j]}\n{cm[i, j]:,}",
                    ha="center", va="center", fontsize=13, color=color, fontweight="bold")

    precision = tp / (tp + fp)
    recall    = tp / (tp + fn) if (tp + fn) > 0 else 1.0
    f1        = 2 * precision * recall / (precision + recall)
    fpr       = fp / (fp + tn)

    fig.text(0.5, -0.04,
             f"Precision={precision:.4f}  Recall/TPR={recall:.4f}  F1={f1:.4f}  FPR={fpr:.4f}",
             ha="center", fontsize=10, color="gray")

    plt.tight_layout()
    out = os.path.join(EVIDENCIAS_DIR, "confusion_matrix.png")
    plt.savefig(out, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"Matriz de confusión guardada en: {out}")


if __name__ == "__main__":
    main()
