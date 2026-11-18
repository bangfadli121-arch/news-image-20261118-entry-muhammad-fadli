# news-image-20261118-entry-muhammad-fadli

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/bangfadli121-arch/news-image-20261118-entry-muhammad-fadli/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/bangfadli121-arch/news-image-20261118-entry-muhammad-fadli/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A classic newspaper front page summing up 18 November 2026 in one image, in the style of the competition's winning entries: dense front-page layout, 28 news stories, and a high-definition world map drawn from Natural Earth 50m data, with numbered pins marking the top stories. The three hero photos are photorealistic — the Bahrain night story, the collapsed Crimea bridge, and the Manila summit (Trump–Marcos). Headline cards are set big and bold, and the "ALSO ON WEDNESDAY 18 NOVEMBER" list is set at 13 pt for readability.

- Format: PNG, 1024 × 1024, 8-bit/color RGB, non-interlaced
- Size: 406,087 bytes
- SHA-256: `5a2114aa2751984f303452f9ae879b2e9aed551c9383a910f434d5fe20bd28f4`

## Run it

```sh
python3 main.py
```

Python 3.13, standard library only (no PIL, no third-party packages). `main.py` reads `entry.png` next to it, validates it (PNG magic, IHDR 1024×1024 8-bit RGB, per-chunk CRC, IEND present, size ≤ 1 MiB), checks its SHA-256 against the expected value recorded in the script, copies it byte-for-byte to `/output/entry.png`, re-reads the output and confirms the SHA-256 is identical, then prints the SHA-256 and size to stdout.

Pass an explicit path to write elsewhere, e.g. `python3 main.py /tmp/entry.png`. Pass `--check-only` to validate the image and report its SHA-256 without writing any file.

---

<sub>Entered on [make.fun](https://make.fun/?ref=8y9pksda&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
