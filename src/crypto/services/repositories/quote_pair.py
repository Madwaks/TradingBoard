from pathlib import Path

from django.conf import settings
from injector import singleton, inject


@singleton
class QuotesPairRepository:
    @inject
    def __init__(self):
        pass

    @property
    def json_files(self) -> Path:
        return settings.CRYPTO_QUOTES_FOLDER / "json"

    @property
    def csv_folder(self) -> Path:
        return (settings.CRYPTO_QUOTES_FOLDER / "csv").iterdir()
