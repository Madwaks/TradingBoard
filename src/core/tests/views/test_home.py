import pytest
from django.test import Client

from core.models import Portfolio, Position


@pytest.mark.django_db
def test_home_view(client: Client):
    response = client.get("/tradingboard/")
    assert response.status_code == 200
    assert len(Portfolio.objects.all()) in response.context_data.values()
    assert len(Position.objects.all()) in response.context_data.values()
