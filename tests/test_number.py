import pytest
from babel.numbers import NumberFormatError

from compass.exception import CompassException
from compass.number import parse_bool, parse_decimal


@pytest.mark.parametrize(
    "text,         bool_",
    [
        ("True", True),  #
        ("False", False),  #
    ],
)
def test_parse_bool(text, bool_):
    assert bool_ == parse_bool(text)


@pytest.mark.parametrize(
    "text",
    [
        ("true"),  # wrong first latter case
        ("false"),  #
        ("1"),  # number
        ("0"),  #
    ],
)
def test_parse_bool_error(text):
    with pytest.raises(ValueError):
        parse_bool(text)


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
