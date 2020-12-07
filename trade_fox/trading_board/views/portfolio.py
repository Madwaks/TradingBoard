from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from trading_board.models import Portfolio


class PortfolioListView(ListView):
    model = Portfolio
    template_name = "portfolio_list.html"


class PortfolioView(TemplateView):
    model = Portfolio
    template_name = "portfolio.html"

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        portfolio = Portfolio.objects.get(pk=pk)
        context = dict(portfolio=portfolio)
        return render(request, context=context, template_name=self.template_name)
