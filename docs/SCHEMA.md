# Archive file formats

All files are UTF-8 with Unix line endings. JSON files are indented with two spaces and end with a newline. Records appear in a fixed order, so unchanged content always produces identical files.

Schema version: **1.0** (the `schema_version` field in `data/statistics.json` and `data/manifest.json`).

## Articles: `archive/YYYY/ID-slug.md` and `pages/ID-slug.md`

Each article is a CommonMark document with a YAML front matter block:

```markdown
---
id: 12345
title: "An Example Album Review"
date: "2012-06-15T10:30:00-05:00"
category: ["Albums"]
---

The article text…
```

| Field | Type | Present | Meaning |
|---|---|---|---|
| `id` | integer | always | Original article ID from the publication's database. Stable, unique, and also the start of the filename. |
| `title` | string | always | The title exactly as published, with entities decoded to Unicode. |
| `date` | string | always | Original publication time in ISO 8601, with the UTC offset in force when it was published. |
| `category` | list of strings | posts | Editorial categories. The primary category comes first. |
| `author` | string | guest posts only | Byline of a guest writer. Everything else is by the publisher. |
| `parent` | integer | some pages | ID of the parent page. |

- `YYYY` is the year of `date`.
- The `slug` part of the filename comes from the title and is for readability only. Identify articles by `id`.
- Links between articles are relative paths to the other `.md` file (for example `../2009/1328-giuseppe-ielasi-aix.md`). They work on GitHub, in the website and in any copy of the repository.

## `data/index.json`

An array with one object per article, sorted chronologically by publication time (UTC), then by `id`:

```json
{
  "id": 12345,
  "type": "post",
  "title": "An Example Album Review",
  "date": "2012-06-15T10:30:00-05:00",
  "category": ["Albums"],
  "markdown_path": "archive/2012/12345-an-example-album-review.md"
}
```

`type` is `post` or `page`. `author` appears only when the article has one. `markdown_path` is relative to the repository root.

Common uses:
- **List by year:** filter on `date[:4]`.
- **Filter by category:** `category` contains the name.
- **Find by original ID:** match on `id`.
- **Find by title:** search `title`.

## `data/statistics.json`

| Field | Meaning |
|---|---|
| `totals` | `documents`, `posts`, `pages`, `words` (words of article text), `excluded` |
| `first_date`, `last_date` | Earliest and latest publication dates |
| `by_year`, `words_by_year` | Article and word counts per publication year |
| `by_category` | Articles per category; an article with two categories counts in both |
| `excluded_by_reason` | Counts from `exclusions.json`, grouped by reason |

## `data/exclusions.json`

Published items the archive deliberately leaves out, sorted by `id`:

```json
{ "id": 52640, "type": "post", "date": "2021-08-10T11:09:45+01:00", "category": ["Mixes"], "reason": "category excluded: Mixes" }
```

## `data/manifest.json`

| Field | Meaning |
|---|---|
| `archive_version` | Date of the source export the archive was built from |
| `generated_from` | Kind and completion time of that export. It is not the build time, so rebuilding the same export changes nothing. |
| `counts` | `documents`, `posts`, `pages`, `excluded`, and `files` (files covered by checksums) |
| `checksum_algorithm` | Always `sha256` |
| `files` | SHA-256 of every article and of `index.json`, `statistics.json` and `exclusions.json` |

## `SHA256SUMS`

The same checksums plus `data/manifest.json`, in the format read by `sha256sum`. To verify a copy:

```sh
sha256sum -c SHA256SUMS
```
