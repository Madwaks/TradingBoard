import logging
import math
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

import pandas as pd
from dateutil import parser
from injector import singleton, inject

from core.services.factories.company import CompanyFactory
from core.services.factories.quote import QuoteFactory
from crypto.models.pair import Pair
from crypto.services.client import BinanceClient

logger = logging.getLogger("django")


@singleton
class PairsImporter:
    @inject
    def __init__(self, client: BinanceClient, company_factory: CompanyFactory):
        self._client = client
        self._company_factory = company_factory

    def build_all_pairs(self):
        data = self._client.get_exchange_info()
        symbols = data["symbols"]
        pairs = [self._build_pair(symbol_info) for symbol_info in symbols]
        self._save_pairs(pairs)

    def _build_pair(self, symbol_info: dict[str, Any]):
        return Pair(
            symbol=symbol_info.get("symbol"),
            base_asset=symbol_info.get("baseAsset"),
            quote_asset=symbol_info.get("quoteAsset"),
            order_types=symbol_info.get("orderTypes"),
        )

    def _save_pairs(self, list_pairs: list[Pair]):
        for pair in list_pairs:
            pair.save()


class TimeUnits(Enum):
    minutes1 = "1m"
    minutes3 = "3m"
    minutes5 = "5m"
    minutes15 = "15m"
    minutes30 = "30m"
    HOUR1 = "1h"
    HOUR2 = "2h"
    HOUR4 = "4h"
    HOUR6 = "6h"
    HOUR8 = "8h"
    HOUR12 = "12h"
    DAY1 = "1d"
    DAY3 = "3d"
    WEEK1 = "1w"
    MONTH1 = "1M"

    @classmethod
    def from_code(cls, code: str):
        for c_type in cls:
            if c_type.value == code:
                return c_type
        return None

    @property
    def binsize(self):
        return self.time_to_binsize[self.value]

    @property
    def time_to_binsize(self):
        return {
            self.minutes1.value: 1,
            self.minutes5.value: 5,
            self.minutes15.value: 15,
            self.HOUR1.value: 60,
            self.HOUR4.value: 240,
            self.DAY1.value: 1440,
        }


@singleton
class QuotesPairImporter:
    @dataclass
    class Configuration:
        file_folder_path: Path

    @inject
    def __init__(
        self,
        quote_factory: QuoteFactory,
        client: BinanceClient,
        configuration: Configuration,
    ):
        self._quote_factory = quote_factory
        self._client = client
        self._config = configuration

    def import_all_quotes(self, time_unit: str):
        for pair in Pair.objects.all()[:2]:
            self.import_quote(pair, TimeUnits.from_code(time_unit))

    def import_quote(self, pair: Pair, time_unit: TimeUnits):

        filename_csv = (
            self._config.file_folder_path / f"{pair.symbol}-{time_unit.value}-data.csv"
        )
        filename_json = (
            self._config.file_folder_path / f"{pair.symbol}-{time_unit.value}-data.json"
        )
        if filename_csv.exists():
            data_df = pd.read_csv(filename_csv)
        else:
            data_df = pd.DataFrame()
        oldest_point, newest_point = self.minutes_of_new_data(
            pair.symbol, time_unit.value, data_df
        )
        delta_min = (newest_point - oldest_point).total_seconds() / 60
        available_data = math.ceil(delta_min / time_unit.binsize)
        if oldest_point == datetime.strptime("1 Jan 2017", "%d %b %Y"):
            logger.info(
                f"Downloading all available {time_unit} data for {pair.symbol}. Be patient..!"
            )
        else:
            logger.log(
                f"Downloading {delta_min} minutes of new data available for {pair.symbol}, i.e. {available_data} instances of {time_unit.value} data."
            )
        klines = self._client.get_historical_klines(
            pair.symbol,
            time_unit.value,
            oldest_point.strftime("%d %b %Y %H:%M:%S"),
            newest_point.strftime("%d %b %Y %H:%M:%S"),
        )
        data = pd.DataFrame(
            klines,
            columns=[
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_av",
                "trades",
                "tb_base_av",
                "tb_quote_av",
                "ignore",
            ],
        )
        data["timestamp"] = pd.to_datetime(data["timestamp"], unit="ms")
        if len(data_df) > 0:
            temp_df = pd.DataFrame(data)
            data_df = data_df.append(temp_df)
        else:
            data_df = data
        data_df.set_index("timestamp", inplace=True)
        data_df.to_csv(filename_csv)
        filename_json.write_text(
            data_df.reset_index().to_json(orient="records", indent=4)
        )
        print("All caught up..!")
        return data_df

    def minutes_of_new_data(self, symbol, time_unit: TimeUnits, data):
        if len(data) > 0:
            old = parser.parse(data["timestamp"].iloc[-1])
        else:
            old = datetime.strptime("1 Jan 2017", "%d %b %Y")
        new = pd.to_datetime(
            self._client.get_klines(symbol=symbol, interval=time_unit)[-1][0], unit="ms"
        )
        time.sleep(0.5)
        return old, new
