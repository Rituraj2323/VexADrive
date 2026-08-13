"""
VexarDrive Analytics Engine
Computes driver risk scores and vehicle health scores, then outputs JSON for the dashboard.
"""
import csv, json, math, os
from collections import defaultdict
from datetime import datetime

DATA_DIR = "/Users/riturajbhattacharjee/.gemini/antigravity/scratch/vexar_data"
OUT_PATH = "/Users/riturajbhattacharjee/.gemini/antigravity/scratch/vexar_data/analytics.json"

# ─── Load CSVs ───────────────────────────────────────────────────
def load_csv(fname):
    with open(os.path.join(DATA_DIR, fname)) as f:
        return list(csv.DictReader(f))

drivers_raw   = load_csv("drivers.csv")
vehicles_raw  = load_csv("vehicles.csv")
trips_raw     = load_csv("trips.csv")
telemetry_raw = load_csv("telemetry.csv")

print(f"Loaded: {len(drivers_raw)} drivers, {len(vehicles_raw)} vehicles, "
      f"{len(trips_raw)} trips, {len(telemetry_raw)} telemetry rows")

# ─── Index by ID ─────────────────────────────────────────────────
drivers  = {d["Driver_ID"]: d  for d in drivers_raw}
vehicles = {v["Vehicle_ID"]: v for v in vehicles_raw}

# ─── Group telemetry ─────────────────────────────────────────────
tel_by_driver  = defaultdict(list)
tel_by_vehicle = defaultdict(list)
trips_by_driver = defaultdict(list)

for row in telemetry_raw:
    tel_by_driver[row["Driver_ID"]].append(row)
    tel_by_vehicle[row["Vehicle_ID"]].append(row)

for row in trips_raw:
    trips_by_driver[row["Driver_ID"]].append(row)

# Reference date for age calculations
REF_DATE = datetime(2026, 8, 13)

# ─── DRIVER RISK SCORING ─────────────────────────────────────────
"""
Risk score 0-100 (higher = more risky).
Components:
  1. Speed violations: % minutes where Speed > 60 kmph (urban two-wheeler limit)
  2. Hard braking:    count of minutes where Accel_X < -0.3g   (deceleration spikes)
  3. Sharp turns:     count of minutes where |Accel_Y| > 0.3g  (lateral g-force)
  4. Sudden yaw:      count of minutes where |Gyro_Z| > 10 dps (abrupt yaw rotation)
  5. Night driving:   % trips with start time hour < 6 or > 21
  6. Experience bonus: reduces raw risk by up to 10pts for experienced drivers

Assumptions:
  - 60 kmph threshold is a reasonable urban speed limit for two-wheelers in India.
  - Accel thresholds are typical IMU-based harsh driving thresholds.
  - Night driving is 21:00–05:59 as per Indian sunset/sunrise norms.
  - Risk components are weighted and normalized to 0-100 scale.
"""

WEIGHTS = {
    "speed":    0.30,
    "braking":  0.25,
    "lateral":  0.20,
    "yaw":      0.15,
    "night":    0.10,
}

driver_results = []

