from pathlib import Path
from typing import Union

import pytest

from core.models import Company, CompanyInfo, Quote


@pytest.fixture(scope="module")
def path_to_test():
    return Path("src/core/tests/companies/mock_data/mock_quotes").absolute()


@pytest.fixture(scope="module")
def empty_company(db) -> Company:
    return Company.objects.create()


@pytest.fixture(scope="module")
def company(db) -> Company:
    return Company.objects.create(name="Tradefox", symbol="ALTR")


@pytest.fixture(scope="module")
def empty_company_info(db) -> CompanyInfo:
    return CompanyInfo.objects.create()


@pytest.fixture(scope="module")
def company_info(db, path_to_test: Union[str, Path]) -> CompanyInfo:
    return CompanyInfo.objects.create(
        quotes_file_path=path_to_test, sector="Finance", sub_sector="Technology"
    )


@pytest.fixture(scope="module")
def quote(db, company: Company) -> Quote:
    return Quote.objects.create(
        date="2021-01-01",
        open=15,
        close=18,
        high=20,
        low=13,
        volume=3000,
        company=company,
    )
