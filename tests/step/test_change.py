from pandas.io import pytables
from compass.step import Change

import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

@pytest.mark.parametrize("value, change", 
                        [(  10., [2, 4]), # exact change
                         (  11., [2, 4]), # round below x.5
                         (   9., [1, 3])]) # round above x.5
def test_first_deposit(value, change):
    data = {
        'Target': [.2, .8],
        'Actual': [0, 0],
        'Price': [1., 2.],
    }
    input = pd.DataFrame(data)
    output = Change(value).run(input)
    data.update({
        'Change': change
    })
    expected = pd.DataFrame(data)
    assert_frame_equal(expected, output)
