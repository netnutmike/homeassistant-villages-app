"""Python library for fetching entertainment events from The Villages, Florida.

This library provides a simple interface to fetch event data from The Villages
entertainment calendar API.
"""

from .client import VillagesEvents
from .exceptions import VillagesEventError, APIError, AuthError

__version__ = "1.1.0"
__all__ = ["VillagesEvents", "VillagesEventError", "APIError", "AuthError"]
