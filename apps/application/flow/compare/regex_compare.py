# coding=utf-8
"""
    @project: maxkb
    @Author：wangliang181230
    @file： regex_compare.py
    @date：2026/3/30 12:11
    @desc:
"""
import re

from .compare import Compare
from common.cache.mem_cache import MemCache

match_cache = MemCache('regex', {
    'TIMEOUT': 3600,  # Cache validity periodfor 1 Hour
    'OPTIONS': {
        'MAX_ENTRIES': 500,  # mostcache 500 piecesentry
        'CULL_FREQUENCY': 10,  # When the arrival limit is reached, Delete approx. 1/10 Cache
    },
})


def compile_and_cache(regex):
    match = match_cache.get(regex)
    if not match:
        match = re.compile(regex).fullmatch
        match_cache.set(regex, match)
    return match


class RegexCompare(Compare):

    def compare(self, source_value, compare, target_value):
        match = compile_and_cache(str(target_value))
        return bool(match(str(source_value)))
