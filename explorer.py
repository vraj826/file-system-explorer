import os
import argparse
import json
from datetime import datetime


def format_metadata(path):
    """Extract metadata for a given file or directory."""
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
    """Non-recursive directory exploration."""
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
        if meta:
            meta["level"] = 0
            results.append(meta)

    return results


def recursive_explore(path, show_hidden=False, max_entries=5000, depth=None):
    """Recursive directory traversal using os.walk()."""
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
        for name in files:
            full_path = os.path.join(root, name)
            meta = format_metadata(full_path)
            if meta:
                meta["level"] = level + 1
                results.append(meta)

    return results


def print_table(data):
    """Print flat table output."""
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
    """Print tree-style recursive output."""
    for entry in data:
        indent = "    " * entry.get("level", 0)
        symbol = "📁" if entry["is_dir"] else "📄" if entry["is_file"] else "🔗"
        print(f"{indent}{symbol} {entry['name']}")


def main():
    parser = argparse.ArgumentParser(description="Advanced File System Explorer")

    parser.add_argument("--path", required=True, help="Directory to explore")
    parser.add_argument("--hidden", action="store_true", help="Show hidden files")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--max", type=int, default=5000, help="Max entries to scan in huge directories")
    parser.add_argument("--recursive", action="store_true", help="Recursively explore directories")
    parser.add_argument("--depth", type=int, default=None, help="Maximum recursion depth")

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
            depth=args.depth
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
        max_entries=args.max
    )

    if args.json:
        print(json.dumps(data, indent=4))
    else:
        print_table(data)


if __name__ == "__main__":
    main()
