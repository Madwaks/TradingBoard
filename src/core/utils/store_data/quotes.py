import logging
from typing import NoReturn

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
                self._save_quotes(list_quotations)
                logger.info(
                    f"[QUOTATIONS] for company <{company.name}> successfully created"
                )

    def update_quotations(self) -> None:
        for company in Company.objects.all():
            if not company.should_update():
                logger.info(
                    f"[QUOTATIONS] for company <{company.name}> already up to date"
                )
                continue

            missing_quotations = self._missing_quote_downloader.get_last_quotations(
                company
            )
            quotes = self._quote_factory.build_quotes_from_dict(
                missing_quotations, company
            )

            self._save_quotes(quotes)

    @staticmethod
    def _save_quotes(quote_list: list[Quote]) -> NoReturn:
        Quote.objects.bulk_create(quote_list)
