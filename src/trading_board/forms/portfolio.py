from django.forms import ModelForm

from trading_board.models import Portfolio


class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = "__all__"
