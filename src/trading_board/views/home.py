from django.views.generic import TemplateView

from data.models.portfolio import Portfolio
from data.models.trade import Trade


class Home(TemplateView):
    template_name = "index.html"


class TradingBoardHome(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        return {
            "total_portfolios": Portfolio.objects.count(),
            "total_trades": Trade.objects.count(),
        }
