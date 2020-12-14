from django.forms import ModelForm

from trading_board.models import Trade


class TradeForm(ModelForm):
    class Meta:
        model = Trade
        exclude = []
