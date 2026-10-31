# Headphone Commute Archive

A permanent, text-only archive of **Headphone Commute**, an independent music publication founded in 2007, writing about electronic, ambient, modern classical, experimental and cinematic music.

The archive contains the publication's reviews, interviews, studio features, label profiles, essays and festival reports, about 2,200 articles, as plain-text Markdown files. It keeps the words, not the website: no images, audio, video or embedded players.

- **Read on the web:** <https://headphonecommute.github.io/headphone-commute-archive/>
- **Read on GitHub:** open any file in [`archive/`](archive/). GitHub displays the Markdown as formatted text.
- **Download everything:** the [latest release](https://github.com/headphonecommute/headphone-commute-archive/releases/latest) has the complete archive as a ZIP. You can also use *Code → Download ZIP*, or `git clone`.

## What's in this repository

| Path | Contents |
|---|---|
| `archive/YYYY/ID-title.md` | One file per article, grouped by year of publication |
| `pages/` | A small number of standalone pages |
| `data/index.json` | Catalogue of every article: ID, title, date, categories, file path |
| `data/statistics.json` | Totals by year and category |
| `data/exclusions.json` | Published items deliberately outside the archive's scope, with reasons |
| `data/manifest.json`, `SHA256SUMS` | Checksums of every file |
| `site/` | Source of the archive website |
| `tools/` | Scripts to build the website and rebuild the catalogue |
| `tests/` | Checks that validate every file in the archive |
| `docs/SCHEMA.md` | Description of every file format |
| `docs/QA_REPORT.md` | How the archive was checked |
| `PRESERVATION.md` | How to keep, verify, mirror and rebuild the archive |

Each article file looks like this:

```markdown
---
id: 18779
title: "Decibel 2012 : Day One"
date: "2012-10-06T06:24:02-05:00"
category: ["Festivals and Events"]
---

The following feature is a series of articles covering…
```

## Verify a copy

```sh
sha256sum -c SHA256SUMS
```

For a deeper check (front matter, links, catalogue, checksums), install Python 3 and run:

```sh
pip install -r requirements.txt
python3 -m pytest tests
```

## Build the website

Install [Hugo](https://gohugo.io/) (tested with 0.140.2) and [Pagefind](https://pagefind.app/) (tested with 1.3.0), then:

```sh
tools/build_site.sh            # writes the site to build/site
```

The result is plain HTML that works on any web host, under any subpath, or opened directly from disk (search needs a web server).

## Rights

The articles are © Mike Lazarev / Headphone Commute, licensed [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/): copy, mirror and share them with credit, non-commercially, without changes. The 20 guest articles (marked with an `author` field) remain © their authors. The tools are MIT-licensed. Full terms are in [`LICENSE.md`](LICENSE.md).

See [`CONTRIBUTING.md`](CONTRIBUTING.md) to report a problem, and [`PRESERVATION.md`](PRESERVATION.md) to help keep the archive alive.
