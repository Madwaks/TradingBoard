from django.db import models


class Indicator(models.Model):
    name = models.CharField(max_length=128, null=True)
    value = models.FloatField(null=True)

    state = models.OneToOneField(
        "IndicatorState",
        related_name="indicator",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    quote = models.ForeignKey(
        "data.Quote",
        related_name="indicators",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

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

    class Meta:
        ordering = ("name",)
        constraints = (
            models.UniqueConstraint(
                fields=("name", "quote"), name="unique_per_name_and_quote"
            ),
        )
