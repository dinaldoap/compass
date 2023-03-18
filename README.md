<p align="center">
  <a href="https://github.com/dinaldoap/compass"><img src="https://raw.githubusercontent.com/dinaldoap/compass/main/docs/img/logo.png" alt="Compass"></a>
</p>
<p align="center">
    <em>Leading investors to theirs targets.</em>
</p>

# Compass

Compass is a command-line interface that is designed for managing investiment portfolios. More specifically, Compass helps investors doing the following tasks:

* [Portfolio spreadsheet setup](#portfolio-spreadsheet-setup)
* [Deposit](#deposit)
* [Withdraw](#withdraw)
* [Rebalancing](#rebalancing) (with cash flows, sells/buys and tracking error)
* [Grouping assets](#grouping-assets)

# Installation

Requirements:
* [Python](https://www.python.org/) 3.8 or greater

With Python installed, run the command as follows:
```bash
pip install --upgrade compass-investor
```

# Basic usage

### Portfolio spreadsheet setup

Suppose you want to start a 60/40 portfolio, you would type the command as follows:
```bash
compass init
```

Observe the outputs generated by the command above: 
* portfolio.xlsx: The porfolio spreadsheet with fictitious tickers. Please, replace its content with you own portfolio. The column layout is as follows:
    * Name: str, description of the ticker, e.g., iShares Core S&P 500 ETF.
    * Ticker: str, ticker name, e.g., IVV.
    * Target: float, target percentage for the ticker, e.g., 40%.
    * Actual: int, number of owned units of the ticker, e.g., 500.
    * Price: float, current price of the ticker, e.g., $100.
    * Group: str, optional, group of the ticker, e.g., Stocks.
    * Additional columns in the spreadsheet are ignored.
* compass.ini: The configuration with an disabled example. Please, replace its content with your own configuration, and remove the character \'#\' to activate it.

### Deposit

Now, suppose you want to deposit $1000, you would **update the column Price** of the portfolio spreadsheet with current prices, close the spreadsheet, and type the command as follows:

```bash
compass change 1000
```

Observe the output generated by the command above:
* Console output: The transaction values (deposit/withdraw and expenses); and the portfolio added with the columns Change, Before and After.
    * Change corresponds to the amount of units you should buy of each ticker to match the deposit value, $1000.
    * Before corresponds to the portfolio allocation before the deposit.
    * After corresponds to the portfolio allocation after the deposit.
* output.xlsx: A spreadsheet with the same table showed in the console output.

After buying the units of the tickers, you should open the portfolio spreadsheet, **update the column Actual** with the final amount of units of each ticker, and close the spreadsheet. 

### Withdraw

Now, suppose you want to withdraw $1000, you would do the same steps done for a deposit, but with negative values. With that said, the command should be as follows:

```bash
compass change -1000
```

And the output generated by the command above are expected to show **negative** values in the column Change, corresponding to the amount of units you should **sell** of each ticker to match the **withdraw** value, $1000.

# Advanced usage

## Rebalancing

Compass always uses deposits/withdraws (cash flows) to move the portfolio allocation towards the target. However, when the portfolio is relatively big, the cash flow might not be enough to keep the portfolio allocation close to the target. In that case, the investor might deliberately buy and sell assets to rebalance the portfolio. 

Suppose you want to deposit $1000 while rebalancing your portfolio, you would type the command as follows:

```bash
compass change 1000 --rebalance=True
```

In the output, the column Change is expected to show positive and negative values, corresponding to, respectively, buys and sells to move the portfolio allocation towards the target.

Now, suppose you want to do the same deposit and rebalancing with no tracking error, you would type the command as follows:

```bash
compass change 1000 --rebalance=True --absolute-distance=0 --relative-distance=0
```


## Getting prices automatically

If you prefer to get prices automatically instead of typing, you might manage your portfolio on an online spreadsheet app that provides asset prices. The additional complexity is that you will have to download a copy of the porfolio spreasheet to your local disk right before running Compass. The steps are as follows:

* Just once:

    1. Import the portfolio spreasheet to the online spreadsheet app of your choice;
    2. Replace the values in column Price with formulas to get the asset prices automatically.    

* Right before running Compass:
    1. Download the spreadsheet to the local directory in which you have done the portfolio setup;
    2. Run Compass in the same directory.

### Google Sheets

Google Sheets offers the function `GoogleFinance`. Please visit Googhe Sheets [documentation](https://support.google.com/docs/answer/3093281) to get more information.



## Grouping assets

Grouping is a handy feature of Compass, but it is hard to understand it without real examples. So, let's appreciate two common use cases that could get value from grouping assets.

### Risk management

Suppose you want to invest on two ETFs, one for US stocks and another for international stocks, your spreadsheet portfolio would be as follows:

| Name            | Ticker | Price  | Actual | Target | Group |
|-----------------|--------|--------|--------|--------|-------|
| Total market US | TUS    | 100.00 |     50 |    50% |       |
| Internacional   | INT    | 100.00 |     50 |    50% |       |


At some point in time, you decide to overweight US value stocks by adding a new asset to your portfolio. In addition, due to risk management, you want the overall US allocation be limited to 50%. The changes required in the spreadsheet portfolio are as follows:

1. Add a line for VUS;
2. Fill the columns Name, Ticker, Price and Actual;
3. In the column Target, set both VUS and TUS' allocations to 25%;
4. In the column Group, add both VUS and TUS to the group US.



| Name            | Ticker | Price  | Actual | Target | Group |
|-----------------|--------|--------|--------|--------|-------|
| Value US        | VUS    | 100.00 |      0 |    25% | US    |
| Total market US | TUS    | 100.00 |     25 |    25% | US    |
| Internacional   | INT    | 100.00 |     50 |    50% |       |

### Deprecated asset

Suppose that company A offers the ETFs AUS and AIN, on which you invest paying an expense ratio of 0.03%, your spreadsheet portfolio would be as follows:

| Name            | Ticker | Price  | Actual | Target | Group |
|-----------------|--------|--------|--------|--------|-------|
| A US            | AUS    | 100.00 |     10 |    10% |       |
| A Internacional | AIN    | 100.00 |     90 |    90% |       |
  
At some point in time, the competitor B launches the ETF BUS, with the same characteristics, but with an expense ratio of 0.02%. Would you sell all units you have from AUS to buy from BUS? Maybe that will not be necessary, since company A might lower the expense ratio of AUS to 0.02% in response to the launch of BUS. The best option seems to be start buying BUS, and keeping AUS for a while. The changes required in the spreadsheet portfolio are as follows:

1. Add a line for BUS;
2. Fill the columns Name, Ticker, Price and Actual;
3. In the column Target, move the allocation of 10% from AUS to BUS;
4. In the column Group, add both BUS and AUS to the group US.

| Name            | Ticker | Price  | Actual | Target | Group |
|-----------------|--------|--------|--------|--------|-------|
| B US            | BUS    | 100.00 |      0 |    10% | US    |
| A US            | AUS    | 100.00 |     10 |     0% | US    |
| A Internacional | AIN    | 100.00 |     90 |    90% |       |

With that setting, Compass will handle AUS as a deprecated asset. That means that its actual allocation is considered as part of the group allocation when depositing or withdrawing from the portfolio. However, its target allocation is not considered when rebalancing inside the group, since all units would be selled to match the target allocation of 0%. It is up to the investor to decide whether and when to replace the deprecated asset based on changes in the expense ratios of the alternatives.

# Contributing

Compass is free to use, and maintained by volunteers. If you wish to contribute, these are the main options:

* :star: [Star](https://docs.github.com/en/get-started/exploring-projects-on-github/saving-repositories-with-stars#starring-a-repository) the [project repository](https://github.com/dinaldoap/compass) to show people that it is useful;
* :eyes: [Watch](https://docs.github.com/en/get-started/quickstart/be-social#watching-a-repository) the [project repository](https://github.com/dinaldoap/compass) to be informed about new releases;
* :monocle_face: Share the [project home page](https://github.com/dinaldoap/compass#readme) with someone that could benefit from it;
* :handshake: Help and get help on [Q&A discussions](https://github.com/dinaldoap/compass/discussions/categories/q-a);
* :bulb: Share ideas and give feedback on [Ideas discussions](https://github.com/dinaldoap/compass/discussions/categories/ideas);
* :lady_beetle: Report bugs on [Issues](https://github.com/dinaldoap/compass/issues);
* :technologist: Fix issues following the [Developer Guide](https://raw.githubusercontent.com/dinaldoap/compass/main/CONTRIBUTING.md).
* :purple_heart: [Sponsor](https://github.com/sponsors) the project (coming soon).
