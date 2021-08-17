from pandas.io import pytables
from compass.step import Change

import pandas as pd
from pandas.testing import assert_frame_equal
import pytest


@pytest.mark.parametrize("group,         value, change", [
                         ([None,  None], 7.,    [1, 3]),  # exact change
                         (['A',   None], 8.,    [2, 3]),  # round below x.5
                         (['A/a', 'B'], 6.,    [2, 2]),  # round above x.5
                         ])
def test_deposit(group, value, change):
    data = {
        'Group': group,
        'Ticker': ['BITO39', 'BIEF39'],
        'Target': [.2, .8],
        'Actual': [1, 1],
        'Price': [1., 2.],
    }
    input = pd.DataFrame(data)
    output = Change(value, False).run(input)
    data.update({
        'Change': change
    })
    expected = pd.DataFrame(data)
    assert_frame_equal(expected, output)


@pytest.mark.parametrize("group,         value, change", [
                         ([None,  None], -9.,   [-3, -3]),  # exact change
                         (['A',   None], -8.,   [-2, -3]),  # round below x.5
                         (['A/a', 'B'], -7.,   [-3, -2]),  # round above x.5
                         ])
def test_withdraw(group, value, change):
    data = {
        'Group': group,
        'Ticker': ['BITO39', 'BIEF39'],
        'Target': [.2, .8],
        'Actual': [2, 4],
        'Price': [1., 2.],
    }
    input = pd.DataFrame(data)
    output = Change(value, False).run(input)
    data.update({
        'Change': change
    })
    expected = pd.DataFrame(data)
    assert_frame_equal(expected, output)


@pytest.mark.parametrize("value, change", [
                         (0.,    [-2, 1]),  # exact change
                         ])
def test_rebalance(value, change):
    data = {
        'Ticker': ['BITO39', 'BIEF39'],
        'Target': [.2, .8],
        'Actual': [4, 3],
        'Price': [1., 2.],
    }
    input = pd.DataFrame(data)
    output = Change(value, True).run(input)
    data.update({
        'Change': change
    })
    expected = pd.DataFrame(data)
    assert_frame_equal(expected, output)


@pytest.mark.parametrize("group,            value, change", [
                         (['A',  'B', 'B'],   4.,  [3,  1,  0]),  # exact change
                         (['A',  'B', 'B'], -10.,  [-1, -1, -8]),  # exact change
                         ])
def test_group(group, value, change):
    data = {
        'Group': group,
        'Ticker': ['BITO39', 'BIEF39', 'BIEF40'],
        'Target': [.2, .8, .0],
        'Actual': [2,  8,  8],
        'Price':  [1., 1., 1.],
    }
    input = pd.DataFrame(data)
    output = Change(value, False).run(input)
    data.update({
        'Change': change
    })
    expected = pd.DataFrame(data)
    assert_frame_equal(expected, output)
