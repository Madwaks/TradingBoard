import os
import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Loads initial companies into DB"

    def handle(self, *args, **options):
        sys.path.insert(0, os.getcwd())
        from src.database_storer.store_company import CompanyStorer

        storer = CompanyStorer()
        storer.store_data_into_django()
