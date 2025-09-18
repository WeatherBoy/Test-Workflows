from typing import Any


def valid_and_digit(
    json_response: Any, lower_bound: int, upper_bound: int, response_key: str | None
) -> int:
    """
    Given a response to a questionnaire loaded from JSON, convert it to an int.

    If the response is a whole number, simply convert it to int and return it.
    If the response is a string representing a digit (e.g., "2"),
    convert it to int and return it.
    If the response is invalid (neither a number nor a valid digit string),
    raise a ValueError with an appropriate message.

    :param json_response: The response value from the JSON, either a number or a digit string (type is `Any`, but for this data it should be either a number or a string).
    :param lower_bound: The minimum valid integer value (inclusive).
    :param upper_bound: The maximum valid integer value (inclusive).
    :param response_key: Optional key name for error messages.

    :return: The response converted to an int.
    """
    if response_key is None:
        response_key = ""

    if isinstance(json_response, int):
        int_response = int(json_response)
    elif isinstance(json_response, str) and json_response.isdigit():
        int_response = int(json_response)
    elif isinstance(json_response, (float, int)) and (
        json_response < lower_bound or json_response > upper_bound
    ):
        raise ValueError(
            f"Invalid {response_key} value. Out of range [{lower_bound}-{upper_bound}]: {json_response!r}"
        )
    else:
        raise ValueError(f"Invalid {response_key} value: {json_response!r}")

    return int_response


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
    if response_key is None:
        response_key = ""

    if isinstance(json_response, (int, float)):
        float_response = float(json_response)
    elif isinstance(json_response, str) and "-" in json_response:
        parts = json_response.split("-")
        low = float(parts[0])
        high = float(parts[1])
        float_response = (low + high) / 2.0  # <-- split the difference
    else:
        raise ValueError(f"Invalid {response_key} value: {json_response!r}")

    return float_response
