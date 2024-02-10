"""Main module."""

import argparse
import configparser
import logging
import sys
from pathlib import Path

from compass.exception import CompassException
from compass.number import parse_bool, parse_decimal
from compass.pipeline import ChangePosition, InitPipeline
from compass.version import __version__


def _parse_args(argv: list, file="compass.ini") -> dict:
    """Parse arguments of the command-line interface.

    Args:
        argv (list): Argument values.
        file (str, optional): Configuration file. Defaults to "compass.ini".

    Returns:
        dict: Configuration.
    """
    parser = argparse.ArgumentParser(
        description="Compass: Leading investors to theirs targets.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    subcommands = []
    subcommands.append(_add_subcommand_init(subparsers))
    subcommands.append(_add_subcommand_change(subparsers))

    configv_argv = _add_config(argv, file, subcommands)
    namespace = parser.parse_args(configv_argv)
    config = dict(vars(namespace))
    return config


def _add_config(argv: list, file: str, subcommands: list):
    if len(argv) == 0 or argv[0] not in subcommands:
        return argv
    subcommand = argv[0]
    subcommand_config = f"{subcommand}_args"
    config_parser = configparser.ConfigParser()
    config_parser.read(file)
    configv = (
        dict(config_parser["compass"]) if config_parser.has_section("compass") else {}
    )
    configv = configv[subcommand_config] if subcommand_config in configv else ""
    configv = configv.split()
    return argv[:1] + configv + argv[1:]


def main(argv: list[str] | None = None):
    """Command-line interface's entrypoint.

    Args:
        argv (list, optional): Argument values. Defaults to None.
    """
    try:
        _run_main(argv)
    except CompassException as ex:
        print(ex)
    # Handle unexpected exceptions with a proper error message
    except Exception as ex:  # pylint: disable=broad-exception-caught
        logging.exception(ex)
        print(
            "Please visit https://github.com/dinaldoap/compass/issues/new to open an issue with the error log above."
        )


def _run_main(argv: list | None = None):
    if argv is None:
        argv = sys.argv[1:]
    config = _parse_args(argv)
    subcommand = config["subcommand"]
    routes = {
        "init": _run_init,
        "change": _run_change,
    }
    if subcommand not in routes:
        raise NotImplementedError(f"Route not implemented for subcommand {subcommand}.")
    routes[subcommand](config)


def _run_init(config):
    if Path("compass.ini").exists():
        print("compass.ini already exists.")
    else:
        _init_config()
    if Path(config["output"]).exists():
        print(f'{config["output"]} already exists.')
    else:
        InitPipeline(config=config).run()


def _init_config():
    configuration = "[compass]\n#change_args=--expense-ratio=0.0 --rebalance=False\n"
    with open("compass.ini", mode="w", encoding="utf-8") as fout:
        fout.write(configuration)


def _run_change(config):
    ChangePosition(config=config).run()


def _add_subcommand_init(subparsers):
    subcommand = "init"
    parser = subparsers.add_parser(
        subcommand,
        help="Initialize portfolio spreadsheat (portfolio.xlsx) and configuration (compass.ini).",
        epilog="""
                    The porfolio spreadsheet (portfolio.xlsx) is initialized with fictitious tickers. Please, replace its content with your own portfolio.
                    And, the configuration (compass.ini) is initialized with an disabled example. Please, replace its content with your own configuration, and remove the character \'#\' to activate it.
                """,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="The portfolio spreadsheet (default: portfolio.xlsx).",
        default="portfolio.xlsx",
    )
    return subcommand


def _add_subcommand_change(subparsers):
    subcommand = "change"
    parser = subparsers.add_parser(
        subcommand,
        help="Calculate how many units to buy/sell per ticker in order to move the portfolio towards the target. The basic inputs are the deposit/withdraw value and the portfolio spreadsheet.",
        epilog="""
                    The deposit/withdraw value (e.g., 1000) and the porfolio spreadsheet (e.g., --portfolio=portolio.xlsx) must be passed as inputs to the basic usage. The expected column layout is as follows:
                    (1) Name: str, description of the ticker, e.g., iShares Core S&P 500 ETF.
                    (2) Ticker: str, ticker name, e.g., IVV.
                    (3) Target: float, target percentage for the ticker, e.g., 40%.
                    (4) Actual: int, number of owned units of the ticker, e.g., 500.
                    (5) Price: float, current price of the ticker, e.g., $100.
                    (6) Group: str, optional, group of the ticker, e.g., Stocks.
                    Additional columns in the spreadsheet are ignored.
                """,
    )
    parser.add_argument(
        "value",
        type=parse_decimal,
        help="Value to be deposited (greater than zero) or withdrawed (less than zero). Zero also can be used when only rebalancing is required.",
    )
    parser.add_argument(
        "-r",
        "--rebalance",
        type=parse_bool,
        help="""Activate/deactivate rebalancing. When True and the tracking error exceeds the allowed range (see --absolute-distance and --relative-distance), a rebalancing is done in order to move the portfolio back to the allowed range of tracking error. When False, only cash flows (deposits and withdraws) are used to balance the portfolio (default: False).""",
        choices=[True, False],
        default=False,
    )
    parser.add_argument(
        "-b",
        "--absolute-distance",
        type=float,
        help="Absolute distance allowed between the actual and the target allocation of each ticker and group (default: 0.05).",
        default=0.05,
    )
    parser.add_argument(
        "-l",
        "--relative-distance",
        type=float,
        help="Relative distance allowed between the actual and the target allocation of each ticker and group (default: 0.25).",
        default=0.25,
    )
    parser.add_argument(
        "-p",
        "--portfolio",
        type=str,
        help="Portfolio with target percentage, actual units and price per ticker (default: portfolio.xlsx).",
        default="portfolio.xlsx",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Spreadsheet with changes to be done per ticker (default: output.xlsx).",
        default="output.xlsx",
    )
    parser.add_argument(
        "-e",
        "--expense-ratio",
        type=float,
        help="Expense ratio (default: 0.0).",
        default=0.0,
    )
    return subcommand


if __name__ == "__main__":
    main()
