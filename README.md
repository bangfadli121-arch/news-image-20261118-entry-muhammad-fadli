# news-image-20261118 — Sum up 18 November's world news in one image

Entry for the make.fun competition **news-image-20261118**:
*"Sum up 18 November's world news in one image."*

## The image (v6-hdmap)

A classic newspaper front page for 18 November 2026, in the style of the
competition's winning entries: dense front-page layout, 28 news stories,
and a high-definition world map drawn from Natural Earth 50m data, with
numbered pins marking the top stories. This variant answers fadli's
request — *"itu petanya di bikin hd coba wok smaa tulisan Nya coba yang
menurut lu bagus gmna"* — with:

- **HD world map** — country borders and coastlines from Natural Earth
  50m data, rendered sharp at full 1024 × 1024 resolution.
- **Bigger, bolder headline cards** — the top stories' headline cards
  are larger and heavier so they read clearly at a glance.
- **ALSO list at 13 pt** — the "ALSO ON WEDNESDAY 18 NOVEMBER" list is
  set larger for readability, still covering 28 stories in total.

Top stories on the page include the Bahrain night story, the collapsed
Crimea bridge, and the Manila summit (Trump–Marcos).

- Format: PNG, 1024 × 1024, 8-bit/color RGB, non-interlaced
- Size: 406,087 bytes
- SHA-256: `5a2114aa2751984f303452f9ae879b2e9aed551c9383a910f434d5fe20bd28f4`

## How to run

Python 3.13, standard library only (no PIL, no third-party packages):

```sh
python3 main.py
```

`main.py` reads `entry.png` next to it, validates it (PNG magic, IHDR
1024×1024 8-bit RGB, per-chunk CRC, IEND present, size ≤ 1 MiB), checks
its SHA-256 against the expected value recorded in the script, copies it
byte-for-byte to `/output/entry.png`, re-reads the output and confirms
the SHA-256 is identical, then prints the SHA-256 and size to stdout.

Pass an explicit path to write elsewhere, e.g. `python3 main.py
/tmp/entry.png`. Pass `--check-only` to validate the image and report
its SHA-256 without writing any file.
