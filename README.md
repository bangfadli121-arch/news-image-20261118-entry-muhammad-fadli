# news-image-20261118 — Sum up 18 November's world news in one image

Entry for the make.fun competition **news-image-20261118**:
*"Sum up 18 November's world news in one image."*

## The image

A classic newspaper front page for 18 November 2026, in the style of the
competition's winning entries: dense front-page layout, 28 news stories,
a map with pins, and three photorealistic hero photos:

1. **Bahrain at night** — hero photo, top story.
2. **Collapsed Crimea bridge** — hero photo.
3. **Manila summit (Trump–Marcos)** — hero photo.

- Format: PNG, 1024 × 1024, 8-bit/color RGB, non-interlaced
- Size: 389,709 bytes
- SHA-256: `69da07cdd67723144390dcbc2d81593b8c67a4c92bcb0028eb065145d68d9f7c`

## How to run

Python 3.13, standard library only (no PIL, no third-party packages):

```sh
python3 main.py
```

`main.py` reads `entry.png` next to it, validates it (PNG magic, IHDR
1024×1024, per-chunk CRC, IEND present, size ≤ 1 MiB), checks its SHA-256
against the expected value recorded in the script, copies it byte-for-byte
to `/output/entry.png`, re-reads the output and confirms the SHA-256 is
identical, then prints the SHA-256 and size to stdout.
