import os
import sys

from django.core.management.base import BaseCommand

from utils.service_provider import provide


class Command(BaseCommand):
    help = "Loads initial companies into DB"

    def handle(self, *args, **options):
        sys.path.insert(0, os.getcwd())

        from crypto.services.quotes_storer import QuotesPairStorer

        quotes_storer = provide(QuotesPairStorer)
        quotes_storer.store_all_quotes()
