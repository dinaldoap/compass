from compass.__main__ import parse_args, transaction, _add_config

_EXPECTED_ARGS = {
    # command line
    "value": 1000.0,
    "rebalance": True,
    "target": "tests/data/portfolio.xlsx",
    "actual": "tests/data/portfolio.xlsx",
    "price": "tests/data/portfolio.xlsx",
    "output": "data/output.xlsx",
    # configuration (compass.ini)
    "expense_ratio": 0.1,
    "spread_ratio": 0.2,
    # default
    "absolute_distance": 0.05,
    "relative_distance": 0.25,
}


def test_parse_args():
    args = parse_args(
        [
            "1,000.00",
            "--target",
            "tests/data/portfolio.xlsx",
            "--actual",
            "tests/data/portfolio.xlsx",
            "--price",
            "tests/data/portfolio.xlsx",
            "--output",
            "data/output.xlsx",
        ],
        "tests/data/compass.ini",
    )
    assert _EXPECTED_ARGS == args


def test_transaction():
    transaction(_EXPECTED_ARGS)
