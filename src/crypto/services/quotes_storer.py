import json

from django.conf import settings
from injector import singleton, inject

from crypto.models import Pair
from crypto.models.quote_pair import QuotePair


@singleton
class QuotesPairStorer:
    @inject
    def __init__(self):
        pass

    def store_all_quotes(self):
        for file in settings.CRYPTO_QUOTES_FOLDER.iterdir():
            pair_symbol = file.name.split("-")[0]
            pair = Pair.objects.get(symbol=pair_symbol)
            breakpoint()
            data = json.loads(file.read_text())
            for obj in data:
                quote = QuotePair(
                    timestamp=obj.get("timestamp"),
                    open=obj.get("open"),
                    close=obj.get("close"),
                    high=obj.get("high"),
                    low=obj.get("low"),
                    volume=obj.get("volume"),
                    devise=pair,
                    close_time=obj.get("close_time"),
                )
                quote.save()
