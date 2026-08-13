"""
VexarDrive Dashboard — Rich Dark Theme with Clean & Spacious Layout.
"""
import json, os

DATA_PATH = "/Users/riturajbhattacharjee/.gemini/antigravity/scratch/vexar_data/analytics.json"
OUT_PATH  = "/Users/riturajbhattacharjee/.gemini/antigravity/scratch/vexardrive_dashboard.html"

with open(DATA_PATH) as f:
    data = json.load(f)

data_js = json.dumps(data)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>VexarDrive — Fleet Dashboards</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#0b0f19;--bg2:#111827;--card:#161e2e;--card-hover:#1c273a;
  --border:#1f293d;--border2:#2d3a52;
  --accent:#3b82f6;--accent2:#6366f1;
  --green:#10b981;--amber:#f59e0b;--red:#ef4444;
  --green-bg:rgba(16,185,129,0.12);--amber-bg:rgba(245,158,11,0.12);--red-bg:rgba(239,68,68,0.12);--blue-bg:rgba(59,130,246,0.12);
  --green-border:rgba(16,185,129,0.3);--amber-border:rgba(245,158,11,0.3);--red-border:rgba(239,68,68,0.3);--blue-border:rgba(59,130,246,0.3);
  --text:#f3f4f6;--text2:#9ca3af;--text3:#6b7280;
  --shadow:0 4px 20px rgba(0,0,0,0.3);
  --shadow-lg:0 10px 30px rgba(0,0,0,0.5);
}}
html{{height:100%;scroll-behavior:smooth}}
body{{
  font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);
  min-height:100vh;
}}

/* Header */
.header{{
  background:rgba(17,24,39,0.95);backdrop-filter:blur(16px);
  border-bottom:1px solid var(--border);
  padding:0 3rem;position:sticky;top:0;z-index:50;
}}
.header-inner{{
  max-width:1200px;margin:0 auto;display:flex;align-items:center;
  justify-content:space-between;height:68px;
}}
.logo{{display:flex;align-items:center;gap:12px;}}
.logo-icon{{
  width:36px;height:36px;background:linear-gradient(135deg,#3b82f6,#6366f1);
  border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:16px;
  box-shadow:0 0 15px rgba(59,130,246,0.4);
}}
.logo-text{{font-size:1.05rem;font-weight:800;color:var(--text);letter-spacing:-0.01em;}}
.logo-sub{{font-size:0.68rem;color:var(--text3);}}
.header-meta{{font-size:0.78rem;color:var(--text2);background:var(--bg);padding:6px 14px;border-radius:20px;border:1px solid var(--border);}}

/* Tabs */
.tabs{{
  background:var(--bg2);border-bottom:1px solid var(--border);
  padding:0 3rem;
}}
.tabs-inner{{
  max-width:1200px;margin:0 auto;display:flex;gap:8px;
}}
.tab{{
  padding:16px 24px;font-size:0.875rem;font-weight:600;color:var(--text2);
  cursor:pointer;border-bottom:3px solid transparent;transition:all 0.2s;
  background:none;border-top:none;border-left:none;border-right:none;
}}
.tab:hover{{color:var(--text);}}
.tab.active{{color:var(--accent);border-bottom-color:var(--accent);}}

/* Content */
.content{{max-width:1200px;margin:0 auto;padding:2.5rem 3rem 4rem;}}
.page{{display:none;}}
.page.active{{display:block;animation:fadeIn 0.25s ease;}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(4px);}}to{{opacity:1;transform:translateY(0);}}}}

/* Section titles */
.section-title{{
  font-size:1.35rem;font-weight:800;color:var(--text);
  margin-bottom:0.5rem;letter-spacing:-0.02em;
}}
.section-desc{{
  font-size:0.875rem;color:var(--text2);line-height:1.6;
  margin-bottom:2rem;max-width:720px;
}}

/* Methodology */
.method{{
  background:linear-gradient(135deg,rgba(59,130,246,0.08) 0%,rgba(17,24,39,0.4) 100%);
  border:1px solid var(--blue-border);
  border-radius:14px;padding:1.5rem 2rem;margin-bottom:2.5rem;
}}
.method.green-m{{
  background:linear-gradient(135deg,rgba(16,185,129,0.08) 0%,rgba(17,24,39,0.4) 100%);
  border-color:var(--green-border);
}}
.method-label{{
  font-size:0.75rem;font-weight:800;text-transform:uppercase;letter-spacing:0.08em;
  margin-bottom:1rem;display:flex;align-items:center;gap:8px;
}}
.method-label.blue{{color:var(--accent);}}
.method-label.green{{color:var(--green);}}
.method-list{{
  display:grid;grid-template-columns:1fr 1fr;gap:12px 36px;
  list-style:none;
}}
.method-list li{{
  font-size:0.83rem;color:var(--text2);line-height:1.5;
  padding-left:16px;position:relative;
}}
.method-list li::before{{
  content:'';position:absolute;left:0;top:7px;
  width:6px;height:6px;border-radius:50%;
}}
.method-list li.blue::before{{background:var(--accent);box-shadow:0 0 8px var(--accent);}}
.method-list li.green::before{{background:var(--green);box-shadow:0 0 8px var(--green);}}

/* KPI row */
.kpi-row{{
  display:grid;grid-template-columns:repeat(4,1fr);gap:1.25rem;
  margin-bottom:2.5rem;
}}
.kpi-card{{
  background:var(--card);border:1px solid var(--border);
  border-radius:14px;padding:1.5rem;box-shadow:var(--shadow);
  transition:transform 0.2s, border-color 0.2s;
}}
.kpi-card:hover{{transform:translateY(-2px);border-color:var(--border2);}}
.kpi-card-val{{font-size:2.2rem;font-weight:900;line-height:1;margin-bottom:6px;}}
.kpi-card-label{{font-size:0.72rem;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:0.06em;}}
.kpi-card-sub{{font-size:0.75rem;color:var(--text2);margin-top:6px;}}
.c-blue{{color:var(--accent);}} .c-green{{color:var(--green);}} .c-amber{{color:var(--amber);}} .c-red{{color:var(--red);}}