for did, d in drivers.items():
    rows = tel_by_driver[did]
    if not rows:
        continue

    n = len(rows)
    speed_viol  = sum(1 for r in rows if float(r["Speed_kmph"])  > 60)
    hard_brake  = sum(1 for r in rows if float(r["Accel_X_g"])   < -0.3)
    sharp_turn  = sum(1 for r in rows if abs(float(r["Accel_Y_g"])) > 0.3)
    yaw_spike   = sum(1 for r in rows if abs(float(r["Gyro_Z_dps"])) > 10)

    speed_pct   = (speed_viol  / n) * 100
    braking_pct = (hard_brake  / n) * 100
    lateral_pct = (sharp_turn  / n) * 100
    yaw_pct     = (yaw_spike   / n) * 100

    # Night driving
    my_trips = trips_by_driver[did]
    night_count = 0
    for t in my_trips:
        try:
            h = int(t["Start_Time"][:2])
            if h < 6 or h >= 21:
                night_count += 1
        except:
            pass
    night_pct = (night_count / len(my_trips)) * 100 if my_trips else 0

    # Normalize each component to 0-100
    # Speed: >60kmph >50% time = fully risky
    speed_score   = min(speed_pct  / 50  * 100, 100)
    braking_score = min(braking_pct/ 20  * 100, 100)
    lateral_score = min(lateral_pct/ 30  * 100, 100)
    yaw_score     = min(yaw_pct    / 15  * 100, 100)
    night_score   = min(night_pct  / 50  * 100, 100)

    raw_risk = (
        WEIGHTS["speed"]   * speed_score   +
        WEIGHTS["braking"] * braking_score +
        WEIGHTS["lateral"] * lateral_score +
        WEIGHTS["yaw"]     * yaw_score     +
        WEIGHTS["night"]   * night_score
    )

    # Experience reduces risk slightly (more experience = better risk management)
    exp = int(d.get("License_Experience_Years", 0))
    exp_bonus = min(exp, 14) / 14 * 10   # max 10pt reduction
    final_risk = max(0, min(100, raw_risk - exp_bonus))

    # Speed stats
    speeds = [float(r["Speed_kmph"]) for r in rows]
    max_spd = max(speeds)
    avg_spd = sum(speeds) / len(speeds)

    driver_results.append({
        "Driver_ID": did,
        "Driver_Name": d["Driver_Name"],
        "Age": int(d["Age"]),
        "Gender": d["Gender"],
        "Experience_Years": exp,
        "Home_Hub": d.get("Home_Hub", ""),
        "Primary_Vehicle_ID": d.get("Primary_Vehicle_ID", ""),
        "Total_Trips": len(my_trips),
        "Total_Minutes": n,
        "Risk_Score": round(final_risk, 1),
        "Speed_Score": round(speed_score, 1),
        "Braking_Score": round(braking_score, 1),
        "Lateral_Score": round(lateral_score, 1),
        "Yaw_Score": round(yaw_score, 1),
        "Night_Score": round(night_score, 1),
        "Speed_Violation_Pct": round(speed_pct, 1),
        "Hard_Brake_Pct": round(braking_pct, 1),
        "Sharp_Turn_Pct": round(lateral_pct, 1),
        "Yaw_Spike_Pct": round(yaw_pct, 1),
        "Night_Trip_Pct": round(night_pct, 1),
        "Max_Speed_kmph": round(max_spd, 1),
        "Avg_Speed_kmph": round(avg_spd, 1),
        "Speed_Violations": speed_viol,
        "Hard_Brakes": hard_brake,
        "Sharp_Turns": sharp_turn,
        "Yaw_Spikes": yaw_spike,
        "Night_Trips": night_count,
    })

driver_results.sort(key=lambda x: x["Risk_Score"], reverse=True)
print(f"Driver scores computed for {len(driver_results)} drivers")

# ─── VEHICLE HEALTH SCORING ──────────────────────────────────────
"""
Health score 0-100 (higher = healthier).
Components:
  1. Vibration (Accel_Z): std dev from 1g — higher std = rougher ride = mechanical wear
  2. Gyro instability: mean magnitude of gyro vector — persistent rotation = frame/wheel issues
  3. Days since last service: >60 days = concern, >90 = critical
  4. Odometer age: normalized by fleet max; higher km = more wear
  5. Manufacture age: older vehicles score lower
  6. Harsh events rate: proportion of minutes with any harsh event on this vehicle

Assumptions:
  - Accel_Z near 1g is normal (gravity). Deviations indicate vibration/bumps.
  - Gyro magnitude baseline: <5 dps is stable.
  - Service interval: 60 days is standard for delivery two-wheelers in India.
  - Manufacture age penalty applies from 2019 onwards (oldest in fleet).
"""

max_odo = max(int(v["Odometer_KM_Start_of_Week"]) for v in vehicles_raw)
min_year = min(int(v["Manufacture_Year"]) for v in vehicles_raw)
max_year = max(int(v["Manufacture_Year"]) for v in vehicles_raw)

