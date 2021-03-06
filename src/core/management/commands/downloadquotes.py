import os
import sys

from django.core.management.base import BaseCommand

from utils.service_provider import provide


class Command(BaseCommand):
    help = "Downloads 10 years quotes in a .txt file"

    def handle(self, *args, **options):
        sys.path.insert(0, os.getcwd())
        from core.utils.download_data.quotes.boursorama import QuotationDownloader

        downloader = provide(QuotationDownloader)
        downloader.download_quotations(force_download=True)