/* Search */
.search-bar{{
  display:flex;align-items:center;gap:14px;margin-bottom:2rem;
}}
.search-input{{
  flex:1;max-width:380px;
  background:var(--card);border:1px solid var(--border);border-radius:10px;
  padding:11px 18px;font-size:0.875rem;color:var(--text);outline:none;
  font-family:inherit;transition:all 0.2s;
}}
.search-input:focus{{border-color:var(--accent);box-shadow:0 0 0 3px rgba(59,130,246,0.15);}}
.search-input::placeholder{{color:var(--text3);}}
.sort-select{{
  background:var(--card);border:1px solid var(--border);border-radius:10px;
  padding:11px 16px;font-size:0.83rem;color:var(--text2);outline:none;cursor:pointer;
  font-family:inherit;
}}

/* Driver table */
.data-table-wrap{{
  background:var(--card);border:1px solid var(--border);border-radius:16px;
  overflow:hidden;box-shadow:var(--shadow);margin-bottom:2.5rem;
}}
table{{width:100%;border-collapse:collapse;}}
th{{
  background:var(--bg2);color:var(--text3);
  font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;
  padding:14px 20px;text-align:left;border-bottom:1px solid var(--border);
  white-space:nowrap;
}}
td{{
  padding:16px 20px;border-bottom:1px solid var(--border);
  font-size:0.875rem;color:var(--text2);white-space:nowrap;
}}
tr:last-child td{{border-bottom:none;}}
tr:hover td{{background:var(--card-hover);}}
.driver-name-cell{{display:flex;align-items:center;gap:14px;}}
.avatar{{
  width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;
  font-size:0.75rem;font-weight:800;flex-shrink:0;
}}
.driver-name{{font-weight:700;color:var(--text);}}
.driver-meta{{font-size:0.73rem;color:var(--text3);margin-top:1px;}}
.badge{{
  display:inline-flex;align-items:center;gap:4px;
  font-size:0.72rem;font-weight:700;padding:4px 12px;
  border-radius:20px;
}}
.badge-safe{{background:var(--green-bg);color:var(--green);border:1px solid var(--green-border);}}
.badge-mod{{background:var(--amber-bg);color:var(--amber);border:1px solid var(--amber-border);}}
.badge-risky{{background:var(--red-bg);color:var(--red);border:1px solid var(--red-border);}}
.badge-ok{{background:var(--green-bg);color:var(--green);border:1px solid var(--green-border);}}
.badge-monitor{{background:rgba(99,102,241,0.12);color:#a5b4fc;border:1px solid rgba(99,102,241,0.3);}}
.badge-due{{background:var(--amber-bg);color:var(--amber);border:1px solid var(--amber-border);}}
.badge-critical{{background:var(--red-bg);color:var(--red);border:1px solid var(--red-border);box-shadow:0 0 10px rgba(239,68,68,0.2);}}

/* Score bar */
.score-bar{{display:flex;align-items:center;gap:12px;}}
.score-bar-track{{
  width:90px;height:7px;background:rgba(255,255,255,0.06);border-radius:4px;overflow:hidden;
}}
.score-bar-fill{{height:100%;border-radius:4px;transition:width 0.6s ease;}}
.score-bar-val{{font-weight:800;font-size:0.95rem;min-width:34px;}}

/* Detail button */
.detail-btn{{
  background:var(--blue-bg);border:1px solid var(--blue-border);
  color:var(--accent);padding:7px 16px;border-radius:8px;cursor:pointer;
  font-size:0.78rem;font-weight:600;font-family:inherit;transition:all 0.2s;
}}
.detail-btn:hover{{background:var(--accent);color:white;border-color:var(--accent);box-shadow:0 0 12px rgba(59,130,246,0.4);}}

/* Charts */
.chart-row{{
  display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:2.5rem;
}}
.chart-card{{
  background:var(--card);border:1px solid var(--border);border-radius:16px;
  padding:1.75rem;box-shadow:var(--shadow);
}}
.chart-card.full{{grid-column:span 2;}}
.chart-title{{font-size:0.95rem;font-weight:700;color:var(--text);margin-bottom:4px;}}
.chart-sub{{font-size:0.78rem;color:var(--text2);margin-bottom:1.25rem;line-height:1.4;}}
canvas{{max-height:280px;}}

/* Detail modal */
.overlay{{
  display:none;position:fixed;inset:0;background:rgba(0,0,0,0.75);backdrop-filter:blur(8px);
  z-index:100;align-items:center;justify-content:center;
}}
.overlay.open{{display:flex;}}
.detail-modal{{
  background:var(--card);border:1px solid var(--border2);border-radius:20px;width:min(680px,92vw);
  max-height:85vh;overflow-y:auto;padding:2.5rem;box-shadow:var(--shadow-lg);
  position:relative;color:var(--text);
}}
.modal-close{{
  position:absolute;top:1.25rem;right:1.25rem;
  background:var(--bg2);border:1px solid var(--border);color:var(--text2);
  width:36px;height:36px;border-radius:10px;cursor:pointer;font-size:1rem;
  display:flex;align-items:center;justify-content:center;transition:all 0.2s;
}}
.modal-close:hover{{background:var(--card-hover);color:var(--text);}}
.modal-name{{font-size:1.3rem;font-weight:800;margin-bottom:4px;}}
.modal-sub{{font-size:0.83rem;color:var(--text2);margin-bottom:2rem;}}
.modal-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:2rem;}}
.modal-stat{{background:var(--bg);border:1px solid var(--border);border-radius:12px;padding:1rem;}}
.modal-stat-label{{font-size:0.68rem;color:var(--text3);font-weight:600;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:3px;}}
.modal-stat-val{{font-size:1.1rem;font-weight:800;color:var(--text);}}
.bar-section{{margin-top:1.5rem;}}
.bar-section-title{{font-size:0.75rem;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:1rem;}}
.bar-row{{margin-bottom:14px;}}
.bar-label{{display:flex;justify-content:space-between;font-size:0.83rem;color:var(--text2);margin-bottom:6px;font-weight:500;}}
.bar-track{{height:8px;background:rgba(255,255,255,0.06);border-radius:4px;overflow:hidden;}}
.bar-fill{{height:100%;border-radius:4px;transition:width 0.8s cubic-bezier(0.16,1,0.3,1);}}

