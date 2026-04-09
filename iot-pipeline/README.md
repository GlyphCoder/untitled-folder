# IoT Pipeline — Quick Start

## What this does

```
Node-RED (sensors) → MQTT → Python (anomaly detection) → InfluxDB → Grafana
```

Simulates temperature, humidity, and wind speed sensors every 2 seconds.
Flags anomalies using an Isolation Forest ML model.

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)

---

## Start

```bash
cd iot-pipeline
docker compose up --build
```

First run takes ~3 min (downloads images). After that, ~20 seconds.

---

## Open the apps

| App | URL | Login |
|---|---|---|
| Node-RED | http://localhost:1880 | none |
| Anomaly API | http://localhost:8000/docs | none |
| InfluxDB | http://localhost:8086 | admin / adminpassword |
| Grafana | http://localhost:3000 | admin / admin |

---

## Deploy the Node-RED flow

1. Go to http://localhost:1880
2. The flow is already loaded — click **Deploy** (red button, top right)
3. Green dots on the MQTT nodes = connected ✓
4. The "Write to InfluxDB" node shows **green = Normal** / **red = ANOMALY**

---

## View dashboards in Grafana

1. Go to http://localhost:3000, log in with admin / admin
2. Click **Dashboards → IoT Pipeline → IoT Sensor Pipeline**
3. Data appears within a few seconds. Dashboard auto-refreshes every 5s.

---

## Test the anomaly API manually

```bash
# Normal reading
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature": 25, "humidity": 55, "wind_speed": 10}'

# Anomalous reading (extreme heat)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature": 75, "humidity": 55, "wind_speed": 10}'
```

---

## Stop

```bash
docker compose down        # stop, keep data
docker compose down -v     # stop, delete all data
```

---

## How anomalies are generated (for testing)

The Node-RED sensor generator injects ~10% anomalous readings automatically:
- **Extreme heat**: temperature 60–75 °C
- **Extreme humidity**: humidity 94–100 %
- **Extreme wind**: wind speed 40–60 m/s

You can also trigger one manually in Node-RED by editing the function node.
