# ⭐ Examples

This folder contains sample outputs generated using the **File System Explorer**.

These examples help users and reviewers understand the tool’s behavior
without running it locally.

---

## 📁 Files Included

###  📌 Milestone 1
#### `basic_output.txt`
- Generated using:
  ```bash
  python explorer.py --path .
  ```
- Demonstrates non-recursive directory scanning
- Shows table-formatted output with metadata

### 📌 Milestone 2
#### `recursive_tree.txt`
- Generated using:
   ```bash
   python explorer.py --path . --recursive
   ```
- Demonstrates recursive traversal using os.walk()
- Shows tree-style directory structure

#### `recursive_output.json`
- Generated using:
  ```bash
  python explorer.py --path . --recursive --json
  ```
- Demonstrates structured JSON output
- Useful for automation, scripting, and data pipelines

### 📌 Milestone 3
#### `filtered_py_files.txt`
- Generated using:
  ```
  python explorer.py --path . --ext .py
  ```
- Demonstrates file extension filtering

#### `large_files.json`
- Generated using:
  ```
  python explorer.py --path . --min-size 1000 --json
  ```
- Demonstrates minimum size filtering with JSON output

#### `keyword_filtered_files.txt`
- Generated using:
  ```
  python explorer.py --path . --name test
  ```
- Demonstrates keyword-based filename filtering

### 📌 Milestone 4
#### `sorted_by_name.txt`
- Generated using:
  ```
  python explorer.py --path . --sort name
  ```
- Demonstrates alphabetical sorting

#### `sorted_by_size.txt`
- Generated using:
  ```
  python explorer.py --path . --sort size
  ```
- Demonstrates sorting by file size

#### `sorted_by_modified.txt`
- Generated using:
  ```
  python explorer.py --path . --recursive --sort modified
  ```
- Demonstrates sorting by last modified time in recursive mode
