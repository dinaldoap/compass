from .base import Step

import pandas as pd
import numpy as np


class Change(Step):
    '''
    Change in the actual allocation required to approximate the target allocation.

    ...
    '''

    def __init__(self, value, rebalance, absolute_distance=0., relative_distance=0.):
        self.value = value
        self.rebalance = rebalance
        self.absolute_distance = absolute_distance
        self.relative_distance = relative_distance

    def run(self, input: pd.DataFrame):
        '''Calculate the change.

        Parameters
        ----------
        input : pandas.DataFrame
            DataFrame with the following columns:
                Target : float
                    Fraction of the wealth that must be allocated in the asset.
                Actual : int
                    Number of asset's units currently owned.
                Price : float
                    Curent price of the asset.                

        Returns
        -------
        pandas.DataFrame    
            DataFrame with the same columns of ``input`` and the following columns:
                Change : int
                    Number of asset's units to buy or sell represented, repectivelly, by a positive or negative value.

        '''
        percentage = input.copy()
        percentage['Actual'] = percentage['Actual'] * percentage['Price']
        total = percentage['Actual'].sum() + self.value
        assert total > 0, 'Full withdraw not supported.'
        percentage['Actual'] = percentage['Actual'] / total
        percentage = _add_group(percentage)
        percentage, levels = _add_hierarchy(percentage)
        change = _hierarchy_change(
            levels, self.value, total, self.rebalance, self.absolute_distance, self.relative_distance, percentage)
        output = input.copy()
        output['Change'] = change
        output = _discretize(self.value, output)
        return output


def _add_group(percentage: pd.DataFrame):
    group = percentage.copy()
    has_group = ~pd.isna(group['Group'])
    group.loc[has_group, 'Group'] = group.loc[has_group,
                                              'Group'] + '/' + group.loc[has_group, 'Ticker']
    group.loc[~has_group, 'Group'] = group.loc[~has_group, 'Ticker']
    return group


def _add_hierarchy(percentage: pd.DataFrame):
    hierarchy = percentage['Group'].str.split('/', expand=True)
    levels = hierarchy.columns
    for level in levels[1:]:
        has_level = ~pd.isna(hierarchy[level])
        hierarchy.loc[has_level, level] = hierarchy.loc[has_level,
                                                        level-1] + '/' + hierarchy.loc[has_level, level]
    hierarchy.columns = map(
        lambda column: 'Group_{}'.format(column), hierarchy.columns)
    hierarchy = pd.concat([percentage, hierarchy], axis='columns')
    return hierarchy, levels


def _hierarchy_change(levels: list, value: float, total: float, rebalance: bool, absolute_distance: float, relative_distance: float, percentage: pd.DataFrame):
    change = pd.Series(index=percentage.index, dtype=np.float64)
    for level in levels:
        if level == 0:
            percentage = _group_change(
                level, value, total, rebalance, absolute_distance, relative_distance, percentage)
        else:
            parent_group_column = 'Group_{}'.format(level-1)
            group_percentage = percentage.groupby(parent_group_column)
            percentage = group_percentage.apply(lambda parent_percentage, : _parent_group_change(
                level, total, rebalance, absolute_distance, relative_distance, parent_percentage))
        leaf = percentage['Group'] == percentage['Group_{}'.format(level)]
        change.loc[leaf] = percentage.loc[leaf, 'Change_{}'.format(level)]
    return change


def _parent_group_change(level: int, total: float, rebalance: bool, absolute_distance: float, relative_distance: float, parent_percentage: pd.DataFrame):
    parent_value = parent_percentage['Change_{}'.format(level-1)].iat[0]
    multiple_targets = (parent_percentage['Target'] > 0).sum() > 1
    parent_rebalance = rebalance and multiple_targets
    return _group_change(level, parent_value, total, parent_rebalance, absolute_distance, relative_distance, parent_percentage)


def _group_change(level: int, value: float, total: float, rebalance: bool, absolute_distance: float, relative_distance: float, parent_percentage: pd.DataFrame):
    group_column = 'Group_{}'.format(level)
    group_percentage = parent_percentage.groupby(
        group_column).agg({'Target': 'sum', 'Actual': 'sum'})
    group_percentage['Change_{}'.format(level)] = _change(
        value, total, rebalance, absolute_distance, relative_distance, group_percentage)
    group_percentage = group_percentage.rename({'Target': 'Target_{}'.format(
        level), 'Actual': 'Actual_{}'.format(level)}, axis='columns')
    group_percentage = parent_percentage.join(
        group_percentage, on=group_column)
    return group_percentage


def _change(value: float, total: float, rebalance: bool, absolute_distance: float, relative_distance: float, percentage: pd.DataFrame):
    # percentage per ticker
    target = percentage['Target'].copy()
    actual = percentage['Actual'].copy()
    # amount changed per ticker
    accum_change = pd.Series(np.zeros(len(target)), index=target.index)

    # deposit or withdraw
    if value != 0:
        change = target - actual
        # remove opposite changes
        if value > 0:
            change = np.maximum(change, [0.])
        elif value < 0:
            change = np.minimum(change, [0.])
        # redistribute percentages
        change = change / change.sum()
        # amount changed per ticker
        change = value * change
    else:
        change = pd.Series(np.zeros(len(target)), index=target.index)

    accum_change += change
    actual = actual + change / total

    # rebalancing
    if rebalance:
        change = target - actual
        # allowed range
        greatest_distance = np.maximum(
            absolute_distance, target * relative_distance)
        min_target = target - greatest_distance
        max_target = target + greatest_distance
        # step to go back to allowed range per ticker
        step_to_range = (actual < min_target) * (min_target - actual)
        step_to_range += (max_target < actual) * (max_target - actual)
        if (step_to_range != 0).any():
            not_zero = (change != 0)
            step_to_range[not_zero] /= change[not_zero]
            assert (step_to_range >= 0).all(
            ), 'All steps are expected to be positive.'
            # greatest step
            greatest_step_index = np.argmax(step_to_range)
            greatest_step = step_to_range[greatest_step_index]
            # move to the nearest point inside the range
            change = greatest_step * change
            # amount changed per ticker
            change += total * change
        else:
            change = pd.Series(np.zeros(len(target)), index=target.index)
    else:
        change = pd.Series(np.zeros(len(target)), index=target.index)

    accum_change += change
    return accum_change


def _discretize(value: float, input: pd.DataFrame):
    output = input.copy()
    price = output['Price'].values
    change = output['Change'].values
    # units per ticker without overflow
    deposit = change > 0
    withdraw = change < 0
    # avoid overflow
    change[deposit] = np.floor(change[deposit] / price[deposit])
    change[withdraw] = np.ceil(change[withdraw] / price[withdraw])
    remainder = value - (change * price).sum()
    # use one ticker to approximate the value
    ticker = _choose_ticker(price, remainder)
    remainder = np.floor(remainder / price[ticker])
    change[ticker] = change[ticker] + remainder
    change = change.astype(int)
    output['Change'] = change
    return output


def _choose_ticker(price: np.array, remainder):
    # ticker that leaves less remainder
    choice = remainder % price
    choice = np.argmin(choice)
    return choice
