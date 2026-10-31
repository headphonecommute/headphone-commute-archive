"""Check the built website, if one has been built (tools/build_site.sh)."""

import importlib.util
from pathlib import Path

import pytest

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "archive").is_dir())
SITE = ROOT / "build" / "site"


@pytest.mark.skipif(not (SITE / "index.html").exists(), reason="site not built")
def test_site_links_assets_and_subpath_safety():
    spec = importlib.util.spec_from_file_location("check_site", Path(__file__).resolve().parents[1] / "tools" / "check_site.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.main(SITE) == 0


@pytest.mark.skipif(not (SITE / "index.html").exists(), reason="site not built")
def test_every_article_has_a_page():
    import json
    index = json.loads((ROOT / "data" / "index.json").read_text(encoding="utf-8"))
    for rec in index:
        page = SITE / (rec["markdown_path"][:-3] + ".html")
        assert page.exists(), rec["markdown_path"]
