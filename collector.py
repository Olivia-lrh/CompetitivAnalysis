"""
Efficient data collection module with async requests and rate limiting.
Uses connection pooling and concurrent requests for optimal performance.
"""
import asyncio
import time
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
import aiohttp
from bs4 import BeautifulSoup

from config import config
from cache import cached


class RateLimiter:
    """Token bucket rate limiter for API calls."""
    
    def __init__(self, rate: int, per: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            rate: Number of requests allowed
            per: Time period in seconds
        """
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = time.time()
    
    async def acquire(self):
        """Acquire permission to make a request."""
        current = time.time()
        time_passed = current - self.last_check
        self.last_check = current
        self.allowance += time_passed * (self.rate / self.per)
        
        if self.allowance > self.rate:
            self.allowance = self.rate
        
        if self.allowance < 1.0:
            sleep_time = (1.0 - self.allowance) * (self.per / self.rate)
            await asyncio.sleep(sleep_time)
            self.allowance = 0.0
        else:
            self.allowance -= 1.0


class DataCollector:
    """Efficient data collector with async requests and caching."""
    
    def __init__(self):
        self.rate_limiter = RateLimiter(rate=config.api_rate_limit)
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Create session with connection pooling."""
        # Use connection pooling for better performance
        connector = aiohttp.TCPConnector(
            limit=config.max_concurrent_requests,
            limit_per_host=5,
            ttl_dns_cache=300
        )
        timeout = aiohttp.ClientTimeout(total=config.request_timeout)
        self._session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close session."""
        if self._session:
            await self._session.close()
    
    async def fetch_url(self, url: str) -> Optional[str]:
        """
        Fetch content from URL with rate limiting.
        
        Args:
            url: URL to fetch
            
        Returns:
            Page content or None on error
        """
        await self.rate_limiter.acquire()
        
        try:
            async with self._session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                return None
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    @cached
    def parse_html(self, html: str) -> Dict[str, Any]:
        """
        Parse HTML content efficiently using lxml parser.
        Uses caching to avoid re-parsing.
        
        Args:
            html: HTML content
            
        Returns:
            Parsed data dictionary
        """
        # Use lxml parser for better performance
        soup = BeautifulSoup(html, 'lxml')
        
        return {
            'title': soup.title.string if soup.title else None,
            'meta_description': self._get_meta_description(soup),
            'headings': [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])],
            'links': [a.get('href') for a in soup.find_all('a', href=True)][:50]  # Limit for performance
        }
    
    @staticmethod
    def _get_meta_description(soup: BeautifulSoup) -> Optional[str]:
        """Extract meta description efficiently."""
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta.get('content') if meta else None
    
    async def collect_batch(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Collect data from multiple URLs concurrently.
        
        Args:
            urls: List of URLs to fetch
            
        Returns:
            List of parsed data dictionaries
        """
        # Use semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(config.max_concurrent_requests)
        
        async def fetch_and_parse(url: str) -> Optional[Dict[str, Any]]:
            async with semaphore:
                html = await self.fetch_url(url)
                if html:
                    data = self.parse_html(html)
                    data['url'] = url
                    return data
                return None
        
        # Gather all results concurrently
        tasks = [fetch_and_parse(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out None and exceptions
        return [r for r in results if r and not isinstance(r, Exception)]


async def collect_competitive_data(urls: List[str]) -> List[Dict[str, Any]]:
    """
    Main entry point for collecting competitive data.
    
    Args:
        urls: List of competitor URLs
        
    Returns:
        List of collected and parsed data
    """
    async with DataCollector() as collector:
        return await collector.collect_batch(urls)
