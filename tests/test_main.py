from pathlib import Path

import pytest

from compass.__main__ import _parse_args, _run_change, main


def test_main():
    with pytest.raises(SystemExit, match="0"):
        main(["--help"])


def test_parse_args_change():
    output = _create_output(".")
    expected_args = _create_config_change(output)
    args = _parse_args(
        [
            "change",
            "1,000.00",
            "--portfolio",
            "tests/data/portfolio.xlsx",
            "--output",
            str(output),
        ],
        "tests/data/compass.ini",
    )
    assert expected_args == args


def test_change(tmp_path):
    output = _create_output(tmp_path)
    _run_change(_create_config_change(output))
    assert output.exists()


def _create_output(tmp_path: str):
    output = Path(tmp_path).joinpath("output.xlsx")
    return output


def _create_config_change(output: Path):
    return {
        # command line
        "subcommand": "change",
        "value": 1000.0,
        "rebalance": True,
        "portfolio": "tests/data/portfolio.xlsx",
        "output": str(output),
        # configuration (compass.ini)
        "expense_ratio": 0.1,
        # default
        "absolute_distance": 0.05,
        "relative_distance": 0.25,
    }
