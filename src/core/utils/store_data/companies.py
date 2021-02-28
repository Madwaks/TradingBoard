import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn

from injector import singleton, inject

from core.models import Company
from core.services.factories.company import CompanyFactory
from core.utils.models.company import Company as CompanyDC

logger = logging.getLogger("django")


@singleton
class CompanyStorer:
    @dataclass
    class Configuration:
        companies_json_path: Path

    @inject
    def __init__(self, config: Configuration, company_factory: CompanyFactory):
        self._raw_companies = config.companies_json_path
        self._company_factory = company_factory

    def store_all_companies(self):
        companies_dc = self._load_companies()
        companies = self._company_factory.build_companies_from_dataclass(companies_dc)

        self._save_companies(companies)
        logger.info(f"Successfully created {Company.objects.count()} companies")

    def store_dc_company(self, company_dc: CompanyDC):
        if Company.objects.filter(symbol=company_dc.symbol).exists():
            logger.warning(f"[COMPANY] {company_dc.name} already exists")
        else:
            company = self._company_factory.build_company_from_dataclass(company_dc)
            company.save()

    def _load_companies(self):
        list_companies = json.loads(self._raw_companies.read_text())
        return [CompanyDC.from_dict(company) for company in list_companies]

    @staticmethod
    def _save_companies(company_list: list[Company]) -> NoReturn:
        Company.objects.bulk_create(company_list)
