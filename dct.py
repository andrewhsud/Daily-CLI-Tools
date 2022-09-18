#!/usr/bin/env python3
import argparse
import datetime as _dt
import hashlib
import os
import sys
from pathlib import Path


def _cmd_stamp(args: argparse.Namespace) -> int:
    now = _dt.datetime.now(_dt.timezone.utc) if args.utc else _dt.datetime.now()
    if args.iso:
        print(now.isoformat())
    elif args.format:
        print(now.strftime(args.format))
    else:
        print(now.strftime("%Y-%m-%d %H:%M:%S"))
    return 0


def _cmd_finddup(args: argparse.Namespace) -> int:
    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        print(f"Path not found: {root}", file=sys.stderr)
        return 2
    hashes = {}
    dupes = {}
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            p = Path(dirpath) / fn
            try:
                h = hashlib.sha256()
                with open(p, 'rb') as fh:
                    for chunk in iter(lambda: fh.read(65536), b''):
                        h.update(chunk)
                digest = h.hexdigest()
            except Exception as e:
                if args.verbose:
                    print(f"skip {p}: {e}", file=sys.stderr)
                continue
            first = hashes.setdefault(digest, p)
            if first is not p:
                dupes.setdefault(digest, [first]).append(p)
    for d, files in dupes.items():
        print(f"hash {d[:12]}…")
        for f in files:
            print(f"  {f}")
    return 0 if dupes else 1


def _cmd_glint(args: argparse.Namespace) -> int:
    """List local git branches merged into main and optionally delete with --prune.
    No remote ops. Safe by default.
    """
    import subprocess
    def run(cmd):
        return subprocess.check_output(cmd, text=True).strip()
    try:
        current = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        main = args.main
        merged = run(["git", "branch", "--merged", main])
    except subprocess.CalledProcessError as e:
        print(f"git error: {e}", file=sys.stderr)
        return 2
    victims = []
    for line in merged.splitlines():
        b = line.replace("*", "").strip()
        if b not in (current, args.main, "main", "master"):
            victims.append(b)
    if not victims:
        print("Nothing to prune.")
        return 1
    print("Merged branches:")
    for v in victims:
        print(f"  {v}")
    if args.prune:
        import subprocess
        for v in victims:
            subprocess.call(["git", "branch", "-d", v])
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="dct", description="Daily CLI Tools")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("stamp", help="print the current timestamp")
    s.add_argument("--utc", action="store_true", help="use UTC time")
    s.add_argument("--iso", action="store_true", help="ISO 8601 output")
    s.add_argument("--format", help="strftime pattern")
    s.set_defaults(func=_cmd_stamp)

    f = sub.add_parser("finddup", help="list duplicate files by SHA-256")
    f.add_argument("path", nargs="?", default=".", help="root directory")
    f.add_argument("-v", "--verbose", action="store_true")
    f.set_defaults(func=_cmd_finddup)

    g = sub.add_parser("glint", help="show/prune local branches merged into main")
    g.add_argument("--main", default="main")
    g.add_argument("--prune", action="store_true")
    g.set_defaults(func=_cmd_glint)

    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

