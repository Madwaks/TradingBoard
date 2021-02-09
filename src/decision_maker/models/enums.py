from enum import Enum
from typing import Union, Optional


class EnumTrend(Enum):
    UP: str = "bullish"
    DOWN: str = "bearish"
    NEUTRAL: str = "neutral"

    @classmethod
    def enum_to_bool(cls, value: Union[str, "EnumTrend"]) -> Optional[bool]:
        if value == cls.UP:
            return True
        elif value == cls.DOWN:
            return False
        return None

    @classmethod
    def sign_to_enum(cls, value: float) -> "EnumTrend":
        if value == -1:
            return cls.UP
        else:
            return cls.DOWN
