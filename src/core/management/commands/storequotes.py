import os
import sys

from django.core.management.base import BaseCommand

from core.utils.store_data.quotes import QuotationStorer
from utils.service_provider import provide


class Command(BaseCommand):
    help = "Loads initial companies into DB"

    def handle(self, *args, **options):
        sys.path.insert(0, os.getcwd())

        storer = provide(QuotationStorer)
        storer.store_quotations()
