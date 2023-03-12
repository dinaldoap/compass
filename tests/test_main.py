from pathlib import Path

import pytest
from pytest import MonkeyPatch

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
        "rebalance": False,
        "portfolio": "tests/data/portfolio.xlsx",
        "output": str(output),
        # configuration (compass.ini)
        "expense_ratio": 0.1,
        # default
        "absolute_distance": 0.05,
        "relative_distance": 0.25,
    }


def test_init(tmp_path: Path, monkeypatch: MonkeyPatch):
    monkeypatch.chdir(tmp_path)
    # Files do not exist
    assert not Path("portfolio.xlsx").exists()
    assert not Path("compass.ini").exists()
    main(["init"])
    # Files are initialized
    assert Path("portfolio.xlsx").exists()
    assert Path("compass.ini").exists()
    # Files are valid
    main(["change", "1000"])
    assert Path("output.xlsx").exists()


@pytest.mark.parametrize(
    "file",
    [
        ("portfolio.xlsx"),
        ("compass.ini"),
    ],
)
def test_init_not_overwrite(file, tmp_path: Path, monkeypatch: MonkeyPatch):
    monkeypatch.chdir(tmp_path)
    # Dummy file is initialized
    Path(file).touch()
    dummy_stat = Path(file).stat()
    # File is not overwritten
    main(["init"])
    not_overwritten_stat = Path(file).stat()
    assert dummy_stat == not_overwritten_stat
    # Remove and initialize file
    Path(file).unlink()
    main(["init"])
    init_stat = Path(file).stat()
    assert dummy_stat != init_stat
