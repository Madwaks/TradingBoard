from datetime import datetime, timezone


def _is_market_ongoing() -> bool:
    return 9 < datetime.now(timezone.utc).hour + 2 < 18
