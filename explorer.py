import os
import argparse
import json
from datetime import datetime

def format_metadata(path):
    """Extract metadata for a given file."""
    try:
        stats = os.lstat(path)  # lstat allows symbolic link detection
    except (FileNotFoundError, PermissionError):
        return None

    return {
        "name": os.path.basename(path),
        "path": path,
        "is_file": os.path.isfile(path),
        "is_dir": os.path.isdir(path),
        "is_link": os.path.islink(path),
        "size_bytes": stats.st_size,
        "modified": datetime.fromtimestamp(stats.st_mtime).isoformat()
    }

def explore_directory(path, show_hidden=False, max_entries=5000):
    """Explore directory with filtering + safety for huge directories."""
    try:
        items = os.listdir(path)
    except FileNotFoundError:
        print("❌ Invalid path: Directory does not exist.")
        return []
    except PermissionError:
        print("❌ Permission denied.")
        return []

    # Handle hidden files
    if not show_hidden:
        items = [item for item in items if not item.startswith(".")]

    # Limit large folders
    if len(items) > max_entries:
        print(f"⚠️  Directory has {len(items)} items. Showing first {max_entries}.")
        items = items[:max_entries]

    results = []
    for item in items:
        full_path = os.path.join(path, item)
        meta = format_metadata(full_path)
        if meta:
            results.append(meta)

    return results

def print_table(data):
    """Print clean table-like output."""
    print(f"{'Type':10} | {'Name':30} | {'Size (bytes)':12} | Last Modified")
    print("-" * 80)

    for entry in data:
        ftype = "FILE" if entry["is_file"] else "DIR" if entry["is_dir"] else "LINK"
        print(f"{ftype:10} | {entry['name'][:30]:30} | {entry['size_bytes']:12} | {entry['modified']}")

def main():
    parser = argparse.ArgumentParser(description="Advanced File System Explorer")

    parser.add_argument("--path", required=True, help="Directory to explore")
    parser.add_argument("--hidden", action="store_true", help="Show hidden files")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--max", type=int, default=5000, help="Max entries to scan in huge directories")

    args = parser.parse_args()

    # Validate path
    if not os.path.isdir(args.path):
        print("❌ Error: Provided --path is not a valid directory.")
        return

    data = explore_directory(args.path, show_hidden=args.hidden, max_entries=args.max)

    if args.json:
        print(json.dumps(data, indent=4))
    else:
        print_table(data)

if __name__ == "__main__":
    main()
