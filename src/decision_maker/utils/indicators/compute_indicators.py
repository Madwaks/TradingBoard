from typing import List, NoReturn

from injector import singleton, inject
from tqdm import tqdm

from core.models import Company
from decision_maker.models import Indicator
from decision_maker.services.factories.indicators import IndicatorFactory


@singleton
class IndicatorComputer:
    @inject
    def __init__(self, indicators_factory: IndicatorFactory):
        self._indicators_factory = indicators_factory

    def compute_indicators_for_all(self):
        for company in tqdm(Company.objects.all()):
            self._compute_indicators_for_company(company)

    def _compute_indicators_for_company(self, company: Company) -> NoReturn:
        quote_as_dataframe = company.quotes.get_as_dataframe()
        indicators = self._indicators_factory.build_indicators_from_dataframe(
            quote_as_dataframe
        )
        self._save_indicators(indicators)

    @staticmethod
    def _save_indicators(indicator_list: List[Indicator]) -> NoReturn:
        Indicator.objects.bulk_create(indicator_list)
