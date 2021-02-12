import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from injector import singleton, inject

from core.models import Company, CompanyInfo

logger = logging.getLogger("django")


@singleton
class CompanyStorer:
    @dataclass
    class Configuration:
        companies_json_path: Path

    @inject
    def __init__(self, config: Configuration):
        self._raw_companies = config.companies_json_path

    def store_companies(self):
        with open(self._raw_companies, "r") as f:
            list_info = json.load(f)

        for info in list_info:
            try:
                _ = Company.objects.get(symbol=info["symbol"])
                logger.warning(f"[COMPANY] {info['name']} already exists")
            except ObjectDoesNotExist:
                company = self._build_company(info)
                logger.info(f"[COMPANY] {company.name} successfully created")

        logger.info(f"Successfully created {Company.objects.count()} companies")

    def _build_company(self, infos: dict[str, Any]) -> Company:
        comp = self._create_company_from_info(infos)
        urls = self._create_company_infos(infos)
        comp.info = urls
        comp.save()
        return comp

    def _create_company_from_info(self, infos: dict[str, Any]) -> Company:
        comp = Company(name=infos["name"], symbol=infos["symbol"])
        return comp

    def _create_company_infos(self, infos: dict[str, Any]) -> CompanyInfo:
        info_urls = CompanyInfo(
            bourso_url=infos["bourso_url"],
            bfm_url=infos["bfm_url"],
            yahoo_url=infos["yahoo_url"],
            quotes_file_path=infos.get("local_file_path"),
            sector=infos["sector"],
            sub_sector=infos["sub_sector"],
        )
        return info_urls

    def update_company_fields(self):
        for info in self.list_info:
            company = Company.objects.get(symbol=info["symbol"])
            missing_fields = set(info.keys()) - set(
                [
                    field.name
                    for field in company._meta.fields
                    if company.__getattribute__(field.name)
                ]
            )

            for miss_field in missing_fields:
                logger.info(f"[UPDATING] {info['name']}")
                company.__setattr__(miss_field, info[miss_field])
                company.save()
                logger.info(f"[COMPANY] {info['name']} successfully updated")