import os
import sys

from django.core.management.base import BaseCommand

from utils.service_provider import provide


class Command(BaseCommand):
    help = "Loads initial companies into DB"

    def handle(self, *args, **options):
        sys.path.insert(0, os.getcwd())
        from core.utils.store_data.companies import CompanyImporter

        storer = provide(CompanyImporter)
        storer.import_all_companies()
