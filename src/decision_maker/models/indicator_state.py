from django.db import models

from decision_maker.models import Indicator


class IndicatorState(models.Model):
    distance = models.FloatField()
    is_above_price = models.BooleanField()

    def is_above_indicator(self, other_indicator: Indicator) -> bool:
        return self.indicator > other_indicator
