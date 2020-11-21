from django.http import HttpRequest
from django.views import View

from trade_fox.trading_board.forms.trade import TradeForm


class TradeView(View):
    form_class = TradeForm

    def get(self, request: HttpRequest, *args, **kwargs):
        pass