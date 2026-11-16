#!/usr/bin/env python3
"""Validate extracted records against a small schema spec.

Stdlib only. No network. Input: a JSON file holding a list of records
(or {"items": [...]}) plus a schema file:

  {"fields": {"name": "string", "price_usd": "number",
              "source_url": "string", "fetched_utc": "string"},
   "required": ["name", "price_usd", "source_url", "fetched_utc"],
   "dedupe_key": "source_url"}

Usage:
  validate.py --input records.json --schema schema.json [--out cleaned.json]

Exit code 0 = all records valid (after dropping dupes/empties);
exit code 1 = one or more records invalid (details on stdout).
Prints: fetched / valid / dropped-invalid / dropped-duplicate counts.
"""
import argparse
import json
import sys

TYPES = {"string": str, "number": (int, float), "boolean": bool}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True)
    p.add_argument("--schema", required=True)
    p.add_argument("--out", default=None)
    args = p.parse_args()

    with open(args.input, encoding="utf-8") as f:
        raw = json.load(f)
    records = raw["items"] if isinstance(raw, dict) else raw
    with open(args.schema, encoding="utf-8") as f:
        spec = json.load(f)

    fields = spec.get("fields", {})
    required = spec.get("required", list(fields))
    dedupe_key = spec.get("dedupe_key")
    seen, valid, invalid = set(), [], []
    for i, rec in enumerate(records):
        problems = []
        if not isinstance(rec, dict):
            invalid.append((i, ["not an object"]))
            continue
        for name in required:
            if name not in rec or rec[name] in (None, ""):
                problems.append(f"missing {name}")
        for name, want in fields.items():
            if name in rec and rec[name] not in (None, ""):
                py = TYPES.get(want)
                if py and not isinstance(rec[name], py):
                    problems.append(f"{name} is {type(rec[name]).__name__}, want {want}")
                if want == "number" and isinstance(rec[name], bool):
                    problems.append(f"{name} is bool, want number")
        if problems:
            invalid.append((i, problems))
        else:
            valid.append(rec)
    dupes = 0
    if dedupe_key:
        deduped = []
        for rec in valid:
            key = rec.get(dedupe_key)
            if key in seen:
                dupes += 1
                continue
            seen.add(key)
            deduped.append(rec)
        valid = deduped
    print(f"fetched={len(records)} valid={len(valid)} "
          f"dropped_invalid={len(invalid)} dropped_duplicate={dupes}")
    for i, problems in invalid[:10]:
        print(f"  record {i}: {'; '.join(problems)}")
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(valid, f, indent=2, ensure_ascii=False)
        print(f"cleaned file: {args.out}")
    return 1 if invalid else 0


if __name__ == "__main__":
    raise SystemExit(main())
