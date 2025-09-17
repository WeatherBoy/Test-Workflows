# Build an HTML dashboard (single file) from the provided questionnaire answers.
# Uses matplotlib.pyplot for a radar chart and Bokeh for interactive bar charts.
# Comments in parentheses from the images are intentionally ignored in the data below.

import math
from pathlib import Path
from textwrap import dedent

# ---- Matplotlib (pyplot) for radar ----
import matplotlib

matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import numpy as np
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, Range1d

# ---- Bokeh for interactive bars ----
from bokeh.plotting import figure
from bokeh.resources import CDN

# --------------------------
# 1) Encode the questionnaire values (from the screenshots)
# --------------------------

data = {}

# B1 - Lifestyle (mixed data; we'll display some as text KPIs and some as bars)
data["B1"] = dict(
    weight_kg=90,
    exercise_days=1,
    healthy_diet_days=6,
    alcohol_yes=True,
    alcohol_often="Occasionally",
    alcohol_units_per_week="8–14",
    smoking="No",
    first_cig_30min="No",
    oral_med="No",
    insulin="Yes",
    other_injections="No",
    glucose_checks_per_week="10–20",
    hypo_any_month="Yes",
    hypos_past_month="10–12",
    needed_assistance_any="No",
    needed_assistance_count=0,
    checkups_past_year=2,
)

# B2 - Emotional distress (assume 0–4 scale; numbers as given)
data["B2"] = {
    "Feeling depressed thinking about diabetes": 0,
    "Diabetes taking too much energy": 1,
    "Feeling overwhelmed by diabetes": 0,
    "Constant concern about food/eating": 0,
    "Feeling alone with diabetes": 0,
    "Feeling burned out managing diabetes": 0,
}

# C - Areas of concern
data["C"] = dict(
    primary_area="B", secondary_area="A", importance_0_4=4, confidence_0_4=2
)

# D1 - Food behavior (assume 0–4, numbers as given)
data["D1"] = {
    "No time to make healthy meals": 1,
    "Eating outside home is difficult": 1,
    "Eat because food is there": 0,
    "Meal plan seems too hard": 0,
    "Hard to avoid high-fat foods": 0,
    "Eat when bored or stressed": 1,
    "Friends/family make it hard": 0,
    "Hungry when on healthy plan": 0,
    "Feel hopeless after many tries": 1,
}

# D4 - DMAS (adherence) – encode as booleans/text; we'll show a compact table
data["D4"] = [
    ("Forget medications?", "No"),
    ("Missed for other reasons in last 2 weeks?", "No"),
    ("Forget to bring meds when traveling?", "No"),
    ("Difficulty remembering all meds?", "Never / very rarely"),
    ("Number of prescribed med types (regular)", "2–4"),
    ("Skip buying meds due to cost?", "No"),
    ("Who ensures you take meds?", "Self"),
]

# WHO-5 (0–5 usually; we keep numbers given)
data["WHO5"] = {
    "Cheerful / in good spirits": 2,
    "Calm and relaxed": 2,
    "Active and vigorous": 2,
    "Woke fresh and rested": 3,
    "Daily life filled with interest": 2,
}

# PSQI – we’ll present key sleep metrics and a frequency bar for symptoms (0–3 scale assumed)
data["PSQI"] = dict(
    schedule=dict(
        bedtime="23:00–23:59",
        latency_min=20,
        getup="07:45–08:00",
        hours_sleep="7–8",
    ),
    symptoms={
        "Cant sleep within 30 min": 1,
        "Wake in night/early morning": 2,
        "Bathroom at night": 3,
        "Cant breathe comfortably": 0,
        "Loud coughing/snoring": 3,
        "Too cold": 0,
        "Too hot": 1,
        "Bad dreams": 1,
        "Pain": 0,
    },
    overall_quality=1,
    sleep_meds=0,
    trouble_staying_awake=0,
    low_enthusiasm=0,
    partner_reports={
        "Loud snoring": 3,
        "Long breathing pauses": 0,
        "Legs twitch/jerk": 0,
        "Disorientation during sleep": 0,
    },
)

