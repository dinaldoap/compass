"""Change step."""

import functools as ft

import numpy as np
import pandas as pd

from compass.exception import CompassException

from .base import Step


class Change(Step):
    """Step which calculates the change required in the actual allocation to
    move it towards the target allocation."""

    def __init__(self, value, rebalance, absolute_distance=0.0, relative_distance=0.0):
        self.value = value
        self.rebalance = rebalance
        self.absolute_distance = absolute_distance
        self.relative_distance = relative_distance

    def run(self, input_: pd.DataFrame):
        """Calculate the change.

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
        """
        percentage = input_.copy()
        percentage["Actual"] = percentage["Actual"] * percentage["Price"]
        total = percentage["Actual"].sum() + self.value
        if total <= 0:
            raise CompassException(
                "Calculations aborted. They are not required since this change ends up with no wealth."
            )
        percentage["Actual"] = percentage["Actual"] / total
        percentage = _add_group(percentage)
        percentage, levels = _add_hierarchy(percentage)
        change = _hierarchy_change(
            levels,
            self.value,
            total,
            self.rebalance,
            self.absolute_distance,
            self.relative_distance,
            percentage,
        )
        output = input_.copy()
        output["Change"] = change.round(2)
        output = _discretize(output)
        return output


def _add_group(percentage: pd.DataFrame):
    group = percentage.copy()
    has_group = ~group["Group"].isna()
    group.loc[has_group, "Group"] = (
        group.loc[has_group, "Group"] + "/" + group.loc[has_group, "Ticker"]
    )
    group.loc[~has_group, "Group"] = group.loc[~has_group, "Ticker"]
    return group


def _add_hierarchy(percentage: pd.DataFrame):
    hierarchy = percentage["Group"].str.split("/", expand=True)
    levels = hierarchy.columns
    for level in levels[1:]:
        has_level = ~hierarchy[level].isna()
        hierarchy.loc[has_level, level] = (
            hierarchy.loc[has_level, level - 1] + "/" + hierarchy.loc[has_level, level]
        )
    hierarchy.columns = map(lambda column: f"Group_{column}", hierarchy.columns)
    hierarchy = pd.concat([percentage, hierarchy], axis="columns")
    return hierarchy, levels


def _hierarchy_change(
    levels: list,
    value: float,
    total: float,
    rebalance: bool,
    absolute_distance: float,
    relative_distance: float,
    percentage: pd.DataFrame,
):  # pylint: disable=too-many-arguments
    change = pd.Series(index=percentage.index, dtype=np.float64)
    for level in levels:
        if level == 0:
            percentage = _group_change(
                level,
                value,
                total,
                rebalance,
                absolute_distance,
                relative_distance,
                percentage,
            )
        else:
            parent_group_column = f"Group_{level - 1}"
            group_percentage = percentage.groupby(
                parent_group_column, dropna=False, group_keys=False
            )
            # freeze some arguments of _parent_group_change
            _parent_group_change_partial = ft.partial(
                _parent_group_change,
                level,
                total,
                rebalance,
                absolute_distance,
                relative_distance,
            )
            # apply _parent_group_change_partial, with freezed arguments, to each DataFrameGroup
            percentage = group_percentage.apply(
                _parent_group_change_partial, include_groups=False
            )
        leaf = percentage["Group"] == percentage[f"Group_{level}"]
        change.loc[leaf] = percentage.loc[leaf, f"Change_{level}"]
    return change


def _parent_group_change(
    level: int,
    total: float,
    rebalance: bool,
    absolute_distance: float,
    relative_distance: float,
    parent_percentage: pd.DataFrame,
):  # pylint: disable=too-many-arguments
    parent_value = parent_percentage[f"Change_{level - 1}"].iat[0]
    multiple_targets = (parent_percentage["Target"] > 0).sum() > 1
    parent_rebalance = rebalance and multiple_targets
    return _group_change(
        level,
        parent_value,
        total,
        parent_rebalance,
        absolute_distance,
        relative_distance,
        parent_percentage,
    )


def _group_change(
    level: int,
    value: float,
    total: float,
    rebalance: bool,
    absolute_distance: float,
    relative_distance: float,
    parent_percentage: pd.DataFrame,
):  # pylint: disable=too-many-arguments
    group_column = f"Group_{level}"
    group_percentage = parent_percentage.groupby(group_column).agg(
        {"Target": "sum", "Actual": "sum"}
    )
    group_percentage[f"Change_{level}"] = _change(
        value, total, rebalance, absolute_distance, relative_distance, group_percentage
    )
    group_percentage = group_percentage.rename(
        {"Target": f"Target_{level}", "Actual": f"Actual_{level}"},
        axis="columns",
    )
    group_percentage = parent_percentage.join(group_percentage, on=group_column)
    return group_percentage


def _change(
    value: float,
    total: float,
    rebalance: bool,
    absolute_distance: float,
    relative_distance: float,
    percentage: pd.DataFrame,
):
    # percentage per ticker
    target = percentage["Target"].copy()
    actual = percentage["Actual"].copy()
    # amount changed per ticker
    accum_change = pd.Series(np.zeros(len(target)), index=target.index)

    # deposit or withdraw
    if value != 0:
        change = target - actual
        # remove opposite changes
        if value > 0:
            change = np.maximum(change, [0.0])
        elif value < 0:
            change = np.minimum(change, [0.0])
        # redistribute percentages
        change = change / change.sum()
        # amount changed per ticker
        change = value * change
    else:
        change = pd.Series(np.zeros(len(target)), index=target.index)

    accum_change += change
    actual = actual + change / total

    # rebalancing
    if rebalance:
        # allowed range
        greatest_distance = np.maximum(absolute_distance, target * relative_distance)
        min_target = np.maximum(target - greatest_distance, 0.0)
        max_target = np.minimum(target + greatest_distance, 1.0)
        # step to go back to allowed range per ticker
        step_to_range = (actual < min_target) * (min_target - actual)
        step_to_range += (max_target < actual) * (max_target - actual)
        if (step_to_range != 0).any():
            # percentages relative to group
            change = _normalize(target) - _normalize(actual)
            # greatest step
            greatest_step_index = np.argmax(np.abs(step_to_range))
            # divide by actual so that the step become relative to group
            greatest_step = step_to_range.iloc[greatest_step_index] / actual.sum()
            # step and change are relative to group
            scale_factor = greatest_step / change.iloc[greatest_step_index]
            # move to the nearest point inside the range
            change = scale_factor * change
            # amount changed per ticker
            change = (actual.sum() * total) * change
        else:
            change = pd.Series(np.zeros(len(target)), index=target.index)
    else:
        change = pd.Series(np.zeros(len(target)), index=target.index)

    accum_change += change
    return accum_change


def _normalize(input_: np.ndarray):
    return input_ / input_.sum()


def _discretize(input_: pd.DataFrame):
    output = input_.copy()
    price = output["Price"].values
    change = output["Change"].values
    # units per ticker without overflow
    deposit = change > 0
    withdraw = change < 0
    # avoid overflow
    change[deposit] = np.floor(change[deposit] / price[deposit])
    change[withdraw] = np.ceil(change[withdraw] / price[withdraw])
    change = change.astype(int)
    output["Change"] = change
    return output
