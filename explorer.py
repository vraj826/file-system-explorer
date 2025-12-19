import os
import argparse
import json
from datetime import datetime


# --------------------------------------------------
# ANSI COLOR SUPPORT (OPTIONAL)
# --------------------------------------------------
class Colors:
    DIR = "\033[94m"     # Blue
    FILE = "\033[92m"    # Green
    LINK = "\033[96m"    # Cyan
    RESET = "\033[0m"


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
    Directories are never filtered out.
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
    Sort files while preserving directory structure.
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
# SUMMARY STATISTICS (Milestone 5)
# --------------------------------------------------
def print_summary(data):
    """
    Print summary statistics for scanned entries.
    """
    total_files = sum(1 for e in data if e["is_file"])
    total_dirs = sum(1 for e in data if e["is_dir"])
    total_links = sum(1 for e in data if e["is_link"])
    total_size = sum(e["size_bytes"] for e in data if e["is_file"])

    print("\nSummary")
    print("-" * 40)
    print(f"Total files       : {total_files}")
    print(f"Total directories : {total_dirs}")
    print(f"Total symlinks    : {total_links}")
    print(f"Total size (bytes): {total_size}")


# --------------------------------------------------
# NON-RECURSIVE DIRECTORY SCAN
# --------------------------------------------------
def explore_directory(path, show_hidden=False, max_entries=5000,
                      ext=None, min_size=None, name=None):
    try:
        items = os.listdir(path)
    except (FileNotFoundError, PermissionError):
        print("❌ Error accessing directory.")
        return []

    if not show_hidden:
        items = [i for i in items if not i.startswith(".")]

    if len(items) > max_entries:
        print(f"⚠️  Directory has {len(items)} items. Showing first {max_entries}.")
        items = items[:max_entries]

    results = []
    for item in items:
        meta = format_metadata(os.path.join(path, item))
        if meta and apply_filters(meta, ext, min_size, name):
            meta["level"] = 0
            results.append(meta)

    return results


# --------------------------------------------------
# RECURSIVE DIRECTORY SCAN
# --------------------------------------------------
def recursive_explore(path, show_hidden=False, max_entries=5000,
                      depth=None, ext=None, min_size=None, name=None):
    results = []

    for root, dirs, files in os.walk(path):
        level = root.replace(path, "").count(os.sep)

        if depth is not None and level > depth:
            continue

        if not show_hidden:
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            files = [f for f in files if not f.startswith(".")]

        if len(dirs) + len(files) > max_entries:
            dirs[:] = dirs[:max_entries]
            files = files[:max_entries]

        dir_meta = format_metadata(root)
        if dir_meta:
            dir_meta["level"] = level
            results.append(dir_meta)

        for fname in files:
            meta = format_metadata(os.path.join(root, fname))
            if meta and apply_filters(meta, ext, min_size, name):
                meta["level"] = level + 1
                results.append(meta)

    return results


# --------------------------------------------------
# OUTPUT FORMATTING
# --------------------------------------------------
def print_table(data, use_color=False):
    print(f"{'Type':10} | {'Name':30} | {'Size (bytes)':12} | Last Modified")
    print("-" * 80)

    for e in data:
        ftype = "FILE" if e["is_file"] else "DIR" if e["is_dir"] else "LINK"

        name = e["name"]
        if use_color:
            if e["is_dir"]:
                name = f"{Colors.DIR}{name}{Colors.RESET}"
            elif e["is_file"]:
                name = f"{Colors.FILE}{name}{Colors.RESET}"
            else:
                name = f"{Colors.LINK}{name}{Colors.RESET}"

        print(f"{ftype:10} | {name[:30]:30} | {e['size_bytes']:12} | {e['modified']}")


def print_tree(data, use_color=False):
    for e in data:
        indent = "    " * e.get("level", 0)

        label = "[DIR]" if e["is_dir"] else "[FILE]" if e["is_file"] else "[LINK]"
        if use_color:
            if e["is_dir"]:
                label = f"{Colors.DIR}{label}{Colors.RESET}"
            elif e["is_file"]:
                label = f"{Colors.FILE}{label}{Colors.RESET}"
            else:
                label = f"{Colors.LINK}{label}{Colors.RESET}"

        print(f"{indent}{label} {e['name']}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Advanced File System Explorer")

    parser.add_argument("--path", required=True)
    parser.add_argument("--hidden", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max", type=int, default=5000)

    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--depth", type=int)

    parser.add_argument("--ext")
    parser.add_argument("--min-size", type=int)
    parser.add_argument("--name")

    parser.add_argument("--sort", choices=["name", "size", "modified"])
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--color", action="store_true")

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print("❌ Invalid directory")
        return

    if args.recursive:
        data = recursive_explore(
            args.path, args.hidden, args.max,
            args.depth, args.ext, args.min_size, args.name
        )

        # level-wise sorting
        sorted_data = []
        for lvl in sorted(set(e["level"] for e in data)):
            lvl_entries = [e for e in data if e["level"] == lvl]
            sorted_data.extend(sort_entries(lvl_entries, args.sort))
        data = sorted_data

        if args.json:
            print(json.dumps(data, indent=4))
        else:
            print_tree(data, args.color)
    else:
        data = explore_directory(
            args.path, args.hidden, args.max,
            args.ext, args.min_size, args.name
        )
        data = sort_entries(data, args.sort)

        if args.json:
            print(json.dumps(data, indent=4))
        else:
            print_table(data, args.color)

    if args.summary:
        print_summary(data)


if __name__ == "__main__":
    main()
