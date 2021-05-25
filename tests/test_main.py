from compass.__main__ import run

def test_run():   
    run([
        '1,000.00',
        '--directory', 'tests/data',
        '--decay_factor', '.9998'
        ])