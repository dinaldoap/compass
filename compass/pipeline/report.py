"""Report pipeline."""
from compass import source, target
from compass.step import (
    HistoricPrint,
    HistoricReport,
    Join,
    MonthPrint,
    ReadSource,
    YearPrint,
)

from .base import Pipeline


class Report(Pipeline):
    def __init__(self, config):
        self.config = config

    def run(self):
        steps = [
            ReadSource(source=source.create_change(config=self.config)),
            Join(
                source=source.create_target(config=self.config),
                on="Ticker",
                add=["Name"],
                how="inner",
            ),
            HistoricReport(
                expense_ratio=self.config["expense_ratio"],
                tax_rate=self.config["tax_rate"],
            ),
            HistoricPrint(
                target=target.create_output(config=self.config, sheet_name="Change")
            ),
            MonthPrint(
                target=target.create_output(
                    config=self.config, sheet_name="Month", append=True
                )
            ),
            YearPrint(
                target=target.create_output(
                    config=self.config, sheet_name="Year", append=True
                )
            ),
        ]
        data = None
        for step in steps:
            data = step.run(input=data)
