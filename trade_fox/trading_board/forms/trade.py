from django import forms
from django.forms import ModelForm

from trade_fox.trading_board.models import Trade


class TradeForm(ModelForm):
    class Meta:
        model = Trade
        fields = ["portfolio", "date"]
