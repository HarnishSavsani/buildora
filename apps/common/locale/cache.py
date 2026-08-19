# apps/common/locale/cache.py
"""
languageConfigurationcachemanage
Avoid repeated scanning of documentsystem and improve performance
"""

import time
from typing import Optional, List, Tuple


class LocaleCache:
    """languageConfigurationcache"""

    def __init__(self, ttl: int = 300):
        """
        Initialize cache

        Args:
            ttl: Cache validity period (seconds), default 5 minute
        """
        self._cache: Optional[List[Tuple[str, str]]] = None
        self._timestamp: float = 0
        self._ttl = ttl

    def get(self) -> Optional[List[Tuple[str, str]]]:
        """getCachedLanguage list"""
        if self._cache is not None and (time.time() - self._timestamp) < self._ttl:
            return self._cache
        return None

    def set(self, languages: List[Tuple[str, str]]):
        """SettingsCachedLanguage list"""
        self._cache = languages
        self._timestamp = time.time()

    def invalidate(self):
        """Clearcache"""
        self._cache = None
        self._timestamp = 0

    @property
    def is_valid(self) -> bool:
        """Check if the cache Yes is valid"""
        return self._cache is not None and (time.time() - self._timestamp) < self._ttl


# global cacheExample
_locale_cache = LocaleCache(ttl=300)


def get_locale_cache() -> LocaleCache:
    """getGlobal cache languageExample"""
    return _locale_cache
