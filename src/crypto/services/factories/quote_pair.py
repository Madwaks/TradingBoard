from injector import inject, singleton

from crypto.models import Pair, QuotePair
from crypto.utils.enums import TimeUnits

QuotePairJSON = dict[str, any]


@singleton
class QuotePairFactory:
    @inject
    def __init__(self):
        pass

    def build_quote_from_pair(
        self, pair: Pair, time_unit: TimeUnits, objs: list[QuotePairJSON]
    ) -> list[QuotePair]:
        return [
            QuotePair(
                timestamp=obj.get("timestamp"),
                open=obj.get("open"),
                close=obj.get("close"),
                high=obj.get("high"),
                low=obj.get("low"),
                volume=obj.get("volume"),
                close_time=obj.get("close_time"),
                pair=pair,
                time_unit=time_unit,
            )
            for obj in objs
        ]

    def _get_time_unit(self, objs: list[QuotePairJSON]):
        objs[1]["timestamp"] - objs[0]["timestamp"]
