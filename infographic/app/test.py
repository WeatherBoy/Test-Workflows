# src/render_infographic.py
from pathlib import Path

import plotly.graph_objects as go
from jinja2 import Environment, FileSystemLoader, select_autoescape
from plotly.offline import plot

# --- 1) Example data (replace with your real questionnaire outputs) ---
patient_data = {
    "patient_id": "P-001",
    "name_or_alias": "Patient A",
    "age": 58,
    "dm_type": "Type 2",
    "hba1c": 7.8,  # optional
    "domains": [
        ("Medication adherence", 6.5, "Often forgets evening dose 2-3 times/week."),
        ("Dietary habits", 8.0, "Late-evening snacking; struggles with portion sizes."),
        ("Physical activity", 7.0, "Wants to walk more but lacks routine."),
        ("Glucose monitoring", 5.0, "Irregular morning checks; no CGM."),
        ("Hypoglycemia concern", 3.0, "Rare hypos; some fear during exercise."),
        ("Sleep quality", 6.0, "Fragmented sleep; wakes twice most nights."),
        ("Foot care", 2.0, "Checks feet weekly; no ulcers reported."),
        ("Mental wellbeing", 7.5, "Feels overwhelmed by conflicting diet advice."),
        ("Access/finances", 4.0, "Can afford meds; asks for dietitian referral."),
    ],
    "highlights": [
        "'I'm not sure what to eat when I'm hungry after 9 pm.'",
        "'I skip the pill if I'm already in bed and remember too late.'",
        "'Walking feels good, but I lose momentum after a week.'",
        "'I want someone to show me a simple meal plan.'",
    ],
    "flags": {
        "Adherence risk": True,
        "Dietitian referral": True,
        "Sleep evaluation": "Consider brief screening (Insomnia symptoms)",
        "CGM interest": False,
        "Foot exam due": "Not urgent (self-checking weekly)",
    },
}

# --- 2) Build Plotly figures (same as your prototype) ---
labels = [d[0] for d in patient_data["domains"]]
scores = [d[1] for d in patient_data["domains"]]
notes = [d[2] for d in patient_data["domains"]]

radar_trace = go.Scatterpolar(
    r=scores + [scores[0]],
    theta=labels + [labels[0]],
    mode="lines+markers",
    fill="toself",
    hovertemplate="<b>%{theta}</b><br>Score: %{r}/10<extra></extra>",
)
radar_fig = go.Figure(data=[radar_trace])
radar_fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
    title="Patient struggle profile (0-10)",
    margin=dict(l=40, r=40, t=60, b=40),
)

top_k = 5
sorted_pairs = sorted(zip(labels, scores, notes), key=lambda x: x[1], reverse=True)
top_labels = [x[0] for x in sorted_pairs][:top_k]
top_scores = [x[1] for x in sorted_pairs][:top_k]

bar_trace = go.Bar(
    x=top_scores[::-1],
    y=top_labels[::-1],
    orientation="h",
    hovertemplate="<b>%{y}</b><br>Score: %{x}/10<extra></extra>",
)
bar_fig = go.Figure(data=[bar_trace])
bar_fig.update_layout(
    title=f"Top {top_k} focus areas",
    xaxis=dict(range=[0, 10]),
    margin=dict(l=100, r=30, t=60, b=40),
)

# Convert figures to embeddable <div> without bundling Plotly.js (template loads it via CDN)
radar_div = plot(radar_fig, include_plotlyjs=False, output_type="div")
bar_div = plot(bar_fig, include_plotlyjs=False, output_type="div")

# --- 3) Render Jinja2 template ---
env = Environment(
    loader=FileSystemLoader("html_templates"),
    autoescape=select_autoescape(enabled_extensions=("html", "xml")),
)
template = env.get_template("diabetes_consult.html")

html = template.render(
    patient=patient_data,
    radar_div=radar_div,
    bar_div=bar_div,
)

# --- 4) Write file ---
out_path = Path("data/dashboards/diabetes_consult_infographic.html")
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(html, encoding="utf-8")

print(out_path.as_posix())
