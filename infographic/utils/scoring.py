from typing import Any, Dict

from utils.string_handling import (
    split_the_difference,
    split_the_difference_datetime,
    valid_and_digit,
)


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


def psqi_c5_sleep_efficiency(psqi_answers: Dict[str, Any]) -> int:
    """
    Compute the sleep efficiency score (C5) for the PSQI.
    Based on the PSQI scoring guidelines:
    - q1_bedtime: reported usual bedtime (e.g., "23:00-23:30")
    - q3_wake_time: reported usual wake time (e.g., "07:00-07:30")
    - q4_sleep_hours: reported hours of sleep (can be a number or a range like "6-7")
    Returns an integer score from 0 to 3.
        0: >=85%
        1: 75-84%
        2: 65-74%
        3: <65%

    Raises ValueError if any of q1, q3, or q4 are missing or invalid.

    :param psqi_answers: Dictionary of PSQI answers.

    :return: Integer score for C5 sleep efficiency.
    """

    q1_key = "q1_bedtime"
    q1 = psqi_answers.get(q1_key)
    bedtime = split_the_difference_datetime(q1, q1_key)

    q3_key = "q3_wake_time"
    q3 = psqi_answers.get(q3_key)
    waketime = split_the_difference_datetime(q3, q3_key)

    # Now we have the bed time and wake time as datetime objects we must find the absolute difference in hours
    total_time_in_bed_hours = (waketime - bedtime).total_seconds() / 3600.0
    assert 0 < total_time_in_bed_hours <= 24, (
        f"Invalid time in bed: {total_time_in_bed_hours!r}"
    )

    q4_key = "q4_sleep_hours"
    q4 = psqi_answers.get(q4_key)
    hours_slept = split_the_difference(q4, q4_key)

    sleep_efficiency = (hours_slept / total_time_in_bed_hours) * 100.0

    if sleep_efficiency >= 85.0:
        return 0
    elif 75.0 <= sleep_efficiency < 85.0:
        return 1
    elif 65.0 <= sleep_efficiency < 75.0:
        return 2
    elif sleep_efficiency < 65.0:
        return 3
    else:
        raise ValueError(f"Invalid sleep efficiency value: {sleep_efficiency!r}")


def psqi_c6_overall_sleep_quality(psqi_answers: Dict[str, Any]) -> int:
    """
    Compute the overall sleep quality score (C6) for the PSQI.
    Based on the PSQI scoring guidelines:
    - q6: self-rated overall sleep quality:
        0 = Very good,
        1 = Fairly good,
        2 = Fairly bad,
        3 = Very bad
    Returns an integer score from 0 to 3.

    Raises ValueError if q6 is missing or invalid.

    :param psqi_answers: Dictionary of PSQI answers.

    :return: Integer score for C6 overall sleep quality.
    """

    q6_key = "q6_overall_quality"
    q6 = psqi_answers.get(q6_key)
    q6 = valid_and_digit(q6, 0, 3, q6_key)

    return q6


def psqi_c7_medication(psqi_answers: Dict[str, Any]) -> int:
    """
    Compute the use of sleep medication score (C7) for the PSQI.
    Based on the PSQI scoring guidelines:
    - q7: frequency of using sleep medication:
        0 = Not during the past month,
        1 = Less than once a week,
        2 = Once or twice a week,
        3 = Three or more times a week
    Returns an integer score from 0 to 3.

    Raises ValueError if q7 is missing or invalid.

    :param psqi_answers: Dictionary of PSQI answers.

    :return: Integer score for C7 use of sleep medication.
    """

    q7_key = "q7_sleep_medication"
    q7 = psqi_answers.get(q7_key)
    q7 = valid_and_digit(q7, 0, 3, q7_key)

    return q7


def hads_anxiety(hads_answers: Dict[str, Any]) -> int:
    """
    Compute the HADS Anxiety score.
    Based on the HADS scoring guidelines:
    - HADS-A consists of 7 questions (A1, A2, A3, A4, A5, A6, A7).
    Each question is scored from 0 to 3.
        0: Not at all
        1: Some of the time
        2: Most of the time
        3: Yes, all of the time
    For a total score ranging from 0 to 21. A higher score indicates greater anxiety.
    NOTE: Question A4 is reverse scored.

    Raises ValueError if any of the HADS-A questions are missing or invalid.

    :param hads_answers: Dictionary of HADS answers.

    :return: Integer score for HADS Anxiety.
    """
    anxiety_questions = ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]
    total_score = 0
    for q in anxiety_questions:
        val = hads_answers.get(q)
        val = valid_and_digit(val, 0, 3, q)
        if q == "A4":
            # Reverse score A4
            val = 3 - val
        total_score += val

    return total_score


