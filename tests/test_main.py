from compass.__main__ import main


def test_main():
    main([
        '1,000.00',
        '--target', 'tests/data/portfolio.xlsx',
        '--actual', 'tests/data/portfolio.xlsx',
        '--price', 'tests/data/portfolio.xlsx',
        '--output', 'data/output.xlsx'
    ])
