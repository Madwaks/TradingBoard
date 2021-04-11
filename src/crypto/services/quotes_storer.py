import json

from injector import singleton, inject

from crypto.models import Pair
from crypto.models.quote_pair import QuotePair
from crypto.services.repositories.quote_pair import QuotesPairRepository


@singleton
class QuotesPairStorer:
    @inject
    def __init__(self, quotes_repository: QuotesPairRepository):
        self._quotes_repository = quotes_repository

    def store_all_quotes(self):
        for file in self._quotes_repository.json_files.iterdir():
            pair_symbol = file.name.split("-")[0]
            pair = Pair.objects.get(symbol=pair_symbol)
            data = json.loads(file.read_bytes())
            for obj in data:
                timestamp = float(obj.get("timestamp")) / 1000
                close_time = float(obj.get("close_time")) / 1000
                quote = QuotePair(
                    timestamp=str(timestamp),
                    open=obj.get("open"),
                    close=obj.get("close"),
                    high=obj.get("high"),
                    low=obj.get("low"),
                    volume=float(obj.get("volume")),
                    pair=pair,
                    close_time=str(close_time),
                )
                quote.save()
