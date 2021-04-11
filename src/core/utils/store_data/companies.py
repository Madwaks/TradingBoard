import json
import logging
from dataclasses import dataclass
from pathlib import Path

from injector import singleton, inject

from core.models import Company, CompanyInfo
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
            self._update_company_info_if_needed(company)
        else:
            company.save()

    def _load_companies(self):
        list_companies = json.loads(self._companies_json_path.read_text())
        return [CompanyDC.from_dict(company) for company in list_companies]

    @staticmethod
    def company_exists(company: Company) -> bool:
        return Company.objects.filter(symbol=company.symbol).exists()

    def _update_company_info_if_needed(self, new_company: Company):
        info_fields_to_exclude = ["company", "id", "quotes_file_path"]
        existing_company = Company.objects.get(symbol=new_company.symbol)
        model_fields = [field.name for field in CompanyInfo._meta.get_fields()]
        diff = [
            field_name
            for field_name in filter(
                lambda field: getattr(new_company.info, field, None)
                != getattr(existing_company.info, field, None),
                model_fields,
            )
            if field_name not in info_fields_to_exclude
        ]
        if diff:
            for field in diff:
                setattr(existing_company.info, field, getattr(new_company.info, field))
            existing_company.info.save()
            existing_company.save()
            logger.info(f"[COMPANY] {new_company.name} updated fields : {diff}")
