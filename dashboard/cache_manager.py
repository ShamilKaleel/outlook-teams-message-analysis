"""
Cache Manager for Analytics Dashboard

Manages saving and loading analytics results to/from JSON files
to avoid unnecessary API calls and provide offline access.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any


class CacheManager:
    """Manages caching of analytics results in JSON format."""

    def __init__(self, cache_dir: str = "cache"):
        """
        Initialize cache manager.

        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = Path(__file__).parent / cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.outlook_cache_file = self.cache_dir / "outlook_analytics.json"
        self.teams_cache_file = self.cache_dir / "teams_analytics.json"

    def save_outlook_analytics(self, data: Dict[str, Any]) -> None:
        """
        Save Outlook analytics to cache.

        Args:
            data: Analytics data dictionary
        """
        cache_data = {
            "cached_at": datetime.now().isoformat(),
            "data": data
        }
        with open(self.outlook_cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)

    def load_outlook_analytics(self) -> Optional[Dict[str, Any]]:
        """
        Load Outlook analytics from cache.

        Returns:
            Cached analytics data or None if not found
        """
        if not self.outlook_cache_file.exists():
            return None

        try:
            with open(self.outlook_cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            return cache_data
        except (json.JSONDecodeError, IOError):
            return None

    def save_teams_analytics(self, data: Dict[str, Any]) -> None:
        """
        Save Teams analytics to cache.

        Args:
            data: Analytics data dictionary
        """
        cache_data = {
            "cached_at": datetime.now().isoformat(),
            "data": data
        }
        with open(self.teams_cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)

    def load_teams_analytics(self) -> Optional[Dict[str, Any]]:
        """
        Load Teams analytics from cache.

        Returns:
            Cached analytics data or None if not found
        """
        if not self.teams_cache_file.exists():
            return None

        try:
            with open(self.teams_cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            return cache_data
        except (json.JSONDecodeError, IOError):
            return None

    def has_outlook_cache(self) -> bool:
        """Check if Outlook analytics cache exists."""
        return self.outlook_cache_file.exists()

    def has_teams_cache(self) -> bool:
        """Check if Teams analytics cache exists."""
        return self.teams_cache_file.exists()

    def clear_outlook_cache(self) -> None:
        """Clear Outlook analytics cache."""
        if self.outlook_cache_file.exists():
            self.outlook_cache_file.unlink()

    def clear_teams_cache(self) -> None:
        """Clear Teams analytics cache."""
        if self.teams_cache_file.exists():
            self.teams_cache_file.unlink()

    def clear_all_cache(self) -> None:
        """Clear all analytics cache."""
        self.clear_outlook_cache()
        self.clear_teams_cache()
