Daily-CLI-Tools
================

A grab‑bag of small, practical command‑line utilities I build for my own daily workflow. Each tool is a single-file script with a consistent interface and good help text.

Why another toolbox?
- I often need tiny helpers across projects
- Keeping them in one repo makes updates easy
- No external services, works offline

Highlights
- Plain Python 3.9+ with zero heavy deps
- Single entry `dct` dispatch with subcommands
- Focus on text, files, and git hygiene

Quick start
- `python3 -m pip install -r requirements.txt` (optional)
- `python3 dct.py --help`

Tools (initial set)
- `stamp` – print timestamps in various formats
- `glint` – tidy up local git branches safely
- `finddup` – scan for duplicate files by hash

Contributing
- Small, focused features only
- Keep commits minimal and well explained
- Prefer standard library over deps when reasonable

License
- MIT

