import pytest
from pytest_factoryboy import register

from core.models import Company
from core.tests.factories.company import CompanyFactory
from core.tests.factories.company_info import CompanyInfoFactory
from core.tests.factories.quotes import QuotesFactory
from decision_maker.services.factories.indicators import DataFrameIndicatorFactory
from decision_maker.tests.factories.indicator import IndicatorFactory

register(CompanyInfoFactory)
register(CompanyFactory)
register(QuotesFactory)
register(IndicatorFactory)


@pytest.mark.django_db
def test_indicator_factory(
    company: Company, df_indicator_factory: DataFrameIndicatorFactory
):
    quotes = company.quotes.get_as_dataframe()
    df = df_indicator_factory.build_indicators_from_dataframe(quotes)
    assert all(
        [
            ind_name in quotes.columns
            for ind_name in df_indicator_factory.new_indicators_name
        ]
    )
    assert len(df) == 0
