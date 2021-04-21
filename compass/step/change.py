from .base import Step

import pandas as pd
import numpy as np


class Change(Step):
    '''
    Change in the actual allocation required to approximate the target allocation.

    ...
    '''

    def __init__(self):
        self.value = 50

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
        actual = actual / (actual.sum() + self.value)
        change = target - actual
        assert np.any(
            change > 0), 'Change is expected to have at least one value greater than zero: {}'.format(change)
        change = np.maximum(change, [0.])
        change = change / change.sum()
        change = (self.value * change)
        change = change // price
        change = change.astype(int)
        output = input.copy()
        output['Change'] = change
        return output
