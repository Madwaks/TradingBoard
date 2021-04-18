import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from injector import singleton, inject

from crypto.models import Pair
from crypto.services.factories.quote_pair import QuotePairFactory
from crypto.utils.enums import TimeUnits


@singleton
class QuotesPairRepository:
    @dataclass
    class Configuration:
        file_folder_path: Path

    @inject
    def __init__(
        self, quote_pair_factory: QuotePairFactory, configuration: Configuration
    ):
        self._config = configuration
        self._quote_pair_factory = quote_pair_factory

    @property
    def json_folder(self) -> Path:
        return self._config.file_folder_path / "json"

    @property
    def csv_folder(self) -> Path:
        return self._config.file_folder_path / "csv"

    @property
    def available_tu(self) -> list[TimeUnits]:
        return [
            TimeUnits.from_code(file_name.name.split("-")[1])
            for file_name in self.json_folder.iterdir()
        ]

    @property
    def available_pair(self) -> list[str]:
        return [
            file_name.name.split("-")[0] for file_name in self.json_folder.iterdir()
        ]

    def get_pair_quotes(self, pair: Pair, time_unit: TimeUnits) -> list[dict[str, Any]]:
        path_to_file = self._get_file_from_pair_and_tu(pair, time_unit)
        objs = json.loads(path_to_file.read_text())
        return objs

    def _get_file_from_pair_and_tu(self, pair: Pair, time_unit: TimeUnits) -> Path:
        return self.json_folder / f"{pair.symbol}-{time_unit.value}-data.json"
