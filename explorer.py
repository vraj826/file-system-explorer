import os
import argparse
import json
from datetime import datetime

def format_metadata(path):
    """Extract metadata for a given file."""
    try:
        stats = os.lstat(path)  # lstat allows symbolic links detection
    except (FileNotFoundError, PermissionError):
        return None

    metadata = {
        "name": os.path.basename(path),
        "path": path,
        "is_file": os.path.isfile(path),
        "is_dir": os.path.isdir(path),
        "is_link": os.path.islink(path),
        "size_bytes": stats.st_size,
        "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
    }
    return metadata


def explore_directory(path, show_hidden=False, max_entries=5000):
    """Explore directory with limit handling for very large folders."""
    try:
        items = os.listdir(path)
    except FileNotFoundError:
        raise FileNotFoundError("Invalid --path: Directory does not exist.")
    except PermissionError:
        raise PermissionError("Permission denied: Cannot access this folder.")

    # Filter hidden files if needed
    if not show_hidden:
        items = [item for item in items if not item.startswith(".")]

    # Limit entries for huge directories
    if len(items) > max_entries:
        print(f"⚠️ Directory has {len(items)} items. Showing first {max_entries}.")
        items = items[:max_entries]

    metadata_list = []

    for item in items:
        full_path = os.path.join(path, item)
        meta = format_metadata(full_path)
        if meta:
            metadata_list.append(meta)

    return metadata_list


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

    # Validate argument: must be a directory
    if not os.path.isdir(args.path):
        print("❌ Error: The provided --path is not a valid directory.")
        return

    # Explore directory
    data = explore_directory(args.path, show_hidden=args.hidden, max_entries=args.max)

    # Output in JSON
    if args.json:
        print(json.dumps(data, indent=4))
    else:
        print_table(data)


if __name__ == "__main__":
    main()
