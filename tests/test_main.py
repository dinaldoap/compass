from compass.__main__ import main, parse_args, _run_report, _run_change

from pathlib import Path
import pytest


def test_main():
    with pytest.raises(SystemExit, match="0"):
        main(["--help"])


def test_parse_args_change():
    output = _create_output(".")
    expected_args = _create_config_change(output)
    args = parse_args(
        [
            "change",
            "1,000.00",
            "--target",
            "tests/data/portfolio.xlsx",
            "--actual",
            "tests/data/portfolio.xlsx",
            "--price",
            "tests/data/portfolio.xlsx",
            "--output",
            str(output),
        ],
        "tests/data/compass.ini",
    )
    assert expected_args == args


def test_change(temp_dir):
    output = _create_output(temp_dir)
    _run_change(_create_config_change(output))
    assert output.exists()


def test_parse_args_report():
    output = _create_output(".")
    expected_config = _create_config_report(output)
    args = parse_args(
        [
            "report",
            "--change",
            "tests/data/change",
            "--target",
            "tests/data/target.xlsx",
            "--output",
            str(output),
        ],
        "tests/data/compass.ini",
    )
    assert expected_config == args


def test_report(temp_dir):
    output = Path(temp_dir).joinpath("report.xlsx")
    _run_report(_create_config_report(output))
    assert output.exists()


def _create_output(temp_dir: str):
    output = Path(temp_dir).joinpath("output.xlsx")
    return output


def _create_config_change(output: Path):
    return {
        # command line
        "subcommand": "change",
        "value": 1000.0,
        "rebalance": True,
        "target": "tests/data/portfolio.xlsx",
        "actual": "tests/data/portfolio.xlsx",
        "price": "tests/data/portfolio.xlsx",
        "output": str(output),
        # configuration (compass.ini)
        "expense_ratio": 0.1,
        # default
        "absolute_distance": 0.05,
        "relative_distance": 0.25,
    }


def _create_config_report(output: Path):
    return {
        "subcommand": "report",
        "change": "tests/data/change",
        "target": "tests/data/target.xlsx",
        "output": str(output),
        # configuration (compass.ini)
        "expense_ratio": 0.2,
        # default
        "tax_rate": 0.15,
    }
