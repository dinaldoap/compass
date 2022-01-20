from compass.number import parse_decimal


def test_parse_decimal():
    assert 1000.0 == parse_decimal("1,000.00")
    assert -1000.0 == parse_decimal("-1,000.00")
