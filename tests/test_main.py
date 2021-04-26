from compass.main import run

def test_run():   
    run([
        '100',
        '--directory', 'tests/data',
        ])