from django.db import models


class Quote(models.Model):
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
        related_name="quote",
    )

    def __str__(self):
        return self.company.name + " - " + str(self.date)

    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"
        ordering = ("date", "company")
        constraints = (
            models.UniqueConstraint(
                fields=("date", "company"), name="unique_per_date_and_company"
            ),
        )