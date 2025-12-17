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

### 🧾 Clean CLI Output
Readable, table-like output:

```
Type       | Name                           | Size (bytes) | Last Modified
--------------------------------------------------------------------------------
FILE       | CONTRIBUTING.md                |         1186 | 2025-12-17T18:41:38.704531
DIR        | examples                       |         4096 | 2025-12-17T18:41:38.722697
FILE       | explorer.py                    |         8374 | 2025-12-17T18:41:38.722697
FILE       | LICENSE                        |          684 | 2025-12-17T18:41:38.704531
FILE       | README.md                      |         5688 | 2025-12-17T18:41:38.716670
FILE       | utils.py                       |          130 | 2025-12-17T18:41:38.722697
```

---

### 🌳 Tree Output (Recursive Mode)
```
📁 file-system-explorer
    📄 CONTRIBUTING.md
    📄 explorer.py
    📄 LICENSE
    📄 README.md
    📄 utils.py
    📁 examples
        📄 basic_output.txt
        📄 README.md
        📄 recursive_output.json
        📄 recursive_tree.txt
        📄 filtered_py_files.txt
        📄 large_files.json
        📄 keyword_filtered_files.txt
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

## 🚀 Upcoming Features (Milestones 4)

### 🔹 Milestone 4 — Sorting & Formatting
Sorting options:
- `--sort name`  
- `--sort size`  
- `--sort modified`  

Planned enhancements:
- Summary view  
- Colorized output  

---

## 🧪 Usage Examples

### 📌 Basic scan
```bash
python explorer.py --path .
```

### 📌 Show hidden files
```bash
python explorer.py --path . --hidden
```

### 📌 JSON output
```bash
python explorer.py --path . --json
```

### 📌 Recursive traversal
```
python explorer.py --path . --recursive
```

### 📌 Recursive with depth limit
```
python explorer.py --path . --recursive --depth 2
```

### 📌 Filter by extension
```
python explorer.py --path . --ext .py
```

### 📌 Filter by minimum size
```
python explorer.py --path . --min-size 1000
```

### 📌 Filter by keyword
```
python explorer.py --path . --name test
```

### 📌 Combine filters (advanced usage)
```
python explorer.py --path . --recursive --ext .py --min-size 500
```

### 📌 Limit scanning for large folders
```bash
python explorer.py --path C:\ --max 2000
```

---

## 📦 Project Structure

```
file-system-explorer/
├── explorer.py         # Main CLI tool (advanced version)
├── utils.py            # Future helper functions: filters, sorting, formatting
├── CONTRIBUTING.md     # Contributor guidelines
├── LICENSE             # MIT License
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
- CLI design  
- Error handling  
- Large input handling
- Tree-based output formatting
- File filtering logic

### ☁️ Cloud & DevOps
- JSON output for automation   
- Portable CLI utilities  

### 🔐 Security
- Safe path inspection  
- Permission-aware filesystem access

---

## 🗺️ Project Roadmap

| Milestone      | Status | Description |
|----------------|--------|-------------|
| Milestone 1    | ✅ Completed | Basic explorer + metadata output |
| Milestone 2    | ✅ Completed | Recursive traversal (--recursive, --depth) |
| Milestone 3    | ✅ Completed | Filters: ext, size, keyword |
| Milestone 4    | ⬜ Pending  | Sorting + color formatting + summary |
| Milestone 5    | ⬜ Future   | Docker support + CI pipeline |

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
