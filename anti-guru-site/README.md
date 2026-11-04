# The Anti-Guru Field Manuals: static site

Hugo + Tailwind CSS v4. Zero JavaScript, zero cookies, zero third-party requests.
Built CSS is about 6 KB gzipped; one self-hosted font (18 KB).

## Run it

```bash
npm install          # Tailwind CLI + font (build tooling only)
npm run dev          # http://localhost:1313
npm run build        # output in ./public
```

Needs Hugo >= 0.128 (tested on 0.139 extended) and Node >= 20.

## Where the cover images go

Hugo serves everything in `static/` from the site root:

| File you drop in                  | Served at                      |
| --------------------------------- | ------------------------------ |
| `static/assets/covers/cover-001.jpg` | `/assets/covers/cover-001.jpg` |
| `static/assets/covers/cover-002.jpg` | `/assets/covers/cover-002.jpg` |

Both are already in place (800 px wide, ~160 KB, resized from your originals, which are kept
in `source-art/` outside the web root). To replace one, overwrite the file keeping the name and a
2:3 ratio. The path is set by `cover:` in each book's front matter.

## Things to change before launch

1. `hugo.toml`: `baseURL`, `newsletterAction` (your email provider's form endpoint), `githubRepo`.
   The GitHub button on `/resources/` stays hidden while the URL contains `CHANGE-ME`.
2. `static/_headers`: if your newsletter host is not buttondown.com, update `form-action`.
3. Turn off open/click tracking in the email provider so "zero tracking" stays true.
4. Book #002 on launch day (10 Nov 2026): in `content/manuals/002-fitness-manual.md` set
   `status: "published"`, `amazon: "<real link>"`, and `asin:`. Remove `release_date` if you like.
5. Add `isbn:` to either book when you have it (shown only if set).

## Structure

```
hugo.toml                  site config, menus, params
assets/css/main.css        Tailwind v4 config (@theme tokens) + components
content/_index.md          homepage hero copy
content/manifesto.md       /manifesto/
content/manuals/*.md       one file per book; ALL metadata + TOC live in front matter
content/resources/         /resources/ intro text
data/resources.yaml        the downloads table (add a row, add a file in static/downloads)
layouts/_default/          baseof, single (prose pages), list
layouts/index.html         homepage
layouts/manuals/           book detail + catalog list
layouts/resources/list.html
layouts/partials/          head, header, footer, book-card, buy-button, newsletter, schema-book...
static/assets/             covers + brand images
static/downloads/          CSV / PY / PDF files
```

## Adding Book #003

1. Copy `content/manuals/001-trading-manual.md` to `003-....md`; change `number`, `volume`, `weight`, `cover`, TOC.
2. Drop `cover-003.jpg` in `static/assets/covers/`.
3. Add files to `static/downloads/003-.../` and rows to `data/resources.yaml`.

No template changes needed. Only books with a content file appear: there are no placeholder pages.

## Licence

Site code and content: CC BY-SA 4.0, like the manuals.
