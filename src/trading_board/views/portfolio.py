from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
)

from data.models.portfolio import Portfolio
from trading_board.forms.portfolio import PortfolioForm


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


class AddPortfolio(CreateView):
    form_class = PortfolioForm
    model = Portfolio
    template_name = "add_portfolio.html"
    success_url = reverse_lazy("portfolios")


class EditPortfolio(UpdateView):
    form_class = PortfolioForm
    model = Portfolio
    success_url = reverse_lazy("portfolios")
    template_name = "update_portfolio.html"


class DeletePortfolio(DeleteView):
    model = Portfolio
    success_url = reverse_lazy("portfolios")
    template_name = "portfolio_confirm_delete.html"
