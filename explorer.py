import os
import argparse
from datetime import datetime

def list_files(path):
    try:
        items = os.listdir(path)
    except FileNotFoundError:
        print("❌ Path not found!")
        return
    except PermissionError:
        print("❌ Permission denied!")
        return

    print(f"\n📂 Exploring: {path}\n")
    
    for item in items:
        full_path = os.path.join(path, item)
        
        if os.path.isfile(full_path):
            size = os.path.getsize(full_path)
            modified = datetime.fromtimestamp(os.path.getmtime(full_path))
            print(f"📝 FILE   | {item} | {size} bytes | Last modified: {modified}")
        
        elif os.path.isdir(full_path):
            print(f"📁 FOLDER | {item}")

def main():
    parser = argparse.ArgumentParser(description="Simple File System Explorer")
    parser.add_argument("--path", required=True, help="Path to explore")
    
    args = parser.parse_args()
    list_files(args.path)

if __name__ == "__main__":
    main()
