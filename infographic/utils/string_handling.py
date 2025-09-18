from typing import Any


def split_the_difference(json_response: Any, response_key: str | None) -> float:
    """
    Given a response to a questionnaire loaded from JSON, convert it to a float.

    If the response is a number (int or float), simply convert it to float and return it.
    If the response is a string representing a range (e.g., "15-30"),
    split the range, convert both parts to float, and return their midpoint.
    If the response is invalid (neither a number nor a valid range string),
    raise a ValueError with an appropriate message.

    :param json_response: The response value from the JSON, either a number or a range string (type is `Any`, but for this data it should be either a number or a string).
    :param response_key: Optional key name for error messages.

    :return: The response converted to a float.
    """
    if isinstance(json_response, (int, float)):
        float_response = float(json_response)
    elif isinstance(json_response, str) and "-" in json_response:
        parts = json_response.split("-")
        low = float(parts[0])
        high = float(parts[1])
        float_response = (low + high) / 2.0  # <-- split the difference
    else:
        if response_key:
            raise ValueError(f"Invalid {response_key} value: {json_response!r}")
        else:
            raise ValueError(f"Invalid value: {json_response!r}")

    return float_response
