from compass.__main__ import main, post


def test_main():
    main([
        '1,000.00',
        '--target', 'tests/data/portfolio.xlsx',
        '--actual', 'tests/data/portfolio.xlsx',
        '--price', 'tests/data/portfolio.xlsx',
        '--output', 'data/output.xlsx'
    ])


def test_post():
    post([
        '1,000.00',
        '--target', 'tests/data/portfolio.xlsx',
        '--actual', 'data/actual_added_change.xlsx',
        '--price', 'tests/data/portfolio.xlsx',
        '--output', 'tests/data/output.xlsx'
    ])
