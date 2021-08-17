from .base import Step

import pandas as pd
import numpy as np


class Change(Step):
    '''
    Change in the actual allocation required to approximate the target allocation.

    ...
    '''

    def __init__(self, value, rebalance):
        self.value = value
        self.rebalance = rebalance

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
            levels, self.value, total, self.rebalance, percentage)
        output = input.copy()
        output['Change'] = change
        output = _discretize(self.value, output)
        return output


def _add_group(percentage: pd.DataFrame):
    group = percentage.copy()
    if 'Group' not in group.columns:
        group['Group'] = None
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


def _hierarchy_change(levels: list, value: float, total: float, rebalance: bool, percentage: pd.DataFrame):
    change = pd.Series(index=percentage.index, dtype=np.float64)
    for level in levels:
        if level == 0:
            percentage = _group_change(
                level, value, total, rebalance, percentage)
        else:
            parent_group_column = 'Group_{}'.format(level-1)
            group_percentage = percentage.groupby(parent_group_column)
            percentage = group_percentage.apply(lambda parent_percentage, : _parent_group_change(
                level, total, rebalance, parent_percentage))
        leaf = percentage['Group'] == percentage['Group_{}'.format(level)]
        change.loc[leaf] = percentage.loc[leaf, 'Change_{}'.format(level)]
    return change


def _parent_group_change(level: int, total: float, rebalance: bool, parent_percentage: pd.DataFrame):
    parent_value = parent_percentage['Change_{}'.format(level-1)].iat[0]
    return _group_change(level, parent_value, total, rebalance, parent_percentage)


def _group_change(level: int, value: float, total: float, rebalance: bool, parent_percentage: pd.DataFrame):
    group_column = 'Group_{}'.format(level)
    group_percentage = parent_percentage.groupby(
        group_column).agg({'Target': 'sum', 'Actual': 'sum'})
    group_percentage['Change_{}'.format(level)] = _change(
        value, total, rebalance, group_percentage)
    group_percentage = group_percentage.rename({'Target': 'Target_{}'.format(
        level), 'Actual': 'Actual_{}'.format(level)}, axis='columns')
    group_percentage = parent_percentage.join(
        group_percentage, on=group_column)
    return group_percentage


def _change(value: float, total: float, rebalance: bool, percentage: pd.DataFrame):
    change = percentage['Target'] - percentage['Actual']
    if rebalance:
        # amount changed per ticker
        change = change * total
    else:
        if value != 0:
            # remove opposite changes
            if value > 0:
                change = np.maximum(change, [0.])
            elif value < 0:
                change = np.minimum(change, [0.])
            # redistribute percentages
            change = change / change.sum()
        # amount changed per ticker
        change = (value * change)
    return change


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
