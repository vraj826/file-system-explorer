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

    IMPORTANT DESIGN DECISION:
    - Directories are NEVER filtered out.
      This preserves directory structure in recursive mode.
    - Filters apply ONLY to files.
    """

    # Always keep directories
    if entry["is_dir"]:
        return True

    # Filter by file extension (e.g. .py, .txt)
    if ext and not entry["name"].endswith(ext):
        return False

    # Filter by minimum file size (in bytes)
    if min_size and entry["size_bytes"] < min_size:
        return False

    # Filter by keyword in filename (case-insensitive)
    if name and name.lower() not in entry["name"].lower():
        return False

    return True


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
    - File-level filters (extension, size, name)
    """
    try:
        items = os.listdir(path)
    except FileNotFoundError:
        print("❌ Invalid path: Directory does not exist.")
        return []
    except PermissionError:
        print("❌ Permission denied.")
        return []

    # Hide dot-files unless explicitly requested
    if not show_hidden:
        items = [item for item in items if not item.startswith(".")]

    # Safety guard for huge directories
    if len(items) > max_entries:
        print(f"⚠️  Directory has {len(items)} items. Showing first {max_entries}.")
        items = items[:max_entries]

    results = []
    for item in items:
        full_path = os.path.join(path, item)
        meta = format_metadata(full_path)

        # Apply filters only if metadata exists
        if meta and apply_filters(meta, ext, min_size, name):
            meta["level"] = 0  # flat structure for non-recursive mode
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
    - Hidden file handling
    - Safety limits
    - File-level filtering
    - Tree-style hierarchy tracking
    """
    results = []

    for root, dirs, files in os.walk(path):
        # Calculate nesting level relative to root path
        level = root.replace(path, "").count(os.sep)

        # Stop traversal if depth limit is exceeded
        if depth is not None and level > depth:
            continue

        # Remove hidden folders/files unless allowed
        if not show_hidden:
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            files = [f for f in files if not f.startswith(".")]

        # Safety guard for extremely large directories
        entries = dirs + files
        if len(entries) > max_entries:
            print(f"⚠️  {root} has {len(entries)} items. Showing first {max_entries}.")
            dirs[:] = dirs[:max_entries]
            files = files[:max_entries]

        # Add directory itself (always included)
        dir_meta = format_metadata(root)
        if dir_meta:
            dir_meta["level"] = level
            results.append(dir_meta)

        # Add files inside the directory (with filters)
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
    """Print flat, table-style output (non-recursive mode)."""
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
    """Print hierarchical tree output (recursive mode)."""
    for entry in data:
        indent = "    " * entry.get("level", 0)
        symbol = "📁" if entry["is_dir"] else "📄" if entry["is_file"] else "🔗"
        print(f"{indent}{symbol} {entry['name']}")


# --------------------------------------------------
# MAIN ENTRY POINT
# --------------------------------------------------
def main():
    """
    Entry point for the CLI tool.
    Handles argument parsing and execution flow.
    """
    parser = argparse.ArgumentParser(description="Advanced File System Explorer")

    # Core arguments
    parser.add_argument("--path", required=True, help="Directory to explore")
    parser.add_argument("--hidden", action="store_true", help="Show hidden files")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--max", type=int, default=5000, help="Max entries to scan in huge directories")

    # Recursive traversal options
    parser.add_argument("--recursive", action="store_true", help="Recursively explore directories")
    parser.add_argument("--depth", type=int, default=None, help="Maximum recursion depth")

    # File filters (Milestone 3)
    parser.add_argument("--ext", type=str, help="Filter files by extension (e.g. .py)")
    parser.add_argument("--min-size", type=int, help="Filter files by minimum size (bytes)")
    parser.add_argument("--name", type=str, help="Filter files by keyword in filename")

    args = parser.parse_args()

    # Validate path early
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

    if args.json:
        print(json.dumps(data, indent=4))
    else:
        print_table(data)


if __name__ == "__main__":
    main()
