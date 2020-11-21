from django.contrib import admin

from .models.trade import TradeAdmin
from ..models import Trade

admin.site.register(Trade, TradeAdmin)
