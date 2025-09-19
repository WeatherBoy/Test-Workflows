from typing import Any, Dict, Tuple


def get_specific_answers_and_comments(
    questionnaire_id: str, answers: Dict[str, Any], comments: Dict[str, Any]
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Extract answers and comments for a specific questionnaire ID.

    :param questionnaire_id: The ID of the questionnaire to extract.
    :param answers: Dictionary containing all answers.
    :param comments: Dictionary containing all comments.

    :return: A tuple containing two dictionaries: (answers_specific, comments_specific).
    """
    answers_specific = answers.get(questionnaire_id)
    assert answers_specific is not None, f"No answers found for {questionnaire_id}"

    comments_specific = comments.get(questionnaire_id)
    assert comments_specific is not None, f"No comments found for {questionnaire_id}"

    return answers_specific, comments_specific
