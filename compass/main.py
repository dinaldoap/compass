from compass.transact import Deposit

import argparse
import sys


def run(argv):
    parser = argparse.ArgumentParser(
        description='Compass: Helping investors to stick with theirs plans.',
        epilog='''
                    Files that must be maintained in --directory: (1) target.xlsx, with standard layout (Name, Ticker, Target); (2) actual.xlsx, with standard layout (Ticker, Actual) or CEI layout (Cód. de Negociação, Qtde.).
                    These files can have additional columns beside the specified in the layout.
                ''')
    parser.add_argument('value', type=float, help='Value of the deposit.')
    parser.add_argument('-d', '--directory', required=True, type=str,
                        help='Directory of the portfolio (default: data).', default='data')
    namespace = parser.parse_args(argv)
    args = dict(vars(namespace))
    Deposit(config=args).run()


def main():
    run(sys.argv[1:])


if __name__ == '__main__':
    main()
