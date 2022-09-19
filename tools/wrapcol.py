#!/usr/bin/env python3
import sys, textwrap

def main(width=80):
    try:
        width = int(sys.argv[1]) if len(sys.argv) > 1 else width
    except ValueError:
        print("usage: wrapcol [width]", file=sys.stderr)
        return 2
    print(textwrap.fill(sys.stdin.read().rstrip("\n"), width=width))

if __name__ == "__main__":
    main()

