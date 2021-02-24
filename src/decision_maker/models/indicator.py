from django.db import models
from django.utils.translation import gettext_lazy as _

from decision_maker.managers.indicator import IndicatorManager


class Indicator(models.Model):
    class AvailableIndicators(models.TextChoices):
        MM7 = "MM7", _("Moyenne mobile 7")
        MM20 = "MM20", _("Moyenne mobile 20")
        MM50 = "MM50", _("Moyenne mobile 50")
        MM100 = "MM100", _("Moyenne mobile 100")
        MM200 = "MM200", _("Moyenne mobile 200")

    objects = IndicatorManager()

    name = models.CharField(
        max_length=128, choices=AvailableIndicators.choices, null=True
    )

    value = models.FloatField(null=True)

    quote = models.ForeignKey(
        "core.Quote", related_name="indicators", on_delete=models.SET_NULL, null=True
    )

    def __str__(self) -> str:
        return f"{str(self.quote)} {str(self.name)}"

    def __add__(self, other):
        return self.value + other.value

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(str(self.pk) + str(self.name))

    class Meta:
        ordering = ("name",)
        constraints = (
            models.UniqueConstraint(
                fields=("name", "quote"), name="unique_per_name_and_quote"
            ),
        )

    def save(self, **kwargs):
        quote = self.quote
        if quote and quote.pk is None:
            quote.save()
        self.quote = quote

        super().save(**kwargs)
