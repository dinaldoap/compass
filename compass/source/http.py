from .base import Source

import pandas as pd
from pathlib import Path
import requests
import json


class YahooPrice(Source):
    def __init__(self, directory, target: Source):
        self.directory = directory
        self.target = target

    def read(self):
        prices = []
        tickers = self.target.read()
        tickers = tickers["Ticker"]
        for ticker in tickers:
            try:
                json = _read_file(Path(self.directory, "{}.json".format(ticker)))
            except FileNotFoundError:
                json = _read_http(ticker)
            price = json["chart"]["result"][0]["meta"]["regularMarketPrice"]
            prices.append(price)
        return pd.DataFrame(
            {
                "Ticker": tickers,
                "Price": prices,
            }
        )


def _read_file(path) -> str:
    return json.load(open(path, "r"))


def _read_http(ticker: str) -> str:
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    url = "https://query1.finance.yahoo.com/v8/finance/chart/{}.SA?region=BR&lang=pt-BR&includePrePost=false&interval=1d&useYfid=true&range=1d&corsDomain=br.financas.yahoo.com&.tsrc=finance".format(
        ticker
    )
    response = requests.get(url=url, headers=headers)
    if 200 != response.status_code:
        raise RuntimeError(
            "Status code 200 expected from Yahoo Finance, but received: {}".format(
                response.status_code
            )
        )
    return response.json()
