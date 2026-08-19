# apps/common/locale/config_helper.py
"""
Language configuration assistant
for Config Class provides language-specific helper methods
"""

import os
from typing import List, Tuple, Dict

from common.utils.logger import maxkb_logger as logger


class LocaleConfigHelper:
    """Language configuration assistant - for Config Class usage"""

    # Mapping of standardized language codes to display names（ISO 639-1 standard）
    STANDARD_LANGUAGE_NAMES = {
        "en": "English",
        "en-US": "English",
        "zh-CN": "Simplified indian",
        "zh-Hant": "Traditional indian",
        "ja": "Japanese",
        "ko": "한국어",
        "fr": "Français",
        "de": "Deutsch",
        "es": "Español",
        "it": "Italiano",
        "pt": "Português",
        "pt-br": "Português (Brasil)",
        "ru": "Русский",
        "ar": "العربية",
        "hi": "हिन्दी",
        "th": "ไทย",
        "vi": "Tiếng Việt",
        "id": "Bahasa Indonesia",
        "ms": "Bahasa Melayu",
        "tr": "Türkçe",
        "nl": "Nederlands",
        "pl": "Polski",
        "sv": "Svenska",
        "da": "Dansk",
        "fi": "Suomi",
        "no": "Norsk",
        "cs": "Čeština",
        "hu": "Magyar",
        "ro": "Română",
        "uk": "Українська",
        "el": "Ελληνικά",
        "he": "עברית",
        "fa": "فارسی",
        "ur": "اردو",
        "bn": "বাংলা",
        "ta": "தமிழ்",
        "te": "తెలుగు",
        "mr": "मराठी",
    }

    DEFAULT_LANGUAGES = [("en", "English"), ("zh", "Simplified indian"), ("zh-hant", "Traditional indian")]

    @staticmethod
    def get_languages(config_object, project_dir: str) -> List[Tuple[str, str]]:
        """
        Get a list of supported languages（With cache）

        Args:
            config_object: Config Example
            project_dir: Project root directory

        Returns:
            Language list [(code, name), ...]
        """
        from .cache import get_locale_cache

        cache = get_locale_cache()

        # Try to get from cache
        cached_languages = cache.get()
        if cached_languages is not None:
            logger.debug("Using cached languages list")
            return cached_languages

        # Deploy external language pack
        from .manager import deploy_external_locales

        deploy_external_locales()

        # Get user-defined language name mapping
        custom_languages = LocaleConfigHelper._parse_custom_languages(config_object.get("LANGUAGES", ""))

        # Scan the language pack directory
        all_languages = {}
        internal_locales_dir = os.path.join(project_dir, "apps", "locales")

        if os.path.isdir(internal_locales_dir):
            LocaleConfigHelper._scan_locale_directory(
                internal_locales_dir, all_languages, LocaleConfigHelper.STANDARD_LANGUAGE_NAMES, custom_languages
            )

        # If no language is detected，Return to default language
        if not all_languages:
            languages = LocaleConfigHelper.DEFAULT_LANGUAGES
        else:
            # Sort by language code and convert to list
            languages = [(code, name) for code, name in sorted(all_languages.items())]

        # cache results
        cache.set(languages)
        logger.info(f"Detected {len(languages)} languages, cached for 5 minutes")

        return languages

    @staticmethod
    def _parse_custom_languages(languages_str: str) -> Dict[str, str]:
        """
        Parse user-defined language name mapping

        Args:
            languages_str: LANGUAGES Configuration string，The format is like "ja:Japanese,ko:한국어"

        Returns:
            Custom language mapping dictionary
        """
        custom_languages = {}
        if not languages_str:
            return custom_languages

        for lang_pair in languages_str.split(","):
            lang_pair = lang_pair.strip()
            if ":" in lang_pair:
                code, name = lang_pair.split(":", 1)
                custom_languages[code.strip()] = name.strip()

        return custom_languages

    @staticmethod
    def _scan_locale_directory(
        locales_dir: str,
        languages_dict: Dict[str, str],
        standard_names: Dict[str, str],
        custom_languages: Dict[str, str],
    ):
        """
        Scan the language packs in the specified directory

        Args:
            locales_dir: Language pack directory path
            languages_dict: Dictionary to store detected languages（will be modified）
            standard_names: Standard language name mapping
            custom_languages: Custom language name mapping
        """
        if not os.path.isdir(locales_dir):
            return

        for lang_dir in os.listdir(locales_dir):
            lang_path = os.path.join(locales_dir, lang_dir)
            if os.path.isdir(lang_path):
                # Convert directory names to standard language code format (zh_CN -> zh-cn, en_US -> en-us)
                lang_code = lang_dir.replace("_", "-")

                # Get display name（priority：Customize > standard mapping > directory name）
                display_name = None
                if lang_code in custom_languages:
                    display_name = custom_languages[lang_code]
                elif lang_code in standard_names:
                    display_name = standard_names[lang_code]
                else:
                    # Try to match the base code（like ja-JP -> ja）
                    base_code = lang_code.split("-")[0]
                    if base_code in custom_languages:
                        display_name = custom_languages[base_code]
                    elif base_code in standard_names:
                        display_name = standard_names[base_code]
                    else:
                        display_name = lang_dir

                # Register the full code and basic code at the same time，Achieve front-end and back-end compatibility
                # For example：Directory name ja_JP，Will register at the same time 'ja-jp' and 'ja'
                languages_dict[lang_code] = display_name

                # If the language code contains locale information，Register the basic code at the same time
                if "-" in lang_code:
                    base_code = lang_code.split("-")[0]
                    # Only if the base code has not been registered yet，just registered it
                    if base_code not in languages_dict:
                        languages_dict[base_code] = display_name

    @staticmethod
    def invalidate_cache():
        """Clear language cache（Called when the language pack is updated）"""
        from .cache import get_locale_cache

        get_locale_cache().invalidate()
        logger.info("Language cache invalidated")
