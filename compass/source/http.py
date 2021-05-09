from .base import Source

import pandas as pd
from pathlib import Path
import requests
import json


class YahooPrice(Source):

    def __init__(self, directory):
        self.directory = directory

    def read(self, tickers):
        prices = []
        for ticker in tickers:
            try:
                json = _read_file(
                    Path(self.directory, '{}.json'.format(ticker)))
            except FileNotFoundError:
                json = _read_http(ticker)
            price = _mean_price(json)
            prices.append(price)
        return pd.DataFrame({
            'Ticker': tickers,
            'Price': prices,
        })


def _mean_price(json):
    indicators = {}
    for indicator in ['low', 'open', 'high', 'close']:
        indicators.update(
            {indicator: json['chart']['result'][0]['indicators']['quote'][0][indicator]})
    price = pd.DataFrame(indicators)
    price = price.dropna()
    decay_factor = .9998
    price['weight'] = decay_factor ** price.index
    candle_price = price[['low', 'open', 'high', 'close']].mean(axis='columns')
    price = (candle_price * price['weight']).sum() / price['weight'].sum()
    return price.round(2)


def _read_file(path) -> str:
    return json.load(open(path, 'r'))


def _read_http(ticker: str) -> str:
    response = requests.get(
        'https://query1.finance.yahoo.com/v8/finance/chart/{}.SA?region=BR&lang=pt-BR&includePrePost=false&interval=1m&useYfid=true&range=7d&corsDomain=br.financas.yahoo.com&.tsrc=finance'.format(ticker))
    assert 200 == response.status_code, 'Status code 200 expected from Yahoo Finance, but received: {}'.format(
        response.status_code)
    return response.json()
