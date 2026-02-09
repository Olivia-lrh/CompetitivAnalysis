"""
Configuration module for Competitive Analysis tool.
Uses environment variables and provides sensible defaults.
"""
import os
from typing import Optional
from pydantic import BaseModel, Field


class Config(BaseModel):
    """Configuration for the competitive analysis tool."""
    
    # Cache settings
    cache_enabled: bool = Field(default=True)
    cache_ttl: int = Field(default=3600, description="Cache TTL in seconds")
    
    # Performance settings
    max_concurrent_requests: int = Field(default=10, description="Max concurrent API requests")
    request_timeout: int = Field(default=30, description="Request timeout in seconds")
    batch_size: int = Field(default=100, description="Batch size for processing")
    
    # API settings
    api_rate_limit: int = Field(default=100, description="API rate limit per minute")
    
    # Data processing
    use_multiprocessing: bool = Field(default=True)
    max_workers: int = Field(default=4)
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        return cls(
            cache_enabled=os.getenv("CACHE_ENABLED", "true").lower() == "true",
            cache_ttl=int(os.getenv("CACHE_TTL", "3600")),
            max_concurrent_requests=int(os.getenv("MAX_CONCURRENT_REQUESTS", "10")),
            request_timeout=int(os.getenv("REQUEST_TIMEOUT", "30")),
            batch_size=int(os.getenv("BATCH_SIZE", "100")),
            api_rate_limit=int(os.getenv("API_RATE_LIMIT", "100")),
            use_multiprocessing=os.getenv("USE_MULTIPROCESSING", "true").lower() == "true",
            max_workers=int(os.getenv("MAX_WORKERS", "4"))
        )


# Global config instance
config = Config.from_env()
