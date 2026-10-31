"""Machine-readable catalogue built from the canonical Markdown files.

Everything here is derived from the files in archive/ and pages/ (plus the
exclusion list), so the catalogue can be rebuilt from a plain copy of the
repository:

    python3 tools/catalogue.py            # rewrite data/*.json and SHA256SUMS
"""

import collections
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

SCHEMA_VERSION = "1.0"
CONTENT_DIRS = ("archive", "pages")


def read_document(path):
    """Return (front matter dict, body) of a Markdown file."""
    text = Path(path).read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing front matter")
    end = text.index("\n---\n", 4)
    return yaml.safe_load(text[4:end]), text[end + 5:]


def content_files(root):
    root = Path(root)
    files = [p for d in CONTENT_DIRS for p in (root / d).rglob("*.md")]
    return sorted(files, key=lambda p: p.relative_to(root).as_posix())


def word_count(body):
    body = re.sub(r"\]\([^)]*\)", "]", body)
    return len(re.findall(r"\w+", body))


def build_index(root):
    root = Path(root)
    records, words = [], {}
    for path in content_files(root):
        meta, body = read_document(path)
        rel = path.relative_to(root).as_posix()
        rec = {
            "id": meta["id"],
            "type": "page" if rel.startswith("pages/") else "post",
            "title": meta["title"],
            "date": meta["date"],
            "category": meta.get("category", []),
        }
        if meta.get("author"):
            rec["author"] = meta["author"]
        rec["markdown_path"] = rel
        records.append(rec)
        words[meta["id"]] = word_count(body)
    # Chronological by the actual moment of publication (dates carry offsets).
    records.sort(key=lambda r: (datetime.fromisoformat(r["date"]).astimezone(timezone.utc), r["id"]))
    return records, words


def build_statistics(index, words, exclusions):
    by_year = collections.Counter(r["date"][:4] for r in index)
    by_cat = collections.Counter(c for r in index for c in r["category"])
    by_reason = collections.Counter(re.sub(r" \(\d+ own words\)$", "", e["reason"]) for e in exclusions)
    return {
        "schema_version": SCHEMA_VERSION,
        "totals": {
            "documents": len(index),
            "posts": sum(r["type"] == "post" for r in index),
            "pages": sum(r["type"] == "page" for r in index),
            "words": sum(words.values()),
            "excluded": len(exclusions),
        },
        "first_date": index[0]["date"] if index else None,
        "last_date": index[-1]["date"] if index else None,
        "by_year": dict(sorted(by_year.items())),
        "by_category": dict(sorted(by_cat.items(), key=lambda kv: (-kv[1], kv[0]))),
        "words_by_year": dict(sorted(collections.Counter(
            {y: sum(words[r["id"]] for r in index if r["date"][:4] == y) for y in by_year}).items())),
        "excluded_by_reason": dict(sorted(by_reason.items(), key=lambda kv: (-kv[1], kv[0]))),
    }


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def dumps(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def write_catalogue(root, source_info):
    """Write data/index.json, data/statistics.json, data/manifest.json and SHA256SUMS."""
    root = Path(root)
    data = root / "data"
    data.mkdir(exist_ok=True)
    exclusions = json.loads((data / "exclusions.json").read_text(encoding="utf-8"))
    index, words = build_index(root)
    (data / "index.json").write_text(dumps(index), encoding="utf-8", newline="\n")
    stats = build_statistics(index, words, exclusions)
    (data / "statistics.json").write_text(dumps(stats), encoding="utf-8", newline="\n")

    covered = [p.relative_to(root).as_posix() for p in content_files(root)]
    covered += ["data/exclusions.json", "data/index.json", "data/statistics.json"]
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "archive_version": source_info["exported"][:10],
        # The source export time, not the build time, so rebuilding unchanged
        # content produces byte-identical files.
        "generated_from": source_info,
        "counts": {
            "documents": len(index),
            "posts": stats["totals"]["posts"],
            "pages": stats["totals"]["pages"],
            "excluded": len(exclusions),
            "files": len(covered),
        },
        "checksum_algorithm": "sha256",
        "files": {p: sha256(root / p) for p in sorted(covered)},
    }
    (data / "manifest.json").write_text(dumps(manifest), encoding="utf-8", newline="\n")
    sums = sorted(covered + ["data/manifest.json"])
    (root / "SHA256SUMS").write_text("".join(f"{sha256(root / p)}  {p}\n" for p in sums),
                                     encoding="utf-8", newline="\n")
    return manifest


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    info = json.loads((root / "data" / "manifest.json").read_text(encoding="utf-8"))["generated_from"]
    m = write_catalogue(root, info)
    print(f"catalogue rebuilt: {m['counts']}")
