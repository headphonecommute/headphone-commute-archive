# Quality assurance report

Source: the publication's database export of 2026-10-31. This report is regenerated after every full conversion.

## Summary

| | Count |
|---|---|
| Published posts and pages read from the source | 3173 |
| Archived (Markdown files written) | 2174 |
| Excluded by scope rules (listed in `data/exclusions.json`) | 999 |
| Conversion failures | 0 |
| Duplicate IDs | 0 |
| Words archived | 1,696,539 |
| Date range | 2008-01-01 to 2026-10-04 |

No article is dropped silently: every published item is either archived or listed with its reason.

## Exclusions by reason

| Reason | Count |
|---|---|
| page not selected for the archive | 350 |
| category excluded: Mixes | 330 |
| category excluded: Out Today | 75 |
| premiere with little text | 22 |
| category excluded: Best of 2011 | 19 |
| category excluded: Best of 2009 | 18 |
| category excluded: Best of 2012 | 16 |
| category excluded: Best of 2015 | 16 |
| category excluded: Best of 2013 | 15 |
| category excluded: Best of 2014 | 14 |
| category excluded: Best of 2016 | 14 |
| category excluded: Best of 2010 | 12 |
| category excluded: Best of 2020 | 12 |
| category excluded: Contemplative Podcast | 12 |
| category excluded: Best of 2021 | 12 |
| category excluded: Best of 2022 | 12 |
| category excluded: Best of 2023 | 12 |
| category excluded: Best of 2025 | 12 |
| category excluded: Best of 2019 | 11 |
| category excluded: Best of 2024 | 11 |
| category excluded: Best of 2008 | 2 |
| category excluded: Best of... | 2 |

## What the conversion changed

Every change below was logged per article. Text inside anything removed was recorded, and QA
accounts for every word of the stored article.

| Change | Occurrences | Articles |
|---|---|---|
| Player shortcodes removed (Bandcamp, SoundCloud, Mixcloud, audio…) | 1286 | 826 |
| Embedded video/player links removed | 406 | 379 |
| Images, iframes, icons, dividers and link lists removed | 8298 | 2174 |
| Non-editorial labels removed with those elements (e.g. “Bandcamp Tidal Spotify”) | 523 | 510 |
| Image captions removed with their images | 164 | 82 |
| Links left empty after their image was removed | 62 | 17 |
| MySpace links kept as text without the link | 63 | 28 |
| Links to other archived articles made relative | 1506 | 682 |
| Links to headphonecommute.com pages outside the archive kept as text | 1404 | 643 |
| Layout tables flattened into paragraphs | 107 | 86 |
| Titles with hidden HTML comments cleaned | 232 | 232 |
| Bold/italic edges moved off punctuation (no text change) | 98 | 63 |
| Bold/italic around punctuation only, formatting dropped (no text change) | 47 | 43 |
| Item-less list wrappers unwrapped | 1 | 1 |
| Approved corrections to the stored text | 1 | 1 |

## Checks run on every article

- **Source accounting:** every word of the stored source text reaches the converted article,
  unless it belonged to something logged as removed (player shortcode, embed address, link icon label,
  image caption). Result: no unexplained text loss.
- **Round trip:** the Markdown is rendered with a CommonMark parser and compared with the cleaned source
  for text, link targets, bold and italics. Result: no differences.
- **Structure:** valid YAML front matter, required fields, no HTML, images or shortcodes left in the text.

Articles flagged by these checks: 0.

## Worth a manual look

Nothing outstanding.

Already reviewed and approved by the publisher (`docs/qa/reviewed.json`); flagged again
automatically if the stored source text changes:

| ID | File | Checked | Reviewed |
|---|---|---|---|
| 18779 | `archive/2012/18779-decibel-2012-day-one.md` | Approved corrections to the stored text | 2026-10-31 |
| 43982 | `archive/2020/43982-dakota-suite-ill-show-you-mine.md` | Item-less list wrappers unwrapped | 2026-10-31 |

## Archive-wide verification

- `pytest tests` validates every file: front matter, unique IDs, UTF-8, no leftover markup, internal
  links resolve, catalogue matches the files, and every checksum matches.
- Two clean rebuilds from the same export produce byte-identical files (`SHA256SUMS` unchanged).
- Last test run: 52 passed, 2 skipped in 7.96s
- A 32-article sample (earliest and latest posts, long and short reviews, interviews, essays, layout
  tables, heavy embeds, imports from earlier platforms) was compared side by side with the source and
  approved by the publisher before the full conversion.
