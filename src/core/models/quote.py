from django.db import models

from core.managers.quotes import QuoteManager


class Quote(models.Model):

    objects = QuoteManager()

    date = models.DateField()
    open = models.FloatField(max_length=128, verbose_name="open_price")
    close = models.FloatField(max_length=128, verbose_name="close_price")
    high = models.FloatField(max_length=128, verbose_name="high_price")
    low = models.FloatField(max_length=128, verbose_name="low_price")
    volume = models.IntegerField(verbose_name="volumes")
    devise = models.CharField(max_length=128, null=True, default="eur")

    company = models.ForeignKey(
        "Company",
        verbose_name="company",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="quotes",
    )

    def __str__(self):
        return f"{self.company.name} - {str(self.date)}"

    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"
        ordering = ("date", "company")
        constraints = (
            models.UniqueConstraint(
                fields=("date", "company"), name="unique_per_date_and_company"
            ),
        )

    def save(self, **kwargs):
        company = self.company
        if company and company.pk is None:
            company.save()
        self.company = company

        super().save(**kwargs)
