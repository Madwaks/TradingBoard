from django.forms import ModelForm

from data.models.portfolio import Portfolio


class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = "__all__"
