import re
from datetime import date
from typing import Any, Dict, List, Tuple

from utils.loader import load_patient_metadata


def slugify(s: str) -> str:
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", s.lower()))


def get_report_meta(patient: str) -> Dict[str, Any]:
    """
    Generate report metadata including a unique report ID based on the patient ID and current date.

    :param patient: The patient ID in the format "Pxxx" (e.g., "P001").

    :return: A dictionary containing report metadata.
    """

    # `patient` is of the form "Pxxx" (e.g., "P001") extract the number part
    patient_number = patient[1:]  # Remove the leading 'P'

    # Get today's date in YYYYMMDD format
    today_str = date.today().strftime("%Y%m%d")

    report_id = f"R-{today_str}-{patient_number}"

    report_meta = {
        "brand": "DTU student prototype",
        "report_title": "Diabetes Report",
        "report_id": report_id,
        "generated": date.today().strftime("%Y-%m-%d"),
    }

    return report_meta


def get_patient_meta(patient: str, metadata_toggle: List[str] | None) -> Dict[str, Any]:
    """
    Load patient metadata and filter it based on the provided toggle list.

    :param patient: The patient ID.
    :param metadata_toggle: A list of metadata keys to include. If None, include all metadata.

    :return: A dictionary containing the filtered patient metadata.
    """

    patient_meta_full = load_patient_metadata(patient).get("metadata", {})
    assert patient_meta_full is not None, f"No metadata found for patient {patient}"

    # Filter metadata based on the provided toggle list
    if metadata_toggle is None:
        patient_meta = patient_meta_full
    else:
        patient_meta = {key: patient_meta_full.get(key) for key in metadata_toggle}

    return patient_meta


def build_sections_and_summaries(
    instruments: List[Dict[str, Any]], responses: Dict[str, Any]
):
    """
    Given a list of instrument definitions and a dictionary of responses,
    build sections and summary data for the dashboard.

    :param instruments: A list of instrument definitions.
    :param responses: A dictionary of responses, keyed by instrument ID.

    :return: A tuple containing:
        - sections: A list of sections for the dashboard.
        - summary_labels: A list of labels for the summary.
        - summary_values: A list of values for the summary.
        - summary_custom: A list of custom targets for the summary.
    """
    sections = []
    summary_labels = []
    summary_values = []
    summary_custom = []

    for instrument in instruments:
        instrument_id = instrument.get("instrument_id", "")
        response = get_response(responses, instrument_id)

        section = create_section(instrument, instrument_id, response)
        standardised_overall_score = get_standardised_overall_score(
            instrument_id, response
        )
        custom_target = f"{instrument_id}-card"  # click → scroll target

        sections.append(section)
        summary_labels.append(instrument_id)
        summary_values.append(standardised_overall_score)
        summary_custom.append(custom_target)

    return sections, summary_labels, summary_values, summary_custom


