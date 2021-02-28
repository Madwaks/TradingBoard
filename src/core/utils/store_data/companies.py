import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Union

from injector import singleton, inject

from core.models import Company
from core.services.factories.company import CompanyFactory
from core.utils.models.company import Company as CompanyDC

logger = logging.getLogger("django")


@singleton
class CompanyImporter:
    @dataclass
    class Configuration:
        companies_json_path: Path

    @inject
    def __init__(self, config: Configuration, company_factory: CompanyFactory):
        self._companies_json_path = config.companies_json_path
        self._company_factory = company_factory

    def import_all_companies(self):
        companies_dc = self._load_companies()
        for company in companies_dc:
            self.import_company(company)

        logger.info(f"Successfully created {Company.objects.count()} companies")

    def import_company(self, company_dc: CompanyDC):
        company = self._company_factory.build_company_from_dataclass(company_dc)
        self._save_company(company)

    def _save_company(self, company: Company):
        if self.company_exists(company):
            logger.warning(f"[COMPANY] {company.name} already exists")
        else:
            company.save()

    def _load_companies(self):
        list_companies = json.loads(self._companies_json_path.read_text())
        return [CompanyDC.from_dict(company) for company in list_companies]

    @staticmethod
    def company_exists(company: Union[Company, CompanyDC]) -> bool:
        return Company.objects.filter(symbol=company.symbol).exists()
