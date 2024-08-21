import functools
import logging
from datetime import datetime
from os import PathLike
from pathlib import Path
from threading import Lock
from typing import Union

import numpy as np
import pandas as pd
import xarray as xr

from gcviz.utils import timeit

files_locks: dict[Path, Lock] = {}


logger = logging.getLogger("gcviz.netcdf")


def load_with_lock(file: Path) -> xr.Dataset:
    if file not in files_locks:
        files_locks[file] = Lock()

    with files_locks[file]:
        return xr.load_dataset(file)


class NetcdfLoader:
    """Loader class for the netcdf files.

    Read all files in the given directory to know networks, sites, compounds and instruments.



    """

    def __init__(
        self,
        directory: PathLike,
        stem_format: str = "network-instrument_site_compound",
        invalid_value: float | None = None,
    ) -> None:
        d = Path(directory)

        if not d.is_dir():
            raise FileNotFoundError(f"{d} is not a directory")

        self.directory = d

        self.logger = logging.getLogger("gcviz.NetcdfLoader")

        variables = stem_format.split("_") + ["file"]

        data = [f.stem.split("_") + [f] for f in d.rglob("*.nc")]

        bad_data = [d for d in data if len(d) != len(variables)]
        if len(bad_data) > 0:
            self.logger.warning(
                f"Files found that do not match format {stem_format} : {bad_data}"
            )

        data = [d for d in data if len(d) == len(variables)]
        if len(data) == 0:
            self.logger.warning(f"No netcdf files found in {d}")

        self.df_files = pd.DataFrame(data, columns=variables)

        self.sites = self.df_files["site"].unique()
        self.compounds = self.df_files["compound"].unique()
        self.instruments = self.df_files["network-instrument"].unique()

        self.invalid_value = invalid_value

    @timeit
    @functools.lru_cache
    def read_data(
        self,
        site: str,
        compound: str,
        date_interval: tuple[datetime | None, datetime | None] = (None, None),
        met_office_only: bool = False,
        pollution_removed: bool = False,
    ) -> pd.Series | None:
        """Read the data from the netcdf files.

        Parameters
        ----------
        sites : list[str]
            The sites to read.
        compounds : list[str]
            The compounds to read.
        date_interval : tuple[datetime, datetime]
            The date interval to read.

        Returns
        -------
        pd.DataFrame
            The dataframe with the data.
        """
        # Get the files to read
        series = []
        self.logger.info(f"Reading {site=} {compound=} {date_interval=}")

        df_this_files = self.df_files[
            (self.df_files["site"] == site) & (self.df_files["compound"] == compound)
        ]
        if len(df_this_files) == 0:
            self.logger.warning(f"No netcdf file found for {site} {compound}")
            return None

        ds = (
            xr.concat([load_with_lock(f) for f in df_this_files["file"]], dim="time")
            .sortby("time")
            .sel(time=slice(date_interval[0], date_interval[1]))
        )
        # Check length of the data
        if len(ds["time"]) == 0:
            self.logger.warning(
                f"No data found for {site=} {compound=} included in {date_interval=} \n"
                f"Valid times are {ds['time'].values}"
            )
            return None

        mask = np.ones_like(ds["mf"].values, dtype=bool)
        if self.invalid_value is not None:
            mask &= ds["mf"] != self.invalid_value
        if met_office_only:
            if "met_office_baseline_flag" not in ds:
                self.logger.warning(
                    f"No met_office_baseline_flag found for {site=} {compound=}"
                )
            # 66 means 'B' in ascii for baseline
            mask &= ds["met_office_baseline_flag"] == 66

        if pollution_removed:
            if "git_pollution_flag" not in ds:
                self.logger.warning(
                    f"No git_pollution_flag found for {site=} {compound=}"
                )
            # 80 means 'P' in ascii for pollution
            mask &= ds["git_pollution_flag"] != 80

        serie = ds["mf"].loc[mask].to_pandas()
        return serie


class GlobalLoader:
    # Global pointer to the loader
    _loader: NetcdfLoader | None = None

    @classmethod
    def set(cls, loader: NetcdfLoader):
        if cls._loader is not None:
            raise RuntimeError("Global loader already set")
        cls._loader = loader

    @classmethod
    def get(cls) -> NetcdfLoader:
        if cls._loader is None:
            raise RuntimeError("Global loader not set")
        return cls._loader


if __name__ == "__main__":
    loader = NetcdfLoader(r"C:\Users\coli\Documents\Data\gcdata")
    print(loader.df_files)

    print(loader.sites, loader.compounds, loader.instruments)

    df = loader.read_data("ASA", "cfc-12", (datetime(2001, 1, 1), datetime(2023, 1, 2)))
    print(df.head())
