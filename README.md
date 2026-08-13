# 🚀 VexarDrive Fleet Intelligence & Analytics Dashboard

An end-to-end telemetry processing engine and interactive web dashboard for **VexarDrive Technologies** fleet operations in Bengaluru.

Live Dashboard URL: **[https://605b18fbc82a2d.lhr.life](https://605b18fbc82a2d.lhr.life)**

---

## 📌 Project Overview

This repository parses, processes, and visualizes multi-modal telematics data from **30 delivery drivers**, **30 fleet two-wheelers**, **450 trips**, and **12,987 per-minute telemetry records**.

It provides two core operational dashboards:
1. **Driver Behaviour Dashboard** — Quantifies driver safety & aggressive driving patterns using IMU (accelerometer + gyroscope) and GPS telemetry.
2. **Vehicle Health Status Dashboard** — Detects mechanical degradation, suspension wear, and maintenance urgency from vibration variance, service logs, and mileage.

---

## 📊 1. Driver Behaviour Scoring Methodology

The **Risk Score ($0$ to $100$)** evaluates driver safety ($0 = \text{safest}$, $100 = \text{most risky}$):

$$\text{Risk Score} = \min\Big(100,\, 0.30 \cdot S + 0.25 \cdot B + 0.20 \cdot L + 0.15 \cdot Y + 0.10 \cdot N - E\Big)$$

Where:
* **Speed Violations ($S$, 30%)**: % of telemetry minutes exceeding $60\text{ km/h}$ (Karnataka urban two-wheeler speed limit).
* **Hard Braking ($B$, 25%)**: % of telemetry minutes with $\text{Accel\_X} < -0.3g$ (harsh deceleration threshold).
* **Sharp Turns ($L$, 20%)**: % of telemetry minutes with $|\text{Accel\_Y}| > 0.3g$ (aggressive cornering).
* **Yaw Spikes ($Y$, 15%)**: % of telemetry minutes with $|\text{Gyro\_Z}| > 10\text{ dps}$ (abrupt steering rotation).
* **Night Driving ($N$, 10%)**: % of trips starting between 21:00 and 05:59.
* **Experience Bonus ($E$)**: Up to $-10$ point reduction for $14+$ years of license experience.

---

## 🔧 2. Vehicle Health Scoring Methodology

The **Health Score ($0$ to $100$)** evaluates mechanical condition ($100 = \text{excellent}$, $0 = \text{critical}$):

$$\text{Health Score} = \max\Big(0,\, 100 - \big(0.25 \cdot V + 0.25 \cdot M + 0.15 \cdot G + 0.15 \cdot O + 0.10 \cdot A + 0.10 \cdot H\big)\Big)$$

Where:
* **Vibration ($V$, 25%)**: Standard deviation of $\text{Accel\_Z}$ from $1g$ gravity baseline (detects rough ride & suspension wear).
* **Service Overdue ($M$, 25%)**: Days since last service ($>30$ days penalized, $>90$ days flagged `CRITICAL`).
* **Gyro Instability ($G$, 15%)**: Mean magnitude of 3-axis gyroscope vector (detects frame/wheel alignment drift).
* **Odometer ($O$, 15%)**: Cumulative mileage normalized against fleet maximum ($46,601\text{ km}$).
* **Vehicle Age ($A$, 10%)**: Manufacture year baseline wear ($2019$ to $2025$).
* **Harsh Events ($H$, 10%)**: % of telemetry minutes with multi-axis IMU spikes recorded on this vehicle.

### Maintenance Status Flags
* **OK (✅)**: Health Score $\ge 60$ and Days Since Service $\le 60$.
* **MONITOR (👁️)**: Health Score $40$–$59$ or minor vibration anomalies.
* **DUE (⚠️)**: Days Since Service $> 60$.
* **CRITICAL (🔴)**: Days Since Service $> 90$ or severe vibration deviation.

---

## 📝 3. Explicit Assumptions

| Parameter | Value | Rationale |
|---|---|---|
| Speed limit | $60\text{ km/h}$ | Karnataka Motor Vehicles Rules — urban two-wheeler limit in Bengaluru |
| Hard braking | $\text{Accel\_X} < -0.3g$ | Industry-standard telematics harsh deceleration threshold |
| Sharp turn | $|\text{Accel\_Y}| > 0.3g$ | Lateral g-force indicating aggressive cornering or lane change |
| Yaw spike | $|\text{Gyro\_Z}| > 10\text{ dps}$ | Sudden yaw rotation threshold for abrupt steering input |
| Normal vibration | $\text{Accel\_Z} \approx 1g$ | Gravity baseline; std dev from $1g$ measures mechanical vibration |
| Service interval | $60\text{ days}$ | Standard for delivery two-wheelers in Indian fleet operations |
| Night hours | $21:00$–$05:59$ | Post-sunset / pre-sunrise increased collision risk window |
| IMU orientation | Fixed per vehicle | Phone mount assumed fixed; axis directions consistent across trips |
| Telemetry interval | $1\text{ row} = 1\text{ min}$ | Per dataset specification; used for event rate calculations |

---

## 💡 4. Additional Dataset Use Cases

1. **ETA Prediction Model**: Training machine learning models on per-minute GPS traces and speed profiles to predict arrival times per hub and time-of-day.
2. **Route Optimisation**: Identifying congestion bottlenecks and actual vs. optimal path divergence.
3. **Fuel / Battery Cost Modelling**: Estimating energy consumption per trip to identify high-cost routes or inefficient driving styles.
4. **Targeted Safety Training**: Clustering drivers by fault type (hard braking vs. speeding vs. yaw rotation) to personalize safety intervention.
5. **Predictive Maintenance ML**: Anomaly detection on vibration drift and IMU variance to flag vehicles before physical breakdown occurs.
6. **Usage-Based Insurance (UBI)**: Pricing insurance premiums based on actual driving telemetry rather than demographic proxies.

---

## 📁 Repository Structure

```
vexardrive-dashboard/
├── index.html            # Single-file self-contained interactive web dashboard
├── extract_vexar.py      # PDF parsing & data extraction script
├── analytics_engine.py   # Telemetry analytics & scoring computation engine
└── build_dashboard.py    # Generator script embedding analytics into index.html
```

---

## ⚙️ How to Run Locally

```bash
# 1. Clone repository
git clone https://github.com/<your-username>/vexardrive-dashboard.git
cd vexardrive-dashboard

# 2. Open dashboard directly in browser
open index.html

# 3. Or launch local HTTP server
python3 -m http.server 8080
# Open http://localhost:8080
```
