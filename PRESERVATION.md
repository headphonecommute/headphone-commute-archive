# Preservation

This document is for anyone who wants to keep the Headphone Commute archive readable for the long term, including after the original publication, its website and its domain are gone.

## What the archive contains

- About 2,200 articles published by Headphone Commute from 2008 onward: album reviews, artist interviews, studio features, label profiles, essays, festival reports, and track and video premieres with substantial text.
- For each article: the full text, the title, the original publication date with its time-zone offset, the editorial categories, and a guest author where there is one.
- A catalogue (`data/`) describing every article, the archive's statistics, the items deliberately left out and why, and checksums of every file.

It does not contain images, audio, video, embedded players, reader comments, or the design of the original website. Mixes and podcasts, yearly "Best of" lists, short release roundups, and pages that were only part of the old site's navigation are outside its scope.

## Why it exists

Headphone Commute's writing documents close to twenty years of independent music. A website depends on its hosting, software, domain and maintainer, and when any of them stops the writing disappears with it. This archive separates the writing from all of that.

## The canonical format

The archive itself is the set of Markdown files in `archive/` and `pages/`. Everything else (the catalogue, the website, any download) is generated from them and can be regenerated.

- **Encoding:** UTF-8 text with Unix line endings.
- **Format:** [CommonMark](https://commonmark.org/) Markdown, with strikethrough as the only extension. No HTML.
- **Header:** each file starts with a short YAML block between `---` lines: `id`, `title`, `date`, `category`, and `author` for guest writers.
- **Links:** links between articles are relative paths to the other file, so they keep working in any copy.

These are among the most widely supported plain-text formats in existence. A file can be read in any text editor, today or decades from now, without special software.

## How articles are organised

`archive/YYYY/ID-title.md`:
- `YYYY` is the year the article was published.
- `ID` is its original, permanent identifier.
- `title` is a readable short name.

An article is identified by its ID; the title part of the filename is only for convenience. `data/index.json` lists every article chronologically.

## Download a complete copy

Any of these gives you the whole archive:

- **GitHub:** on the repository page, use *Code → Download ZIP*, or `git clone` the repository.
- **Releases:** each archive version is published as a downloadable ZIP.
- **Internet Archive:** a deposited copy (see "Where copies are kept").

Nothing else is needed to read the articles.

## Verify a copy

Every file's SHA-256 checksum is recorded in `SHA256SUMS` and in `data/manifest.json`. In the archive folder:

```sh
sha256sum -c SHA256SUMS
```

Every line should end in `OK`. On macOS, use `shasum -a 256 -c SHA256SUMS`. For a deeper check of structure, links and catalogue, run the tests: `pip install -r requirements.txt && python3 -m pytest tests`.

## Rebuild the website

1. Install Hugo (tested with 0.140.2) and Pagefind (tested with 1.3.0). Both are single programs with no other dependencies.
2. Run `tools/build_site.sh`.
3. Publish the folder `build/site` on any static host, or open `build/site/index.html` from disk.

If those tools become unavailable, the site is a convenience, not the archive. The Markdown files remain readable as they are, and any future Markdown publishing tool can present them.

## Create an independent mirror

You are encouraged to keep a copy. To mirror the archive:

1. Download or clone it.
2. Verify it with `sha256sum -c SHA256SUMS`.
3. Host the files, the built website, or both, wherever you like.

Please keep the files unaltered, and keep `LICENSE.md` with them. If you rebuild the catalogue after changes, use `python3 tools/catalogue.py`, but a mirror should normally not change anything.

## Where copies are kept

- The public GitHub repository, <https://github.com/headphonecommute/headphone-commute-archive>, and its website, <https://headphonecommute.github.io/headphone-commute-archive/>
- Release ZIP files attached to that repository: <https://github.com/headphonecommute/headphone-commute-archive/releases>
- The Internet Archive (archive.org): deposit in preparation; its address will be added here

 The exact addresses are also listed in `README.md`. No single service can guarantee permanent availability, which is why the archive is kept in several independent places and why private copies matter.

## If the original website disappears

Nothing in this archive depends on the original website, its hosting or its domain:

- No file links to the original site to work.
- No file loads anything from it.
- Article dates, titles and text are stored in the files themselves.

To continue preserving it:

- Keep at least one verified copy, ideally in more than one place.
- If the GitHub repository becomes unavailable, re-publish a verified copy elsewhere (another code host, a static web host or a library repository) together with `LICENSE.md` and this document.
- Deposit copies with institutions that preserve digital culture.
- When you make a copy, verify its checksums against an existing copy. Matching checksums show the text is unchanged.
