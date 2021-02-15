import pytest

from core.models import Position


@pytest.mark.django_db
def test_position(position: Position):
    current_price = 5
    assert position.size == position.price * position.nb_titres
    assert position.amount(current_price) == current_price * position.nb_titres
