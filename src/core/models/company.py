from datetime import date

from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=128)
    symbol = models.CharField(max_length=128)
    sector = models.CharField(max_length=256, blank=True, null=True)
    sub_sector = models.CharField(max_length=256, blank=True, null=True)
    creation_date = models.IntegerField(blank=True, null=True)
    market_cap = models.CharField(max_length=128, blank=True, null=True)

    quotes_file_path = models.CharField(max_length=128, blank=True, null=True)

    info_url = models.OneToOneField(
        "CompanyInfoUrl",
        verbose_name="company_urls",
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
    def last_dated_quotation(self) -> str:
        quotation_date = self.quotation.latest("date").date
        return quotation_date

    @property
    def is_up_to_date(self) -> bool:
        return self.last_dated_quotation == date.today().strftime("%m-%d-%Y")
