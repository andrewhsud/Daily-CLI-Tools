#!/usr/bin/env python3
import json, sys

def main():
    data = json.load(sys.stdin)
    json.dump(data, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")

if __name__ == "__main__":
    main()

