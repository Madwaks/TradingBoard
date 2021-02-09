from pathlib import Path
from typing import Union

import pytest

from core.models import Company, CompanyInfo


@pytest.fixture(scope="module")
def path_to_test():
    return Path("src/core/tests/companies/mock_data/test.json").absolute()


@pytest.fixture(scope="module")
def company(path_to_test: Union[Path, str]) -> Company:
    return Company(name="Tradefox", symbol="ALTR")


@pytest.fixture(scope="module")
def empty_company_info() -> CompanyInfo:
    return CompanyInfo()
