# The World in One Day — 18 November 2026

Entry for the make.fun competition
**news-image-20261118 — "Sum up 18 November's world news in one image"**
($250 prize pool; deadline Friday 20 November 2026, 07:00 WIB).

The entry is a classic newspaper front page, **THE WORLD IN ONE DAY**,
dated **Wednesday, 18 November 2026**. Every story in it happened, or was
first reported, on 18 November 2026.

## The day's news in the image

- **Lead — Asia / Diplomacy: TRUMP MEETS MARCOS IN MANILA.**
  State visit and luncheon at Malacañang on Wednesday, before Trump flies
  to Shenzhen, where he, Xi and Putin hold the first trilateral on
  Thursday. The Quad flags (USA, Japan, India, Australia) run beneath the
  lead; the Quad leaders met in Manila on Tuesday.
- **Ukraine / War: CRIMEA BRIDGE HIT FOR SECOND DAY.**
  Kyiv strikes the span again as Russian missiles pound bridges in the
  capital.
- **Trade / APEC: CANADA AND CHINA EXTEND TRADE DEALS.**
  Xi meets Carney on the eve of the APEC summit in Shenzhen.
- **Weather: CYCLONE AKVAN NEARS INDIA.**
  Bay of Bengal storm to turn severe by Thursday; India on high alert.
- **Also today (ticker):** UK sanctions firms over Israeli settlements;
  Baidu chief warns of AI bubble; India re-elected to ITU Council
  2027–2030; India wins 10th SAFF title (beat Pakistan 2–1); US presses
  UN over Taiwan flights.

## How it works

`main.py` (Python 3.13, standard library only — no network, no packages)
copies the `entry.png` held in this repository to the output directory as
`entry.png`. Before copying it validates the file: PNG magic bytes, every
chunk's CRC, a closing IEND chunk, 1024×1024 pixels, 8-bit true colour,
and at most 1 MiB. It then re-reads the output and prints its sha256, so a
run is verifiably byte-identical to the image in the repository.

## Running it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Without `MAKEFUN_OUTPUT_DIR` it writes to `/output` (the grader's path).
Run it twice with different output directories: both outputs are
byte-identical to `entry.png` in this repository
(sha256 `c9b2b31bfaff62bfd6e63a778d023bb66195ffe9b3d2420708ae378961cb725d`).

## Files

| File | What it is |
| --- | --- |
| `entry.png` | The image: 1024×1024 PNG, 114,602 bytes |
| `main.py` | The program: validates and copies `entry.png` |
| `README.md` | This file |
| `LICENSE` | MIT License |
| `.makefun/owner.json` | Claim file naming the entrant's Solana wallet |
