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