# HADS – two subscales; numbers as given
data["HADS_A"] = {  # Anxiety items (7)
    "Tense / wound up": 3,
    "Frightened feeling of something happening": 3,
    "Worrying thoughts": 3,
    "Can sit at ease / relaxed": 1,
    "Frightened feeling like butterflies": 3,
    "Restless / on the move": 3,
    "Sudden feelings of panic": 3,
}
data["HADS_D"] = {  # Depression items (7)
    "Enjoy things as before": 0,
    "Laugh and see funny side": 0,
    "Feel cheerful": 0,
    "Feel slowed down": 3,
    "Lost interest in appearance": 3,
    "Look forward with enjoyment": 0,
    "Enjoy good book/radio/TV": 0,
}

# PAID
data["PAID"] = {
    "Depressed thinking about diabetes": 1,
    "Diabetes takes too much energy": 1,
    "Overwhelmed by diabetes": 1,
    "Constantly concerned about food": 0,
    "Burned out managing diabetes": 1,
}

# --------------------------
# 2) Matplotlib Radar: combine a few domains (Food, Distress, Sleep symptoms avg, Adherence)
# --------------------------
radar_labels = [
    "Food behavior",
    "Emotional distress",
    "Sleep symptoms",
    "Medication adherence (inverse)",
    "Wellbeing (WHO-5)",
]


# Normalize each domain to 0–10 for a gestalt
def avg(values):
    return sum(values) / len(values) if values else 0.0


food_avg_0_4 = avg(list(data["D1"].values()))
distress_avg_0_4 = avg(list(data["B2"].values()))
sleep_avg_0_3 = avg(list(data["PSQI"]["symptoms"].values()))
adherence_inverse = 10.0  # start high
# Penalize inverse adherence by 'No' answers that suggest issues (here, all look good)
# For a first draft, compute a simple score where lower problems -> higher score.
adherence_inverse = 10.0 - 0.0  # placeholder; no clear issues from D4

who5_avg_0_5 = avg(list(data["WHO5"].values()))

# Scale to 0–10
food_0_10 = food_avg_0_4 * (10 / 4)
distress_0_10 = distress_avg_0_4 * (10 / 4)
sleep_0_10 = sleep_avg_0_3 * (10 / 3)
who5_0_10 = who5_avg_0_5 * (10 / 5)

radar_values = [food_0_10, distress_0_10, sleep_0_10, adherence_inverse, who5_0_10]

# Radar plot setup
N = len(radar_labels)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
values = radar_values + radar_values[:1]
angles = angles + angles[:1]

fig = plt.figure(figsize=(5, 5))
ax = plt.subplot(111, polar=True)
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

ax.set_thetagrids(np.degrees(angles[:-1]), radar_labels)
ax.set_rlabel_position(0)
ax.set_ylim(0, 10)
ax.plot(angles, values, marker="o")
ax.fill(angles, values, alpha=0.25)

radar_path = Path("/mnt/data/radar_overview.png")
fig.tight_layout()
fig.savefig(radar_path, dpi=150)
plt.close(fig)


# --------------------------
# 3) Bokeh charts: multiple bar charts
# --------------------------
def bokeh_bar(title, mapping, x_range=None, y_max=4, tooltips=None):
    labels = list(mapping.keys())
    values = list(mapping.values())

    if x_range is None:
        x_range = labels
    src = ColumnDataSource(dict(label=labels, value=values))
    p = figure(title=title, x_range=x_range, height=350, toolbar_location=None)
    p.vbar(x="label", top="value", width=0.8, source=src)
    p.y_range = Range1d(0, y_max)
    p.xgrid.visible = False
    p.add_tools(
        HoverTool(tooltips=tooltips or [("Item", "@label"), ("Score", "@value")])
    )
    p.xaxis.major_label_orientation = math.radians(15)
    return p


