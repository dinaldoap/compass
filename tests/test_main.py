from compass.main import run

def test_run():   
    run([
        '100',
        '--actual', 'tests/data/actual_default.xlsx',
        ])