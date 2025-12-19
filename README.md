# 📁 File System Explorer

A command-line tool for exploring directories, inspecting metadata, detecting symbolic links, handling large folders safely, filtering hidden files, and exporting results in clean table or JSON formats.  
Built as part of my **Open-Source Contribution preparation (Systems / OS / File Tools / Security)**.

---

## ⭐ Features (Current – Advanced Version)

### 🔍 File & Directory Analysis
- List all files & folders in a directory  
- Detect file type:  
  - **FILE**  
  - **DIR**  
  - **SYMLINK**  
- Extract metadata:
  - Size (bytes)  
  - Last modified timestamp  
  - Absolute path  

---

### 🔁 Recursive Directory Traversal
- Recursively explore subdirectories using `os.walk()`  
- Tree-style hierarchical output  
- Optional depth control  
- Recursive JSON export  

Supported flags:
```bash
--recursive
```
```
--depth <number>
```

### 🧵 Symbolic Link Detection
- Uses `os.lstat()` to differentiate between files and links  
- JSON output includes:
```json
{
    "is_link": true
}
```

---

### 📂 Hidden Files Support
- Hidden files (`.filename`) are skipped by default  
- Show them using:
```bash
--hidden
```

---

### ⚠️ Handles Very Large Directories
- Protects against scanning huge folders by default  
- Warns when the number of items is large  
- User-controlled scan limit:
```bash
--max 5000
```

---

### ❌ Robust Error Handling
Handles common issues gracefully:

- Invalid path  
- Permission denied  
- Path is not a directory  
- Restricted system folders  

---

### 🧾 Clean CLI Output (Non-Recursive)
Readable, table-like output:

```
Type       | Name                           | Size (bytes) | Last Modified
--------------------------------------------------------------------------------
FILE       | CONTRIBUTING.md                |         1186 | 2025-12-17T18:41:38.704531
DIR        | examples                       |         4096 | 2025-12-17T18:41:38.722697
FILE       | explorer.py                    |         8374 | 2025-12-17T18:41:38.722697
FILE       | LICENSE                        |          684 | 2025-12-17T18:41:38.704531
FILE       | README.md                      |         5688 | 2025-12-17T18:41:38.716670
```

---

### 🌳 Tree Output (Recursive Mode)
```
[DIR] .
    [FILE] CONTRIBUTING.md
    [FILE] explorer.py
    [FILE] LICENSE
    [FILE] README.md
    [DIR] examples
        [FILE] basic_output.txt
        [FILE] filtered_py_files.txt
        [FILE] keyword_filtered_files.txt
        [FILE] large_files.json
        [FILE] README.md
        [FILE] recursive_output.json
        [FILE] recursive_tree.txt
        [FILE] sorted_by_modified.txt
        [FILE] sorted_by_name.txt
        [FILE] sorted_by_size.txt
```

---

### 🧱 JSON Output
Perfect for automation, scripting, or data pipelines:

```bash
python explorer.py --path . --json
python explorer.py --path . --recursive --json
```

Results are printed as formatted JSON.

---

### 🔎 File Filters (Milestone 3)

Filters apply only to files (directories are preserved).

   - Filter by extension:
   ```
   --ext .py
   ```
   - Filter by minimum size:
   ```
   --min-size 1000
   ```
   - Filter by keyword:
   ```
   --name report
   ```

Filters can be combined and work in both recursive and non-recursive modes.

---

### 🔃 Sorting (Milestone 4)

Sort files in a directory or recursive scan.

Supported options:
   - Sort by name:
   ```
   --sort name
```
   - Sort by file size:
   ```
   --sort size
   ```
   - Sort by last modified time:
   ```
   --sort modified
   ```

Sorting behavior:
- Applies only to files
- Directories retain structure and order
- Works in recursive and non-recursive modes
- Can be combined with filters

---

### 📊 Summary Statistics (Milestone 5)

Display useful summary information at the end of output.
```
--summary
```

Includes:
- Total files
- Total directories
- Total symbolic links
- Total size of files (bytes)

### 🎨 Colorized Output (Milestone 5)

