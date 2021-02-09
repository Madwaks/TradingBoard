from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.forms.position import PositionForm
from core.models.portfolio import Portfolio


class AddTrade(CreateView):
    form_class = PositionForm
    model = Portfolio
    template_name = "add_trade.html"
    success_url = reverse_lazy("trades")
