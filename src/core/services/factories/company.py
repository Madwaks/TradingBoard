import datetime
from typing import Optional

from injector import singleton, inject
from pandas import DataFrame, read_table, Series

from core.models import Company, Quote
from core.services.factories.company_info import CompanyInfoFactory
from core.utils.models.company import Company as CompanyDC


@singleton
class CompanyFactory:
    @inject
    def __init__(self, company_info_factory: CompanyInfoFactory):
        self._company_info_factory = company_info_factory

    def build_companies_from_dataclass(
        self, list_dc_companies: list[CompanyDC]
    ) -> list[Company]:
        return [
            self.build_company_from_dataclass(company_dc)
            for company_dc in list_dc_companies
        ]

    def build_company_from_dataclass(self, company_dc: CompanyDC) -> Company:
        return Company(
            name=company_dc.name,
            symbol=company_dc.symbol,
            info=self._company_info_factory.build_company_info(company_dc.info),
        )

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
