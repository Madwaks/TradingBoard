from datetime import date
from typing import Optional

from django.db import models


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
    def last_dated_quotation(self) -> Optional[str]:
        return self.quotes.latest("date").date if self.quotes.exists() else None

    @property
    def is_up_to_date(self) -> bool:
        return self.last_dated_quotation == date.today().strftime("%m-%d-%Y")

    def save(self, **kwargs):
        info = self.info
        if info and info.pk is None:
            info.save()
        self.info = info

        super().save(**kwargs)
