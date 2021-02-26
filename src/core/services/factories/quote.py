import datetime
from typing import Optional, Any

from injector import singleton
from pandas import DataFrame, read_table, Series

from core.models import Company, Quote


@singleton
class QuoteFactory:
    def build_quote_from_dict(self, quote_as_dict: dict[str, Any]) -> Quote:
        pass

    @staticmethod
    def extract_from_file(company: Company) -> list[Quote]:
        def parse_row(row: Series) -> Optional[Quote]:
            if row["date"] == "10/11/2020 00:00":
                return None
            return Quote(
                date=datetime.datetime.strptime(
                    row["date"].split(" ")[0], "%d/%m/%Y"
                ).date(),
                open=row["ouv"],
                close=row["clot"],
                high=row["haut"],
                low=row["bas"],
                volume=row["vol"],
                devise=row["devise"],
                company=company,
            )

        quotations: DataFrame = read_table(company.info.quotes_file_path)
        list_quotation = quotations.apply(parse_row, axis=1).dropna().to_list()
        return list_quotation