def hads_depression(hads_answers: Dict[str, Any]) -> int:
    """
    Compute the HADS Depression score.
    Based on the HADS scoring guidelines:
    - HADS-D consists of 7 questions (D1, D2, D3, D4, D5, D6, D7).
    Each question is scored from 0 to 3.
        0: Not at all
        1: Some of the time
        2: Most of the time
        3: Yes, all of the time
    For a total score ranging from 0 to 21. A higher score indicates greater depressive tendencies.
    NOTE: (The entire HADS-D is reversed.. almost) Questions D1, D2, D3, D6, D7 are reverse scored.

    Raises ValueError if any of the HADS-D questions are missing or invalid.

    :param hads_answers: Dictionary of HADS answers.

    :return: Integer score for HADS Depression.
    """
    depression_questions = ["D1", "D2", "D3", "D4", "D5", "D6", "D7"]
    total_score = 0
    for q in depression_questions:
        val = hads_answers.get(q)
        val = valid_and_digit(val, 0, 3, q)
        if q in ["D1", "D2", "D3", "D6", "D7"]:
            # scored reverse
            val = 3 - val
        total_score += val

    return total_score


def danish_medicine_adherence_scale(dmas_answers: Dict[str, Any]) -> float:
    """
    Compute the Danish Medicine Adherence Scale (DMAS) score.
    NOTE: this is by far the least straightforward instrument and worst documented.

    Based on the DMAS scoring guidelines:
    - The DMAS consists of 7 questions (D4-1 to D4-7).
    - Questions D4-1, D4-2, D4-3, and D4-6 are binary (yes/no) questions where "yes" = 1 point and "no" = 0 points.
    - Question D4-4 is a frequency question with 5 options:
        "never" = 0 points
        "rarely" = 1 point
        "sometimes" = 2 points
        "usually" = 3 points
        "always" = 4 points
    This score is then scaled to a 0-1 range by dividing by 4.
    - Questions D4-5 and D4-7 are open-ended questions and are not scored.
    The total DMAS score is the sum of the points from the binary questions and the scaled frequency question.

    Raises ValueError if any of the DMAS questions are missing or invalid.

    :param dmas_answers: Dictionary of DMAS answers.

    :return: Float score for DMAS (0.0 to 5.0).
    """
    binary_questions = ["D4-1", "D4-2", "D4-3", "D4-6"]

    total_score = 0

    # Each "yes" in the binary questions adds 1 point
    for question in binary_questions:
        answer = dmas_answers.get(question)
        assert isinstance(answer, str), (
            f"Invalid answer type for {question}: {answer!r}, expected str"
        )
        answer = answer.lower()
        assert answer in ["yes", "no"], (
            f"Invalid answer for {question}: {answer!r}, expected 'yes' or 'no'"
        )
        if answer == "yes":
            total_score += 1

    # D4-4 is a frequency question with 5 options
    d4_4_answer = dmas_answers.get("D4-4")
    assert isinstance(d4_4_answer, str), (
        f"Invalid answer type for D4-4: {d4_4_answer!r}, expected str"
    )
    d4_4_answer = d4_4_answer.lower()
    assert d4_4_answer in ["never", "rarely", "sometimes", "usually", "always"], (
        f"Invalid answer for D4-4: {d4_4_answer!r}, expected one of 'never', 'rarely', 'sometimes', 'usually', 'always'"
    )
    d4_4_score_map = {
        "never": 0,
        "rarely": 1,
        "sometimes": 2,
        "usually": 3,
        "always": 4,
    }
    total_score += d4_4_score_map[d4_4_answer] / 4  # get to scale of 0-1

    return total_score


def simple_response_to_score_map(
    answers: Dict[str, Any], questions: list[str], answer_range: tuple[int, int]
) -> int:
    """
    Compute a simple total score for a questionnaire where each question has the same scoring range.
    Each question is scored within the provided answer_range (inclusive).
    Raises ValueError if any of the questions are missing or invalid.

    :param answers: Dictionary of questionnaire answers.
    :param questions: List of question IDs to include in the score.
    :param answer_range: Tuple of (min, max) valid integer values for each question.

    :return: Integer total score for the questionnaire.
    """
    total_score = 0

    low_val, high_val = answer_range
    for question_id in questions:
        val = answers.get(question_id)
        val = valid_and_digit(val, low_val, high_val, question_id)
        total_score += val

    return total_score
