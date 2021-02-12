from django.db import models
from django.utils.translation import gettext_lazy as _


class Indicator(models.Model):
    class AvailableIndicators(models.TextChoices):
        MM7 = "MM7", _("Moyenne mobile 7")
        MM20 = "MM20", _("Moyenne mobile 20")
        MM50 = "MM50", _("Moyenne mobile 50")
        MM100 = "MM100", _("Moyenne mobile 100")
        MM200 = "MM200", _("Moyenne mobile 200")

    name = models.CharField(
        max_length=128, choices=AvailableIndicators.choices, null=True
    )

    value = models.FloatField(null=True)

    state = models.OneToOneField(
        "IndicatorState",
        related_name="indicator",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    quote = models.ForeignKey(
        "core.Quote",
        related_name="indicators",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
        return hash(str(self.pk) + self.name)

    def clean_fields(self, exclude=None):
        breakpoint()

    def save(self, **kwargs):
        self.full_clean()
        super().save(**kwargs)

    class Meta:
        ordering = ("name",)
        constraints = (
            models.UniqueConstraint(
                fields=("name", "quote"), name="unique_per_name_and_quote"
            ),
        )
