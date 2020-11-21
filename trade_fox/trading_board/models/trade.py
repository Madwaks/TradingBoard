from datetime import time
from enum import Enum

from django.db import models


class TradeType(Enum):
    ACHAT = "Buy"
    VENTE = "Sell"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Trade(models.Model):
    date = models.DateField()
    type = models.CharField(max_length=128, choices=TradeType.choices(), blank=False, null=False)
    open_price = models.FloatField(default=0.0)
    close_price = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.date)
