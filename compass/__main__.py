"""Main module."""
import argparse
import configparser
import sys

from compass.number import parse_bool, parse_decimal
from compass.pipeline import ChangePosition


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
        epilog="""
                    A single spreadsheet (portolio.xlsx) must be maintained to the basic usage. The expected column layout is as follows:
                    (1) Name: str, description of the ticker, e.g., iShares Core S&P 500 ETF.
                    (2) Ticker: str, ticker name, e.g., IVV.
                    (3) Target: float, target percentage for the ticker, e.g., 40%.
                    (4) Actual: int, number of owned units of the ticker, e.g., 500.
                    (5) Price: float, current price of the ticker, e.g., $100.
                    Additional columns in the spreadsheet are ignored.
                """,
    )
    subparsers = parser.add_subparsers(dest="subcommand")
    subcommands = []
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


def main(argv: list = None):
    """Command-line interface's entrypoint.

    Args:
        argv (list, optional): Argument values. Defaults to None.

    Raises:
        RuntimeError: When subcommand value is not expected.
    """
    if argv is None:
        argv = sys.argv[1:]
    config = _parse_args(argv)
    subcommand = config["subcommand"]
    routes = {
        "change": _run_change,
    }
    if subcommand not in routes:
        raise RuntimeError(f"Subcommad {subcommand} not expected.")
    routes[subcommand](config)


def _run_change(config):
    ChangePosition(config=config).run()


def _add_subcommand_change(subparsers):
    subcommand = "change"
    parser = subparsers.add_parser(subcommand)
    parser.add_argument(
        "value",
        type=parse_decimal,
        help="Value to be deposited (greater than zero) or withdrawed (less than zero). Zero also can be used when only rebalancing is required.",
    )
    parser.add_argument(
        "-r",
        "--rebalance",
        type=parse_bool,
        help="""Allow rebalancing. A rebalancing is done when one distance is exceeded (see --absolute-distance and --relative-distance).
                                                     A rebalancing moves the portfolio up to the point where the exceeded distance goes back to the allowed range  (default: True).""",
        choices=[True, False],
        default=True,
    )
    parser.add_argument(
        "-b",
        "--absolute-distance",
        type=float,
        help="Absolute distance allowed between the actual and the target allocation of each ticker and group (default: 5%%).",
        default=0.05,
    )
    parser.add_argument(
        "-l",
        "--relative-distance",
        type=float,
        help="Relative distance allowed between the actual and the target allocation of each ticker and group (default: 25%%).",
        default=0.25,
    )
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        help="Target of the portfolio in terms of percentages per ticker (default: portfolio.xlsx).",
        default="portfolio.xlsx",
    )
    parser.add_argument(
        "-a",
        "--actual",
        type=str,
        help="Actual portfolio in terms of units per ticker (default: portfolio.xlsx).",
        default="portfolio.xlsx",
    )
    parser.add_argument(
        "-p",
        "--price",
        type=str,
        help="Prices of the tickers (default: portfolio.xlsx).",
        default="portfolio.xlsx",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output with changes to be done per ticker (default: output.xlsx).",
        default="output.xlsx",
    )
    parser.add_argument(
        "-e",
        "--expense-ratio",
        type=float,
        help="Expense ratio (default: 0.03%%).",
        default=0.0003,
    )
    return subcommand


if __name__ == "__main__":
    main()
