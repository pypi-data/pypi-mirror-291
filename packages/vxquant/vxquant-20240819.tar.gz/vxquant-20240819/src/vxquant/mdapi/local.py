import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Literal, Union, Optional, Dict, List

import polars as pl
from tqdm import tqdm
from vxutils import to_datetime, Datetime
from ..__base import VXCalendar, VXInstruments

from .basic import (
    VXCalendarProvider,
    VXStorageMixin,
    VXDayHistoryProvider,
    VXFactorProvider,
    VXMinHistoryProvider,
    VXInstrumentsProvider,
    VXHistoryProvider,
)


class VXLocalStorage(VXStorageMixin):

    __data_root__: Path = Path().home() / ".data"
    __suffix__: Literal["csv", "parquet"] = "csv"

    @classmethod
    def init_storage(
        cls,
        data_dir: Optional[Path] = None,
        suffix: Optional[Literal["csv", "parquet"]] = None,
    ) -> None:
        cls.__suffix__ = suffix if suffix is not None else "csv"
        if data_dir:
            cls.__data_root__ = Path(data_dir)
        else:
            cls.__data_root__ = Path().home() / ".data"

        cls.__data_root__.mkdir(exist_ok=True, parents=True)

    def save(self, data: pl.DataFrame, identify: str) -> None:

        if self.__suffix__ == "csv":
            data.write_csv(
                self.__data_root__ / f"{identify}.csv",
                date_format="%Y-%m-%d",
                datetime_format="%Y-%m-%d %H:%M:%S",
            )
        else:
            data.write_parquet(
                self.__data_root__ / f"{identify}.parquet",
            )

    def read(self, identify: str) -> pl.DataFrame:

        filename = self.__data_root__ / f"{identify}.{self.__suffix__}"

        if not filename.exists():
            logging.debug(f"File {filename} not exists. ")
            return pl.DataFrame({})

        return (
            pl.read_csv(self.__data_root__ / f"{identify}.csv")
            if self.__suffix__ == "csv"
            else pl.read_parquet(self.__data_root__ / f"{identify}.parquet")
        )

    def clear(self, identify: str) -> None:
        (self.__data_root__ / f"{identify}.{self.__suffix__}").unlink(missing_ok=True)


class VXLocalCalendarProvider(VXCalendarProvider, VXLocalStorage):

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        if data_dir:
            data_dir = Path(data_dir)
        else:
            data_dir = Path().home() / ".data"

        self.init_storage(data_dir, "csv")


class VXLocalInstrumentsProvider(VXInstrumentsProvider, VXLocalStorage):
    def __init__(self, data_dir: Optional[Path] = None) -> None:
        if data_dir:
            data_dir = Path(data_dir) / "instruments"
        else:
            data_dir = Path().home() / ".data/instruments"

        self.init_storage(data_dir, "csv")


class VXLocalDayHistoryProvider(VXDayHistoryProvider, VXLocalStorage):

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        if data_dir:
            data_dir = Path(data_dir) / f"history/{self.__identity__}/"
        else:
            data_dir = Path().home() / f".data/history/{self.__identity__}/"
        self.init_storage(data_dir=data_dir, suffix="parquet")


class VXLocalMinHistoryProvider(VXMinHistoryProvider, VXLocalStorage):

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        if data_dir:
            data_dir = Path(data_dir) / f"history/{self.__identity__}/"
        else:
            data_dir = Path().home() / f".data/history/{self.__identity__}/"

        self.init_storage(data_dir=data_dir, suffix="parquet")


class VXLocalFactorProvider(VXFactorProvider, VXLocalStorage):

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        if data_dir:
            data_dir = Path(data_dir) / "factors"
        else:
            data_dir = Path().home() / ".data/factors"

        self.init_storage(data_dir, "parquet")
