from compass.transact import Deposit
from compass.number import parse_decimal

import argparse
import sys
import configparser


def run(argv):
    parser = argparse.ArgumentParser(
        description='Compass: Helping investors to stick with theirs plans.',
        epilog='''
                    Files that must be maintained in --directory:
                    (1) target.xlsx, with standard layout (Name, Ticker, Target);
                    (2) actual.xlsx, with standard layout (Ticker, Actual) or CEI's layout (Cód. de Negociação, Qtde.);
                    (3) actual.html, with CEI's page (https://cei.b3.com.br/CEI_Responsivo/ConsultarCarteiraAtivos.aspx) or Warren's page showing QUANTIDADE on Meus ativos (https://warren.com.br/app/#/v3/trade)
                    These files can have additional columns beside the specified in the layout.
                ''')
    parser.add_argument('value', type=parse_decimal,
                        help='Value to be deposited (positive number) or withdrawed (negative number). When value is zero, the portfolio is rebalanced.')
    parser.add_argument('-t', '--target', type=str,
                        help='Target of the portfolio in terms of percentages per ticker (default: data/portfolio.xlsx).', default='data/portfolio.xlsx')
    parser.add_argument('-a', '--actual', type=str,
                        help='Actual portfolio in terms of units per ticker (default: data/portfolio.xlsx).', default='data/portfolio.xlsx')
    parser.add_argument('-p', '--price', type=str,
                        help='Prices of the tickers (default: data/portfolio.xlsx).', default='data/portfolio.xlsx')
    parser.add_argument('-o', '--output', type=str,
                        help='Output with changes to be done per ticker (default: data/output.xlsx).', default='data/output.xlsx')
    parser.add_argument('-e', '--expense-ratio', type=float,
                        help='Expense ratio (default: 0.03%%).', default=0.0003)

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
            configv.extend([key, value])
        else:
            configv.append(value)
    return configv + argv


def main():
    run(sys.argv[1:])


if __name__ == '__main__':
    main()
