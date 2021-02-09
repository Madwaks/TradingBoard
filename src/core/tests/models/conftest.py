from pathlib import Path

import pytest

from core.utils.store_data.companies import CompanyStorer
from utils.service_provider import provide


@pytest.fixture(scope="module")
def path_to_test():
    return Path("src/core/tests/companies/mock_data/test.json").absolute()


@pytest.fixture(scope="module")
def company_storer(path_to_test: Path) -> CompanyStorer:
    comp_st = provide(CompanyStorer)
    comp_st._raw_companies = path_to_test
    return comp_st