# Emotional distress (0–4)
p_b2 = bokeh_bar("Emotional distress (0–4)", data["B2"], y_max=4)

# Food behavior (0–4)
p_d1 = bokeh_bar("Food behavior (0–4)", data["D1"], y_max=4)

# WHO-5 (0–5)
p_who5 = bokeh_bar("WHO-5 wellbeing (0–5)", data["WHO5"], y_max=5)

# PAID (0–4)
p_paid = bokeh_bar("PAID – problem areas (0–4)", data["PAID"], y_max=4)

# PSQI symptoms (0–3)
p_psqi = bokeh_bar(
    "PSQI – sleep symptoms frequency (0–3)", data["PSQI"]["symptoms"], y_max=3
)

# HADS subscales (0–3 per item typically; we just display the raw item scores)
p_hads_a = bokeh_bar("HADS – Anxiety items", data["HADS_A"], y_max=3)
p_hads_d = bokeh_bar("HADS – Depression items", data["HADS_D"], y_max=3)

# Dump components
script_b2, div_b2 = components(p_b2)
script_d1, div_d1 = components(p_d1)
script_who5, div_who5 = components(p_who5)
script_paid, div_paid = components(p_paid)
script_psqi, div_psqi = components(p_psqi)
script_hads_a, div_hads_a = components(p_hads_a)
script_hads_d, div_hads_d = components(p_hads_d)

bokeh_scripts = "\n".join(
    [
        script_b2,
        script_d1,
        script_who5,
        script_paid,
        script_psqi,
        script_hads_a,
        script_hads_d,
    ]
)
bokeh_resources = CDN.render()

# --------------------------
# 4) Assemble HTML
# --------------------------
b1_cards = f"""
<div class="kpi">Weight: <b>{data["B1"]["weight_kg"]} kg</b></div>
<div class="kpi">Exercise days (last week): <b>{data["B1"]["exercise_days"]}</b> / 7</div>
<div class="kpi">Healthy diet days (last week): <b>{data["B1"]["healthy_diet_days"]}</b> / 7</div>
<div class="kpi">Alcohol: <b>{"Yes" if data["B1"]["alcohol_yes"] else "No"}</b> · {data["B1"]["alcohol_often"]} · {data["B1"]["alcohol_units_per_week"]} units/week</div>
<div class="kpi">Smoking: <b>{data["B1"]["smoking"]}</b> · First cigarette within 30 min: {data["B1"]["first_cig_30min"]}</div>
<div class="kpi">Therapy: Oral meds: <b>{data["B1"]["oral_med"]}</b> · Insulin: <b>{data["B1"]["insulin"]}</b> · Other injections: <b>{data["B1"]["other_injections"]}</b></div>
<div class="kpi">Glucose checks/week: <b>{data["B1"]["glucose_checks_per_week"]}</b></div>
<div class="kpi">Hypoglycemia in past month: <b>{data["B1"]["hypo_any_month"]}</b> · Episodes: {data["B1"]["hypos_past_month"]}</div>
<div class="kpi">Assistance needed during hypos: <b>{data["B1"]["needed_assistance_any"]}</b> · Count: {data["B1"]["needed_assistance_count"]}</div>
<div class="kpi">Check-ups past year: <b>{data["B1"]["checkups_past_year"]}</b></div>
"""

psqi_summary = data["PSQI"]["schedule"]
psqi_cards = f"""
<div class="kpi">Bedtime: <b>{psqi_summary["bedtime"]}</b></div>
<div class="kpi">Sleep latency: <b>{psqi_summary["latency_min"]} min</b></div>
<div class="kpi">Get-up time: <b>{psqi_summary["getup"]}</b></div>
<div class="kpi">Hours of actual sleep: <b>{psqi_summary["hours_sleep"]}</b></div>
<div class="kpi">Overall sleep quality (0 best → higher worse?): <b>{data["PSQI"]["overall_quality"]}</b></div>
"""

