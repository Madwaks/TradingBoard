from enum import Enum
from typing import Optional

from django.db import models
from django.utils.translation import gettext_lazy as _


class TradeType(Enum):
    ACHAT = "Buy"
    VENTE = "Sell"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Position(models.Model):
    class ReasonClosed(models.TextChoices):
        SL = "STOP", _("StopLoss")
        TP = "TAKE", _("TakeProfit")
        OTHER = "OTHER", _("Other")

    date = models.DateField()

    nb_titres: int = models.IntegerField()
    price: float = models.FloatField()

    take_profit: Optional[float] = models.FloatField(null=True)
    stop_loss: Optional[float] = models.FloatField(null=True)

    reason_closed: ReasonClosed = models.CharField(
        max_length=128, choices=ReasonClosed.choices, null=True
    )

    portfolio = models.ForeignKey(
        "core.Portfolio",
        verbose_name="portfolio",
        related_name="positions",
        on_delete=models.CASCADE,
        null=True,
    )

    @property
    def size(self) -> float:
        return self.price * self.nb_titres

    def amount(self, current_price: float) -> float:
        return current_price * self.nb_titres
