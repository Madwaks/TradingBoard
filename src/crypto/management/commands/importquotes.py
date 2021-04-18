import os
import sys

from django.core.management.base import BaseCommand

from utils.service_provider import provide


class Command(BaseCommand):
    help = "Loads initial companies into DB"

    @property
    def choices(self) -> list[str]:
        return ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"]

    def add_arguments(self, parser):
        parser.add_argument(
            "--time-unit", choices=self.choices, type=str, required=True
        )

    def handle(self, *args, **options):
        sys.path.insert(0, os.getcwd())
        from crypto.services.pairs_importer import QuotesPairImporter
        from crypto.utils.enums import TimeUnits

        tu = TimeUnits.from_code(options["time_unit"])
        pair_importer = provide(QuotesPairImporter)
        pair_importer.import_all_quotes(time_unit=tu)

        from crypto.services.quotes_storer import QuotesPairStorer

        quotes_storer = provide(QuotesPairStorer)
        quotes_storer.store_all_quotes(time_unit=tu)
