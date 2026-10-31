#!/usr/bin/env python3
"""Build the downloadable release ZIPs.

    python3 tools/package.py [--site build/site] [--out build/release]

Writes:
  headphone-commute-archive-VERSION.zip          the archive: articles, catalogue,
                                                 checksums, licence and documentation
  headphone-commute-archive-VERSION-website.zip  the built website (if --site exists)
  SHA256SUMS-release.txt                         checksums of the ZIPs

The ZIPs are deterministic: entries are sorted and carry the archive
version's date, so the same archive always produces identical files.
"""

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_PARTS = ["archive", "pages", "data", "docs", "LICENSES", "SHA256SUMS", "README.md",
                 "LICENSE.md", "PRESERVATION.md", "CONTRIBUTING.md"]


def files_under(base, parts):
    out = []
    for part in parts:
        p = base / part
        if p.is_file():
            out.append(p)
        elif p.is_dir():
            out.extend(f for f in p.rglob("*") if f.is_file())
    return sorted(out, key=lambda f: f.relative_to(base).as_posix())


def write_zip(path, base, files, prefix, date):
    stamp = tuple(int(x) for x in date.split("-")) + (0, 0, 0)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in files:
            info = zipfile.ZipInfo(f"{prefix}/{f.relative_to(base).as_posix()}", date_time=stamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, f.read_bytes())


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--site", default=str(ROOT / "build" / "site"))
    ap.add_argument("--out", default=str(ROOT / "build" / "release"))
    args = ap.parse_args()
    version = json.loads((ROOT / "data" / "manifest.json").read_text(encoding="utf-8"))["archive_version"]
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    name = f"headphone-commute-archive-{version}"
    made = [out / f"{name}.zip"]
    write_zip(made[0], ROOT, files_under(ROOT, ARCHIVE_PARTS), name, version)
    site = Path(args.site)
    if (site / "index.html").exists():
        made.append(out / f"{name}-website.zip")
        write_zip(made[1], site, files_under(site, ["."]), f"{name}-website", version)
    (out / "SHA256SUMS-release.txt").write_text("".join(f"{sha256(p)}  {p.name}\n" for p in made), encoding="utf-8")
    for p in made:
        print(f"{p}  {p.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
