from pathlib import Path
from typing import Any, Dict, List

import plotly.graph_objects as go
from jinja2 import Environment, FileSystemLoader, select_autoescape
from plotly.offline import plot
from visualisation.helpers import (
    build_sections_and_summaries,
    get_patient_meta,
    get_report_meta,
)

HTML_TEMPLATES_DIR = "data/html_templates"


def dashboard_v1a(
    patient: str, instruments: List[Dict[str, Any]], responses: Dict[str, Any]
):
    """ """
    VERSION = "v1a"

    sections, summary_labels, summary_values, summary_custom = (
        build_sections_and_summaries(instruments, responses)
    )

    report_meta = get_report_meta(patient)

    metadata_toggle = [
        "full_name",
        "cpr",
        "sex",
        "height_cm",
        "phone",
        "email",
        "status",
        "next_appointment",
    ]
    patient_meta = get_patient_meta(patient, metadata_toggle)

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
        summary_fig,
        include_plotlyjs=False,
        output_type="div",
        config={"responsive": True},
    )

    # ------------ render ------------
    env = Environment(
        loader=FileSystemLoader(HTML_TEMPLATES_DIR),
        autoescape=select_autoescape(("html", "xml")),
    )
    tpl = env.get_template(f"diabetes_report_template_{VERSION}.html")

    html = tpl.render(
        report_meta=report_meta,
        patient=patient_meta,
        summary_bar_div=summary_bar_div,
        sections=sections,
    )

    out_path = Path(f"data/dashboards/final_report_{VERSION}.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(out_path.as_posix())


def dashboard_v1b(
    patient: str, instruments: List[Dict[str, Any]], responses: Dict[str, Any]
):
    """ """
    VERSION = "v1b"

    sections, summary_labels, summary_values, summary_custom = (
        build_sections_and_summaries(instruments, responses)
    )

    report_meta = get_report_meta(patient)

    metadata_toggle = [
        "full_name",
        "cpr",
        "sex",
        "height_cm",
        "status",
        "next_appointment",
    ]
    patient_meta = get_patient_meta(patient, metadata_toggle)

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
        summary_fig,
        include_plotlyjs=False,
        output_type="div",
        config={"responsive": True},
    )

    # ------------ render ------------
    env = Environment(
        loader=FileSystemLoader(HTML_TEMPLATES_DIR),
        autoescape=select_autoescape(("html", "xml")),
    )
    tpl = env.get_template(f"diabetes_report_template_{VERSION}.html")

    html = tpl.render(
        report_meta=report_meta,
        patient=patient_meta,
        summary_bar_div=summary_bar_div,
        sections=sections,
    )

    out_path = Path(f"data/dashboards/final_report_{VERSION}.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(out_path.as_posix())


def dashboard_v2a(
    patient: str, instruments: List[Dict[str, Any]], responses: Dict[str, Any]
):
    """ """
    VERSION = "v2a"
    TEMPLATE_VERSION = "v1a"

    sections, summary_labels, summary_values, summary_custom = (
        build_sections_and_summaries(instruments, responses)
    )

    report_meta = get_report_meta(patient)

    metadata_toggle = [
        "full_name",
        "cpr",
        "sex",
        "height_cm",
        "phone",
        "email",
        "status",
        "next_appointment",
    ]
    patient_meta = get_patient_meta(patient, metadata_toggle)

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
        title="Questionnaire summary (percentage scores, higher = worse)",
        xaxis=dict(title=None),
        yaxis=dict(
            title="Percentage (0-100)",
            range=[0, 100],  # always 0 to 100
        ),
        margin=dict(l=60, r=30, t=60, b=60),
    )
    summary_bar_div = plot(
        summary_fig,
        include_plotlyjs=False,
        output_type="div",
        config={"responsive": True},
    )

    # ------------ render ------------
    env = Environment(
        loader=FileSystemLoader(HTML_TEMPLATES_DIR),
        autoescape=select_autoescape(("html", "xml")),
    )
    tpl = env.get_template(f"diabetes_report_template_{TEMPLATE_VERSION}.html")

    html = tpl.render(
        report_meta=report_meta,
        patient=patient_meta,
        summary_bar_div=summary_bar_div,
        sections=sections,
    )

    out_path = Path(f"data/dashboards/final_report_{VERSION}.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(out_path.as_posix())


def dashboard_v2b(
    patient: str, instruments: List[Dict[str, Any]], responses: Dict[str, Any]
):
    """ """
    VERSION = "v2b"
    TEMPLATE_VERSION = "v1b"

    sections, summary_labels, summary_values, summary_custom = (
        build_sections_and_summaries(instruments, responses)
    )

    report_meta = get_report_meta(patient)

    metadata_toggle = [
        "full_name",
        "cpr",
        "sex",
        "height_cm",
        "status",
        "next_appointment",
    ]
    patient_meta = get_patient_meta(patient, metadata_toggle)

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
        title="Questionnaire summary (percentage scores, higher = worse)",
        xaxis=dict(title=None),
        yaxis=dict(
            title="Percentage (0-100)",
            range=[0, 100],  # always 0 to 100
        ),
        margin=dict(l=60, r=30, t=60, b=60),
    )
    summary_bar_div = plot(
        summary_fig,
        include_plotlyjs=False,
        output_type="div",
        config={"responsive": True},
    )

    # ------------ render ------------
    env = Environment(
        loader=FileSystemLoader(HTML_TEMPLATES_DIR),
        autoescape=select_autoescape(("html", "xml")),
    )
    tpl = env.get_template(f"diabetes_report_template_{TEMPLATE_VERSION}.html")

    html = tpl.render(
        report_meta=report_meta,
        patient=patient_meta,
        summary_bar_div=summary_bar_div,
        sections=sections,
    )

    out_path = Path(f"data/dashboards/final_report_{VERSION}.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(out_path.as_posix())