d4_rows = "".join(f"<tr><td>{q}</td><td>{a}</td></tr>" for q, a in data["D4"])

html = dedent(f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Patient Questionnaire – Prototype</title>
  {bokeh_resources}
  <style>
    body {{
      margin: 0; padding: 0;
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
      background: #0b0e14; color: #e7edf3;
    }}
    .wrap {{ max-width: 1200px; margin: 24px auto 64px; padding: 0 16px; }}
    h1 {{ font-size: 24px; margin: 0 0 6px; }}
    h2 {{ font-size: 18px; margin: 16px 0 8px; }}
    .grid {{ display: grid; gap: 16px; }}
    .g-2 {{ grid-template-columns: 1fr 1fr; }}
    .g-3 {{ grid-template-columns: 1fr 1fr 1fr; }}
    .card {{
      background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 14px; padding: 12px 14px;
      box-shadow: 0 8px 28px rgba(0,0,0,0.35);
    }}
    .kpi {{ font-size: 14px; margin: 6px 0; color: #cfd7e3; }}
    .muted {{ color: #9aa4b2; font-size: 13px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
    th, td {{ padding: 8px 6px; border-bottom: 1px dashed rgba(255,255,255,0.12); }}
    th {{ text-align: left; color: #9aa4b2; font-weight: 600; }}
    img.radar {{ width: 100%; max-width: 520px; display:block; margin: 0 auto; }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Patient questionnaire – single-visit overview</h1>
    <div class="muted">Prototype — numbers are displayed on their native scales from each instrument.</div>

    <div class="grid g-2" style="margin-top:16px;">
      <div class="card">
        <h2>B1 · Lifestyle (key metrics)</h2>
        {b1_cards}
      </div>
      <div class="card">
        <h2>Overview (radar)</h2>
        <img class="radar" src="radar_overview.png" alt="Radar overview">
        <div class="muted">Scaled 0–10 across domains for quick orientation.</div>
      </div>
    </div>

    <div class="grid g-2" style="margin-top:16px;">
      <div class="card"><h2>B2 · Emotional distress</h2>{div_b2}</div>
      <div class="card"><h2>D1 · Food behavior</h2>{div_d1}</div>
    </div>

    <div class="grid g-2" style="margin-top:16px;">
      <div class="card"><h2>WHO-5 wellbeing</h2>{div_who5}</div>
      <div class="card"><h2>PAID · problem areas</h2>{div_paid}</div>
    </div>

    <div class="grid g-2" style="margin-top:16px;">
      <div class="card">
        <h2>PSQI · schedule summary</h2>
        {psqi_cards}
        <h2 style="margin-top:10px;">PSQI · symptoms</h2>
        {div_psqi}
      </div>
      <div class="card">
        <h2>D4 · Adherence (DMAS)</h2>
        <table>
          <thead><tr><th>Question</th><th>Answer</th></tr></thead>
          <tbody>{d4_rows}</tbody>
        </table>
      </div>
    </div>

    <div class="grid g-2" style="margin-top:16px;">
      <div class="card"><h2>HADS · Anxiety</h2>{div_hads_a}</div>
      <div class="card"><h2>HADS · Depression</h2>{div_hads_d}</div>
    </div>

    <div class="muted" style="margin-top:12px;">Primary concern: {data["C"]["primary_area"]} · Secondary: {data["C"]["secondary_area"]} · Importance: {data["C"]["importance_0_4"]} · Confidence: {data["C"]["confidence_0_4"]}</div>
  </div>

  {bokeh_scripts}
</body>
</html>
""")

# Save HTML and copy radar image next to it
out_file = Path("/mnt/data/patient_questionnaire_dashboard.html")
out_file.write_text(html, encoding="utf-8")

# Save the radar image next to HTML (already saved)
# We need to ensure the relative path works; copy to same dir with the expected name.
# Already saved to /mnt/data/radar_overview.png

(str(out_file), str(radar_path))
