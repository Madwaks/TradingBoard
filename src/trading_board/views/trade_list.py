from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from trading_board.forms.trade import TradeForm
from trading_board.models import Trade


class TradeListView(FormMixin, ListView):
    model = Trade
    template_name = "trade_list.html"
    form_class = TradeForm
