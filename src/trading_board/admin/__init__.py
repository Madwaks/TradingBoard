from django.contrib import admin

from .models.portfolio import PortfolioAdmin
from .models.trade import TradeAdmin
from ..models import Trade, Portfolio

admin.site.register(Trade, TradeAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
