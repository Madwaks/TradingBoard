from django.db.models import (
    Model,
    FloatField,
    IntegerField,
    ForeignKey,
    CharField,
    SET_NULL,
)


class QuotePair(Model):
    timestamp = CharField(default=512)
    open = FloatField(max_length=128, verbose_name="open_price")
    close = FloatField(max_length=128, verbose_name="close_price")
    high = FloatField(max_length=128, verbose_name="high_price")
    low = FloatField(max_length=128, verbose_name="low_price")
    volume = IntegerField(verbose_name="volumes")
    devise = ForeignKey(
        "crypto.Pair",
        related_name="quotes",
        max_length=128,
        null=True,
        on_delete=SET_NULL,
    )
    close_time = CharField(default=512)
