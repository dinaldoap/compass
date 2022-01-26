from compass.pipeline import Transaction, Report
from compass.number import parse_bool, parse_decimal

import argparse
import sys
import configparser


def parse_args(argv, file="compass.ini"):
    parser = argparse.ArgumentParser(
        description="Compass: Helping investors to stick with theirs plans.",
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
                                                     A rebalancing moves the portfolio up to the point where the exceeded distance goes back to the allowed range  (default: true).""",
        default="true",
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

    configv_argv = _add_config(argv, file)
    namespace = parser.parse_args(configv_argv)
    args = dict(vars(namespace))
    return args


def _add_config(argv, file):
    config_parser = configparser.ConfigParser()
    config_parser.read(file)
    configv = (
        dict(config_parser["compass"]) if config_parser.has_section("compass") else {}
    )
    configv = configv["compass_args"] if "compass_args" in configv else ""
    configv = configv.split()
    return configv + argv


def main(argv=sys.argv[1:]):
    args = parse_args(argv)
    transaction(args)


def transaction(args):
    Transaction(config=args).run()


def report(config):
    Report(config=config).run()


if __name__ == "__main__":
    main()
