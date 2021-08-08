from compass.transact import Deposit
from compass.number import parse_decimal

import argparse
import re
import sys
import configparser


def run(argv):
    parser = argparse.ArgumentParser(
        description='Compass: Helping investors to stick with theirs plans.',
        epilog='''
                    A single spreadsheet (portolio.xlsx) must be maintained to the basic usage. The expected column layout is as follows:
                    (1) Name: str, description of the ticker, e.g., iShares Core S&P 500 ETF.
                    (2) Ticker: str, ticker name, e.g., IVV.
                    (3) Target: float, target percentage for the ticker, e.g., 40%.
                    (4) Actual: int, number of owned units of the ticker, e.g., 500.
                    (5) Price: float, current price of the ticker, e.g., $100.
                    Additional columns in the spreadsheet are ignored.
                ''')
    parser.add_argument('value', type=parse_decimal,
                        help='Value to be deposited (positive number) or withdrawed (negative number). When value is zero, the portfolio is rebalanced.')
    parser.add_argument('-t', '--target', type=str,
                        help='Target of the portfolio in terms of percentages per ticker (default: data/portfolio.xlsx).', default='data/portfolio.xlsx')
    parser.add_argument('-a', '--actual', type=str, nargs='+',
                        help='Actual portfolio in terms of units per ticker (default: data/portfolio.xlsx).', default='data/portfolio.xlsx')
    parser.add_argument('-p', '--price', type=str,
                        help='Prices of the tickers (default: data/portfolio.xlsx).', default='data/portfolio.xlsx')
    parser.add_argument('-o', '--output', type=str,
                        help='Output with changes to be done per ticker (default: data/output.xlsx).', default='data/output.xlsx')
    parser.add_argument('-e', '--expense-ratio', type=float,
                        help='Expense ratio (default: 0.03%%).', default=0.0003)
    parser.add_argument('-s', '--spread-ratio', type=float,
                        help='Spread ratio (default: 0.00%%).', default=0.)

    configv_argv = _add_config(argv)
    namespace = parser.parse_args(configv_argv)
    args = dict(vars(namespace))
    Deposit(config=args).run()


def _add_config(argv):
    config = configparser.ConfigParser()
    config.read('data/config.ini')
    config = dict(config['compass'])
    configv = []
    for (key, value) in config.items():
        if key.startswith('--'):
            configv.extend([key] + _split_by_whitspace(value))
        else:
            configv.append(_split_by_whitspace(value))
    return configv + argv


def _split_by_whitspace(value: str):
    if re.match(r'".*"', value) or re.match(r"'.*'", value):
        return [value]
    else:
        return value.split(' ')


def main():
    run(sys.argv[1:])


if __name__ == '__main__':
    main()
