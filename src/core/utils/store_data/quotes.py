import json
import logging
from pathlib import Path
from typing import NoReturn, Union

from injector import singleton, inject
from tqdm import tqdm

from core.models import Company, Quote
from core.services.factories.quote import QuoteFactory
from core.utils.download_data.quotes.update import MissingQuoteDownloader
from core.utils.models.quotes import Quote as QuoteDC

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

    def write_quotation_json(
        self,
        input_file_path: Union[Path, str],
        output_folder_path: Union[Path, str],
        company: Company,
    ) -> None:
        list_quotations: list[QuoteDC] = self._quote_factory.extract_from_file(
            input_file_path
        )

        (output_folder_path / company.symbol / ".json").write_text(
            json.dumps(
                [json.dumps(quote, indent=4) for quote in list_quotations], indent=4
            )
        )

    def store_quotations_from_json(self, folder_path: Union[Path, str]):
        all_stored_companies = Company.objects.all()
        for company in tqdm(all_stored_companies):
            if company.quotes.exists():
                logger.info(f"[QUOTATIONS] for company <{company.name}> already exists")
            else:
                list_quotations = json.loads((folder_path / company.symbol).read_text())
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
            quotes = self._quote_factory.build_quotes_from_dataclass(
                missing_quotations, company
            )

            self._save_quotes(quotes)

    @staticmethod
    def _save_quotes(quote_list: list[Quote]) -> NoReturn:
        Quote.objects.bulk_create(quote_list)
