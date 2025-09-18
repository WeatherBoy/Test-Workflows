from typing import Any, Dict


def psqi_c1_duration(psqi_answers: Dict[str, Any]) -> int:
    """
    Compute the duration of sleep (C1) for the PSQI.
    Based on the PSQI scoring guidelines:
    - q4_sleep_hours: reported hours of sleep (can be a number or a range like "6-7")
    Returns an integer score from 0 to 3.
    0: >7 hours
    1: 6-7 hours
    2: 5-6 hours
    3: <5 hours

    Raises ValueError if q4_sleep_hours is missing or invalid.

    :param psqi_answers: Dictionary of PSQI answers.

    :return: Integer score for C1 duration of sleep.
    """
    q4 = psqi_answers.get("q4_sleep_hours")
    if isinstance(q4, (int, float)):
        q4 = float(q4)
    elif isinstance(q4, str) and "-" in q4:
        parts = q4.split("-")
        low = float(parts[0])
        high = float(parts[1])
        q4 = (low + high) / 2.0  # <-- split the difference
    else:
        raise ValueError(f"Invalid q4_sleep_hours value: {q4!r}")

    if q4 >= 7:
        return 0
    elif 6 <= q4 < 7:
        return 1
    elif 5 <= q4 < 6:
        return 2
    elif q4 < 5:
        return 3
    else:
        raise ValueError(f"Invalid q4_sleep_hours value: {q4!r}")


def psqi_c2_disturbance(psqi_answers: Dict[str, Any]) -> int:
    """
    Compute the sleep disturbance score (C2) for the PSQI.
    NOTE: answer q5j have been removed for simplicity.

    Based on the PSQI scoring guidelines:
    - q5b to q5i: frequency of various sleep disturbances:
    0 = Not during the past month,
    1 = Less than once a week,
    2 = Once or twice a week,
    3 = Three or more times a week
    Returns an integer score from 0 to 3.
    0: 0
    1: 1-8
    2: 9-16
    3: 17-24

    Raises ValueError if any of q5b to q5i are missing or invalid.

    :param psqi_answers: Dictionary of PSQI answers.

    :return: Integer score for C2 sleep disturbance.
    """
    disturbance_questions = [
        "q5b",
        "q5c",
        "q5d",
        "q5e",
        "q5f",
        "q5g",
        "q5h",
        "q5i",
    ]
    total_score = 0
    for q in disturbance_questions:
        val = psqi_answers.get(q)
        if isinstance(val, str) and val.isdigit():
            val = int(val)
        if val is None or not isinstance(val, int) or val < 0 or val > 3:
            raise ValueError(f"Invalid {q} value: {val!r}")
        total_score += val

    if total_score == 0:
        return 0
    elif 1 <= total_score <= 8:
        return 1
    elif 9 <= total_score <= 16:
        return 2
    elif 17 <= total_score <= 24:
        return 3
    else:
        raise ValueError(f"Invalid total disturbance score: {total_score!r}")
