from typing import Any, Callable, Dict

from helpers import get_specific_answers_and_comments
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
    simple_response_to_score_map,
)

QUESTTIONNAIRE_IDS = [
    "B1_Lifestyle",
    "B2_EmotionalDistress",
    "C_AreasOfConcern",
    "D1_FoodBehavior",
    "D4_DMAS",
    "WHO5",
    "PSQI",
    "HADS",
]


def process_responses(answers: Dict[str, Any], comments: Dict[str, Any]):
    """ """
    processors: Dict[str, Callable[[Dict[str, Any]], Dict[str, int]]] = {
        "B1_Lifestyle": lambda x: x,  # No processing yet
        "B2_EmotionalDistress": process_emotional_distress_response,
        "C_AreasOfConcern": lambda x: x,  # No processing yet
        "D1_FoodBehavior": process_food_behavior_response,
        "D4_DMAS": lambda x: x,  # No processing yet,
        "WHO5": process_who5_response,
        "PSQI": process_psqi_response,
        "HADS": process_hads_response,
    }

    processed_data = {}

    for questionnaire_id in QUESTTIONNAIRE_IDS:
        answers_specific, comments_specific = get_specific_answers_and_comments(
            questionnaire_id, answers, comments
        )
        process = processors.get(questionnaire_id)
        if process:
            response_score = process(answers_specific)
            processed_data[questionnaire_id] = {
                "answers": answers_specific,
                "comments": comments_specific,
                "scores": response_score,
            }

    return processed_data


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
    overall_score = c1 + c2 + c3 + c4 + c5 + c6 + c7

    psqi_response = {
        "component_scores": {
            "C1_duration": c1,
            "C2_disturbance": c2,
            "C3_latency": c3,
            "C4_day_dysfunction": c4,
            "C5_sleep_efficiency": c5,
            "C6_overall_sleep_quality": c6,
            "C7_medication": c7,
        },
        "overall_score": overall_score,
    }

    return psqi_response


def process_who5_response(response: Dict[str, Any]) -> Dict[str, int]:
    """
    This function processes the responses for a WHO-5 questionnaire.

    The World Health Organization-Five Well-Being Index (WHO-5) is a short self-reported measure of current mental well-being.

    :param response: Dictionary of WHO-5 answers.

    :return: Dictionary with total score and percentage score.
    """

    question_ids = ["Q1", "Q2", "Q3", "Q4", "Q5"]
    answer_range = (1, 5)
    overall_score = simple_response_to_score_map(response, question_ids, answer_range)

    percentage_score = overall_score * 4  # Scale to percentage (0-100)

    who5_response = {
        "overall_score": overall_score,
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
    overall_score = anxiety_score + depression_score

    hads_response = {
        "anxiety_score": anxiety_score,
        "depression_score": depression_score,
        "overall_score": overall_score,
    }

    return hads_response


def process_emotional_distress_response(response: Dict[str, Any]) -> Dict[str, int]:
    """
    This function processes the responses for an Emotional Distress questionnaire.

    The B2 - Emotional Distress is a self-assessment scale to detect levels of emotional distress. It was designed specifically for the DiaFocus project.

    :param response: Dictionary of Emotional Distress answers.
    :return: Dictionary with emotional distress score.
    """

    question_ids = ["B2-1", "B2-2", "B2-3", "B2-4", "B2-5", "B2-6"]
    answer_range = (0, 4)
    overall_score = simple_response_to_score_map(response, question_ids, answer_range)

    emotional_distress_response = {"overall_score": overall_score}

    return emotional_distress_response


def process_food_behavior_response(response: Dict[str, Any]) -> Dict[str, int]:
    """
    This function processes the responses for a Food Behavior questionnaire.

    The D1 - Food Behavior is a self-assessment scale to detect levels of food behavior. It was designed specifically for the DiaFocus project.

    :param response: Dictionary of Food Behavior answers.
    :return: Dictionary with food behavior score.
    """

    question_ids = ["C1-1", "C1-2", "C1-3", "C1-4", "C1-5", "C1-6"]
    answer_range = (0, 4)

    overall_score = simple_response_to_score_map(response, question_ids, answer_range)

    food_behavior_response = {"overall_score": overall_score}

    return food_behavior_response
