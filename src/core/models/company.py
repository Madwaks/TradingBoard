from datetime import date, timedelta
from typing import Optional

from django.db import models

from core.managers.company import CompanyManager
from core.models import Quote
from core.utils.etc import _is_market_ongoing


class Company(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    symbol = models.CharField(max_length=128, null=False, blank=False)

    info = models.OneToOneField(
        "CompanyInfo",
        verbose_name="company_informations",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="company",
    )
    objects = CompanyManager()

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ("name",)
        constraints = (
            models.UniqueConstraint(
                fields=("name", "symbol"), name="unique_per_name_symbol"
            ),
        )

    def __str__(self):
        return self.name

    @property
    def last_dated_quotation(self) -> Optional[Quote]:
        return self.quotes.latest("date") if self.quotes.exists() else None

    @property
    def is_up_to_date(self) -> bool:
        return self.last_dated_quotation == date.today().strftime("%m-%d-%Y")

    @property
    def should_update(self) -> bool:
        yesterday = date.today() - timedelta(days=1)
        last_quot_in_db = self.last_dated_quotation
        return last_quot_in_db == date.today() or (
            last_quot_in_db == yesterday and _is_market_ongoing()
        )

    def save(self, **kwargs):
        info = self.info
        if info and info.pk is None:
            info.save()
        self.info = info

        super().save(**kwargs)
