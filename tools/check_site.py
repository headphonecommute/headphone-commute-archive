#!/usr/bin/env python3
"""Check a built site: every relative link and asset resolves to a file,
and no page loads scripts, styles, fonts or images from another host.

    scripts/check_site.py build/site
"""
import re
import sys
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path


class Refs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.assets = [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        for key in ("src", "href") if tag in ("script", "img", "link", "iframe", "source", "audio", "video") else ():
            if a.get(key):
                self.assets.append((tag, a[key]))


def main(site):
    site = Path(site).resolve()
    pages = sorted(site.rglob("*.html"))
    broken, external_assets, absolute_internal = [], [], []
    for page in pages:
        refs = Refs()
        refs.feed(page.read_text(encoding="utf-8"))
        for tag, url in refs.assets:
            if re.match(r"[a-z]+:|//", url, re.I):
                external_assets.append((page.relative_to(site), tag, url))
        for url in refs.links + [u for _, u in refs.assets]:
            if re.match(r"[a-z][a-z0-9+.-]*:|//|#", url, re.I) or not url:
                continue
            if url.startswith("/"):
                absolute_internal.append((page.relative_to(site), url))
                continue
            path = urllib.parse.unquote(url.split("#")[0].split("?")[0])
            if not path:
                continue
            target = (page.parent / path).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                broken.append((page.relative_to(site), url))
    print(f"{len(pages)} pages checked")
    for label, items in (("broken relative links", broken), ("assets from other hosts", external_assets),
                         ("root-relative links (break under a subpath)", absolute_internal)):
        print(f"{label}: {len(items)}")
        for item in items[:10]:
            print("   ", *item)
    return 1 if broken or external_assets or absolute_internal else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "build/site"))
