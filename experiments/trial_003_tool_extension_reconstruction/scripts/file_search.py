"""L2 Script Tool: file_search
Search files under a directory containing specific keywords.
Usage: python file_search.py <root_dir> <keyword> [--ext .py .md]
"""
import argparse
import os
import sys
from pathlib import Path


def search_files(root_dir, keyword, extensions=None):
    root = Path(root_dir)
    if not root.exists():
        return {"error": f"Directory not found: {root_dir}", "matches": []}
    matches = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if extensions and path.suffix not in extensions:
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            if keyword.lower() in content.lower():
                matches.append(str(path))
        except (OSError, PermissionError):
            continue
    return {"root": str(root), "keyword": keyword, "count": len(matches), "matches": matches}


def main():
    parser = argparse.ArgumentParser(description="Search files by keyword")
    parser.add_argument("root_dir", help="Root directory to search")
    parser.add_argument("keyword", help="Keyword to search for")
    parser.add_argument("--ext", nargs="*", default=None, help="File extensions filter")
    args = parser.parse_args()
    result = search_files(args.root_dir, args.keyword, args.ext)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    import json
    main()
