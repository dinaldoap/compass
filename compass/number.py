from babel import numbers
import re


def parse_decimal(text: str, locale=numbers.LC_NUMERIC) -> float:
    match = re.search(r'[\d,.]+', text)
    if match:
        decimal = match.group(0)
        decimal = numbers.parse_decimal(decimal, locale=locale, strict=True)
        decimal = float(decimal)
        return decimal
    return None


def format_currency(decimal: float) -> str:
    return numbers.format_currency(decimal, currency='BRL')
