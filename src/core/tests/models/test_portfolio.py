import pytest

from core.models import Portfolio, Position


@pytest.mark.django_db
def test_portfolio(position: Position, portfolio: Portfolio):
    assert str(portfolio) == portfolio.name
    assert len(portfolio.trade_history) == 0

    position.portfolio = portfolio
    position.save()

    assert len(portfolio.trade_history) == 1
