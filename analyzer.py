"""
Efficient data processing and analysis module.
Uses vectorized operations and optimized algorithms.
"""
from typing import List, Dict, Any, Set
from collections import Counter
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

from config import config


class DataAnalyzer:
    """Analyzes competitive data with optimized algorithms."""
    
    @staticmethod
    def analyze_keywords(data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze keywords from collected data efficiently.
        Uses Counter for O(n) complexity instead of nested loops.
        
        Args:
            data_list: List of collected data dictionaries
            
        Returns:
            Analysis results
        """
        # Use Counter for efficient counting
        all_words = []
        all_headings = []
        
        for data in data_list:
            # Extract title words
            if data.get('title'):
                all_words.extend(data['title'].lower().split())
            
            # Extract heading text
            if data.get('headings'):
                for heading in data['headings']:
                    all_headings.append(heading.lower())
                    all_words.extend(heading.lower().split())
        
        # Use Counter for O(n) counting instead of loops
        word_counts = Counter(all_words)
        
        # Filter out common stop words (simple version for demo)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        filtered_counts = {word: count for word, count in word_counts.items() 
                          if word not in stop_words and len(word) > 2}
        
        # Get top keywords efficiently
        top_keywords = dict(Counter(filtered_counts).most_common(20))
        
        return {
            'top_keywords': top_keywords,
            'total_unique_words': len(filtered_counts),
            'total_headings': len(all_headings)
        }
    
    @staticmethod
    def calculate_similarity(data1: Dict[str, Any], data2: Dict[str, Any]) -> float:
        """
        Calculate content similarity using Jaccard similarity.
        O(n) complexity with set operations.
        
        Args:
            data1: First data dictionary
            data2: Second data dictionary
            
        Returns:
            Similarity score (0-1)
        """
        # Extract words from both datasets
        words1 = set()
        words2 = set()
        
        for data, word_set in [(data1, words1), (data2, words2)]:
            if data.get('title'):
                word_set.update(data['title'].lower().split())
            if data.get('headings'):
                for h in data['headings']:
                    word_set.update(h.lower().split())
        
        # Use set operations for O(n) complexity
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    @staticmethod
    def _process_chunk(chunk: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process a chunk of data (for parallel processing)."""
        analyzer = DataAnalyzer()
        return analyzer.analyze_keywords(chunk)
    
    @staticmethod
    def analyze_batch_parallel(data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze data in parallel using multiprocessing.
        Splits data into chunks for parallel processing.
        
        Args:
            data_list: List of data to analyze
            
        Returns:
            List of analysis results
        """
        if not config.use_multiprocessing or len(data_list) < config.batch_size:
            # Not worth parallelizing for small datasets
            return [DataAnalyzer.analyze_keywords(data_list)]
        
        # Split data into chunks
        chunk_size = max(1, len(data_list) // config.max_workers)
        chunks = [data_list[i:i + chunk_size] 
                 for i in range(0, len(data_list), chunk_size)]
        
        # Process chunks in parallel
        with ProcessPoolExecutor(max_workers=config.max_workers) as executor:
            results = list(executor.map(DataAnalyzer._process_chunk, chunks))
        
        return results
    
    @staticmethod
    def calculate_link_metrics(data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate link-based metrics efficiently.
        Uses sets for O(1) lookups.
        
        Args:
            data_list: List of collected data
            
        Returns:
            Link metrics
        """
        all_domains: Set[str] = set()
        total_links = 0
        
        for data in data_list:
            links = data.get('links', [])
            total_links += len(links)
            
            # Extract domains efficiently
            for link in links:
                if link and '://' in link:
                    try:
                        domain = link.split('://')[1].split('/')[0]
                        all_domains.add(domain)
                    except IndexError:
                        continue
        
        return {
            'total_links': total_links,
            'unique_domains': len(all_domains),
            'avg_links_per_page': total_links / len(data_list) if data_list else 0
        }
    
    @staticmethod
    def generate_report(data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive analysis report.
        
        Args:
            data_list: List of collected data
            
        Returns:
            Complete analysis report
        """
        if not data_list:
            return {'error': 'No data to analyze'}
        
        # Run all analyses
        keyword_analysis = DataAnalyzer.analyze_keywords(data_list)
        link_metrics = DataAnalyzer.calculate_link_metrics(data_list)
        
        # Calculate average similarities (optimized to avoid O(n²))
        # Only compare first 10 pages to limit complexity
        similarities = []
        sample_size = min(10, len(data_list))
        for i in range(sample_size):
            for j in range(i + 1, sample_size):
                sim = DataAnalyzer.calculate_similarity(data_list[i], data_list[j])
                similarities.append(sim)
        
        avg_similarity = float(np.mean(similarities)) if similarities else 0.0
        
        return {
            'total_pages_analyzed': len(data_list),
            'keyword_analysis': keyword_analysis,
            'link_metrics': link_metrics,
            'avg_content_similarity': round(avg_similarity, 3),
            'performance_note': 'Used optimized algorithms for O(n) complexity where possible'
        }
