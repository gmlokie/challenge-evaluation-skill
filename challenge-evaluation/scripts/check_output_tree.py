#!/usr/bin/env python3
"""Check the exact output tree a grader will see for plain-relative-name violations.

Why this exists: best-game-01 rounds 1-3 were ALL rejected on run_completes
with one reason — output path "screenshots/.gitkeep" is not a plain relative
name. The local kit check passed 13/13 and the repo looked clean; the failure
was a dotfile that main.ts's copyEntryFolder() copied blindly from
screenshots/ into /output. The lesson: verify the EXACT artifact the grader
sees, not the repo tree, and never theorize a grader failure before reading
the live check reason.

What it does (read-only): walk the folders an entry's build copies into the
output (default: game, screenshots) and flag every path that is NOT a plain
relative name:
  - any path component starting with "." (dotfiles/dotdirs: .gitkeep, .DS_Store)
  - symlinks and non-regular files (the dossier refuses them anyway)
  - names containing backslashes or ".." components

Usage:
  python3 check_output_tree.py <entry-dir> [--folders game screenshots]
  Exit 0 = clean, exit 1 = violations found (receipt printed either way).

Example (red/green test, 2026-11-16):
  scratch copy of the entry + planted screenshots/.gitkeep  -> FAIL, flags it
  current best-game-01 tree (4 JPGs only)                 -> PASS
"""
import argparse
import os
import sys


def scan(root, folders):
    """Return (violations, warnings, files_seen)."""
    violations = []
    warnings = []
    files_seen = 0
    for folder in folders:
        base = os.path.join(root, folder)
        if not os.path.isdir(base):
            warnings.append(f"folder missing: {folder}/ (skipped)")
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            # dot-directories: flag and do not descend silently — report them
            for d in list(dirnames):
                if d.startswith("."):
                    rel = os.path.relpath(os.path.join(dirpath, d), root)
                    violations.append(f"{rel}/ (dot-directory)")
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            for name in filenames:
                files_seen += 1
                full = os.path.join(dirpath, name)
                rel = os.path.relpath(full, root)
                parts = rel.split(os.sep)
                if any(p.startswith(".") for p in parts):
                    violations.append(f"{rel} (dotfile — not a plain relative name)")
                elif "\\" in name or ".." in parts:
                    violations.append(f"{rel} (non-plain name)")
                elif not os.path.isfile(full) or os.path.islink(full):
                    violations.append(f"{rel} (symlink / non-regular file)")
    return violations, warnings, files_seen


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("entry_dir", help="entry directory (beside main.ts)")
    p.add_argument("--folders", nargs="+", default=["game", "screenshots"],
                   help="folders the build copies into the output (default: game screenshots)")
    args = p.parse_args()

    violations, warnings, files_seen = scan(args.entry_dir, args.folders)
    print(f"check_output_tree: {args.entry_dir}")
    print(f"  folders scanned: {', '.join(args.folders)}")
    print(f"  files seen: {files_seen}")
    for w in warnings:
        print(f"  WARN: {w}")
    if violations:
        print(f"  VIOLATIONS: {len(violations)}")
        for v in violations:
            print(f"    - {v}")
        print("  verdict: FAIL — fix before submit (remove/skip dotfiles in the copied folders)")
        return 1
    print("  verdict: PASS — output tree holds plain relative names only")
    return 0


if __name__ == "__main__":
    sys.exit(main())
