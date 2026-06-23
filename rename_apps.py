import os
import re

# The project root
ROOT_DIR = r"c:\Users\HP\Documents\PFA project"

# Files to skip
SKIP_DIRS = {".git", "venv", ".gemini", "staticfiles", "media", "__pycache__"}

# Replacements (old: new)
REPLACEMENTS = {
    # books -> catalog
    r"\bbooks\b": "catalog",
    # notifications -> alerts
    r"\bnotifications\b": "alerts",
    # stats -> dashboard
    r"\bstats\b": "dashboard",
}

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False
        
    new_content = content
    # We must ensure we don't break things like 'books' in normal text if it's not code,
    # but since it's an app name, \bbooks\b is usually safe for code.
    # Actually, let's just do exact string replacements for specific patterns to be extremely safe:
    
    # Imports:
    new_content = re.sub(r'\bfrom books\b', 'from catalog', new_content)
    new_content = re.sub(r'\bimport books\b', 'import catalog', new_content)
    new_content = re.sub(r'\bfrom notifications\b', 'from alerts', new_content)
    new_content = re.sub(r'\bimport notifications\b', 'import alerts', new_content)
    new_content = re.sub(r'\bfrom stats\b', 'from dashboard', new_content)
    new_content = re.sub(r'\bimport stats\b', 'import dashboard', new_content)
    
    # URL namespaces
    new_content = new_content.replace("'books:", "'catalog:")
    new_content = new_content.replace('"books:', '"catalog:')
    new_content = new_content.replace("'notifications:", "'alerts:")
    new_content = new_content.replace('"notifications:', '"alerts:')
    new_content = new_content.replace("'stats:", "'dashboard:")
    new_content = new_content.replace('"stats:', '"dashboard:')
    
    # Foreign Keys and App Labels
    new_content = new_content.replace("'books.", "'catalog.")
    new_content = new_content.replace('"books.', '"catalog.')
    new_content = new_content.replace("'notifications.", "'alerts.")
    new_content = new_content.replace('"notifications.', '"alerts.')
    new_content = new_content.replace("'stats.", "'dashboard.")
    new_content = new_content.replace('"stats.', '"dashboard.')

    # Exact string matches for dependencies and config
    new_content = new_content.replace("'books'", "'catalog'")
    new_content = new_content.replace('"books"', '"catalog"')
    new_content = new_content.replace("'notifications'", "'alerts'")
    new_content = new_content.replace('"notifications"', '"alerts"')
    new_content = new_content.replace("'stats'", "'dashboard'")
    new_content = new_content.replace('"stats"', '"dashboard"')

    # Template paths inside views/render
    new_content = new_content.replace('"books/', '"catalog/')
    new_content = new_content.replace("'books/", "'catalog/")
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {filepath}")
        return True
    return False

def main():
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for file in files:
            if file.endswith('.py') or file.endswith('.html'):
                filepath = os.path.join(root, file)
                # Skip the rename script itself
                if file == "rename_apps.py":
                    continue
                if process_file(filepath):
                    count += 1
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    main()
