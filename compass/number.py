import re
from distutils.util import strtobool

from babel import numbers


def parse_bool(text: str):
    return bool(strtobool(text))


def parse_decimal(text: str, locale=numbers.LC_NUMERIC) -> float:
    match = re.search(r"-?[\d,.]+", text)
    if match:
        decimal = match.group(0)
    else:
        decimal = text
    decimal = numbers.parse_decimal(decimal, locale=locale, strict=True)
    decimal = float(decimal)
    return decimal


def format_currency(decimal: float) -> str:
    return numbers.format_currency(decimal, currency="BRL")
