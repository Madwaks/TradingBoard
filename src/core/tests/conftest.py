from pathlib import Path

import pytest
from pytest_factoryboy import register

from core.forms.portfolio import PortfolioForm
from core.forms.position import PositionForm
from core.models import Portfolio, Position
from core.tests.factories.company import CompanyFactory
from core.tests.factories.company_info import CompanyInfoFactory
from core.tests.factories.portfolio import PortfolioFactory
from core.tests.factories.position import PositionFactory
from core.tests.factories.quotes import QuotesFactory
from core.utils.store_data.companies import CompanyImporter
from decision_maker.tests.factories.indicator import IndicatorFactory
from utils.service_provider import provide

register(CompanyInfoFactory)
register(CompanyFactory)
register(QuotesFactory)
register(IndicatorFactory)


register(PositionFactory)
register(PortfolioFactory)


@pytest.fixture(scope="module")
def path_to_test():
    return Path("src/core/tests/mock_data/test.json").absolute()


@pytest.fixture(scope="module")
def company_storer(path_to_test: Path) -> CompanyImporter:
    comp_st = provide(CompanyImporter)
    comp_st._companies_json_path = path_to_test
    return comp_st


@pytest.fixture(scope="function")
def portfolio_form(portfolio: Portfolio):
    return PortfolioForm(data=portfolio)


@pytest.fixture(scope="function")
def position_form(position: Position):
    return PositionForm(data=position)
