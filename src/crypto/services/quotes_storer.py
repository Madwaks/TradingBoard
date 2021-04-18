from injector import singleton, inject

from crypto.models import Pair
from crypto.services.factories.quote_pair import QuotePairFactory
from crypto.services.repositories.quote_pair import QuotesPairRepository
from crypto.utils.enums import TimeUnits


@singleton
class QuotesPairStorer:
    @inject
    def __init__(
        self, quotes_repository: QuotesPairRepository, quote_factory: QuotePairFactory
    ):
        self._quote_factory = quote_factory
        self._quotes_repository = quotes_repository

    def store_all_quotes(self, time_unit: TimeUnits):
        availale_pair = self._quotes_repository.available_pair
        for pair_symbol in availale_pair:
            pair = Pair.objects.get(symbol=pair_symbol)
            self._store_quotes_for_pair_and_tu(pair, time_unit)

    def _store_quotes_for_pair_and_tu(self, pair: Pair, time_unit: TimeUnits):
        objs = self._quotes_repository.get_pair_quotes(pair, time_unit=time_unit)
        quotes = self._quote_factory.build_quote_from_pair(
            pair, time_unit=time_unit, objs=objs
        )
        for quote in quotes:
            quote.save()
