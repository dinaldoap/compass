import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from compass.step import Change


@pytest.mark.parametrize(
    "group,         value, change",
    [
        ([None, None], 7.0, [1, 3]),  # exact change
        (["A", None], 8.0, [1, 3]),  # round below x.5
        (["A/a", "B"], 6.0, [0, 2]),  # round above x.5
        (["A/B/C", None], 7.0, [1, 3]),  # level with no group parent
    ],
)
def test_deposit(group, value, change):
    data = {
        "Group": group,
        "Ticker": ["BITO39", "BIEF39"],
        "Target": [0.2, 0.8],
        "Actual": [1, 1],
        "Price": [1.0, 2.0],
    }
    input = pd.DataFrame(data)
    output = Change(value, False).run(input)
    data.update({"Change": change})
    expected = pd.DataFrame(data)
    assert_frame_equal(expected, output)


@pytest.mark.parametrize(
    "group,         value, change",
    [
        ([None, None], -9.0, [-1, -3]),  # exact change
        (["A", None], -8.0, [-1, -3]),  # round below x.5
        (["A/a", "B"], -7.0, [-1, -2]),  # round above x.5
    ],
)
def test_withdraw(group, value, change):
    data = {
        "Group": group,
        "Ticker": ["BITO39", "BIEF39"],
        "Target": [0.2, 0.8],
        "Actual": [2, 4],
        "Price": [1.0, 2.0],
    }
    input = pd.DataFrame(data)
    output = Change(value, False).run(input)
    data.update({"Change": change})
    expected = pd.DataFrame(data)
    assert_frame_equal(expected, output)


@pytest.mark.parametrize(
    "actual, target, group,         value, abs_dist, rel_dist,     change",
    [
        # BITO40 is sold for rebalancing outside group A, but not inside since only BITO39 has a target
        ([0, 10, 0], [0.2, 0.0, 0.8], ["A", "A", None], 0.0, 0.0, 0.0, [0, -8, 8]),
        # Value is used to buy BIEF39. Then, BITO40 is sold for rebalancing outside group A, but not inside since only BITO39 has a target
        ([0, 8, 0], [0.2, 0.0, 0.8], ["A", "A", None], 2.0, 0.0, 0.0, [0, -6, 8]),
        # BITO40 is sold for rebalancing inside group A
        ([0, 2, 8], [0.1, 0.1, 0.8], ["A", "A", None], 0.0, 0.0, 0.0, [1, -1, 0]),
        # Rebalancing is done to the allowed absolute distance range inside and outside group A
        ([1, 8, 1], [0.3, 0.1, 0.6], ["A", "A", None], 0.0, 0.1, 0.0, [2, -6, 4]),
        # No rebalancing is done due to the allowed absolute distance range
        ([0, 4, 6], [0.2, 0.2, 0.6], ["A", "A", None], 0.0, 0.2, 0.0, [0, 0, 0]),
        # No rebalancing is done due to the allowed relative distance range
        ([1, 1, 8], [0.2, 0.2, 0.6], ["A", "A", None], 0.0, 0.0, 0.5, [0, 0, 0]),
    ],
)
def test_rebalance(actual, target, group, value, abs_dist, rel_dist, change):
    data = {
        "Group": group,
        # BITO40 is a legacy ETF grouped with BITO39
        "Ticker": ["BITO39", "BITO40", "BIEF39"],
        "Target": target,
        # There are 3 BITO40, but only 2 will be sold for rebalancing
        "Actual": actual,
        "Price": [1.0, 1.0, 1.0],
    }
    input = pd.DataFrame(data)
    output = Change(value, True, abs_dist, rel_dist).run(input)
    data.update({"Change": change})
    expected = pd.DataFrame(data)
    assert_frame_equal(expected, output)


@pytest.mark.parametrize(
    "group,            value, change",
    [
        (["A", "B", "B"], 4.0, [2, 1, 0]),  # exact change
        (["A", "B", "B"], -10.0, [0, -1, -8]),  # exact change
    ],
)
def test_group(group, value, change):
    data = {
        "Group": group,
        "Ticker": ["BITO39", "BIEF39", "BIEF40"],
        "Target": [0.2, 0.8, 0.0],
        "Actual": [2, 8, 8],
        "Price": [1.0, 1.0, 1.0],
    }
    input = pd.DataFrame(data)
    output = Change(value, False).run(input)
    data.update({"Change": change})
    expected = pd.DataFrame(data)
    assert_frame_equal(expected, output)
