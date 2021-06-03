from .base import Step

import pandas as pd
import numpy as np


class Change(Step):
    '''
    Change in the actual allocation required to approximate the target allocation.

    ...
    '''

    def __init__(self, value):
        self.value = value

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
        target = input['Target'].values
        actual = input['Actual'].values
        price = input['Price'].values
        actual = actual * price
        total = actual.sum() + self.value
        assert total > 0, 'Full withdraw not supported.'
        actual = actual / total
        change = target - actual
        if self.value == 0:
            # amount changed per ticker
            change = change * total
        else:
            # remove opposite transactions
            if self.value > 0:
                change = np.maximum(change, [0.])
            elif self.value < 0:
                change = np.minimum(change, [0.])
            # redistribute percentages
            change = change / change.sum()
            # amount changed per ticker
            change = (self.value * change)
        # units per ticker without overflow
        deposit = change > 0
        withdraw = change < 0
        # avoid overflow
        change[deposit] = np.floor(change[deposit] / price[deposit])
        change[withdraw] = np.ceil(change[withdraw] / price[withdraw])
        remainder = self.value - (change * price).sum()
        remainder = np.sign(self.value) * remainder
        # use one ticker to approximate the value
        ticker = _choose_ticker(change, price, remainder)
        remainder = np.floor(remainder / price[ticker])
        remainder = np.sign(self.value) * remainder
        change[ticker] = change[ticker] + remainder
        change = change.astype(int)
        output = input.copy()
        output['Change'] = change
        return output


def _choose_ticker(change: np.array, price: np.array, remainder):
    # prioritize changed tickers
    mask = change != 0
    mask = mask if np.any(mask) else np.array([True] * len(mask))
    index = np.array(range(len(change)))
    # ticker that leaves less remainder
    choice = remainder % price
    choice = np.argmin(choice[mask])
    choice = index[mask][choice]
    return choice
