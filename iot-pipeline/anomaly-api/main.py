from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.ensemble import IsolationForest
import numpy as np

app = FastAPI(title="IoT Anomaly Detection")

# ── Train model once at startup ───────────────────────────────────────────────
# Generate 1000 "normal" sensor readings as training data
rng = np.random.default_rng(42)
normal_data = np.column_stack([
    rng.uniform(15, 40, 1000),   # temperature: 15–40 °C
    rng.uniform(30, 80, 1000),   # humidity:    30–80 %
    rng.uniform(0,  25, 1000),   # wind_speed:   0–25 m/s
])

model = IsolationForest(contamination=0.05, random_state=42)
model.fit(normal_data)
print("✅ Anomaly detection model ready")


# ── Request / Response schemas ────────────────────────────────────────────────
class Reading(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float


# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(reading: Reading):
    X = [[reading.temperature, reading.humidity, reading.wind_speed]]

    # predict() returns 1 (normal) or -1 (anomaly)
    is_anomaly = model.predict(X)[0] == -1

    # decision_function() returns a score: lower = more anomalous
    score = round(float(model.decision_function(X)[0]), 4)

    return {"anomaly": is_anomaly, "score": score}
