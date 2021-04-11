from enum import Enum

from django.contrib.postgres.fields import ArrayField
from django.db.models import Model, CharField


class Statuses(Enum):
    ACTIVE = "TRADING"


class Pair(Model):
    symbol = CharField(max_length=20)
    base_asset = CharField(max_length=10)
    quote_asset = CharField(max_length=10)
    order_types = ArrayField(base_field=CharField(max_length=64, null=True), size=10)

    def __str__(self) -> CharField:
        return self.symbol
