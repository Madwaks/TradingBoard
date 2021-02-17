import pytest

from core.forms.portfolio import PortfolioForm


@pytest.mark.django_db
def test_portfolio_form(portfolio_form: PortfolioForm):
    assert portfolio_form.data.name
    assert portfolio_form.data.amount
