from django.forms import ModelForm

from core.models.portfolio import Portfolio


class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = "__all__"
