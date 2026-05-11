"""Swimming research comparison and benchmark search."""
import json
import logging
from typing import Dict, Any, List, Optional
from duckduckgo_search import DDGS

from src.config import RESEARCH_CACHE_FILE
from src.storage import DataStore

logger = logging.getLogger(__name__)


class ResearchService:
    """Searches for swimming benchmarks and compares performance."""

    @staticmethod
    def load_cache() -> Dict[str, Any]:
        """Load research cache from file."""
        if not RESEARCH_CACHE_FILE.exists():
            return {}
        try:
            with open(RESEARCH_CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning("Failed to load research cache from %s: [%s] %s", RESEARCH_CACHE_FILE, type(e).__name__, e)
            return {}

    @staticmethod
    def save_cache(cache: Dict[str, Any]) -> None:
        """Save research cache to file."""
        RESEARCH_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(RESEARCH_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)

    @classmethod
    def search_benchmarks(cls, stroke: str, distance: int, age: int, gender: str = "female") -> List[Dict[str, Any]]:
        """Search for age-group swimming benchmarks.
        
        Returns:
            List of search results with title, body, and URL.
        """
        cache_key = f"{stroke}_{distance}m_age{age}_{gender}"
        cache = cls.load_cache()
        
        if cache_key in cache:
            return cache[cache_key]
        
        query = f"{stroke} {distance}m swimming benchmark time age {age} {gender}"
        
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
                cache[cache_key] = results
                cls.save_cache(cache)
                return results
        except (ConnectionError, TimeoutError) as e:
            logger.error("Network error during benchmark search for '%s': [%s] %s", query, type(e).__name__, e)
            return []
        except Exception as e:
            logger.error("Search failed for query '%s'", query, exc_info=True)
            return []

    @classmethod
    def get_comparison(cls, stroke: str, distance: int, age: int, gender: str = "female") -> Dict[str, Any]:
        """Compare Sunny's best time against benchmarks.
        
        Returns:
            Dictionary with best time, benchmark data, and percentile estimate.
        """
        from src.analytics import PerformanceAnalytics
        
        pb_df = PerformanceAnalytics.get_personal_bests()
        pb_row = pb_df[(pb_df["stroke"] == stroke) & (pb_df["distance"] == distance)]
        
        if pb_row.empty:
            return {"error": "No personal best found for this event"}
        
        best_time = pb_row.iloc[0]["time"]
        best_date = pb_row.iloc[0]["date"]
        
        benchmarks = cls.search_benchmarks(stroke, distance, age, gender)
        
        return {
            "stroke": stroke,
            "distance": distance,
            "personal_best": best_time,
            "pb_date": best_date,
            "age": age,
            "gender": gender,
            "benchmarks": benchmarks,
            "note": "Percentile calculation requires specific benchmark tables"
        }

    @classmethod
    def add_manual_benchmark_url(cls, url: str, description: str) -> None:
        """Add a manually provided benchmark URL to cache."""
        cache = cls.load_cache()
        if "manual_urls" not in cache:
            cache["manual_urls"] = []
        cache["manual_urls"].append({"url": url, "description": description})
        cls.save_cache(cache)
