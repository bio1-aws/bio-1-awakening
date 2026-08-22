"""L2 Script Tool: text_process
Text statistics: char count, line count, keyword frequency.
Usage: python text_process.py <file_path> [--keywords kw1 kw2]
"""
import argparse
import json
import re
from pathlib import Path


def analyze_text(file_path, keywords=None):
    path = Path(file_path)
    if not path.exists():
        return {"error": f"File not found: {file_path}"}
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    words = re.findall(r"\w+", text.lower())
    result = {
        "file": str(path),
        "total_chars": len(text),
        "total_lines": len(lines),
        "non_empty_lines": sum(1 for l in lines if l.strip()),
        "total_words": len(words),
        "keyword_freq": {},
    }
    if keywords:
        for kw in keywords:
            result["keyword_freq"][kw] = text.lower().count(kw.lower())
    return result


def main():
    parser = argparse.ArgumentParser(description="Text statistics tool")
    parser.add_argument("file_path", help="Path to text file")
    parser.add_argument("--keywords", nargs="*", default=None, help="Keywords to count")
    args = parser.parse_args()
    result = analyze_text(args.file_path, args.keywords)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
