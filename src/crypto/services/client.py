import math
from datetime import datetime
from logging import getLogger
from time import strptime, sleep
from typing import TYPE_CHECKING

from binance.client import Client
from pandas import to_datetime, DataFrame

from crypto.models import Pair

if TYPE_CHECKING:
    from crypto.services.pairs_importer import TimeUnits

logger = getLogger("django")


class BinanceClient(Client):
    PUBLIC_API_VERSION = "v3"

    def get_needed_pair_quotes(
        self, pair: Pair, time_unit: "TimeUnits", existing_data: DataFrame
    ):
        oldest_point, newest_point = self._get_minutes_of_new_data(
            pair.symbol, time_unit.value, existing_data
        )
        delta_min = (newest_point - oldest_point).total_seconds() / 60
        available_data = math.ceil(delta_min / time_unit.binsize)
        if oldest_point == strptime("1 Jan 2017", "%d %b %Y"):
            logger.info(
                f"Downloading all available {time_unit} data for {pair.symbol}. Be patient..!"
            )
        else:
            logger.info(
                f"Downloading {delta_min} minutes of new data available for {pair.symbol}, i.e. {available_data} instances of {time_unit.value} data."
            )
        klines = self.get_historical_klines(
            pair.symbol,
            time_unit.value,
            oldest_point.strftime("%d %b %Y %H:%M:%S"),
            newest_point.strftime("%d %b %Y %H:%M:%S"),
        )
        data = DataFrame(
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
        if data.shape[0] == 0:
            return
        return data

    def _get_minutes_of_new_data(
        self, symbol: str, time_unit: "TimeUnits", data: DataFrame
    ):
        if len(data) > 0:
            old = datetime.fromtimestamp(data["timestamp"].iloc[-1] / 1000)
        else:
            old = datetime.strptime("1 Jan 2017", "%d %b %Y")
        new = to_datetime(
            self.get_klines(symbol=symbol, interval=time_unit)[-1][0], unit="ms"
        )
        sleep(0.5)
        return old, new
