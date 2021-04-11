from django.db.models import (
    Model,
    FloatField,
    IntegerField,
    ForeignKey,
    SET_NULL,
    DateTimeField,
)

from datetime import datetime


class QuotePair(Model):
    timestamp = DateTimeField()
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
    close_time = DateTimeField(null=True)

    @property
    def open_date(self):
        return datetime.fromtimestamp(float(self.timestamp))

    @property
    def close_date(self):
        return datetime.fromtimestamp(float(self.close_time))
