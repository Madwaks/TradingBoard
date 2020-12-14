from enum import Enum

from django.db import models
from django.db.models import SET_NULL


class TradeType(Enum):
    ACHAT = "Buy"
    VENTE = "Sell"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Trade(models.Model):
    date = models.DateField()
    type = models.CharField(
        max_length=128, choices=TradeType.choices(), blank=False, null=False
    )
    open_price = models.FloatField(default=0.0)
    close_price = models.FloatField(default=0.0)

    portfolio = models.ForeignKey(
        "Portfolio", on_delete=SET_NULL, related_name="trades", null=True
    )

    def __str__(self):
        return str(self.date)