vehicle_results = []

for vid, v in vehicles.items():
    rows = tel_by_vehicle[vid]
    if not rows:
        vib_std = gyro_mag_mean = harsh_rate = 0.0
    else:
        n = len(rows)
        accel_z = [float(r["Accel_Z_g"]) for r in rows]
        vib_std = math.sqrt(sum((z - 1.0)**2 for z in accel_z) / n)

        gyro_mags = [
            math.sqrt(float(r["Gyro_X_dps"])**2 + float(r["Gyro_Y_dps"])**2 + float(r["Gyro_Z_dps"])**2)
            for r in rows
        ]
        gyro_mag_mean = sum(gyro_mags) / n

        harsh = sum(1 for r in rows if
                    abs(float(r["Accel_X_g"])) > 0.3 or
                    abs(float(r["Accel_Y_g"])) > 0.3 or
                    abs(float(r["Accel_Z_g"]) - 1.0) > 0.15)
        harsh_rate = (harsh / n) * 100

    # Days since service
    last_svc = datetime.strptime(v["Last_Service_Date"], "%Y-%m-%d")
    days_since_svc = (REF_DATE - last_svc).days

    # Odometer
    odo = int(v["Odometer_KM_Start_of_Week"])

    # Age
    mfg_year = int(v["Manufacture_Year"])
    vehicle_age_years = REF_DATE.year - mfg_year

    # ── Component scores (all 0-100, where 100 = worst/unhealthiest) ──
    # Vibration: std dev > 0.05g is concerning
    vib_score    = min(vib_std / 0.1 * 100, 100)
    # Gyro: mean magnitude > 10 dps is concerning
    gyro_score   = min(gyro_mag_mean / 10 * 100, 100)
    # Service: >60 days = 50%, >90 days = 100%
    svc_score    = min(max(0, days_since_svc - 30) / 60 * 100, 100)
    # Odometer: normalized
    odo_score    = (odo / max_odo) * 100
    # Age: 2019 = 7yr old, 2025 = 1yr old
    age_range = max_year - min_year if max_year > min_year else 1
    age_score    = ((max_year - mfg_year) / age_range) * 100
    # Harsh events
    harsh_score  = min(harsh_rate / 30 * 100, 100)

    # Weighted unhealthy score
    w_vib   = 0.25
    w_gyro  = 0.15
    w_svc   = 0.25
    w_odo   = 0.15
    w_age   = 0.10
    w_harsh = 0.10

    unhealthy = (w_vib  * vib_score  + w_gyro * gyro_score +
                 w_svc  * svc_score  + w_odo  * odo_score  +
                 w_age  * age_score  + w_harsh * harsh_score)

    health_score = round(max(0, 100 - unhealthy), 1)

    # Maintenance flag
    if days_since_svc > 90:
        maintenance_flag = "CRITICAL"
    elif days_since_svc > 60:
        maintenance_flag = "DUE"
    elif health_score < 40:
        maintenance_flag = "MONITOR"
    else:
        maintenance_flag = "OK"

    vehicle_results.append({
        "Vehicle_ID": vid,
        "Make": v["Make"],
        "Model": v["Model"],
        "Vehicle_Type": v["Vehicle_Type"],
        "Manufacture_Year": mfg_year,
        "Registration_Date": v["Registration_Date"],
        "Odometer_KM": odo,
        "Last_Service_Date": v["Last_Service_Date"],
        "Days_Since_Service": days_since_svc,
        "Health_Score": health_score,
        "Vibration_Std": round(vib_std, 4),
        "Gyro_Mag_Mean": round(gyro_mag_mean, 2),
        "Harsh_Event_Pct": round(harsh_rate, 1),
        "Service_Score": round(svc_score, 1),
        "Odo_Score": round(odo_score, 1),
        "Vib_Score": round(vib_score, 1),
        "Maintenance_Flag": maintenance_flag,
        "Vehicle_Age_Years": vehicle_age_years,
    })

