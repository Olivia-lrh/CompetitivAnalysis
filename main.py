"""
Main module for Competitive Analysis tool.
Orchestrates data collection and analysis with optimal performance.
"""
import asyncio
import time
from typing import List, Dict, Any

from collector import collect_competitive_data
from analyzer import DataAnalyzer
from cache import cache_manager


class CompetitiveAnalysis:
    """Main class for competitive analysis operations."""
    
    def __init__(self):
        self.analyzer = DataAnalyzer()
    
    async def analyze_competitors(self, urls: List[str]) -> Dict[str, Any]:
        """
        Analyze competitor websites.
        
        Args:
            urls: List of competitor URLs
            
        Returns:
            Analysis results
        """
        start_time = time.time()
        
        # Collect data asynchronously
        print(f"Collecting data from {len(urls)} URLs...")
        data = await collect_competitive_data(urls)
        collection_time = time.time() - start_time
        
        # Analyze collected data
        print(f"Analyzing {len(data)} pages...")
        analysis_start = time.time()
        report = self.analyzer.generate_report(data)
        analysis_time = time.time() - analysis_start
        
        # Add performance metrics
        report['performance_metrics'] = {
            'total_time': round(time.time() - start_time, 2),
            'collection_time': round(collection_time, 2),
            'analysis_time': round(analysis_time, 2),
            'pages_collected': len(data),
            'pages_per_second': round(len(data) / collection_time, 2) if collection_time > 0 else 0
        }
        
        return report
    
    def clear_cache(self):
        """Clear all cached data."""
        cache_manager.clear()
        print("Cache cleared")


def main():
    """Example usage of the competitive analysis tool."""
    # Example competitor URLs (replace with real URLs)
    competitor_urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net",
    ]
    
    analysis = CompetitiveAnalysis()
    
    # Run analysis
    print("Starting competitive analysis...")
    results = asyncio.run(analysis.analyze_competitors(competitor_urls))
    
    # Display results
    print("\n" + "="*60)
    print("COMPETITIVE ANALYSIS REPORT")
    print("="*60)
    
    for key, value in results.items():
        if isinstance(value, dict):
            print(f"\n{key.upper().replace('_', ' ')}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"\n{key}: {value}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
