"""
Corrected extraction of VexarDrive telemetry.
Pages 37-291: Trip_ID, Driver_ID, Vehicle_ID, Timestamp, Latitude, Longitude
Pages 292-546: Speed_kmph, Accel_X_g, Accel_Y_g, Accel_Z_g, Gyro_X_dps, Gyro_Y_dps, Gyro_Z_dps
Merge row-by-row to build complete telemetry CSV.
"""
import pypdf
import csv
import re
import os

PDF_PATH = "/Users/riturajbhattacharjee/.gemini/antigravity/scratch/vexar_dataset.pdf"
OUT_DIR  = "/Users/riturajbhattacharjee/.gemini/antigravity/scratch/vexar_data"
os.makedirs(OUT_DIR, exist_ok=True)

reader = pypdf.PdfReader(PDF_PATH)

# ────────────────────────────────────────────────────
# PART 1: Extract location rows from pages 37–291
# Format: T00001 D01 V01 2026-08-04 11:08:00 12.991693 77.559009
# ────────────────────────────────────────────────────
print("Extracting telemetry location data (pages 37-291)...")
loc_rows = []

loc_pattern = re.compile(
    r"(T\d{5})\s+(D\d+)\s+(V\d+)\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+([\d.]+)\s+([\d.]+)"
)

for pg_idx in range(36, 291):  # pages 37-291
    text = reader.pages[pg_idx].extract_text()
    if not text:
        continue
    for line in text.split("\n"):
        m = loc_pattern.search(line)
        if m:
            loc_rows.append({
                "Trip_ID": m.group(1),
                "Driver_ID": m.group(2),
                "Vehicle_ID": m.group(3),
                "Timestamp": m.group(4),
                "Latitude": float(m.group(5)),
                "Longitude": float(m.group(6)),
            })

print(f"  → {len(loc_rows)} location rows")

# ────────────────────────────────────────────────────
# PART 2: Extract sensor rows from pages 292–546
# Format: 22.1 0.07 -0.035 0.998 1.49 1.09 -1.33
# ────────────────────────────────────────────────────
print("Extracting sensor data (pages 292-546)...")
sensor_rows = []

sensor_pattern = re.compile(
    r"^(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)"
)

for pg_idx in range(291, 546):  # pages 292-546
    text = reader.pages[pg_idx].extract_text()
    if not text:
        continue
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        # Skip header lines
        if "Speed_kmph" in line or "Accel" in line or "Gyro" in line:
            continue
        m = sensor_pattern.match(line)
        if m:
            sensor_rows.append({
                "Speed_kmph": float(m.group(1)),
                "Accel_X_g": float(m.group(2)),
                "Accel_Y_g": float(m.group(3)),
                "Accel_Z_g": float(m.group(4)),
                "Gyro_X_dps": float(m.group(5)),
                "Gyro_Y_dps": float(m.group(6)),
                "Gyro_Z_dps": float(m.group(7)),
            })

print(f"  → {len(sensor_rows)} sensor rows")

# ────────────────────────────────────────────────────
# PART 3: Merge row-by-row
# ────────────────────────────────────────────────────
print("Merging...")
merged = []
n = min(len(loc_rows), len(sensor_rows))
for i in range(n):
    row = {}
    row.update(loc_rows[i])
    row.update(sensor_rows[i])
    merged.append(row)

print(f"  → {len(merged)} merged telemetry rows")

with open(f"{OUT_DIR}/telemetry.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Trip_ID","Driver_ID","Vehicle_ID","Timestamp","Latitude","Longitude",
        "Speed_kmph","Accel_X_g","Accel_Y_g","Accel_Z_g","Gyro_X_dps","Gyro_Y_dps","Gyro_Z_dps"
    ])
    writer.writeheader()
    writer.writerows(merged)

# Also re-extract trips with distance/speed from a better parse
print("\nRe-extracting trips with full columns...")

def get_pages_text(start, end):
    texts = []
    for i in range(start-1, end):
        t = reader.pages[i].extract_text()
        if t:
            texts.append(t)
    return "\n".join(texts)

trips_text_all = get_pages_text(10, 36)

# Main trip header: T00001 D01 V01 2026-08-04 11:08:00 11:24:00 16
trip_main = re.compile(
    r"(T\d{5})\s+(D\d+)\s+(V\d+)\s+(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(\d+)"
)

trip_dict = {}
for line in trips_text_all.split("\n"):
    m = trip_main.match(line.strip())
    if m:
        trip_dict[m.group(1)] = {
            "Trip_ID": m.group(1),
            "Driver_ID": m.group(2),
            "Vehicle_ID": m.group(3),
            "Trip_Date": m.group(4),
            "Start_Time": m.group(5),
            "End_Time": m.group(6),
            "Duration_Min": int(m.group(7)),
            "Distance_KM": "",
            "Avg_Speed_kmph": "",
            "Max_Speed_kmph": "",
        }

# Parse distance/speed columns - they appear after the main data block
# Look for: T-prefixed line with floats at end
dist_speed = re.compile(
    r"(T\d{5})\s+(D\d+)\s+(V\d+)\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s+\d{2}:\d{2}:\d{2}\s+\d+\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)"
)
for line in trips_text_all.split("\n"):
    m = dist_speed.match(line.strip())
    if m and m.group(1) in trip_dict:
        trip_dict[m.group(1)]["Distance_KM"] = float(m.group(4))
        trip_dict[m.group(1)]["Avg_Speed_kmph"] = float(m.group(5))
        trip_dict[m.group(1)]["Max_Speed_kmph"] = float(m.group(6))

trips = list(trip_dict.values())
trips.sort(key=lambda x: x["Trip_ID"])
print(f"  → {len(trips)} trips")

with open(f"{OUT_DIR}/trips.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Trip_ID","Driver_ID","Vehicle_ID","Trip_Date","Start_Time","End_Time",
        "Duration_Min","Distance_KM","Avg_Speed_kmph","Max_Speed_kmph"
    ])
    writer.writeheader()
    writer.writerows(trips)

print("Done! All CSVs saved to:", OUT_DIR)

# Print a quick summary sample
import csv as csv2

print("\n=== TELEMETRY SAMPLE (first 3 rows) ===")
with open(f"{OUT_DIR}/telemetry.csv") as f:
    for i, line in enumerate(f):
        if i < 4:
            print(line.strip())

print("\n=== TRIPS SAMPLE (first 3 rows) ===")
with open(f"{OUT_DIR}/trips.csv") as f:
    for i, line in enumerate(f):
        if i < 4:
            print(line.strip())
