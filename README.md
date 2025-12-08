# 📁 File System Explorer
A command-line tool for exploring directories, viewing metadata, filtering files, and generating clean output formats.  
Built as part of my **GSoC preparation (Systems / OS / CLI Tools / Security)**.

---

## ⭐ Features (Current – Milestone 1)

- List all files & folders in a given directory  
- Show file metadata:
  - File size  
  - Last modified timestamp  
- Identify file vs folder  
- Simple CLI interface (`--path`)
- Basic error handling

---

## 🚀 Upcoming Features (Milestones 2–4)

### 🔹 **Milestone 2 — Recursive Exploration**
- `--recursive` flag to scan all subdirectories  
- Tree-style output (like `tree` command)  
- Count total files & folders  

### 🔹 **Milestone 3 — Filters**
- Filter by extension → `--ext .txt`  
- Filter by minimum size → `--min-size 1000`  
- Filter by keyword in name → `--name report`  

### 🔹 **Milestone 4 — Output Enhancements**
- JSON output → `--json`  
- Sorting options:
  - `--sort size`
  - `--sort name`
  - `--sort modified`
- Colorful CLI formatting  
- Summary view (total size, number of files, etc.)

---

## 🧪 Usage

### **Basic run:**
```bash
python explorer.py --path .
