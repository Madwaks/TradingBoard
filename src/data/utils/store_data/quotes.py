import datetime
import logging
from datetime import date
from pathlib import Path
from typing import Union, IO, List, Dict, Any, Optional

from django.db import IntegrityError
from injector import singleton, inject
from pandas import Series, DataFrame, read_table
from tqdm import tqdm

from data.models import Company, Quote
from data.utils.download_data.quotes.update import MissingQuoteDownloader


logger = logging.getLogger("django")


@singleton
class QuotationStorer:
    @inject
    def __init__(self, missing_quote_downloader: MissingQuoteDownloader):
        self._missing_quote_downloader = missing_quote_downloader

    def store_quotations(self):
        all_stored_companies = Company.objects.all()
        for company in tqdm(all_stored_companies):
            if company.quote.exists():
                logger.info(f"[QUOTATIONS] for company <{company.name}> already exists")
            else:
                list_quotations = self._extract_from_file(company.quotes_file_path)
                logger.info(f"[STORING COMPANY] <{company.name}> 's quotations ")
                for quote in list_quotations:
                    try:
                        qu = Quote(**quote, company=company)
                        qu.save()
                    except IntegrityError:
                        logger.info(
                            f"[QUOTATION - {quote['date']}] for company <{company.name}> already exists"
                        )
                logger.info(
                    f"[QUOTATIONS] for company <{company.name}> successfully created"
                )

    def update_quotations(self) -> None:
        for company in Company.objects.all():
            if self.should_update(company):
                logger.info(
                    f"[QUOTATIONS] for company <{company.name}> already up to date"
                )
                continue

            missing_quotations = self._missing_quote_downloader.get_last_quotations(
                company
            )

            if missing_quotations:
                self._store_missing_quotations(missing_quotations)
                logger.info(
                    f"[QUOTATIONS]  <{company.name}> {len(missing_quotations)} rows updated"
                )
            else:
                logger.info(
                    f"[QUOTATIONS] for company <{company.name}> already up to date"
                )

    def should_update(self, company: Company) -> bool:
        yesterday = date.today() - datetime.timedelta(days=1)
        last_quot_in_db = company.last_dated_quotation
        return last_quot_in_db == datetime.date.today() or (
            last_quot_in_db == yesterday and self._is_market_ongoing()
        )

    @staticmethod
    def _is_market_ongoing() -> bool:
        return 9 < datetime.datetime.now(datetime.timezone.utc).hour + 2 < 17

    @staticmethod
    def _extract_from_file(file_path: Union[str, Path, IO]) -> List[Dict[str, Any]]:
        def parse_row(row: Series) -> Optional[Dict[str, Any]]:
            if row["date"] == "10/11/2020 00:00":
                return None
            return {
                "date": datetime.datetime.strptime(
                    row["date"].split(" ")[0], "%d/%m/%Y"
                ).date(),
                "open": row["ouv"],
                "close": row["clot"],
                "high": row["haut"],
                "low": row["bas"],
                "volume": row["vol"],
                "devise": row["devise"],
            }

        quotations: DataFrame = read_table(file_path)
        list_quotation = quotations.apply(parse_row, axis=1).dropna().to_list()
        return list_quotation

    def _store_missing_quotations(self, missing_quotations: List[Dict]):
        for quot in missing_quotations:
            try:
                qu = Quote(**quot)
                qu.save()
            except Exception as e:
                logger.info(e)
                raise (e)
