#!/usr/bin/env python3
"""URL Shortener - shorten URLs to short codes, stored in a local JSON file."""
import argparse, json, os, string
DEFAULT_FILE = "urls.json"
ALPHABET = string.digits + string.ascii_letters

def encode(n):
    if n == 0: return ALPHABET[0]
    out = ""
    while n: n, r = divmod(n, len(ALPHABET)); out = ALPHABET[r] + out
    return out

def load(path):
    if not os.path.exists(path): return {}
    with open(path, encoding="utf-8") as f: return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f: json.dump(data, f, indent=2)

def main():
    p = argparse.ArgumentParser(description="URL Shortener (local JSON storage)")
    p.add_argument("--file", default=DEFAULT_FILE)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("shorten"); s.add_argument("url")
    r = sub.add_parser("resolve"); r.add_argument("code")
    sub.add_parser("list")
    args = p.parse_args(); data = load(args.file)
    if args.cmd == "shorten":
        code = encode(len(data) + 1)
        data[code] = args.url; save(args.file, data)
        print(f"Short code: {code} -> {args.url}")
    elif args.cmd == "resolve":
        print(data.get(args.code, f"No URL found for code '{args.code}'"))
    elif args.cmd == "list":
        if not data: print("No shortened URLs yet.")
        for code, url in data.items(): print(f"{code} -> {url}")

if __name__ == "__main__":
    main()
