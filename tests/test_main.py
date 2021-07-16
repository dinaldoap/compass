from compass.__main__ import run


def test_run():
    run([
        '1,000.00',
        '--target', 'tests/data/portfolio.xlsx',
        '--actual', 'tests/data/portfolio.xlsx',
        '--price', 'tests/data/portfolio.xlsx'
    ])
