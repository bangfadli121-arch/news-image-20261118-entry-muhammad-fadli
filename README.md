# One Day in Photos — 18 November 2026

A make.fun entry for **news-image-20261118**, "Sum up 18 November's
world news in one image" — $250 prize pool, entries close Friday
20 November 2026 at 07:00 WIB.

The image is a photographic newspaper front page, **THE WORLD IN ONE
DAY**, dated Wednesday, 18 November 2026. It sums up a single day of
world news — 28 stories, all from 18 November or first reported that
day — in the language of a photo-led front page: three large hero
photographs carry the biggest stories, a world map with location pins
places the rest, and a ticker along the foot carries the remaining
headlines.

## The three hero photographs

**Manila — the lead.** Trump meets Marcos at Malacañang: a state visit
and luncheon on Wednesday, before Trump flies on to Shenzhen, where
the first Trump–Xi–Putin trilateral takes place on Thursday. The
headline reads "Trump in Manila for first Quad in two years" — the
Quad leaders met in Manila the day before, and their flags run under
the lead story.

**Ukraine.** Kyiv hits the Crimean Bridge for the second day running,
while Russian missiles pound bridges in the capital.

**Weather.** Cyclone Akvan, in the Bay of Bengal, bears down on India
and is due to turn severe by Thursday.

## The map and the ticker

The world map marks where the day's stories happened, with pins kept
well apart so no two overlap. Around it, the front page covers the
rest of the day: Canada and China extend their trade deals and Xi
meets Carney on the eve of the APEC summit in Shenzhen; the UK
sanctions firms over Israeli settlements; the Baidu chief warns of an
AI bubble; India is re-elected to the ITU Council for 2027–2030;
India takes its 10th SAFF title by beating Pakistan 2–1; and the US
presses the UN over Taiwan flights — 28 stories in total.

## The program

`main.py` uses only the Python 3.13 standard library, so it runs in
the bare harness sandbox with no network and no installed packages.
It reads `entry.png` from this repository and checks it end to end —
PNG magic bytes, every chunk framed correctly with a matching CRC, a
single IHDR first and an IEND last with nothing after it, 1024×1024
pixels, 8-bit RGB or RGBA, at most 1 MiB, and the exact sha256 of the
submitted image — then copies it byte for byte to the output
directory, re-reads the copy, and compares it with the input. The
printed digest therefore proves the run emitted exactly the shipped
bytes.

Run it:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

With `MAKEFUN_OUTPUT_DIR` unset it writes to `/output`, the grader's
directory. Two runs into different directories give byte-identical
output: sha256
`02ef0be82e86b96b98e526e33877d75a6a32a394d6ab431806daa8e8fdd57de0`.

## Contents

- `entry.png` — the front page itself, a 1024×1024 PNG of 368,910 bytes
- `main.py` — the validating copy program
- `README.md` — this description
- `LICENSE` — MIT License
- `.makefun/owner.json` — claim file with the entrant's Solana wallet
