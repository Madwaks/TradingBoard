from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from core.forms.position import PositionForm


class Position(object):
    pass


class TradeListView(FormMixin, ListView):
    model = Position
    template_name = "trade_list.html"
    form_class = PositionForm
