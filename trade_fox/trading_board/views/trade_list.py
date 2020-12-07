from django.views.generic import ListView

from trading_board.models import Trade


class TradeListView(ListView):
    model = Trade
    template_name = "trade_list.html"