/* Vehicle cards */
.veh-list{{margin-bottom:2.5rem;}}
.veh-item{{
  background:var(--card);border:1px solid var(--border);border-radius:16px;
  padding:1.5rem 2rem;margin-bottom:1rem;box-shadow:var(--shadow);
  display:grid;grid-template-columns:1.2fr 1fr 1fr 1fr auto;gap:1.5rem;align-items:center;
  transition:border-color 0.2s, transform 0.2s;
}}
.veh-item:hover{{transform:translateY(-2px);border-color:var(--border2);}}
.veh-item.critical-item{{border-left:4px solid var(--red);}}
.veh-item.due-item{{border-left:4px solid var(--amber);}}
.veh-item.monitor-item{{border-left:4px solid #6366f1;}}
.veh-item.ok-item{{border-left:4px solid var(--green);}}
.vi-id{{font-size:0.75rem;color:var(--text3);font-family:'JetBrains Mono',monospace;}}
.vi-name{{font-size:1rem;font-weight:700;color:var(--text);}}
.vi-model{{font-size:0.8rem;color:var(--text2);}}
.vi-stat-val{{font-size:1.15rem;font-weight:800;color:var(--text);}}
.vi-stat-label{{font-size:0.7rem;color:var(--text3);font-weight:500;}}

/* Assumptions */
.assume-table{{
  width:100%;border-collapse:collapse;
  background:var(--card);border:1px solid var(--border);border-radius:16px;
  overflow:hidden;box-shadow:var(--shadow);margin-bottom:2.5rem;
}}
.assume-table th{{
  background:var(--bg2);font-size:0.72rem;font-weight:700;color:var(--text3);
  text-transform:uppercase;letter-spacing:0.06em;
  padding:14px 20px;text-align:left;border-bottom:1px solid var(--border);
}}
.assume-table td{{
  padding:14px 20px;font-size:0.85rem;color:var(--text2);
  border-bottom:1px solid var(--border);line-height:1.5;
}}
.assume-table tr:last-child td{{border-bottom:none;}}
.assume-table tr:hover td{{background:var(--card-hover);}}

/* Uses */
.uses-list{{display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;}}
.use-card{{
  background:var(--card);border:1px solid var(--border);border-radius:16px;
  padding:1.5rem 1.75rem;box-shadow:var(--shadow);transition:all 0.2s;
}}
.use-card:hover{{border-color:var(--border2);transform:translateY(-2px);}}
.use-icon{{font-size:1.6rem;margin-bottom:10px;}}
.use-title{{font-size:0.95rem;font-weight:700;color:var(--text);margin-bottom:6px;}}
.use-desc{{font-size:0.83rem;color:var(--text2);line-height:1.6;}}

/* Responsive */
@media(max-width:900px){{
  .header,.tabs,.content{{padding-left:1.5rem;padding-right:1.5rem;}}
  .kpi-row{{grid-template-columns:1fr 1fr;}}
  .chart-row{{grid-template-columns:1fr;}}
  .chart-card.full{{grid-column:span 1;}}
  .method-list{{grid-template-columns:1fr;}}
  .veh-item{{grid-template-columns:1fr 1fr;}}
  .uses-list{{grid-template-columns:1fr;}}
  .modal-grid{{grid-template-columns:1fr 1fr;}}
}}
@media(max-width:600px){{
  .kpi-row{{grid-template-columns:1fr;}}
  .veh-item{{grid-template-columns:1fr;}}
}}
</style>
</head>
<body>

<header class="header">
  <div class="header-inner">
    <div class="logo">
      <div class="logo-icon">🚀</div>
      <div>
        <div class="logo-text">VexarDrive Fleet Dashboards</div>
        <div class="logo-sub">Fleet Analytics & Intelligence</div>
      </div>
    </div>
    <div class="header-meta">Aug 2026 · Week 1 · 30 Drivers · 30 Vehicles · Bengaluru</div>
  </div>
</header>

<div class="tabs">
  <div class="tabs-inner">
    <button class="tab active" id="tab-drivers" onclick="goTo('drivers')">Driver Behaviour</button>
    <button class="tab" id="tab-vehicles" onclick="goTo('vehicles')">Vehicle Health</button>
    <button class="tab" id="tab-notes" onclick="goTo('notes')">Assumptions & Other Uses</button>
  </div>
</div>

<div class="content">

<!-- ═══════ DRIVER BEHAVIOUR ═══════ -->
<div class="page active" id="page-drivers">

  <h1 class="section-title">Driver Behaviour Dashboard</h1>
  <p class="section-desc">Identifies and scores risky vs. safe driving patterns for each of the 30 drivers, using IMU sensor data (accelerometer + gyroscope) and GPS speed readings.</p>

  <div class="method">
    <div class="method-label blue">📐 Scoring Methodology — Risk Score (0 = safest, 100 = riskiest)</div>
    <ul class="method-list">
      <li class="blue"><strong>Speed Violations (30%)</strong> — % of minutes exceeding 60 km/h, the Karnataka urban two-wheeler limit</li>
      <li class="blue"><strong>Hard Braking (25%)</strong> — % of minutes with Accel_X &lt; −0.3g (industry deceleration threshold)</li>
      <li class="blue"><strong>Sharp Turns (20%)</strong> — % of minutes with |Accel_Y| &gt; 0.3g (aggressive lateral force)</li>
      <li class="blue"><strong>Yaw Spikes (15%)</strong> — % of minutes with |Gyro_Z| &gt; 10 dps (abrupt steering rotation)</li>
      <li class="blue"><strong>Night Driving (10%)</strong> — % of trips starting between 21:00–05:59 (low-visibility window)</li>
      <li class="blue"><strong>Experience Bonus</strong> — Up to −10 pts for 14+ years license experience</li>
    </ul>
  </div>

  <div class="kpi-row" id="driverKPIs"></div>

  <div class="search-bar">
    <input class="search-input" id="driverSearch" placeholder="Search by name, ID, or hub…" oninput="filterDrivers()"/>
    <select class="sort-select" id="driverSort" onchange="filterDrivers()">
      <option value="risk-desc">Risk: High → Low</option>
      <option value="risk-asc">Risk: Low → High</option>
      <option value="name">Name A–Z</option>
      <option value="speed">Max Speed ↓</option>
    </select>
  </div>

  <div class="data-table-wrap">
    <table>
      <thead><tr>
        <th>#</th><th>Driver</th><th>Hub</th><th>Exp</th>
        <th>Risk Score</th><th>Speed Viol%</th><th>Hard Brake%</th>
        <th>Max Speed</th><th>Rating</th><th></th>
      </tr></thead>
      <tbody id="driverTableBody"></tbody>
    </table>
  </div>

  <div class="chart-row">
    <div class="chart-card full">
      <div class="chart-title">Risk Score — All 30 Drivers</div>
      <div class="chart-sub">Ranked from highest to lowest risk. Green = safe, amber = moderate, red = high risk.</div>
      <canvas id="c-allrisk"></canvas>
    </div>
    <div class="chart-card">
      <div class="chart-title">Risk Component Breakdown — Top 10</div>
      <div class="chart-sub">Stacked weighted contribution of each factor.</div>
      <canvas id="c-riskcomp"></canvas>
    </div>
    <div class="chart-card">
      <div class="chart-title">Experience vs Risk Score</div>
      <div class="chart-sub">Does more license experience correlate with safer driving?</div>
      <canvas id="c-expvsr"></canvas>
    </div>
  </div>
</div>

<!-- ═══════ VEHICLE HEALTH ═══════ -->
<div class="page" id="page-vehicles">

  <h1 class="section-title">Vehicle Health Status Dashboard</h1>
  <p class="section-desc">Identifies vehicles showing signs of mechanical wear or irregular sensor signatures that may need maintenance, using vibration, gyro stability, service records, and mileage.</p>

  <div class="method green-m">
    <div class="method-label green">📐 Scoring Methodology — Health Score (0 = critical, 100 = excellent)</div>
    <ul class="method-list">
      <li class="green"><strong>Vibration (25%)</strong> — Std dev of Accel_Z from 1g; higher = rougher ride / worn suspension</li>
      <li class="green"><strong>Service Overdue (25%)</strong> — Days since last service; &gt;30d = penalty, &gt;90d = critical</li>
      <li class="green"><strong>Gyro Instability (15%)</strong> — Mean gyro vector magnitude; persistent rotation = frame/wheel anomaly</li>
      <li class="green"><strong>Odometer (15%)</strong> — Normalized km vs fleet max; higher = more cumulative wear</li>
      <li class="green"><strong>Vehicle Age (10%)</strong> — Older manufacture year = higher baseline wear</li>
      <li class="green"><strong>Harsh Events (10%)</strong> — % of minutes with multi-axis IMU spikes on this vehicle</li>
    </ul>
  </div>

  <div class="kpi-row" id="vehicleKPIs"></div>

  <div class="search-bar">
    <input class="search-input" id="vehicleSearch" placeholder="Search by ID, make, or model…" oninput="filterVehicles()"/>
  </div>

  <div class="veh-list" id="vehList"></div>

  <div class="chart-row">
    <div class="chart-card">
      <div class="chart-title">Days Since Last Service</div>
      <div class="chart-sub">Red = &gt;90 days (critical), amber = &gt;60 days (due), green = on schedule.</div>
      <canvas id="c-service"></canvas>
    </div>
    <div class="chart-card">
      <div class="chart-title">Vibration Level (Accel_Z Std Dev)</div>
      <div class="chart-sub">Higher deviation from 1g = more mechanical roughness.</div>
      <canvas id="c-vib"></canvas>
    </div>
    <div class="chart-card">
      <div class="chart-title">Odometer vs Health Score</div>
      <div class="chart-sub">Does higher mileage predict lower vehicle health?</div>
      <canvas id="c-odohealth"></canvas>
    </div>
    <div class="chart-card">
      <div class="chart-title">Average Health by Manufacturer</div>
      <div class="chart-sub">Which makes hold up best in fleet operations?</div>
      <canvas id="c-makehealth"></canvas>
    </div>
  </div>
</div>

<!-- ═══════ ASSUMPTIONS & OTHER USES ═══════ -->
<div class="page" id="page-notes">

  <h1 class="section-title">Assumptions</h1>
  <p class="section-desc">All explicit assumptions used in the scoring models, with justifications.</p>

  <table class="assume-table">
    <thead><tr><th>Parameter</th><th>Value</th><th>Rationale</th></tr></thead>
    <tbody>
      <tr><td>Speed limit</td><td>60 km/h</td><td>Karnataka Motor Vehicles Rules — urban two-wheeler limit in Bengaluru</td></tr>
      <tr><td>Hard braking</td><td>Accel_X &lt; −0.3g</td><td>Industry-standard telematics harsh deceleration threshold</td></tr>
      <tr><td>Sharp turn</td><td>|Accel_Y| &gt; 0.3g</td><td>Lateral g-force indicating aggressive cornering or lane change</td></tr>
      <tr><td>Yaw spike</td><td>|Gyro_Z| &gt; 10 dps</td><td>Sudden yaw rotation threshold for abrupt steering input</td></tr>
      <tr><td>Normal vibration</td><td>Accel_Z ≈ 1g</td><td>Gravity baseline; std dev from 1g measures mechanical vibration</td></tr>
      <tr><td>Service interval</td><td>60 days</td><td>Standard for delivery two-wheelers in Indian fleet operations</td></tr>
      <tr><td>Night hours</td><td>21:00–05:59</td><td>Post-sunset / pre-sunrise increased collision risk window</td></tr>
      <tr><td>IMU orientation</td><td>Consistent per driver</td><td>Phone mount assumed fixed; axis directions consistent across trips</td></tr>
      <tr><td>Telemetry interval</td><td>1 row = 1 minute</td><td>Per dataset specification; used for event rate calculations</td></tr>
    </tbody>
  </table>

  <h1 class="section-title" style="margin-top:3rem;">Other Proposed Uses for This Dataset</h1>
  <p class="section-desc">Beyond the two dashboards, this dataset can power several additional analytics products.</p>

  <div class="uses-list">
    <div class="use-card"><div class="use-icon">📦</div><div class="use-title">ETA Prediction</div><div class="use-desc">Per-minute GPS + speed data can train ML models to predict delivery arrival times based on real traffic patterns per hub and time-of-day.</div></div>
    <div class="use-card"><div class="use-icon">🛣️</div><div class="use-title">Route Optimisation</div><div class="use-desc">Lat/lon traces reveal actual routes vs optimal paths. Clustering trips can surface high-congestion zones per time window.</div></div>
    <div class="use-card"><div class="use-icon">💰</div><div class="use-title">Fuel / Battery Cost Modelling</div><div class="use-desc">Speed profiles + distance enable per-trip fuel estimates. Identify high-cost drivers or inefficient routes.</div></div>
    <div class="use-card"><div class="use-icon">🧠</div><div class="use-title">Targeted Safety Training</div><div class="use-desc">Cluster drivers by behavioural signature (braking vs speeding vs yaw) to personalise training interventions.</div></div>
    <div class="use-card"><div class="use-icon">🔮</div><div class="use-title">Predictive Maintenance ML</div><div class="use-desc">IMU signatures can train anomaly-detection models to flag vehicles for service before breakdown occurs.</div></div>
    <div class="use-card"><div class="use-icon">📜</div><div class="use-title">Insurance Telematics (UBI)</div><div class="use-desc">Risk scores from actual driving data are ideal for usage-based insurance pricing, replacing age-based proxies.</div></div>
  </div>
</div>

</div><!-- end content -->

<!-- DETAIL MODAL -->
<div class="overlay" id="overlay" onclick="if(event.target===this)closeModal()">
  <div class="detail-modal">
    <button class="modal-close" onclick="closeModal()">✕</button>
    <div class="modal-name" id="m-name">—</div>
    <div class="modal-sub" id="m-sub">—</div>
    <canvas id="m-radar" style="max-height:260px;margin-bottom:1.5rem;"></canvas>
    <div class="modal-grid" id="m-stats"></div>
    <div class="bar-section">
      <div class="bar-section-title">Risk Factor Scores (each 0–100)</div>
      <div class="bar-row"><div class="bar-label"><span>Speed Violations</span><span id="b-speed">—</span></div><div class="bar-track"><div class="bar-fill" id="bf-speed" style="background:var(--red);"></div></div></div>
      <div class="bar-row"><div class="bar-label"><span>Hard Braking</span><span id="b-brake">—</span></div><div class="bar-track"><div class="bar-fill" id="bf-brake" style="background:var(--amber);"></div></div></div>
      <div class="bar-row"><div class="bar-label"><span>Sharp Turns</span><span id="b-turn">—</span></div><div class="bar-track"><div class="bar-fill" id="bf-turn" style="background:#8b5cf6;"></div></div></div>
      <div class="bar-row"><div class="bar-label"><span>Yaw Spikes</span><span id="b-yaw">—</span></div><div class="bar-track"><div class="bar-fill" id="bf-yaw" style="background:var(--accent);"></div></div></div>
      <div class="bar-row"><div class="bar-label"><span>Night Driving</span><span id="b-night">—</span></div><div class="bar-track"><div class="bar-fill" id="bf-night" style="background:#6366f1;"></div></div></div>
    </div>
  </div>
</div>

<script>
const DATA = {data_js};
const drivers = DATA.drivers;
const vehicles = DATA.vehicles;

/* Nav */
function goTo(name) {{
  document.querySelectorAll('.page').forEach(function(p) {{ p.classList.remove('active'); }});
  document.querySelectorAll('.tab').forEach(function(t) {{ t.classList.remove('active'); }});
  document.getElementById('page-' + name).classList.add('active');
  document.getElementById('tab-' + name).classList.add('active');
  window.scrollTo(0, 0);
}}

/* Chart.js */
Chart.defaults.color = '#9ca3af';
Chart.defaults.borderColor = '#1f293d';
Chart.defaults.font.family = 'Inter';
var BL = '#3b82f6', GR = '#10b981', AM = '#f59e0b', RD = '#ef4444';
var BLA = 'rgba(59,130,246,0.15)', GRA = 'rgba(16,185,129,0.15)', AMA = 'rgba(245,158,11,0.15)', RDA = 'rgba(239,68,68,0.15)';

function mkC(id, type, labels, datasets, opts) {{
  opts = opts || {{}};
  var el = document.getElementById(id);
  if (!el) return null;
  return new Chart(el, {{
    type: type, data: {{labels: labels, datasets: datasets}},
    options: {{
      responsive: true, maintainAspectRatio: true,
      plugins: Object.assign({{
        legend: {{labels: {{font: {{size: 11}}, boxWidth: 12, padding: 12}}}},
        tooltip: {{backgroundColor: '#111827', borderColor: '#2d3a52', borderWidth: 1, titleFont: {{size: 11}}, bodyFont: {{size: 10}}, padding: 10, cornerRadius: 8}}
      }}, opts.plugins || {{}}),
      scales: opts.scales || {{
        x: {{grid: {{color: '#1f293d'}}, ticks: {{font: {{size: 10}}}}}},
        y: {{grid: {{color: '#1f293d'}}, ticks: {{font: {{size: 10}}}}}}
      }}
    }}
  }});
}}

function riskColor(s) {{ return s > 20 ? RD : s > 10 ? AM : GR; }}
function riskBadge(s) {{
  if (s > 20) return '<span class="badge badge-risky">⚠️ High Risk</span>';
  if (s > 10) return '<span class="badge badge-mod">🟡 Moderate</span>';
  return '<span class="badge badge-safe">✅ Safe</span>';
}}
function healthColor(s) {{ return s >= 60 ? GR : s >= 40 ? AM : RD; }}

/* ═══ DRIVERS ═══ */
var sortedD = drivers.slice().sort(function(a,b) {{ return b.Risk_Score - a.Risk_Score; }});
var safest = sortedD[sortedD.length - 1];
var riskiest = sortedD[0];
var avgRisk = (drivers.reduce(function(s,d) {{ return s + d.Risk_Score; }}, 0) / drivers.length).toFixed(1);
var avgMaxSpd = (drivers.reduce(function(s,d) {{ return s + d.Max_Speed_kmph; }}, 0) / drivers.length).toFixed(1);

document.getElementById('driverKPIs').innerHTML =
  '<div class="kpi-card"><div class="kpi-card-val c-red">' + riskiest.Risk_Score + '</div><div class="kpi-card-label">Highest Risk</div><div class="kpi-card-sub">' + riskiest.Driver_Name + ' (' + riskiest.Driver_ID + ')</div></div>' +
  '<div class="kpi-card"><div class="kpi-card-val c-green">' + safest.Risk_Score + '</div><div class="kpi-card-label">Lowest Risk</div><div class="kpi-card-sub">' + safest.Driver_Name + ' (' + safest.Driver_ID + ')</div></div>' +
  '<div class="kpi-card"><div class="kpi-card-val c-amber">' + avgRisk + '</div><div class="kpi-card-label">Fleet Avg Risk</div><div class="kpi-card-sub">Across all 30 drivers</div></div>' +
  '<div class="kpi-card"><div class="kpi-card-val c-blue">' + avgMaxSpd + '</div><div class="kpi-card-label">Avg Max Speed</div><div class="kpi-card-sub">km/h across fleet</div></div>';

var avatarColors = ['#3b82f6','#8b5cf6','#06b6d4','#10b981','#f59e0b','#ef4444','#ec4899','#14b8a6'];
function ac(did) {{ return avatarColors[parseInt(did.slice(1)) % avatarColors.length]; }}

function buildDriverTable(list) {{
  document.getElementById('driverTableBody').innerHTML = list.map(function(d, i) {{
    var rc = riskColor(d.Risk_Score);
    var col = ac(d.Driver_ID);
    var initials = d.Driver_Name.split(' ').map(function(w) {{ return w[0]; }}).join('').slice(0,2);
    return '<tr>' +
      '<td style="color:var(--text3);font-weight:700;">' + (i+1) + '</td>' +
      '<td><div class="driver-name-cell"><div class="avatar" style="background:' + col + '22;color:' + col + '">' + initials + '</div><div><div class="driver-name">' + d.Driver_Name + '</div><div class="driver-meta">' + d.Driver_ID + ' · ' + d.Gender + ' · Age ' + d.Age + '</div></div></div></td>' +
      '<td>' + d.Home_Hub + '</td>' +
      '<td>' + d.Experience_Years + ' yr</td>' +
      '<td><div class="score-bar"><span class="score-bar-val" style="color:' + rc + '">' + d.Risk_Score + '</span><div class="score-bar-track"><div class="score-bar-fill" style="width:' + (d.Risk_Score/30*100) + '%;background:' + rc + '"></div></div></div></td>' +
      '<td>' + d.Speed_Violation_Pct + '%</td>' +
      '<td>' + d.Hard_Brake_Pct + '%</td>' +
      '<td style="font-weight:700;color:var(--accent);">' + d.Max_Speed_kmph + '</td>' +
      '<td>' + riskBadge(d.Risk_Score) + '</td>' +
      '<td><button class="detail-btn" onclick="openModal(\\\'' + d.Driver_ID + '\\\')">Details</button></td>' +
      '</tr>';
  }}).join('');
}}

function filterDrivers() {{
  var q = document.getElementById('driverSearch').value.toLowerCase();
  var sort = document.getElementById('driverSort').value;
  var list = drivers.slice();
  if (q) list = list.filter(function(d) {{ return d.Driver_Name.toLowerCase().indexOf(q) >= 0 || d.Driver_ID.toLowerCase().indexOf(q) >= 0 || d.Home_Hub.toLowerCase().indexOf(q) >= 0; }});
  if (sort === 'risk-desc') list.sort(function(a,b) {{ return b.Risk_Score - a.Risk_Score; }});
  if (sort === 'risk-asc')  list.sort(function(a,b) {{ return a.Risk_Score - b.Risk_Score; }});
  if (sort === 'name')      list.sort(function(a,b) {{ return a.Driver_Name.localeCompare(b.Driver_Name); }});
  if (sort === 'speed')     list.sort(function(a,b) {{ return b.Max_Speed_kmph - a.Max_Speed_kmph; }});
  buildDriverTable(list);
}}
filterDrivers();

/* Charts */
mkC('c-allrisk', 'bar',
  sortedD.map(function(d) {{ return d.Driver_ID; }}),
  [{{label: 'Risk Score', data: sortedD.map(function(d) {{ return d.Risk_Score; }}),
    backgroundColor: sortedD.map(function(d) {{ var c = riskColor(d.Risk_Score); return c === RD ? RDA : c === AM ? AMA : GRA; }}),
    borderColor: sortedD.map(function(d) {{ return riskColor(d.Risk_Score); }}),
    borderWidth: 2, borderRadius: 6, borderSkipped: false}}],
  {{plugins: {{legend: {{display: false}}}},
    scales: {{x: {{grid: {{display: false}}, ticks: {{font: {{size: 9}}, maxRotation: 45}}}}, y: {{min: 0, max: 30}}}}}}
);

var top10 = sortedD.slice(0, 10);
mkC('c-riskcomp', 'bar', top10.map(function(d) {{ return d.Driver_ID; }}), [
  {{label: 'Speed (30%)',   data: top10.map(function(d) {{ return +(d.Speed_Score * 0.30).toFixed(1); }}), backgroundColor: 'rgba(239,68,68,0.75)', borderRadius: 3}},
  {{label: 'Braking (25%)', data: top10.map(function(d) {{ return +(d.Braking_Score * 0.25).toFixed(1); }}), backgroundColor: 'rgba(245,158,11,0.75)', borderRadius: 3}},
  {{label: 'Lateral (20%)', data: top10.map(function(d) {{ return +(d.Lateral_Score * 0.20).toFixed(1); }}), backgroundColor: 'rgba(139,92,246,0.75)', borderRadius: 3}},
  {{label: 'Yaw (15%)',     data: top10.map(function(d) {{ return +(d.Yaw_Score * 0.15).toFixed(1); }}), backgroundColor: 'rgba(59,130,246,0.75)', borderRadius: 3}},
  {{label: 'Night (10%)',   data: top10.map(function(d) {{ return +(d.Night_Score * 0.10).toFixed(1); }}), backgroundColor: 'rgba(99,102,241,0.75)', borderRadius: 3}},
], {{scales: {{x: {{stacked: true, grid: {{display: false}}}}, y: {{stacked: true, min: 0}}}}}});

mkC('c-expvsr', 'scatter', null, [{{
  label: 'Driver', data: drivers.map(function(d) {{ return {{x: d.Experience_Years, y: d.Risk_Score}}; }}),
  backgroundColor: drivers.map(function(d) {{ return riskColor(d.Risk_Score) + '44'; }}),
  borderColor: drivers.map(function(d) {{ return riskColor(d.Risk_Score); }}),
  borderWidth: 2, pointRadius: 8
}}], {{scales: {{
  x: {{title: {{display: true, text: 'License Experience (years)'}}, min: 0, grid: {{display: false}}}},
  y: {{title: {{display: true, text: 'Risk Score'}}, min: 0}}
}}}});

/* Modal */
var radarInst = null;
function openModal(did) {{
  var d = drivers.find(function(x) {{ return x.Driver_ID === did; }});
  if (!d) return;
  document.getElementById('m-name').textContent = d.Driver_Name;
  document.getElementById('m-sub').textContent = d.Driver_ID + ' · ' + d.Home_Hub + ' · ' + d.Experience_Years + ' yr experience · ' + d.Total_Trips + ' trips · ' + d.Total_Minutes + ' minutes tracked';
  var stats = [
    ['Risk Score', d.Risk_Score + ' / 100'], ['Max Speed', d.Max_Speed_kmph + ' km/h'], ['Avg Speed', d.Avg_Speed_kmph + ' km/h'],
    ['Hard Brakes', d.Hard_Brakes + ' events (' + d.Hard_Brake_Pct + '%)'], ['Sharp Turns', d.Sharp_Turns + ' events (' + d.Sharp_Turn_Pct + '%)'],
    ['Yaw Spikes', d.Yaw_Spikes + ' events (' + d.Yaw_Spike_Pct + '%)'],
    ['Night Trips', d.Night_Trips + ' of ' + d.Total_Trips], ['Speed Violations', d.Speed_Violations + ' mins (' + d.Speed_Violation_Pct + '%)'],
    ['Vehicle', d.Primary_Vehicle_ID],
  ];
  document.getElementById('m-stats').innerHTML = stats.map(function(s) {{ return '<div class="modal-stat"><div class="modal-stat-label">' + s[0] + '</div><div class="modal-stat-val">' + s[1] + '</div></div>'; }}).join('');
  var bars = [['bf-speed','b-speed',d.Speed_Score],['bf-brake','b-brake',d.Braking_Score],['bf-turn','b-turn',d.Lateral_Score],['bf-yaw','b-yaw',d.Yaw_Score],['bf-night','b-night',d.Night_Score]];
  bars.forEach(function(b) {{ document.getElementById(b[0]).style.width = b[2] + '%'; document.getElementById(b[1]).textContent = b[2].toFixed(1); }});
  if (radarInst) radarInst.destroy();
  radarInst = new Chart(document.getElementById('m-radar'), {{
    type: 'radar', data: {{labels: ['Speed','Braking','Lateral','Yaw','Night'],
    datasets: [{{label: d.Driver_Name, data: [d.Speed_Score, d.Braking_Score, d.Lateral_Score, d.Yaw_Score, d.Night_Score],
      backgroundColor: 'rgba(59,130,246,0.15)', borderColor: BL, borderWidth: 2, pointBackgroundColor: BL, pointRadius: 4}}]}},
    options: {{responsive: true, maintainAspectRatio: true,
      scales: {{r: {{min: 0, max: 100, grid: {{color: '#1f293d'}}, ticks: {{color: '#6b7280', font: {{size: 9}}, backdropColor: 'transparent'}}, pointLabels: {{color: '#9ca3af', font: {{size: 11, weight: '600'}}}}}}}},
      plugins: {{legend: {{display: false}}}}}}
  }});
  document.getElementById('overlay').classList.add('open');
}}
function closeModal() {{ document.getElementById('overlay').classList.remove('open'); }}

/* ═══ VEHICLES ═══ */
var sortedV = vehicles.slice().sort(function(a,b) {{ return a.Health_Score - b.Health_Score; }});
var bestV = sortedV[sortedV.length - 1];
var worstV = sortedV[0];
var maintCount = vehicles.filter(function(v) {{ return v.Maintenance_Flag === 'CRITICAL' || v.Maintenance_Flag === 'DUE'; }}).length;
var avgHealth = (vehicles.reduce(function(s,v) {{ return s + v.Health_Score; }}, 0) / vehicles.length).toFixed(1);

document.getElementById('vehicleKPIs').innerHTML =
  '<div class="kpi-card"><div class="kpi-card-val c-red">' + worstV.Health_Score + '</div><div class="kpi-card-label">Needs Most Attention</div><div class="kpi-card-sub">' + worstV.Vehicle_ID + ' ' + worstV.Make + ' ' + worstV.Model + '</div></div>' +
  '<div class="kpi-card"><div class="kpi-card-val c-green">' + bestV.Health_Score + '</div><div class="kpi-card-label">Healthiest Vehicle</div><div class="kpi-card-sub">' + bestV.Vehicle_ID + ' ' + bestV.Make + ' ' + bestV.Model + '</div></div>' +
  '<div class="kpi-card"><div class="kpi-card-val c-amber">' + maintCount + '</div><div class="kpi-card-label">Due / Critical</div><div class="kpi-card-sub">Vehicles needing service</div></div>' +
  '<div class="kpi-card"><div class="kpi-card-val c-blue">' + avgHealth + '</div><div class="kpi-card-label">Fleet Avg Health</div><div class="kpi-card-sub">Out of 100</div></div>';

function flagBadge(f) {{
  var cls = {{OK:'badge-ok',MONITOR:'badge-monitor',DUE:'badge-due',CRITICAL:'badge-critical'}}[f];
  var em = {{OK:'✅',MONITOR:'👁️',DUE:'⚠️',CRITICAL:'🔴'}}[f];
  return '<span class="badge ' + cls + '">' + em + ' ' + f + '</span>';
}}

function buildVehList(list) {{
  document.getElementById('vehList').innerHTML = list.map(function(v) {{
    var hc = healthColor(v.Health_Score);
    var cls = v.Maintenance_Flag.toLowerCase() + '-item';
    return '<div class="veh-item ' + cls + '">' +
      '<div class="vi-primary"><div class="vi-id">' + v.Vehicle_ID + '</div><div class="vi-name">' + v.Make + ' ' + v.Model + '</div><div class="vi-model">' + v.Manufacture_Year + ' · ' + v.Odometer_KM.toLocaleString() + ' km</div></div>' +
      '<div><div class="vi-stat-val" style="color:' + hc + '">' + v.Health_Score + '<span style="font-size:0.65rem;color:var(--text3);font-weight:500;"> /100</span></div><div class="vi-stat-label">Health Score</div></div>' +
      '<div><div class="vi-stat-val" style="color:' + (v.Days_Since_Service > 90 ? RD : v.Days_Since_Service > 60 ? AM : GR) + '">' + v.Days_Since_Service + 'd</div><div class="vi-stat-label">Since Service</div></div>' +
      '<div><div class="vi-stat-val">' + v.Vibration_Std + '</div><div class="vi-stat-label">Vibration σ</div></div>' +
      '<div>' + flagBadge(v.Maintenance_Flag) + '</div>' +
      '</div>';
  }}).join('');
}}

function filterVehicles() {{
  var q = document.getElementById('vehicleSearch').value.toLowerCase();
  var list = vehicles.slice();
  if (q) list = list.filter(function(v) {{ return v.Vehicle_ID.toLowerCase().indexOf(q) >= 0 || v.Make.toLowerCase().indexOf(q) >= 0 || v.Model.toLowerCase().indexOf(q) >= 0; }});
  list.sort(function(a,b) {{ return a.Health_Score - b.Health_Score; }});
  buildVehList(list);
}}
filterVehicles();

/* Vehicle charts */
var svc = vehicles.slice().sort(function(a,b) {{ return b.Days_Since_Service - a.Days_Since_Service; }});
mkC('c-service', 'bar', svc.map(function(v){{return v.Vehicle_ID;}}), [{{
  label:'Days', data:svc.map(function(v){{return v.Days_Since_Service;}}),
  backgroundColor: svc.map(function(v){{return v.Days_Since_Service>90?RDA:v.Days_Since_Service>60?AMA:GRA;}}),
  borderColor: svc.map(function(v){{return v.Days_Since_Service>90?RD:v.Days_Since_Service>60?AM:GR;}}),
  borderWidth:2, borderRadius:6, borderSkipped:false
}}], {{plugins:{{legend:{{display:false}}}}, scales:{{x:{{grid:{{display:false}}}}, y:{{title:{{display:true,text:'Days'}}}}}}}});

var vib = vehicles.slice().sort(function(a,b){{return b.Vibration_Std-a.Vibration_Std;}});
mkC('c-vib', 'bar', vib.map(function(v){{return v.Vehicle_ID;}}), [{{
  label:'Std Dev', data:vib.map(function(v){{return v.Vibration_Std;}}),
  backgroundColor: vib.map(function(v){{return v.Vibration_Std>0.06?RDA:v.Vibration_Std>0.04?AMA:GRA;}}),
  borderColor: vib.map(function(v){{return v.Vibration_Std>0.06?RD:v.Vibration_Std>0.04?AM:GR;}}),
  borderWidth:2, borderRadius:6, borderSkipped:false
}}], {{plugins:{{legend:{{display:false}}}}, scales:{{x:{{grid:{{display:false}}}}, y:{{title:{{display:true,text:'σ (g)'}}}}}}}});

mkC('c-odohealth', 'scatter', null, [{{
  label:'Vehicle', data:vehicles.map(function(v){{return{{x:v.Odometer_KM,y:v.Health_Score}};}}),
  backgroundColor: vehicles.map(function(v){{return healthColor(v.Health_Score)+'44';}}),
  borderColor: vehicles.map(function(v){{return healthColor(v.Health_Score);}}),
  borderWidth:2, pointRadius:8
}}], {{scales:{{x:{{title:{{display:true,text:'Odometer (km)'}},grid:{{display:false}}}}, y:{{title:{{display:true,text:'Health Score'}},min:0,max:100}}}}}});

mkC('c-makehealth', 'bar',
  DATA.makes.map(function(m){{return m.make;}}),
  [{{label:'Avg Health', data:DATA.makes.map(function(m){{return m.avg_health;}}),
    backgroundColor: DATA.makes.map(function(m){{return m.avg_health>60?GRA:m.avg_health>45?AMA:RDA;}}),
    borderColor: DATA.makes.map(function(m){{return m.avg_health>60?GR:m.avg_health>45?AM:RD;}}),
    borderWidth:2, borderRadius:6, borderSkipped:false}}],
  {{plugins:{{legend:{{display:false}}}}, scales:{{x:{{grid:{{display:false}}}}, y:{{min:0,max:100}}}}}});
</script>
</body>
</html>"""

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Dashboard written: {OUT_PATH}")
