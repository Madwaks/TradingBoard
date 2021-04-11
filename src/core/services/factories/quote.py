from datetime import datetime
from typing import Optional

from injector import singleton
from pandas import DataFrame, read_table, Series

from core.models import Company, Quote
from core.utils.models.quotes import Quote as QuoteDC


@singleton
class QuoteFactory:
    def build_quotes_from_dataclass(
        self, list_dc_quotes: list[QuoteDC], company: Company
    ) -> list[Quote]:
        return [
            Quote(
                date=quote_dc.date,
                open=quote_dc.open,
                close=quote_dc.close,
                high=quote_dc.high,
                low=quote_dc.low,
                volume=quote_dc.volume,
                company=company,
            )
            for quote_dc in list_dc_quotes
        ]

    @staticmethod
    def extract_from_file(file_path: str) -> list[QuoteDC]:
        def parse_row(row: Series) -> Optional[QuoteDC]:
            if row["date"] == "10/11/2020 00:00":
                return None
            date = row["date"].split(" ")[0]
            return QuoteDC(
                date=datetime.strptime(date, "%d/%m/%Y"),
                open=row["ouv"],
                close=row["clot"],
                high=row["haut"],
                low=row["bas"],
                volume=row["vol"],
                devise=row["devise"],
            )

        quotations: DataFrame = read_table(file_path)
        list_quotation = quotations.apply(parse_row, axis=1).dropna().to_list()
        return list_quotation
