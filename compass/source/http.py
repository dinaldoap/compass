from .base import Source

import numpy as np
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
            price = json['chart']['result'][0]['meta']['regularMarketPrice']
            prices.append(price)
        return pd.DataFrame({
            'Ticker': tickers,
            'Price': prices,
        })


def _read_file(path) -> str:
    return json.load(open(path, 'r'))


def _read_http(ticker: str) -> str:
    response = requests.get(
        'https://query1.finance.yahoo.com/v8/finance/chart/{}.SA?region=BR&lang=pt-BR&includePrePost=false&interval=1d&useYfid=true&range=1d&corsDomain=br.financas.yahoo.com&.tsrc=finance'.format(ticker))
    assert 200 == response.status_code, 'Status code 200 expected from Yahoo Finance, but received: {}'.format(
        response.status_code)
    return response.json()