def create_section(
    instrument: Dict[str, Any], instrument_id: str, response: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Given an instrument definition and its response, create a section for the dashboard.

    :param instrument: The instrument definition.
    :param instrument_id: The instrument ID.
    :param response: The response for the instrument.

    :return: A dictionary representing the section for the dashboard.
    """

    scales, answer_range = get_instrument_scales(instrument)

    answers = response.get("answers", {})

    comments = response.get("comments", {})
    title = instrument.get("title", "")
    badge_text = get_badge_text(answer_range)

    rows = get_section_rows(instrument, answers, comments, scales)

    section = {
        "id": instrument_id,
        "title": title,
        "badge_text": badge_text,
        "rows": rows,
    }

    return section


def get_standardised_overall_score(
    instrument_id: str, response: Dict[str, Any]
) -> float:
    """
    Given an instrument ID and its response, return the standardised overall score (0-100).
    Raise an assertion error if the response, overall score, or max score is not found.

    :param instrument_id: The instrument ID.
    :param response: The response for the instrument.

    :return: The standardised overall score (0-100).
    """
    response_scores = response.get("scores")
    assert response_scores is not None, (
        f"No scores found in response for instrument {instrument_id}"
    )

    overall_score = response_scores.get("overall_score")
    assert overall_score is not None, (
        f"No overall score found in response for instrument {instrument_id}"
    )

    max_score = response_scores.get("max_score")
    assert max_score is not None, (
        f"No max score found in response for instrument {instrument_id}"
    )

    standardised_overall_score = (overall_score / max_score) * 100

    return standardised_overall_score


def get_response(responses: Dict[str, Any], instrument_id: str) -> Dict[str, Any]:
    """
    Given a dictionary of responses and an instrument ID,
    return the response for the given instrument ID.
    Raise an assertion error if the response is not found.

    :param responses: The dictionary of responses.
    :param instrument_id: The instrument ID to look for.

    :return: The response for the given instrument ID.
    """

    response = responses.get(instrument_id)
    assert response is not None, f"No response found for instrument {instrument_id}"
    return response


def get_badge_text(answer_range: Tuple[int, int] | None) -> str:
    """
    Given an answer range, return a badge text for the dashboard.
    If answer_range is None, return an empty string.

    :param answer_range: A tuple of (min, max) answer range.

    :return: A badge text for the dashboard.
    """

    if answer_range is None:
        return ""

    return f"Scale {answer_range[0]}-{answer_range[1]} | higher = worse"


def get_instrument_scales(
    instrument: Dict[str, Any],
) -> Tuple[Dict[str, Any], Tuple[int, int]] | Tuple[None, None]:
    """
    Given an instrument definition, return its scales and answer range.
    If no scales are found, return (None, None).

    :param instrument: The instrument definition.

    :return: A tuple containing the scales dictionary and a tuple of (min, max) answer range.
    """
    scales = instrument.get("scales")

    if scales is None:
        print(f"No scales found for instrument {instrument.get('instrument_id', '')}")
        return None, None

    answer_range = [0, 0]

    # Check that all scales have the same range
    for indx, scale in enumerate(scales.values()):
        scale_range = scale.get("range")

        assert scale_range is not None, (
            f"No range found for scale {scale.get('name', '')} in instrument {instrument.get('instrument_id', '')}"
        )

        if indx == 0:
            answer_range = scale_range
        elif scale_range != answer_range:
            raise ValueError(
                f"Different answer ranges found in instrument {instrument.get('instrument_id', '')}: {answer_range} and {scale_range}"
            )

    answer_range = (int(answer_range[0]), int(answer_range[1]))

    return scales, answer_range


def get_section_rows(
    instrument: Dict[str, Any],
    answers: Dict[str, int | str],
    comments: Dict[str, str | None],
    scales: Dict[str, Any] | None,
) -> List[Dict[str, Any]]:
    """
    Given an instrument definition and the corresponding answers + comments,
    return a list of section rows for the dashboard.

    :param instrument: The instrument definition.
    :param answers: The answers for the instrument.
    :param comments: The comments for the answers (for the instrument).
    :param scales: The scales for the instrument.

    :return: A list of section rows.
    """
    instrument_id = instrument.get("instrument_id", "")

    section_rows = []
    for question in instrument.get("questions", []):
        question_id = question.get("id", "")

        # Get data for section row
        question_text = question.get("text", "")
        answer = get_answer(answers, question_id, instrument_id)
        score = get_answer_score(answer)
        translation = get_translation(scales, answer, question)
        comment = comments.get(question_id, "")

        # Fill section row
        section_rows.append(
            {
                "question": question_text,
                "score": score,
                "translation": translation,
                "comment": comment,
                "slug": slugify(question_text),
            }
        )

    return section_rows


def get_answer(
    answers: Dict[str, Any], question_id: str, instrument_id: str
) -> int | str:
    """
    Given a dictionary of answers, return the answer for the given question ID.
    Raise an assertion error if the answer is not found.

    :param answers: The dictionary of answers.
    :param question_id: The question ID to look for.
    :param instrument_id: The instrument ID (for error messages).

    :return: The answer for the given question ID.
    """

    answer = answers.get(question_id)
    assert answer is not None, (
        f"No answer found for question {question_id} in instrument {instrument_id}"
    )
    return answer


def get_translation(
    scales: Dict[str, Any] | None, answer: int | str | None, question: Dict[str, Any]
) -> str:
    """
    Given the scales, answer, and question definition, return the translation for the answer.
    If scales is None, return an empty string.
    If answer is None, return an empty string.

    :param scales: The scales for the instrument.
    :param answer: The answer to translate.
    :param question: The question definition (to get the scale key).

    :return: The translation for the answer.
    """

    if scales is None:
        translation = ""
    elif answer is None:
        translation = ""
    else:
        question_scale_key = question.get("scale", "")
        question_scale = scales.get(question_scale_key, {})
        translation = question_scale.get("labels", {}).get(answer, "")

    if translation is None:
        print(
            f"in `get_translation`: answer = {answer}, translation = {translation}\n\n"
        )

    return translation


def get_answer_score(answer: int | str | None) -> float | str:
    """
    Given an answer, return its score as a float.
    If the answer is not a number, return None.

    :param answer: The answer to convert to a score.

    :return: The score as a float, or None if the answer is not a number.
    """

    if isinstance(answer, (int, float)):
        return float(answer)

    return ""  # Not a number
