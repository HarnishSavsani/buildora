# apps/common/locale/__init__.py
"""
languagemanagepublic common module
Provide common language configuration and deployment functions for cross-projects
"""

from .manager import LocaleManager, get_locale_manager, deploy_external_locales
from .config_helper import LocaleConfigHelper

__all__ = [
    'LocaleManager',
    'get_locale_manager',
    'deploy_external_locales',
    'LocaleConfigHelper'
]
