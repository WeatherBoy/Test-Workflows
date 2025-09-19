from pathlib import Path

import plotly.graph_objects as go
from jinja2 import Environment, FileSystemLoader, select_autoescape
from plotly.offline import plot

# --- sample data (unchanged structure) ---
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
        "“I'm not sure what to eat when I'm hungry after 9 pm.”",
        "“I skip the pill if I'm already in bed and remember too late.”",
        "“Walking feels good, but I lose momentum after a week.”",
        "“I want someone to show me a simple meal plan.”",
    ],
    "flags": {
        "Adherence risk": True,
        "Dietitian referral": True,
        "Sleep evaluation": "Consider brief screening (Insomnia symptoms)",
        "CGM interest": False,
        "Foot exam due": "Not urgent (self-checking weekly)",
    },
}

# --- per-category cutoffs (edit freely or load from a JSON later) ---
cutoffs = {
    "Medication adherence": 5.0,
    "Dietary habits": 7.0,
    "Physical activity": 6.0,
    "Glucose monitoring": 6.0,
    "Sleep quality": 5.5,
    "Mental wellbeing": 6.0,
    # others omitted -> no cutoff (all blue)
}


def slugify(text: str) -> str:
    import re

    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


# Build domain rows with slugs (for the table + anchors)
domains = [
    {"label": lbl, "score": sc, "note": note, "slug": slugify(lbl)}
    for (lbl, sc, note) in patient_data["domains"]
]

# --- BAR (stacked by cutoff) ---
# Sort bars by score (desc) for the overview
sorted_domains = sorted(domains, key=lambda d: d["score"], reverse=True)

labels_sorted = [d["label"] for d in sorted_domains]
scores_sorted = [d["score"] for d in sorted_domains]
slugs_sorted = [d["slug"] for d in sorted_domains]

below, above = [], []
for d in sorted_domains:
    s = d["score"]
    c = cutoffs.get(d["label"])
    if c is None:
        below.append(s)
        above.append(0.0)
    else:
        below.append(min(s, c))
        above.append(max(0.0, s - c))

# Reverse arrays so highest appears at the TOP of the chart
y = labels_sorted[::-1]
x_below = below[::-1]
x_above = above[::-1]
cd = slugs_sorted[::-1]

bars_below = go.Bar(
    x=x_below,
    y=y,
    orientation="h",
    name="≤ cutoff",
    marker=dict(color="#6ea8fe"),
    customdata=cd,
    hovertemplate="<b>%{y}</b><br>≤ cutoff: %{x:.1f}/10<extra></extra>",
)
bars_above = go.Bar(
    x=x_above,
    y=y,
    orientation="h",
    name="Above",
    marker=dict(color="#ff6b6b"),
    customdata=cd,
    hovertemplate="<b>%{y}</b><br>Above: %{x:.1f}/10<extra></extra>",
)

bar_fig = go.Figure([bars_below, bars_above])
bar_fig.update_layout(
    barmode="stack",
    title="Focus areas (with cutoffs)",
    xaxis=dict(range=[0, 10], title=None),
    yaxis=dict(title=None),
    margin=dict(l=140, r=30, t=60, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
bar_div = plot(
    bar_fig, include_plotlyjs=False, output_type="div", config={"responsive": True}
)

# --- (Optional) Radar; set show_radar=False to hide completely ---
show_radar = False
radar_div = ""
if show_radar:
    r = scores_sorted + [scores_sorted[0]]
    th = labels_sorted + [labels_sorted[0]]
    radar = go.Scatterpolar(
        r=r,
        theta=th,
        mode="lines+markers",
        fill="toself",
        hovertemplate="<b>%{theta}</b><br>Score: %{r}/10<extra></extra>",
    )
    radar_fig = go.Figure([radar])
    radar_fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        title="Patient struggle profile (0-10)",
        margin=dict(l=40, r=40, t=60, b=40),
    )
    radar_div = plot(
        radar_fig,
        include_plotlyjs=False,
        output_type="div",
        config={"responsive": True},
    )

# --- Render template ---
env = Environment(
    loader=FileSystemLoader("html_templates"),
    autoescape=select_autoescape(enabled_extensions=("html", "xml")),
)
template = env.get_template("diabetes_consult.html")

html = template.render(
    patient=patient_data,
    domains=domains,  # for table (original order)
    bar_div=bar_div,
    radar_div=radar_div,
    show_radar=show_radar,
)

out_path = Path("data/dashboards/diabetes_consult_infographic.html")
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(html, encoding="utf-8")

print(out_path.as_posix())