Enable colored output for better readability.
```
--color
```
- Directories → Blue
- Files → Green
- Symlinks → Cyan
- Disabled by default (safe for redirection & CI)

---

## 🧪 Usage Examples

### Milestone 1
#### 📌 Basic scan
```bash
python explorer.py --path .
```

#### 📌 Show hidden files
```bash
python explorer.py --path . --hidden
```

#### 📌 Limit scanning for large folders
```
python explorer.py --path C:\ --max 2000
```

### Milestone 2
#### 📌 JSON output
```bash
python explorer.py --path . --json
```

#### 📌 Recursive traversal
```
python explorer.py --path . --recursive
```

#### 📌 Recursive with depth limit
```
python explorer.py --path . --recursive --depth 2
```

### Milestone 3
#### 📌 Filter by extension
```
python explorer.py --path . --ext .py
```

#### 📌 Filter by minimum size
```
python explorer.py --path . --min-size 1000
```

#### 📌 Filter by keyword
```
python explorer.py --path . --name test
```

#### 📌 Combine filters (advanced usage)
```
python explorer.py --path . --recursive --ext .py --min-size 500
```

### Milestone 4
#### 📌 Sort by name
```
python explorer.py --path . --sort name
```

#### 📌 Sort by size
```
python explorer.py --path . --sort size
```

#### 📌 Sort by modified time (recursive)
```
python explorer.py --path . --recursive --sort modified
```

#### 📌 Combine filters + sorting
```
python explorer.py --path . --recursive --ext .py --sort size
```

### Milestone 5
#### 📌 Summary statistics
```
python explorer.py --path . --recursive --summary
```

#### 📌Colorized output
```
python explorer.py --path . --recursive --color
```

### Everything combined
```
python explorer.py --path . --recursive --ext .py --sort modified --summary --color
```
- ``` python explorer.py --path . # Milestone 1 (Basic Scan) ```
- ``` --recursive                 # Milestone 2 (Recursive traversal) ```
- ``` --ext .py                   # Milestone 3 (Filter by extension) ```
- ``` --sort modified             # Milestone 4 (Sort by modified time) ```
- ``` --summary --color           # Milestone 5 (Summary Statistics & Colorized Output) ```
---

## 📦 Project Structure

```
file-system-explorer/
├── explorer.py         # Main CLI tool (advanced version)
├── CONTRIBUTING.md     # Contributor guidelines
├── LICENSE             # MIT License
├── examples/           # folder having test runs
└── README.md
```

---

## 🛠 Requirements
- Python **3.8+**  
- No external libraries required  

---

## 🧠 Learning Goals

### 🖥️ Operating Systems
- Directory traversal
- Recursive filesystem exploration
- File metadata handling  
- Detecting symbolic links  

### 🧩 Systems Programming
- CLI design with ` argparse `
- Error handling  
- Large input handling
- Tree-based output formatting
- File filtering logic

### ☁️ Cloud & DevOps
- JSON output for automation   
- Scriptable CLI tools
- CI-safe output design  

### 🔐 Security
- Safe path inspection  
- Permission-aware filesystem access
- Symlink handling

---

## 🗺️ Project Roadmap

| Milestone      | Status | Description |
|----------------|--------|-------------|
| Milestone 1    | ✅ Completed | Basic explorer + metadata output |
| Milestone 2    | ✅ Completed | Recursive traversal (--recursive, --depth) |
| Milestone 3    | ✅ Completed | Filters: ext, size, keyword |
| Milestone 4    | ✅ Completed | Sorting: name, size, modified |
| Milestone 5    | ✅ Completed | Summary stats + Color output |
| Milestone 6    | ⬜ Future   | Docker support + CI pipeline |

---

## 🤝 Contributing

Contributions are welcome!  
Please read [`CONTRIBUTING.md`](./CONTRIBUTING.md) to understand the process.

---

## 📄 License

This project is licensed under the **MIT License**.  
See [`LICENSE`](./LICENSE) for details.

---

## ⭐ Acknowledgements

This project is part of my Open-Source Contribution preparation — learning real-world systems programming concepts by building practical CLI tools.
