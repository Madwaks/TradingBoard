from django.views.generic import TemplateView

from core.models.portfolio import Portfolio
from core.models.position import Position


class Home(TemplateView):
    template_name = "index.html"


class TradingBoardHome(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        return {
            "total_portfolios": Portfolio.objects.count(),
            "total_trades": Position.objects.count(),
        }