vehicle_results.sort(key=lambda x: x["Health_Score"])
print(f"Vehicle scores computed for {len(vehicle_results)} vehicles")

# ─── Fleet-level summary ──────────────────────────────────────────
risky_drivers   = sum(1 for d in driver_results  if d["Risk_Score"]   > 60)
critical_vehicles = sum(1 for v in vehicle_results if v["Maintenance_Flag"] in ["CRITICAL", "DUE"])
avg_risk        = sum(d["Risk_Score"]   for d in driver_results)  / len(driver_results)
avg_health      = sum(v["Health_Score"] for v in vehicle_results) / len(vehicle_results)

summary = {
    "total_drivers": len(driver_results),
    "total_vehicles": len(vehicle_results),
    "total_trips": len(trips_raw),
    "total_telemetry_rows": len(telemetry_raw),
    "risky_drivers": risky_drivers,
    "vehicles_needing_attention": critical_vehicles,
    "fleet_avg_risk_score": round(avg_risk, 1),
    "fleet_avg_health_score": round(avg_health, 1),
}

# ─── Hub-level aggregation ────────────────────────────────────────
hub_stats = defaultdict(lambda: {"risk_sum": 0, "count": 0, "risky": 0})
for d in driver_results:
    hub = d["Home_Hub"]
    hub_stats[hub]["risk_sum"] += d["Risk_Score"]
    hub_stats[hub]["count"] += 1
    if d["Risk_Score"] > 60:
        hub_stats[hub]["risky"] += 1

hubs = [
    {
        "hub": h,
        "avg_risk": round(s["risk_sum"] / s["count"], 1),
        "driver_count": s["count"],
        "risky_count": s["risky"]
    }
    for h, s in hub_stats.items()
]
hubs.sort(key=lambda x: x["avg_risk"], reverse=True)

# ─── Make + model stats ───────────────────────────────────────────
make_stats = defaultdict(lambda: {"health_sum": 0, "count": 0})
for v in vehicle_results:
    make_stats[v["Make"]]["health_sum"] += v["Health_Score"]
    make_stats[v["Make"]]["count"] += 1

makes = [
    {"make": m, "avg_health": round(s["health_sum"]/s["count"], 1), "count": s["count"]}
    for m, s in make_stats.items()
]
makes.sort(key=lambda x: x["avg_health"], reverse=True)

# ─── Speed distribution for chart ────────────────────────────────
speed_bins = [0]*7  # 0-10, 10-20, 20-30, 30-40, 40-50, 50-60, 60+
for r in telemetry_raw:
    s = float(r["Speed_kmph"])
    idx = min(int(s // 10), 6)
    speed_bins[idx] += 1

# ─── Write JSON ──────────────────────────────────────────────────
output = {
    "summary": summary,
    "drivers": driver_results,
    "vehicles": vehicle_results,
    "hubs": hubs,
    "makes": makes,
    "speed_distribution": {
        "labels": ["0-10","10-20","20-30","30-40","40-50","50-60","60+"],
        "values": speed_bins
    }
}

with open(OUT_PATH, "w") as f:
    json.dump(output, f, indent=2)

print(f"\nAnalytics JSON saved to: {OUT_PATH}")
print(f"\n=== FLEET SUMMARY ===")
for k, v in summary.items():
    print(f"  {k}: {v}")

print(f"\n=== TOP 5 RISKIEST DRIVERS ===")
for d in driver_results[:5]:
    print(f"  {d['Driver_ID']} {d['Driver_Name']}: Risk={d['Risk_Score']} "
          f"(speed={d['Speed_Score']:.1f} brake={d['Braking_Score']:.1f})")

print(f"\n=== BOTTOM 5 HEALTHIEST VEHICLES (needs attention) ===")
for v in vehicle_results[:5]:
    print(f"  {v['Vehicle_ID']} {v['Make']} {v['Model']}: Health={v['Health_Score']} "
          f"Flag={v['Maintenance_Flag']} ServiceDays={v['Days_Since_Service']}")
