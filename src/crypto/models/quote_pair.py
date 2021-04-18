from datetime import datetime

from django.db.models import (
    Model,
    FloatField,
    IntegerField,
    ForeignKey,
    SET_NULL,
    CharField,
)

from crypto.utils.enums import TimeUnits


class QuotePair(Model):
    timestamp = IntegerField()
    open = FloatField(max_length=128, verbose_name="open_price")
    close = FloatField(max_length=128, verbose_name="close_price")
    high = FloatField(max_length=128, verbose_name="high_price")
    low = FloatField(max_length=128, verbose_name="low_price")
    volume = IntegerField(verbose_name="volumes")
    pair = ForeignKey(
        "crypto.Pair",
        related_name="quotes",
        max_length=128,
        null=True,
        on_delete=SET_NULL,
    )
    close_time = IntegerField(null=True, blank=True)
    time_unit = CharField(max_length=128, default=TimeUnits.DAY1.value)

    @property
    def open_date(self):
        return datetime.fromtimestamp(float(self.timestamp))

    @property
    def close_date(self):
        return datetime.fromtimestamp(float(self.close_time))
