"""Number utility functions."""

import re

from babel import numbers


def parse_bool(text: str):
    """Convert text to bool.

    Args:
        text (str): Textual value.

    Raises:
        CompassException: when 'text' is neither 'True' or 'False'.

    Returns:
        _type_: True, when 'text' is 'True';
                False, when 'text' is 'False'.
    """
    if text == "True":
        return True
    if text == "False":
        return False
    raise ValueError(f"Value {text} not valid as boolean. Use True or False instead.")


def parse_decimal(text: str, locale=numbers.LC_NUMERIC) -> float:
    """Convert text to float.

    Args:
        text (str): Textual value.
        locale (_type_, optional): _description_. Defaults to numbers.LC_NUMERIC.

    Returns:
        float: Float value.
    """
    match = re.search(r"-?[\d,.]+", text)
    decimal = match.group(0) if match else text
    decimal = numbers.parse_decimal(decimal, locale=locale, strict=True)
    decimal = float(decimal)
    return decimal


def format_currency(decimal: float) -> str:
    """Convert float to text and format as currency.

    Args:
        decimal (float): Float value.

    Returns:
        str: Textual value.
    """
    return numbers.format_currency(decimal, currency="BRL")
