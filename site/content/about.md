---
title: About this archive
description: What the Headphone Commute text archive contains, how it is built, and how to download, verify and mirror it.
---

Headphone Commute is an independent music publication founded in 2007 by Mike Lazarev, writing about electronic, ambient, modern classical, experimental and cinematic music. For close to twenty years it published album reviews, artist interviews, studio visits, label profiles, festival reports and essays.

This archive preserves that writing. It keeps the words, not the website: there are no images, audio players, videos or embedded media, and no design from the original site. What remains is the text of each article, its title, its original publication date and its categories.

## What is included

Reviews, interviews, studio features, label profiles, essays, festival reports, and track and video premieres with substantial text. Mixes and podcasts, the yearly "Best of" lists, the short "Out Today" release roundups and pages that were part of the old site's navigation are outside the archive's scope. The archive's catalogue lists each of them with its reason.

Articles were converted from the publication's own database without rewriting. Paragraphs, headings, quotations, lists, emphasis and links are kept. Links between articles point to the archived copies. Links to other websites are kept as they were, even where those sites have since changed or disappeared.

## Why it exists

Websites depend on hosting, software, domain names and someone to pay for and maintain them. When any of those stops, the writing goes with it. This archive is designed so that the text survives independently: it is stored as ordinary files, in open formats, in several places, and anyone may keep a copy.

No single service can promise to keep anything forever. The archive's survival depends on copies existing in more than one place, which is why downloading and mirroring it is encouraged.

## How it is organised

Each article is one plain-text [Markdown](https://commonmark.org/) file, readable in any text editor:

- `archive/2012/18779-decibel-2012-day-one.md`: the year of publication, then the article's original ID number and a short name.
- A short header at the top of each file records the ID, title, date (with its original time zone offset) and categories.
- `data/index.json` lists every article with its title, date, categories and file path, for software and researchers.
- `data/statistics.json` holds totals by year and category; `data/exclusions.json` lists what is outside the archive's scope and why.
- `data/manifest.json` and `SHA256SUMS` record a checksum of every file.

The full description of each format is in `docs/SCHEMA.md` in the repository.

## Download, verify and mirror

The complete archive is a [public repository](https://github.com/headphonecommute/headphone-commute-archive): the Markdown files, the catalogue, the conversion tools, this website's source and the documentation. Downloading it gives you everything; nothing else is needed to read the articles. Each version is also published as a [downloadable ZIP](https://github.com/headphonecommute/headphone-commute-archive/releases/latest).

To check that a copy is complete and unaltered, run this in the archive folder on any Linux or macOS computer:

```
sha256sum -c SHA256SUMS
```

To rebuild this website from a copy, install [Hugo](https://gohugo.io/) and [Pagefind](https://pagefind.app/) and run `tools/build_site.sh`. The result is a folder of plain HTML pages that can be hosted anywhere, or opened directly from disk (search needs a web server; everything else works offline).

## Rights

The articles are © Mike Lazarev / Headphone Commute and licensed under [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/): you may copy, mirror and share them, with credit, non-commercially and unchanged. Guest articles, marked with their author's name, remain © their authors and may be shared only as part of complete, unaltered copies of the archive. The tools that build the archive are MIT-licensed. Full terms are in `LICENSE.md` in the repository.
