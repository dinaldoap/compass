from compass.__main__ import parse_args, post, transaction

import pandas as pd

_EXPECTED_ARGS = {
    'value': 1000.,
    'rebalance': False,
    'target': 'tests/data/portfolio.xlsx',
    'actual': 'tests/data/portfolio.xlsx',
    'price': 'tests/data/portfolio.xlsx',
    'output': 'data/output.xlsx',
    'expense_ratio': .0003,
    'spread_ratio': 0.,
    'absolute_distance': .05,
    'relative_distance': .25,
}


def test_parse_args():
    args = parse_args([
        '1,000.00',
        '--target', 'tests/data/portfolio.xlsx',
        '--actual', 'tests/data/portfolio.xlsx',
        '--price', 'tests/data/portfolio.xlsx',
        '--output', 'data/output.xlsx',
    ])
    assert _EXPECTED_ARGS == args


def test_transaction():
    transaction(_EXPECTED_ARGS)


def test_post():
    pd.DataFrame(columns=['Ticker', 'Actual']).to_excel(
        'data/actual_added_change.xlsx')
    post({
        'actual': 'data/actual_added_change.xlsx',
        'output': 'tests/data/output.xlsx',
    })
