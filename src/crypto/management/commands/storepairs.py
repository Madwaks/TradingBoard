import os
import sys

from django.core.management.base import BaseCommand

from utils.service_provider import provide


class Command(BaseCommand):
    help = "Loads initial companies into DB"

    def handle(self, *args, **options):
        sys.path.insert(0, os.getcwd())
        from crypto.services.pairs_importer import PairsImporter

        pair_importer = provide(PairsImporter)
        pair_importer.build_all_pairs()
