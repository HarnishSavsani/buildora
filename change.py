import os
import re
import time
import json
from deep_translator import GoogleTranslator

# --- CONFIGURATION ---
PROJECT_DIR = '.' 
CACHE_FILE = 'translation_cache.json'
BATCH_SIZE = 50

# Directories we absolutely want to skip to save time and prevent messing up dependencies
IGNORE_DIRS = {'node_modules', 'venv', 'env', '.venv', '.git', '__pycache__', 'dist', 'build', '.idea', '.vscode'}

# Binary extensions we should not even attempt to open
IGNORE_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.webp', # Images
    '.pdf', '.zip', '.tar', '.gz', '.rar', '.7z',             # Archives
    '.pyc', '.so', '.dll', '.exe', '.bin',                    # Compiled Binaries
    '.ttf', '.woff', '.woff2', '.eot',                        # Fonts
    '.sqlite3', '.db'                                         # Databases
}

CHINESE_REGEX = re.compile(r'[\u4e00-\u9fa5]+[^\s\n\r"\'`<>{}();,]*[\u4e00-\u9fa5]+|[\u4e00-\u9fa5]')
translator = GoogleTranslator(source='zh-CN', target='en')

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def extract_unique_strings():
    """Finds all unique Chinese strings across all text-readable files."""
    unique_strings = set()
    file_list = []

    for root, dirs, files in os.walk(PROJECT_DIR):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in IGNORE_EXTENSIONS:
                continue

            filepath = os.path.join(root, file)
            try:
                # Attempt to read as UTF-8 text. If it fails, its likely a binary file.
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                matches = CHINESE_REGEX.findall(content)
                if matches:
                    file_list.append(filepath)  # Only track files that actually contain Chinese
                    for m in matches:
                        unique_strings.add(m.strip())
            except UnicodeDecodeError:
                # File is binary or not UTF-8, safely skip it.
                pass
            except Exception:
                pass

    return list(unique_strings), file_list

def batch_translate(strings_to_translate, cache):
    """Translates strings in chunks to avoid rate limits and speed up the process."""
    DELIMITER = " ||| "
    untranslated = [s for s in strings_to_translate if s not in cache and s]

    print(f"Total unique Chinese phrases: {len(strings_to_translate)}")
    print(f"Already cached: {len(strings_to_translate) - len(untranslated)}")
    print(f"Needs translation: {len(untranslated)}")

    for i in range(0, len(untranslated), BATCH_SIZE):
        batch = untranslated[i:i + BATCH_SIZE]
        combined_text = DELIMITER.join(batch)

        try:
            translated_combined = translator.translate(combined_text)
            translated_parts = translated_combined.split("|||")

            if len(translated_parts) == len(batch):
                for original, trans in zip(batch, translated_parts):
                    cache[original] = trans.strip()
            else:
                for item in batch:
                    cache[item] = translator.translate(item).strip()

            print(f"Translated batch {i // BATCH_SIZE + 1}/{(len(untranslated) + BATCH_SIZE - 1) // BATCH_SIZE}")
            save_cache(cache)
            time.sleep(0.5)

        except Exception as e:
            print(f"Batch failed. Retrying individually...")
            for item in batch:
                try:
                    cache[item] = translator.translate(item).strip()
                except Exception:
                    cache[item] = item
            save_cache(cache)

    return cache

def apply_translations_to_files(file_list, cache):
    """Replaces Chinese strings with English across all identified text files."""
    print("\nApplying translations to files...")
    # Sort keys by length descending to prevent sub-string collision
    sorted_keys = sorted(cache.keys(), key=len, reverse=True)

    for filepath in file_list:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            modified = False
            for key in sorted_keys:
                if key in content and key != cache[key]:
                    content = content.replace(key, cache[key])
                    modified = True

            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated: {filepath}")
        except Exception as e:
            print(f"Could not update {filepath}: {e}")

def main():
    print("Step 1: Scanning project for text files with Chinese characters...")
    unique_strings, file_list = extract_unique_strings()
    
    print(f"\nStep 2: Batch translating... (Found {len(file_list)} files with Chinese text)")
    cache = load_cache()
    updated_cache = batch_translate(unique_strings, cache)

    print("\nStep 3: Writing changes to codebase...")
    apply_translations_to_files(file_list, updated_cache)
    print("\n✅ Done! All text files updated in English.")

if __name__ == "__main__":
    main()