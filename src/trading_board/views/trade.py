from django.urls import reverse_lazy
from django.views.generic import CreateView

from trading_board.forms.trade import TradeForm
from trading_board.models import Portfolio


class AddTrade(CreateView):
    form_class = TradeForm
    model = Portfolio
    template_name = "add_trade.html"
    success_url = reverse_lazy("trades")
