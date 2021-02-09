import os
import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Update Companies in DB"

    def handle(self, *args, **options):
        sys.path.insert(0, os.getcwd())
        from src.database_storer.store_company import CompanyStorer

        storer = CompanyStorer()
        storer.update_company_fields()
