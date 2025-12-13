# Examples

This folder contains sample outputs generated using the **File System Explorer**.

These examples help users and reviewers understand the tool’s behavior
without running it locally.

---

## Files Included

### `basic_output.txt`
- Generated using:
  ```bash
  python explorer.py --path .
  ```
- Demonstrates non-recursive directory scanning
- Shows table-formatted output with metadata

### `recursive_tree.txt`
- Generated using:
   ```bash
   python explorer.py --path . --recursive
   ```
- Demonstrates recursive traversal using os.walk()
- Shows tree-style directory structure

### `recursive_output.json`
- Generated using:
  ```bash
  python explorer.py --path . --recursive --json
  ```
- Demonstrates structured JSON output
- Useful for automation, scripting, and data pipelines
