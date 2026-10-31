"""Validate the published archive. These tests read only the repository's own
files, so anyone with a copy can run them offline, with no other services."""

import json
import os
import re
from datetime import datetime
from pathlib import Path

import pytest
from markdown_it import MarkdownIt

from catalogue import build_index, content_files, read_document, sha256

# The archive root is the nearest folder above this file that has archive/.
ROOT = next(p for p in Path(__file__).resolve().parents if (p / "archive").is_dir())
FILES = content_files(ROOT)
md = MarkdownIt("commonmark").enable(["table", "strikethrough"])

pytestmark = pytest.mark.skipif(not FILES, reason="archive not generated")


def load(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def documents():
    return [(p, *read_document(p)) for p in FILES]


def test_front_matter_is_valid(documents):
    allowed = {"id", "title", "date", "category", "author", "parent"}
    for path, meta, body in documents:
        assert set(meta) <= allowed, f"{path}: unexpected keys {set(meta) - allowed}"
        assert isinstance(meta["id"], int), path
        assert isinstance(meta["title"], str) and meta["title"].strip(), path
        assert meta["title"] == meta["title"].strip(), path
        assert not re.search(r"<[A-Za-z/!]", meta["title"]), f"{path}: markup in title"
        datetime.fromisoformat(meta["date"])  # raises if invalid
        assert re.search(r"[+-]\d{2}:\d{2}$", meta["date"]), f"{path}: date lacks offset"
        if path.parts[-3] == "archive" or "archive" in path.parts:
            assert isinstance(meta["category"], list) and meta["category"], path


def test_bodies_are_not_empty(documents):
    for path, meta, body in documents:
        assert re.search(r"\w", body), f"{path}: empty body"


def test_ids_unique_and_match_filenames(documents):
    ids = [meta["id"] for _, meta, _ in documents]
    assert len(ids) == len(set(ids))
    for path, meta, _ in documents:
        assert path.name.startswith(f"{meta['id']}-"), path


def test_files_are_in_their_publication_year(documents):
    for path, meta, _ in documents:
        if "archive" in path.parts:
            assert path.parent.name == meta["date"][:4], path


def test_utf8_and_line_endings():
    for p in FILES:
        raw = p.read_bytes()
        raw.decode("utf-8")  # raises on invalid UTF-8
        assert b"\r" not in raw, p
        assert raw.endswith(b"\n") and not raw.endswith(b"\n\n"), p
        assert "�" not in raw.decode("utf-8"), f"{p}: replacement character"
        assert not re.search("[-]", raw.decode("utf-8")), f"{p}: private-use placeholder left over"


def test_no_html_media_or_shortcodes(documents):
    for path, _, body in documents:
        for tok in md.parse(body):
            assert tok.type != "html_block", f"{path}: HTML block {tok.content[:60]!r}"
            for child in tok.children or []:
                assert child.type not in ("html_inline", "image"), f"{path}: {child.type} {child.content[:60]!r}"
        assert not re.search(r"\[/?(bandcamp|soundcloud|mixcloud|audio|vimeo|youtube|caption|tracklist|embed|gallery)(?=[\s=\]])[^\]]*\](?!\()", body), path
        assert not re.search(r"<\s*(iframe|script|img|audio|video|object|embed)\b", body, re.I), path


def test_no_links_to_original_site_or_myspace(documents):
    for path, _, body in documents:
        assert not re.search(r"\]\(https?://(www\.)?headphonecommute\.com", body), path
        assert not re.search(r"\]\(https?://([\w-]+\.)?myspace\.com", body, re.I), path


def test_internal_links_resolve(documents):
    for path, _, body in documents:
        for target in re.findall(r"\]\(([^)\s]+)\)", body):
            if re.match(r"[a-z][a-z0-9+.-]*:", target, re.I):
                continue
            assert target.endswith(".md"), f"{path}: unexpected relative link {target}"
            assert (path.parent / target).resolve().is_file(), f"{path}: broken link {target}"


def test_index_matches_files(documents):
    index = load("index.json")
    assert index == build_index(ROOT)[0]
    assert {r["markdown_path"] for r in index} == {p.relative_to(ROOT).as_posix() for p in FILES}


def test_exclusions_do_not_overlap_index():
    index_ids = {r["id"] for r in load("index.json")}
    excluded = load("exclusions.json")
    assert all(e["reason"] for e in excluded)
    assert not index_ids & {e["id"] for e in excluded}


def test_statistics_agree_with_index():
    index, stats = load("index.json"), load("statistics.json")
    assert stats["totals"]["documents"] == len(index)
    assert sum(stats["by_year"].values()) == len(index)
    assert stats["totals"]["excluded"] == len(load("exclusions.json"))


def test_manifest_checksums():
    manifest = load("manifest.json")
    for rel, digest in manifest["files"].items():
        assert sha256(ROOT / rel) == digest, f"checksum mismatch: {rel}"
    covered = {p.relative_to(ROOT).as_posix() for p in FILES}
    assert covered <= set(manifest["files"]), "files missing from manifest"


def test_sha256sums_file_matches():
    for line in (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, rel = line.split("  ", 1)
        assert sha256(ROOT / rel) == digest, rel
