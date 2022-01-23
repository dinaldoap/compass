from .base import Pipeline
import pandas as pd
from compass.number import parse_decimal


class Report(Pipeline):
    columns = {
        "Entrada/Saída": "Transaction",  # Credito == deposit and Debito == withdraw
        "Data": "Date",
        "Movimentação": "Type",
        "Produto": "Ticker",
        "Quantidade": "Change",
        "Preço unitário": "Price",
    }

    def run(self):
        df_trans = (
            pd.read_excel("2022.xlsx")
            .pipe(print_df)
            .pipe(lambda df: df[self.columns.keys()])
            .rename(self.columns, axis="columns")
            .pipe(lambda df: df[df["Change"].str.fullmatch(r"\d+")])
            .assign(Change=lambda df: df["Change"].apply(int))
            .pipe(lambda df: df[df["Price"] != "-"])
            .query("Type == 'Transferência - Liquidação'")
            .assign(
                Change=lambda df: (
                    (df["Transaction"] == "Credito")
                    + (df["Transaction"] == "Debito") * -1
                )
                * df["Change"]
            )
            .assign(Ticker=lambda df: df["Ticker"].apply(split_first_trim))
            .pipe(lambda df: df[["Date", "Ticker", "Change", "Price"]])
            .pipe(print_df)
        )


def split_first_trim(text):
    return text.split("-")[0].strip()


def print_df(df):
    # print(df['Price'].unique())
    print(df)
    # print(len(df))
    # print(df.dtypes)
    return df
