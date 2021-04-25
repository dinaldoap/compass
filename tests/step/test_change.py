from pandas.io import pytables
from compass.step import Change

import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

@pytest.mark.parametrize("value, change", 
                        [(  7., [1, 3]), # exact change
                         (  8., [1, 3]), # round below x.5
                         (   6., [0, 2])]) # round above x.5
def test_deposit(value, change):
    data = {
        'Target': [.2, .8],
        'Actual': [1, 1],
        'Price': [1., 2.],
    }
    input = pd.DataFrame(data)
    output = Change(value).run(input)
    data.update({
        'Change': change
    })
    expected = pd.DataFrame(data)
    assert_frame_equal(expected, output)