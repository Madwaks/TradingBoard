from typing import NoReturn, List

from injector import singleton
from pandas import DataFrame

from core.models import Quote
from decision_maker.models import Indicator
from decision_maker.utils.indicators.moving_average import simple_moving_average


@singleton
class DataFrameIndicatorFactory:
    def __init__(self):
        self.new_indicators_name: set = set()

    def build_indicators_from_dataframe(
        self, quotes_as_dataframe: DataFrame
    ) -> List[Indicator]:
        self._build_dataframe(quotes_as_dataframe)
        return self._build_indicators(quotes_as_dataframe)

    def _build_dataframe(self, quotes_as_dataframe: DataFrame) -> NoReturn:
        self.new_indicators_name.add(
            simple_moving_average(quotes_as_dataframe, period=7)
        )
        self.new_indicators_name.add(
            simple_moving_average(quotes_as_dataframe, period=20)
        )
        self.new_indicators_name.add(
            simple_moving_average(quotes_as_dataframe, period=50)
        )
        self.new_indicators_name.add(
            simple_moving_average(quotes_as_dataframe, period=100)
        )
        self.new_indicators_name.add(
            simple_moving_average(quotes_as_dataframe, period=200)
        )

    def _build_indicators(self, quotes_as_dataframe: DataFrame) -> List[Indicator]:
        list_indicators = []
        for i, row in quotes_as_dataframe.fillna(None).iterrows():
            quote = Quote.objects.get(id=row["id"])
            breakpoint()
            # if all([isna(row_value) ])
            for indicator_name in self.new_indicators_name:
                if quote.indicators.filter(name=indicator_name).exists():
                    continue
                list_indicators.append(
                    Indicator(
                        name=indicator_name, value=row[indicator_name], quote=quote
                    )
                )

        return list_indicators
