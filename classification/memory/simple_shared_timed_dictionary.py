from cachetools import TTLCache

MAXSIZE = 1000
TTL = 10


class SimpleSharedTimedDictionary:
    """Simple dictionary for time based memory"""
    def __init__(self, maxsize: int | None = None, ttl: int | None = None):
        self.data = TTLCache(maxsize=maxsize or MAXSIZE, ttl=ttl or TTL)  # type: ignore
