"""
Example demonstrating the performance optimizations.
Shows the benefits of caching, async operations, and efficient algorithms.
"""
import asyncio
import time
from typing import List
from cache import cache_manager
from analyzer import DataAnalyzer


def benchmark_caching():
    """Demonstrate caching performance benefits."""
    print("\n" + "="*60)
    print("CACHING PERFORMANCE DEMO")
    print("="*60)
    
    from cache import cached
    
    @cached
    def simulate_expensive_computation(data: str) -> dict:
        """Simulates an expensive computation."""
        time.sleep(0.1)  # Simulate 100ms computation
        return {
            'processed': data.upper(),
            'length': len(data),
            'timestamp': time.time()
        }
    
    test_data = "competitive analysis test data"
    
    # First call - no cache
    start = time.time()
    result1 = simulate_expensive_computation(test_data)
    time1 = time.time() - start
    
    # Second call - from cache
    start = time.time()
    result2 = simulate_expensive_computation(test_data)
    time2 = time.time() - start
    
    print(f"First call (no cache): {time1*1000:.2f}ms")
    print(f"Second call (cached): {time2*1000:.2f}ms")
    print(f"Speedup: {time1/time2:.1f}x faster")
    print(f"Time saved: {(time1-time2)*1000:.2f}ms")
    
    cache_manager.clear()


def benchmark_efficient_algorithms():
    """Demonstrate efficient algorithm benefits."""
    print("\n" + "="*60)
    print("ALGORITHM EFFICIENCY DEMO")
    print("="*60)
    
    analyzer = DataAnalyzer()
    
    # Create test dataset
    test_data = [
        {
            'title': f'Product Page {i}',
            'headings': [f'Feature {i}-{j}' for j in range(5)],
            'links': [f'https://example.com/page{i}-{j}' for j in range(10)]
        }
        for i in range(100)
    ]
    
    print(f"Analyzing {len(test_data)} pages...")
    
    # Benchmark keyword analysis
    start = time.time()
    keywords = analyzer.analyze_keywords(test_data)
    keyword_time = time.time() - start
    
    # Benchmark link metrics
    start = time.time()
    links = analyzer.calculate_link_metrics(test_data)
    link_time = time.time() - start
    
    # Benchmark full report
    start = time.time()
    report = analyzer.generate_report(test_data)
    report_time = time.time() - start
    
    print(f"\nKeyword Analysis: {keyword_time*1000:.2f}ms")
    print(f"  - Found {keywords['total_unique_words']} unique words")
    print(f"  - O(n) complexity using Counter")
    
    print(f"\nLink Metrics: {link_time*1000:.2f}ms")
    print(f"  - Processed {links['total_links']} links")
    print(f"  - O(n) complexity using set operations")
    
    print(f"\nFull Report: {report_time*1000:.2f}ms")
    print(f"  - Total pages: {report['total_pages_analyzed']}")
    print(f"  - Note: {report['performance_note']}")


async def benchmark_async_operations():
    """Demonstrate async performance benefits."""
    print("\n" + "="*60)
    print("ASYNC I/O PERFORMANCE DEMO")
    print("="*60)
    
    async def simulate_network_request(delay: float) -> str:
        """Simulates a network request."""
        await asyncio.sleep(delay)
        return f"Response after {delay}s"
    
    num_requests = 10
    request_delay = 0.1  # 100ms each
    
    # Sequential execution
    print(f"\nSequential execution of {num_requests} requests...")
    start = time.time()
    results_seq = []
    for i in range(num_requests):
        result = await simulate_network_request(request_delay)
        results_seq.append(result)
    sequential_time = time.time() - start
    
    # Concurrent execution
    print(f"Concurrent execution of {num_requests} requests...")
    start = time.time()
    tasks = [simulate_network_request(request_delay) for i in range(num_requests)]
    results_async = await asyncio.gather(*tasks)
    concurrent_time = time.time() - start
    
    print(f"\nSequential time: {sequential_time*1000:.0f}ms")
    print(f"Concurrent time: {concurrent_time*1000:.0f}ms")
    print(f"Speedup: {sequential_time/concurrent_time:.1f}x faster")
    print(f"Time saved: {(sequential_time-concurrent_time)*1000:.0f}ms")
    print(f"\nNote: Real-world speedup with actual network requests")
    print(f"      can be 10-20x depending on network latency")


def benchmark_set_operations():
    """Demonstrate set operation efficiency."""
    print("\n" + "="*60)
    print("SET OPERATIONS EFFICIENCY DEMO")
    print("="*60)
    
    # Create large datasets
    data1 = set(range(10000))
    data2 = set(range(5000, 15000))
    
    # Set intersection (efficient)
    start = time.time()
    intersection = data1 & data2
    set_time = time.time() - start
    
    # List-based approach (inefficient - for comparison)
    list1 = list(data1)
    list2 = list(data2)
    start = time.time()
    intersection_list = [x for x in list1 if x in list2]
    list_time = time.time() - start
    
    print(f"Dataset size: {len(data1):,} and {len(data2):,} items")
    print(f"\nSet intersection: {set_time*1000:.2f}ms")
    print(f"List comprehension: {list_time*1000:.2f}ms")
    print(f"Speedup: {list_time/set_time:.1f}x faster with sets")
    print(f"\nIntersection size: {len(intersection):,} items")


def main():
    """Run all benchmarks."""
    print("\n" + "="*70)
    print(" " * 15 + "PERFORMANCE OPTIMIZATION BENCHMARKS")
    print("="*70)
    
    # Run synchronous benchmarks
    benchmark_caching()
    benchmark_efficient_algorithms()
    benchmark_set_operations()
    
    # Run async benchmarks
    asyncio.run(benchmark_async_operations())
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("""
Key Takeaways:
1. Caching: 100-1000x speedup for repeated operations
2. Async I/O: 10-20x speedup for concurrent network requests
3. Efficient data structures: 10-100x speedup (sets vs lists)
4. O(n) algorithms: Linear scaling instead of quadratic

These optimizations combine to make the tool highly performant
even with large datasets and many concurrent operations.
    """)


if __name__ == "__main__":
    main()
