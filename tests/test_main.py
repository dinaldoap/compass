from compass.main import run

def test_run():   
    run([
        '100',
        '--source-type', 'default',
        '--source-path', 'tests/data/actual_default.xlsx',
        ])