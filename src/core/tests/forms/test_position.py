import pytest

from core.forms.position import PositionForm
from core.models import Portfolio


@pytest.mark.django_db
def test_position_form(position_form: PositionForm):
    assert isinstance(position_form.data.portfolio, Portfolio)
