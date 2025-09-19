from typing import Any, Dict

from scoring import (
    hads_anxiety,
    hads_depression,
    psqi_c1_duration,
    psqi_c2_disturbance,
    psqi_c3_latency,
    psqi_c4_day_dysfunction,
    psqi_c5_sleep_efficiency,
    psqi_c6_overall_sleep_quality,
    psqi_c7_medication,
)


def process_psqi_response(response: Dict[str, Any]) -> Dict[str, int]:
    """
    This function processes the responses for a PSQI questionnaire.

    The Pittsburg Sleep Quality Index (PSQI) is a self-rated questionnaire which assesses sleep quality and disturbances over a 1-month time interval.

    :param response: Dictionary of PSQI answers.

    :return: Dictionary with component scores and global score.
    """
    c1 = psqi_c1_duration(response)
    c2 = psqi_c2_disturbance(response)
    c3 = psqi_c3_latency(response)
    c4 = psqi_c4_day_dysfunction(response)
    c5 = psqi_c5_sleep_efficiency(response)
    c6 = psqi_c6_overall_sleep_quality(response)
    c7 = psqi_c7_medication(response)
    global_score = c1 + c2 + c3 + c4 + c5 + c6 + c7

    psqi_response = {
        "C1_duration": c1,
        "C2_disturbance": c2,
        "C3_latency": c3,
        "C4_day_dysfunction": c4,
        "C5_sleep_efficiency": c5,
        "C6_overall_sleep_quality": c6,
        "C7_medication": c7,
        "global_score": global_score,
    }

    return psqi_response


def process_who5_response(response: Dict[str, Any]) -> Dict[str, int]:
    """
    This function processes the responses for a WHO-5 questionnaire.

    The World Health Organization-Five Well-Being Index (WHO-5) is a short self-reported measure of current mental well-being.

    :param response: Dictionary of WHO-5 answers.

    :return: Dictionary with total score and percentage score.
    """
    q1 = response.get("Q1", 0)
    q2 = response.get("Q2", 0)
    q3 = response.get("Q3", 0)
    q4 = response.get("Q4", 0)
    q5 = response.get("Q5", 0)
    total_score = q1 + q2 + q3 + q4 + q5
    percentage_score = total_score * 4  # Scale to 0-100

    who5_response = {
        "Q1": q1,
        "Q2": q2,
        "Q3": q3,
        "Q4": q4,
        "Q5": q5,
        "total_score": total_score,
        "percentage_score": percentage_score,
    }

    return who5_response


def process_hads_response(response: Dict[str, Any]) -> Dict[str, int]:
    """
    This function processes the responses for a HADS questionnaire.

    The Hospital Anxiety and Depression Scale (HADS) is a self-assessment scale to detect states of depression and anxiety.

    :param response: Dictionary of HADS answers.
    :return: Dictionary with anxiety score, depression score, and total score.
    """

    anxiety_score = hads_anxiety(response)
    depression_score = hads_depression(response)
    total_score = anxiety_score + depression_score

    hads_response = {
        "anxiety_score": anxiety_score,
        "depression_score": depression_score,
        "total_score": total_score,
    }

    return hads_response


def process_emotional_distress_response(response: Dict[str, Any]) -> Dict[str, int]:
    """
    This function processes the responses for an Emotional Distress questionnaire.

    The B2 - Emotional Distress is a self-assessment scale to detect levels of emotional distress. It was designed specifically for the DiaFocus project.

    :param response: Dictionary of Emotional Distress answers.
    :return: Dictionary with emotional distress score.
    """

    b2_1 = response.get("B2-1", 0)
    b2_2 = response.get("B2-2", 0)
    b2_3 = response.get("B2-3", 0)
    b2_4 = response.get("B2-4", 0)
    b2_5 = response.get("B2-5", 0)
    b2_6 = response.get("B2-6", 0)

    total_score = b2_1 + b2_2 + b2_3 + b2_4 + b2_5 + b2_6

    emotional_distress_response = {
        "B2-1": b2_1,
        "B2-2": b2_2,
        "B2-3": b2_3,
        "B2-4": b2_4,
        "B2-5": b2_5,
        "B2-6": b2_6,
        "total_score": total_score,
    }

    return emotional_distress_response
