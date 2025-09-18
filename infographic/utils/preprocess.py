from typing import Any, Dict, Tuple


def split_answers_and_comments(
    responses: Dict[str, Any],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Split a flat dictionary of responses into answers and comments.
    Assumes the structure of `responses` is as follows:
    {
        "questionnaires": {
            "PSQI": {
                "q1_bedtime": "22:30-23:00",
                "q2_sleep_latency_min": {"answer": 15, "comment": "Usually takes me 15 minutes"},
                ...
            },
            "OtherQuestionnaire": {
                ...
            }
        }
    }
    """
    # Top layer keys are the questionnaire IDs
    # Second layer keys are the question IDs with values being either a literal answer or a comment (str)
    answers: Dict[str, Dict[str, Any]] = {}
    comments: Dict[str, Dict[str, str | None]] = {}

    questionnaires = responses.get("questionnaires", {})

    for questionnaire_id, questionnaire in questionnaires.items():
        questionnaire_answers = {}
        questionnaire_comments = {}
        for question, answer in questionnaire.items():
            if isinstance(answer, dict):
                # answer is of type `dict`, then it's split into a literal answer and a comment
                answer_literal = answer.get("answer")
                comment = answer.get("comment")
                questionnaire_answers[question] = answer_literal
                questionnaire_comments[question] = comment
            else:
                # answer is a literal value
                questionnaire_answers[question] = answer
                questionnaire_comments[question] = None

        answers[questionnaire_id] = questionnaire_answers
        comments[questionnaire_id] = questionnaire_comments

    return answers, comments
