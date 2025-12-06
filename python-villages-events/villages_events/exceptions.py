"""Exception classes for Villages Events library."""


class VillagesEventError(Exception):
    """Base exception for Villages Events library."""
    pass


class APIError(VillagesEventError):
    """Exception raised when API requests fail."""
    pass


class AuthError(VillagesEventError):
    """Exception raised when authentication fails."""
    pass
