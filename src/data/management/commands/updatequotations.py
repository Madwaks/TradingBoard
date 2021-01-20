import os
import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Loads initial companies into DB"

    def handle(self, *args, **options):
        sys.path.insert(0, os.getcwd())
        from src.database_storer.store_quotations import QuotationStorer

        storer = QuotationStorer()
        storer.update_quotations()
