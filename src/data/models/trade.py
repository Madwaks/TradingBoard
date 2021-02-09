from enum import Enum

from django.db import models

from decision_maker.models.enums import PositionStatus


class TradeType(Enum):
    ACHAT = "Buy"
    VENTE = "Sell"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Trade(models.Model):
    company = models.OneToOneField(
        "Company",
        verbose_name="company",
        related_name="positions",
        on_delete=models.SET_NULL,
        null=True,
    )
    date = models.DateField()
    nb_titres = models.IntegerField()
    pru = models.FloatField()
    status = models.CharField(max_length=128, choices=PositionStatus.choices)

    portfolio = models.ForeignKey(
        "Portfolio",
        verbose_name="portfolio",
        related_name="positions",
        on_delete=models.CASCADE,
        null=True,
    )

    @property
    def size(self) -> float:
        return self.pru * self.nb_titres

    def amount(self, current_price: float) -> float:
        return current_price * self.nb_titres
