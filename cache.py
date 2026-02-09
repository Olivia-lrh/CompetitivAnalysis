"""
Efficient caching module using in-memory cache with TTL.
Provides decorators for caching function results.
"""
import functools
import hashlib
import json
import time
from typing import Any, Callable, Optional
from cachetools import TTLCache

from config import config


class CacheManager:
    """Manages in-memory caching with TTL support."""
    
    def __init__(self, maxsize: int = 1000, ttl: int = 3600):
        """
        Initialize cache manager.
        
        Args:
            maxsize: Maximum number of items in cache
            ttl: Time to live in seconds
        """
        self._cache = TTLCache(maxsize=maxsize, ttl=ttl)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        return self._cache.get(key)
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        self._cache[key] = value
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
    
    @staticmethod
    def generate_key(*args, **kwargs) -> str:
        """Generate cache key from function arguments."""
        # Create a string representation of arguments
        key_data = {
            "args": args,
            "kwargs": sorted(kwargs.items())
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        # Use hash for efficient key storage
        return hashlib.md5(key_str.encode()).hexdigest()


# Global cache instance
cache_manager = CacheManager(ttl=config.cache_ttl)


def cached(func: Callable) -> Callable:
    """
    Decorator to cache function results.
    Uses efficient hash-based keys and TTL cache.
    
    Args:
        func: Function to cache
        
    Returns:
        Wrapped function with caching
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not config.cache_enabled:
            return func(*args, **kwargs)
        
        # Generate cache key
        cache_key = f"{func.__name__}:{CacheManager.generate_key(*args, **kwargs)}"
        
        # Check cache
        cached_result = cache_manager.get(cache_key)
        if cached_result is not None:
            return cached_result
        
        # Execute function and cache result
        result = func(*args, **kwargs)
        cache_manager.set(cache_key, result)
        
        return result
    
    return wrapper
