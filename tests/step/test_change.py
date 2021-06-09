from pandas.io import pytables
from compass.step import Change

import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

@pytest.mark.parametrize("value, change", 
                        [(  7., [1, 3]), # exact change
                         (  8., [2, 3]), # round below x.5
                         (   6., [2, 2])]) # round above x.5
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

@pytest.mark.parametrize("value, change", 
                        [(  -9., [-3, -3]), # exact change
                         (  -8., [-2, -3]), # round below x.5
                         (   -7., [-3, -2])]) # round above x.5
def test_withdraw(value, change):
    data = {
        'Target': [.2, .8],
        'Actual': [2, 4],
        'Price': [1., 2.],
    }
    input = pd.DataFrame(data)
    output = Change(value).run(input)
    data.update({
        'Change': change
    })
    expected = pd.DataFrame(data)
    assert_frame_equal(expected, output)

@pytest.mark.parametrize("value, change", 
                        [(  0., [-2, 1]), # exact change
                        ])
def test_rebalance(value, change):
    data = {
        'Target': [.2, .8],
        'Actual': [4, 3],
        'Price': [1., 2.],
    }
    input = pd.DataFrame(data)
    output = Change(value).run(input)
    data.update({
        'Change': change
    })
    expected = pd.DataFrame(data)
    assert_frame_equal(expected, output)