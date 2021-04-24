from compass.step import Change

import pandas as pd
from pandas.testing import assert_frame_equal

def test_first_deposit():
    data = {
        'Target': [.2, .8],
        'Actual': [0, 0],
        'Price': [1., 2.],
    }
    input = pd.DataFrame(data)
    output = Change(10.).run(input)
    data.update({
        'Change': [2, 4]
    })
    expected = pd.DataFrame(data)
    assert_frame_equal(expected, output)
