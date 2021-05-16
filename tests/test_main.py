from compass.main import run

def test_run():   
    run([
        '1,000.00',
        '--directory', 'tests/data',
        ])