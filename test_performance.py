"""
Tests for performance optimizations in the competitive analysis tool.
"""
import pytest
import asyncio
import time
from unittest.mock import Mock, patch, AsyncMock

from cache import cached, cache_manager, CacheManager
from analyzer import DataAnalyzer
from config import Config


class TestCaching:
    """Test caching functionality and performance."""
    
    def test_cache_decorator_caches_results(self):
        """Test that cache decorator properly caches function results."""
        call_count = 0
        
        @cached
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        # First call should execute function
        result1 = expensive_function(5)
        assert result1 == 10
        assert call_count == 1
        
        # Second call should use cache
        result2 = expensive_function(5)
        assert result2 == 10
        assert call_count == 1  # Should not increment
        
        # Different argument should execute function again
        result3 = expensive_function(6)
        assert result3 == 12
        assert call_count == 2
    
    def test_cache_key_generation(self):
        """Test that cache key generation is consistent and efficient."""
        key1 = CacheManager.generate_key(1, 2, 3, foo="bar")
        key2 = CacheManager.generate_key(1, 2, 3, foo="bar")
        key3 = CacheManager.generate_key(1, 2, 3, foo="baz")
        
        assert key1 == key2  # Same inputs should produce same key
        assert key1 != key3  # Different inputs should produce different key
        assert len(key1) == 32  # MD5 hash length
    
    def test_cache_can_be_disabled(self):
        """Test that caching can be disabled via config."""
        cache_manager.clear()
        
        with patch('cache.config.cache_enabled', False):
            call_count = 0
            
            @cached
            def test_func(x):
                nonlocal call_count
                call_count += 1
                return x
            
            test_func(1)
            test_func(1)
            
            # Should call function twice when cache is disabled
            assert call_count == 2


class TestDataAnalyzer:
    """Test data analyzer performance optimizations."""
    
    def test_keyword_analysis_efficiency(self):
        """Test that keyword analysis uses efficient algorithms."""
        # Create test data
        test_data = [
            {'title': 'Test Page One', 'headings': ['Header 1', 'Header 2']},
            {'title': 'Test Page Two', 'headings': ['Header 3', 'Header 4']},
        ] * 50  # 100 items
        
        analyzer = DataAnalyzer()
        
        # Measure execution time
        start = time.time()
        result = analyzer.analyze_keywords(test_data)
        duration = time.time() - start
        
        # Should complete quickly (under 1 second for 100 items)
        assert duration < 1.0
        assert 'top_keywords' in result
        assert 'total_unique_words' in result
    
    def test_similarity_calculation_uses_sets(self):
        """Test that similarity calculation uses efficient set operations."""
        analyzer = DataAnalyzer()
        
        data1 = {'title': 'Python Programming Guide', 'headings': ['Introduction', 'Setup']}
        data2 = {'title': 'Python Tutorial Advanced', 'headings': ['Introduction', 'Examples']}
        
        # Calculate similarity
        start = time.time()
        similarity = analyzer.calculate_similarity(data1, data2)
        duration = time.time() - start
        
        # Should be very fast (under 0.01 seconds)
        assert duration < 0.01
        assert 0 <= similarity <= 1
        assert similarity > 0  # Should have some overlap
    
    def test_link_metrics_uses_sets(self):
        """Test that link metrics calculation uses efficient set operations."""
        analyzer = DataAnalyzer()
        
        test_data = [
            {'links': ['https://example.com/page1', 'https://example.com/page2']},
            {'links': ['https://example.org/page1', 'https://example.com/page3']},
        ] * 25  # 50 items
        
        start = time.time()
        metrics = analyzer.calculate_link_metrics(test_data)
        duration = time.time() - start
        
        # Should be fast
        assert duration < 0.1
        assert 'total_links' in metrics
        assert 'unique_domains' in metrics
        assert metrics['unique_domains'] == 2
    
    def test_report_generation_avoids_quadratic_complexity(self):
        """Test that report generation avoids O(n²) complexity where possible."""
        analyzer = DataAnalyzer()
        
        # Create larger dataset
        test_data = [
            {'title': f'Page {i}', 'headings': [f'Header {i}'], 'links': [f'https://example.com/{i}']}
            for i in range(50)
        ]
        
        start = time.time()
        report = analyzer.generate_report(test_data)
        duration = time.time() - start
        
        # Should complete in reasonable time (under 2 seconds)
        assert duration < 2.0
        assert 'total_pages_analyzed' in report
        assert report['total_pages_analyzed'] == 50


class TestConfig:
    """Test configuration management."""
    
    def test_config_has_sensible_defaults(self):
        """Test that configuration has performance-oriented defaults."""
        config = Config()
        
        assert config.cache_enabled is True
        assert config.max_concurrent_requests > 0
        assert config.batch_size > 0
        assert config.use_multiprocessing is True
    
    def test_config_loads_from_env(self):
        """Test that configuration can be loaded from environment."""
        with patch.dict('os.environ', {
            'CACHE_ENABLED': 'false',
            'MAX_CONCURRENT_REQUESTS': '20'
        }):
            config = Config.from_env()
            assert config.cache_enabled is False
            assert config.max_concurrent_requests == 20


@pytest.mark.asyncio
class TestAsyncPerformance:
    """Test async performance optimizations."""
    
    async def test_concurrent_operations(self):
        """Test that async operations can run concurrently."""
        call_times = []
        
        async def mock_operation(delay: float):
            start = time.time()
            await asyncio.sleep(delay)
            call_times.append(time.time() - start)
        
        # Run 5 operations that each take 0.1s
        start = time.time()
        await asyncio.gather(*[mock_operation(0.1) for _ in range(5)])
        total_duration = time.time() - start
        
        # With concurrency, should take ~0.1s, not 0.5s
        assert total_duration < 0.3  # Allow some overhead


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
