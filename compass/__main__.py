from compass.pipeline import Transaction, Post
from compass.number import parse_bool, parse_decimal

import argparse
import re
import sys
import configparser


def parse_args(argv):
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
                        help='Value to be deposited (greater than zero) or withdrawed (less than zero). Zero also can be used when only rebalancing is required.')
    parser.add_argument('-r', '--rebalance', type=parse_bool,
                        help='''Allow rebalancing. A rebalancing is done when one distance is exceeded (see --absolute-distance and --relative-distance).
                                                     A rebalancing moves the portfolio up to the point where the exceeded distance goes back to the allowed range  (default: true).''', default='true')
    parser.add_argument('-b', '--absolute-distance', type=float,
                        help='Absolute distance allowed between the actual and the target allocation of each ticker and group (default: 5%%).', default=.05)
    parser.add_argument('-l', '--relative-distance', type=float,
                        help='Relative distance allowed between the actual and the target allocation of each ticker and group (default: 25%%).', default=.25)
    parser.add_argument('-t', '--target', type=str,
                        help='Target of the portfolio in terms of percentages per ticker (default: portfolio.xlsx).', default='portfolio.xlsx')
    parser.add_argument('-a', '--actual', type=str,
                        help='Actual portfolio in terms of units per ticker (default: portfolio.xlsx).', default='portfolio.xlsx')
    parser.add_argument('-p', '--price', type=str,
                        help='Prices of the tickers (default: portfolio.xlsx).', default='portfolio.xlsx')
    parser.add_argument('-o', '--output', type=str,
                        help='Output with changes to be done per ticker (default: output.xlsx).', default='output.xlsx')
    parser.add_argument('-e', '--expense-ratio', type=float,
                        help='Expense ratio (default: 0.03%%).', default=0.0003)
    parser.add_argument('-s', '--spread-ratio', type=float,
                        help='Spread ratio (default: 0.00%%).', default=0.)

    configv_argv = _add_config(argv)
    namespace = parser.parse_args(configv_argv)
    args = dict(vars(namespace))
    return args


def _add_config(argv):
    config = configparser.ConfigParser()
    config.read('compass.ini')
    config = dict(config['compass']) if config.has_section('compass') else {}
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


def main(argv=sys.argv[1:]):
    args = parse_args(argv)
    transaction(args)
    input('Press Enter to add Change to Actual or Ctrl+C to cancel...')
    post(args)


def transaction(args):
    Transaction(config=args).run()


def post(args):
    Post(config=args).run()


if __name__ == '__main__':
    main()
