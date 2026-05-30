class ProviderError(Exception):
    """Base class for provider errors."""
    
class ProviderConnectionError(ProviderError):
    """Raised when there is a connection error with the provider."""
    
class ProviderAuthenticationError(ProviderError):
    """Raised when there is an authentication error with the provider."""
    
class ProviderTimeoutError(ProviderError):
    """Raised when a request to the provider times out."""
    
class ProviderRateLimitError(ProviderError):
    """Raised when the provider rate limit is exceeded."""
    