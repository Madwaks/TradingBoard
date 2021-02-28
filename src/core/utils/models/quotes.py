from dataclasses import dataclass, field
from datetime import datetime

from dataclasses_json import DataClassJsonMixin


@dataclass
class Quote(DataClassJsonMixin):
    open: float
    high: float
    low: float
    close: float
    volume: int
    date: datetime = field(default_factory=datetime)
