import pytest

from core.models import Quote


@pytest.mark.django_db
def test_quote(quote: Quote):
    assert str(quote) == f"{quote.company.name} - {str(quote.date)}"
