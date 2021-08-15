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
        change = _change(self.value, total, self.rebalance, percentage)
        output = input.copy()
        output['Change'] = change
        output = _discretize(self.value, output)
        return output

def _change(value: float, total: float, rebalance: bool, percentage: pd.DataFrame):
    change = percentage['Target'] - percentage['Actual']
    if rebalance:
        # amount changed per ticker
        change = change * total
    else:
        # remove opposite transactions
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
