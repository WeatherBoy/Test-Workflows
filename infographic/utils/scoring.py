from typing import Any, Dict

from string_handling import split_the_difference, valid_and_digit


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
    q4_key = "q4_sleep_hours"
    q4 = psqi_answers.get(q4_key)
    q4 = split_the_difference(q4, q4_key)

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
        "q5b_wake_during_night",
        "q5c_bathroom",
        "q5d_cant_breathe",
        "q5e_snore",
        "q5f_cold",
        "q5g_hot",
        "q5h_bad_dreams",
        "q5i_pain",
    ]
    total_score = 0
    for q in disturbance_questions:
        val = psqi_answers.get(q)
        val = valid_and_digit(val, 0, 3, q)
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


def psqi_c3_latency(psqi_answers: Dict[str, Any]) -> int:
    """
    Compute the sleep latency score (C3) for the PSQI.
    Based on the PSQI scoring guidelines:
    - q2_sleep_latency_min: minutes to fall asleep (can be a number or a range like "15-30")
    - q5a: frequency of having trouble falling asleep within 30 minutes:
        0 = Not during the past month,
        1 = Less than once a week,
        2 = Once or twice a week,
        3 = Three or more times a week
    Returns an integer score from 0 to 3. Based on q2 and q5a combined.

    Raises ValueError if q2_sleep_latency_min or q5a are missing or invalid.

    :param psqi_answers: Dictionary of PSQI answers.

    :return: Integer score for C3 sleep latency.
    """
    q2_key = "q2_sleep_latency_min"
    q2 = psqi_answers.get(q2_key)
    q2 = split_the_difference(q2, q2_key)

    q5a_key = "q5a_cant_sleep_30min"
    q5a = psqi_answers.get(q5a_key)
    q5a = valid_and_digit(q5a, 0, 3, q5a_key)

    q2new = None
    if 0 <= q2 <= 15:
        q2new = 0
    elif 15 < q2 <= 30:
        q2new = 1
    elif 30 < q2 <= 60:
        q2new = 2
    elif q2 > 60:
        q2new = 3
    else:
        raise ValueError(f"Invalid q2_sleep_latency_min value: {q2!r}")

    if q5a + q2new == 0:
        return 0
    elif 1 <= q5a + q2new <= 2:
        return 1
    elif 3 <= q5a + q2new <= 4:
        return 2
    elif 5 <= q5a + q2new <= 6:
        return 3
    else:
        raise ValueError(f"Invalid q2_sleep_latency_min or q5a values: {q2!r}, {q5a!r}")


def psqi_c4_day_dysfunction(psqi_answers: Dict[str, Any]) -> int:
    """
    Compute the daytime dysfunction score (C4) for the PSQI.
    Based on the PSQI scoring guidelines:
    - q8: frequency of having trouble staying awake during the day:
        0 = Not during the past month,
        1 = Less than once a week,
        2 = Once or twice a week,
        3 = Three or more times a week
    - q9: quantity of trouble keeping up enthusiasm to get things done:
        0 = No problem at all,
        1 = Only a very slight problem,
        2 = Somewhat of a problem,
        3 = A very big problem
    Returns an integer score from 0 to 3. Based on q8 and q9 combined.
    Raises ValueError if q8 or q9 are missing or invalid.

    :param psqi_answers: Dictionary of PSQI answers.

    :return: Integer score for C4 daytime dysfunction.
    """

    q8_key = "q8_trouble_staying_awake"
    q8 = psqi_answers.get(q8_key)
    q8 = valid_and_digit(q8, 0, 3, q8_key)

    q9_key = "q9_low_enthusiasm"
    q9 = psqi_answers.get(q9_key)
    q9 = valid_and_digit(q9, 0, 3, q9_key)

    total_score = q8 + q9

    if total_score == 0:
        return 0
    elif 1 <= total_score <= 2:
        return 1
    elif 3 <= total_score <= 4:
        return 2
    elif 5 <= total_score <= 6:
        return 3
    else:
        raise ValueError(f"Invalid total day dysfunction score: {total_score!r}")
