import os
import argparse
import json
from datetime import datetime


# --------------------------------------------------
# METADATA EXTRACTION
# --------------------------------------------------
def format_metadata(path):
    """
    Collect metadata for a file or directory.

    Uses os.lstat() instead of os.stat() so that
    symbolic links can be detected without following them.
    """
    try:
        stats = os.lstat(path)
    except (FileNotFoundError, PermissionError):
        # File may disappear or be restricted during scan
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


# --------------------------------------------------
# FILE FILTERS (Milestone 3)
# --------------------------------------------------
def apply_filters(entry, ext=None, min_size=None, name=None):
    """
    Apply user-specified filters to files.

    DESIGN DECISION:
    - Directories are NEVER filtered out
    - Filters apply ONLY to files
    """

    if entry["is_dir"]:
        return True

    if ext and not entry["name"].endswith(ext):
        return False

    if min_size and entry["size_bytes"] < min_size:
        return False

    if name and name.lower() not in entry["name"].lower():
        return False

    return True


# --------------------------------------------------
# SORTING (Milestone 4)
# --------------------------------------------------
def sort_entries(entries, sort_key=None):
    """
    Sort file entries based on user preference.

    - Directories keep their relative order
    - Only files are sorted
    - Sorting is stable and predictable
    """
    if not sort_key:
        return entries

    dirs = [e for e in entries if e["is_dir"]]
    files = [e for e in entries if e["is_file"]]

    if sort_key == "name":
        files.sort(key=lambda x: x["name"].lower())

    elif sort_key == "size":
        files.sort(key=lambda x: x["size_bytes"])

    elif sort_key == "modified":
        files.sort(key=lambda x: x["modified"])

    return dirs + files


# --------------------------------------------------
# NON-RECURSIVE DIRECTORY SCAN
# --------------------------------------------------
def explore_directory(path, show_hidden=False, max_entries=5000,
                      ext=None, min_size=None, name=None):
    """
    Scan a single directory (non-recursive).

    Supports:
    - Hidden file filtering
    - Safety limits for very large directories
    - File-level filters
    """
    try:
        items = os.listdir(path)
    except FileNotFoundError:
        print("❌ Invalid path: Directory does not exist.")
        return []
    except PermissionError:
        print("❌ Permission denied.")
        return []

    if not show_hidden:
        items = [item for item in items if not item.startswith(".")]

    if len(items) > max_entries:
        print(f"⚠️  Directory has {len(items)} items. Showing first {max_entries}.")
        items = items[:max_entries]

    results = []
    for item in items:
        full_path = os.path.join(path, item)
        meta = format_metadata(full_path)

        if meta and apply_filters(meta, ext, min_size, name):
            meta["level"] = 0
            results.append(meta)

    return results


# --------------------------------------------------
# RECURSIVE DIRECTORY SCAN (os.walk)
# --------------------------------------------------
def recursive_explore(path, show_hidden=False, max_entries=5000,
                      depth=None, ext=None, min_size=None, name=None):
    """
    Recursively scan directories using os.walk().

    Supports:
    - Depth-limited traversal
    - File filtering
    - Tree-style hierarchy tracking
    """
    results = []

    for root, dirs, files in os.walk(path):
        level = root.replace(path, "").count(os.sep)

        if depth is not None and level > depth:
            continue

        if not show_hidden:
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            files = [f for f in files if not f.startswith(".")]

        entries = dirs + files
        if len(entries) > max_entries:
            print(f"⚠️  {root} has {len(entries)} items. Showing first {max_entries}.")
            dirs[:] = dirs[:max_entries]
            files = files[:max_entries]

        # Add directory itself
        dir_meta = format_metadata(root)
        if dir_meta:
            dir_meta["level"] = level
            results.append(dir_meta)

        # Add files
        for fname in files:
            full_path = os.path.join(root, fname)
            meta = format_metadata(full_path)

            if meta:
                meta["level"] = level + 1
                if apply_filters(meta, ext, min_size, name):
                    results.append(meta)

    return results


# --------------------------------------------------
# OUTPUT FORMATTING
# --------------------------------------------------
def print_table(data):
    """Print flat, table-style output."""
    print(f"{'Type':10} | {'Name':30} | {'Size (bytes)':12} | Last Modified")
    print("-" * 80)

    for entry in data:
        ftype = "FILE" if entry["is_file"] else "DIR" if entry["is_dir"] else "LINK"
        print(
            f"{ftype:10} | "
            f"{entry['name'][:30]:30} | "
            f"{entry['size_bytes']:12} | "
            f"{entry['modified']}"
        )


def print_tree(data):
    
    for entry in data:
        indent = "    " * entry.get("level", 0)

        if entry["is_dir"]:
            symbol = "[DIR]"
        elif entry["is_file"]:
            symbol = "[FILE]"
        else:
            symbol = "[LINK]"

        print(f"{indent}{symbol} {entry['name']}")

# --------------------------------------------------
# MAIN ENTRY POINT
# --------------------------------------------------
def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Advanced File System Explorer")

    # Core arguments
    parser.add_argument("--path", required=True, help="Directory to explore")
    parser.add_argument("--hidden", action="store_true", help="Show hidden files")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--max", type=int, default=5000, help="Max entries to scan in huge directories")

    # Recursive options
    parser.add_argument("--recursive", action="store_true", help="Recursively explore directories")
    parser.add_argument("--depth", type=int, default=None, help="Maximum recursion depth")

    # Filters (Milestone 3)
    parser.add_argument("--ext", type=str, help="Filter files by extension (e.g. .py)")
    parser.add_argument("--min-size", type=int, help="Filter files by minimum size (bytes)")
    parser.add_argument("--name", type=str, help="Filter files by keyword in filename")

    # Sorting (Milestone 4)
    parser.add_argument(
        "--sort",
        choices=["name", "size", "modified"],
        help="Sort files by name, size, or modified time"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print("❌ Error: Provided --path is not a valid directory.")
        return

    # Recursive mode
    if args.recursive:
        data = recursive_explore(
            args.path,
            show_hidden=args.hidden,
            max_entries=args.max,
            depth=args.depth,
            ext=args.ext,
            min_size=args.min_size,
            name=args.name
        )

        # Sort level-by-level to preserve tree structure
        sorted_data = []
        levels = sorted(set(e["level"] for e in data))

        for lvl in levels:
            level_entries = [e for e in data if e["level"] == lvl]
            sorted_data.extend(sort_entries(level_entries, args.sort))

        data = sorted_data

        if args.json:
            print(json.dumps(data, indent=4))
        else:
            print_tree(data)
        return

    # Non-recursive mode
    data = explore_directory(
        args.path,
        show_hidden=args.hidden,
        max_entries=args.max,
        ext=args.ext,
        min_size=args.min_size,
        name=args.name
    )

    data = sort_entries(data, args.sort)

    if args.json:
        print(json.dumps(data, indent=4))
    else:
        print_table(data)


if __name__ == "__main__":
    main()
