import pytest
from babel.numbers import NumberFormatError

from compass.number import parse_decimal


@pytest.mark.parametrize(
    "text,         decimal",
    [
        ("1,000.00", 1000.0),  # deposit
        ("-1,000.00", -1000.0),  # withdraw
        ("--1,000.00", -1000.0),  # ingored characteres
        ("abc-1,000.00xyz", -1000.0),  # ingored characteres
    ],
)
def test_parse_decimal(text, decimal):
    assert decimal == parse_decimal(text)


@pytest.mark.parametrize(
    "text",
    [
        ("1.000,00"),  # wrong locale
        ("abc"),  # invalid characteres
    ],
)
def test_parse_decimal_error(text):
    with pytest.raises(NumberFormatError):
        parse_decimal(text)
