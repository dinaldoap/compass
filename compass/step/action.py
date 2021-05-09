from .base import Step

import pandas as pd


class Action(Step):
    def run(self, input: pd.DataFrame):
        output = input.copy()
        output['After'] = (output['Actual'] +
                           output['Change']) * output['Price']
        output['After'] = output['After'] / output['After'].sum()
        output['After'] = output['After'].round(2)
        output.to_excel('data/action.xlsx', index=False)
        return output
