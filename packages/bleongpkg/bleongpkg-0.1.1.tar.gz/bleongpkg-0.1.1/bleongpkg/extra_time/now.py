import arrow


def now() -> str:
    return arrow.utcnow().isoformat()
