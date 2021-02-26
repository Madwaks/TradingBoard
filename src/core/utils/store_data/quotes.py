import logging
from typing import List, Dict, NoReturn

from injector import singleton, inject
from tqdm import tqdm

from core.models import Company, Quote
from core.services.factories.quote import QuoteFactory
from core.utils.download_data.quotes.update import MissingQuoteDownloader

logger = logging.getLogger("django")


@singleton
class QuotationStorer:
    @inject
    def __init__(
        self,
        missing_quote_downloader: MissingQuoteDownloader,
        quote_factory: QuoteFactory,
    ):
        self._missing_quote_downloader = missing_quote_downloader
        self._quote_factory = quote_factory

    def store_quotations(self):
        all_stored_companies = Company.objects.all()
        for company in tqdm(all_stored_companies):
            if company.quotes.exists():
                logger.info(f"[QUOTATIONS] for company <{company.name}> already exists")
            else:
                list_quotations = self._quote_factory.extract_from_file(company)
                logger.info(f"[STORING COMPANY] <{company.name}> 's quotations ")
                self._save_indicators(list_quotations)
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

    def _store_missing_quotations(self, missing_quotations: List[Dict]):
        for quot in missing_quotations:
            try:
                qu = Quote(**quot)
                qu.save()
            except Exception as e:
                logger.info(e)
                raise (e)

    @staticmethod
    def _save_indicators(quote_list: list[Quote]) -> NoReturn:
        Quote.objects.bulk_create(quote_list)
