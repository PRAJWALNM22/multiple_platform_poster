"""Platform adapters used by the posting service."""


class PlatformNotImplementedError(RuntimeError):
    """Raised when a platform adapter has not been connected to its API yet."""
