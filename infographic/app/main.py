import re
from datetime import date
from pathlib import Path

import plotly.graph_objects as go
from jinja2 import Environment, FileSystemLoader, select_autoescape
from plotly.offline import plot


# ------------ helpers ------------
def slugify(s: str) -> str:
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", s.lower()))


# ------------ patient + report meta ------------
patient = {
    "full_name": "Jens Nielsen",
    "cpr": "310585-1122",
    "sex": "Male",
    "height_cm": 180,
    "phone": "+45 12345678",
    "email": "jnls@1234.com",
    "status": "Enrolled",
    "joined": "2019-05-31",
    "next_consult": "2025-10-01",
}

report_meta = {
    "brand": "diacare",
    "report_title": "Patient Report",
    "report_id": "R-24001",
    "generated": date.today().strftime("%Y-%m-%d"),
    "page": "1/1",
}

# ------------ reusable scales (0-3) ------------
SCALES = {
    "frequency_0_3": {
        0: "Not during the past month",
        1: "Less than once a week",
        2: "Once or twice a week",
        3: "Three or more times a week",
    },
    "quality_0_3": {
        0: "Very good",
        1: "Fairly good",
        2: "Fairly bad",
        3: "Very bad",
    },
    "severity_0_3": {
        0: "None",
        1: "Mild",
        2: "Moderate",
        3: "Severe",
    },
}

# ------------ instrument “schemas” (what’s needed) ------------
# For each questionnaire: an id, title, short label (for x-axis), items (id/text/scale_key).
# All items here use 0-3 scales for a simple demo.
instruments = [
    {
        "id": "psqi",
        "title": "Pittsburgh Sleep Quality Index",
        "label": "PSQI",
        "items": [
            {
                "id": "psqi_q5a",
                "text": "Cannot get to sleep within 30 minutes",
                "scale": "frequency_0_3",
            },
            {"id": "psqi_q6", "text": "Overall sleep quality", "scale": "quality_0_3"},
        ],
    },
    {
        "id": "hads",
        "title": "Hospital Anxiety and Depression Scale",
        "label": "HADS",
        "items": [
            {"id": "hads_q1", "text": "Tension, restlessness", "scale": "severity_0_3"},
            {"id": "hads_q2", "text": "Loss of interest", "scale": "severity_0_3"},
        ],
    },
    {
        "id": "who5",
        "title": "WHO-5 Well-Being Index",
        "label": "WHO-5",
        "items": [
            {
                "id": "who5_q1",
                "text": "Felt cheerful and in good spirits",
                "scale": "severity_0_3",
            },
            {"id": "who5_q2", "text": "Felt calm and relaxed", "scale": "severity_0_3"},
        ],
    },
    {
        "id": "phq9",
        "title": "PHQ-9 Depression",
        "label": "PHQ-9",
        "items": [
            {
                "id": "phq9_q1",
                "text": "Little pleasure in doing things",
                "scale": "severity_0_3",
            },
            {
                "id": "phq9_q2",
                "text": "Feeling down, depressed",
                "scale": "severity_0_3",
            },
        ],
    },
    {
        "id": "gad7",
        "title": "GAD-7 Anxiety",
        "label": "GAD-7",
        "items": [
            {
                "id": "gad7_q1",
                "text": "Feeling nervous, anxious",
                "scale": "severity_0_3",
            },
            {
                "id": "gad7_q2",
                "text": "Not being able to stop worrying",
                "scale": "severity_0_3",
            },
        ],
    },
    {
        "id": "adherence",
        "title": "Medication Adherence",
        "label": "Adherence",
        "items": [
            {"id": "adh_q1", "text": "Missed evening dose", "scale": "frequency_0_3"},
            {
                "id": "adh_q2",
                "text": "Confusion about schedule",
                "scale": "severity_0_3",
            },
        ],
    },
    {
        "id": "activity",
        "title": "Physical Activity",
        "label": "Activity",
        "items": [
            {"id": "act_q1", "text": "≥30 min activity", "scale": "frequency_0_3"},
            {"id": "act_q2", "text": "Gets out of breath", "scale": "severity_0_3"},
        ],
    },
    {
        "id": "diet",
        "title": "Dietary Habits",
        "label": "Diet",
        "items": [
            {
                "id": "diet_q1",
                "text": "Late-evening snacking",
                "scale": "frequency_0_3",
            },
            {"id": "diet_q2", "text": "Portion size control", "scale": "severity_0_3"},
        ],
    },
]

# ------------ mock responses (≤ 2 per questionnaire) ------------
responses = {
    "psqi": {"psqi_q5a": 1, "psqi_q6": 1},
    "hads": {"hads_q1": 2, "hads_q2": 1},
    "who5": {"who5_q1": 1, "who5_q2": 2},
    "phq9": {"phq9_q1": 2, "phq9_q2": 1},
    "gad7": {"gad7_q1": 1, "gad7_q2": 2},
    "adherence": {"adh_q1": 1, "adh_q2": 1},
    "activity": {"act_q1": 1, "act_q2": 1},
    "diet": {"diet_q1": 2, "diet_q2": 1},
}

# ------------ build sections + totals ------------
sections = []
summary_labels = []
summary_values = []
summary_custom = []

for inst in instruments:
    qid = inst["id"]
    label = inst["label"]
    rows = []
    total = 0
    max_total = 0

    for item in inst["items"]:
        iid = item["id"]
        scale_key = item["scale"]
        scale = SCALES[scale_key]
        if iid not in responses.get(qid, {}):
            continue
        v = int(responses[qid][iid])
        rows.append(
            {
                "question": item["text"],
                "score": float(v),
                "translation": scale.get(v, str(v)),
                "comment": "",
                "slug": slugify(item["text"]),
            }
        )
        total += v
        max_total += 3  # every item is 0-3 in this demo

    sections.append(
        {
            "id": qid,
            "title": inst["title"],
            "badge_text": "Scale 0-3 | higher = worse",
            "subtitle": "",
            "rows": rows,
        }
    )

    summary_labels.append(label)
    summary_values.append(total)
    summary_custom.append(f"{qid}-card")  # click → scroll target

# ------------ summary bar (vertical, unsorted, same order as instruments) ------------
summary_fig = go.Figure(
    [
        go.Bar(
            x=summary_labels,
            y=summary_values,
            customdata=summary_custom,
            hovertemplate="<b>%{x}</b><br>Total: %{y}<extra></extra>",
            marker=dict(color="#6ea8fe"),
        )
    ]
)
summary_fig.update_layout(
    title="Questionnaire summary (total scores)",
    xaxis=dict(title=None),
    yaxis=dict(title="Total"),
    margin=dict(l=60, r=30, t=60, b=60),
)
summary_bar_div = plot(
    summary_fig, include_plotlyjs=False, output_type="div", config={"responsive": True}
)

# ------------ render ------------
env = Environment(
    loader=FileSystemLoader("html_templates"),
    autoescape=select_autoescape(("html", "xml")),
)
tpl = env.get_template("diabetes_report_template2.html")

html = tpl.render(
    report_meta=report_meta,
    patient=patient,
    summary_bar_div=summary_bar_div,
    sections=sections,
)

out_path = Path("data/dashboards/final_report.html")
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(html, encoding="utf-8")
print(out_path.as_posix())
