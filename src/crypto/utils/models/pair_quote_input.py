from dataclasses import dataclass
from typing import Optional


@dataclass
class PairQuoteInput:
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    close_time: int
    quote_av: Optional[float] = None
    trades: Optional[int] = None
    tb_base_av: Optional[float] = None
    tb_quote_av: Optional[float] = None
