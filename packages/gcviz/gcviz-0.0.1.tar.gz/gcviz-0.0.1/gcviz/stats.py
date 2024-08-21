import logging
from enum import StrEnum

import numpy as np
import pandas as pd
from pybaselines import Baseline

from gcviz.utils import timeit


class Statistics(StrEnum):
    """Class to define the statistics to calculate."""

    EVENT = "events"
    MEAN_YEARS = "annual-means"
    MEAN_MOUNTHS = "mounthly-means"
    MEAN_WEEKS = "weekly-means"
    MEAN_DAYS = "daily-means"
    MEAN_HOURS = "hourly-means"


mean_resamplers = {
    Statistics.MEAN_YEARS: "YE",
    Statistics.MEAN_MOUNTHS: "ME",
    Statistics.MEAN_WEEKS: "W",
    Statistics.MEAN_DAYS: "D",
    Statistics.MEAN_HOURS: "h",
}


class TimeAverageType(StrEnum):
    HOUR_OF_DAY = "hour of day"
    DAY_OF_WEEK = "day of week"
    MONTH_OF_YEAR = "month of year"


groupping = {
    TimeAverageType.HOUR_OF_DAY: "hour",
    TimeAverageType.DAY_OF_WEEK: "dayofweek",
    TimeAverageType.MONTH_OF_YEAR: "month",
}

x_ticks = {
    TimeAverageType.HOUR_OF_DAY: {i: f"{i}:00" for i in range(24)},
    TimeAverageType.DAY_OF_WEEK: {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday",
    },
    TimeAverageType.MONTH_OF_YEAR: {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    },
}


def apply_statistics(data: pd.Series, statistic: Statistics) -> pd.Series | None:
    """Apply the statistic to the data.

    Parameters
    ----------
    data : pd.DataFrame
        The data to apply the statistic.
    statistic : Statistics
        The statistic to apply.

    Returns
    -------
    pd.Series
        The series with the statistic.
    """
    match statistic:
        case Statistics.EVENT:
            return data
        case (
            Statistics.MEAN_YEARS
            | Statistics.MEAN_MOUNTHS
            | Statistics.MEAN_WEEKS
            | Statistics.MEAN_DAYS
            | Statistics.MEAN_HOURS
        ):
            return data.resample(mean_resamplers[statistic]).mean()
        case _:
            raise ValueError(f"Statistic {statistic} not implemented.")


@timeit
def fit_baseline(serie: pd.Series) -> pd.Series | None:
    """Fit a baseline to the serie.

    Parameters
    ----------
    serie : pd.Series
        The serie to fit.

    Returns
    -------
    pd.Series
        The baseline fitted to the serie.
    """

    logger = logging.getLogger(__name__)

    mask = ~np.isnan(serie.values)
    if mask.sum() <= 10:
        logger.debug(f"Not enough data for baseline.")
        return

    # Convert the date time to integer as required by the baseline function
    x_baseline = serie[mask].index.astype("int64") * 1e-9

    baseline_fitter = Baseline(x_baseline, check_finite=False)
    y_baseline, _ = baseline_fitter.pspline_arpls(serie[mask], lam=10)

    return pd.Series(y_baseline, index=serie[mask].index)
