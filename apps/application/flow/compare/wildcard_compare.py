# coding=utf-8
"""
    @project: maxkb
    @Author：wangliang181230
    @file： wildcard_compare.py
    @date：2026/3/30 12:11
    @desc:
"""
import fnmatch
import re

from .compare import Compare
from common.cache.mem_cache import MemCache


match_cache = MemCache('wildcard_to_regex', {
    'TIMEOUT': 3600, # Cache validity periodfor 1 Hour
    'OPTIONS': {
        'MAX_ENTRIES': 500, # mostcache 500 piecesentry
        'CULL_FREQUENCY': 10, # When the arrival limit is reached, Delete approx. 1/10 Cache
    },
})


def translate_and_compile_and_cache(wildcard):
    match = match_cache.get(wildcard)
    if not match:
        regex = fnmatch.translate(wildcard)
        match = re.compile(regex).match
        match_cache.set(wildcard, match)
    return match

class WildcardCompare(Compare):

    def compare(self, source_value, compare, target_value):
        # Convert toRegular, higher performance
        match = translate_and_compile_and_cache(str(target_value))
        return bool(match(str(source_value)))
