# One Day of World News — 18 November 2026

A make.fun entry for **news-image-20261118**, "Sum up 18 November's
world news in one image" — $250 prize pool, entries close Friday
20 November 2026 at 07:00 WIB.

The image is a newspaper front page called **THE WORLD IN ONE DAY**,
dated Wednesday, 18 November 2026. Everything on the page is news from
that single day: stories that happened on 18 November, or were first
reported then.

## What the front page covers

**Manila — the lead story.** Trump meets Marcos: a state visit and
luncheon at Malacañang on Wednesday, then Trump flies on to Shenzhen,
where the first Trump–Xi–Putin trilateral takes place on Thursday.
The flags of the Quad — USA, Japan, India, Australia — run under the
lead; the Quad leaders met in Manila the day before.

**Ukraine.** Kyiv hits the Crimean Bridge for the second day running,
while Russian missiles pound bridges in the capital.

**Trade, ahead of APEC.** Canada and China extend their trade deals,
and Xi meets Carney on the eve of the Shenzhen summit.

**Weather.** Cyclone Akvan, in the Bay of Bengal, bears down on India
and is due to turn severe by Thursday.

**The ticker along the bottom** carries the rest of the day: the UK
sanctions firms over Israeli settlements, the Baidu chief warns of an
AI bubble, India is re-elected to the ITU Council for 2027–2030,
India takes its 10th SAFF title by beating Pakistan 2–1, and the US
presses the UN over Taiwan flights.

## The program

`main.py` needs nothing but Python 3.13's standard library. It reads
`entry.png` from this repository, checks it thoroughly — PNG signature,
well-formed chunks with correct CRCs, a closing IEND, 1024×1024 pixels,
8-bit true colour, at most 1 MiB, and the exact sha256 of the shipped
image — and copies it to the output directory. It re-reads the copy and
compares it with the input, then prints the digest, so any run can be
shown to be byte-identical to the image in the repository.

Run it:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Leave `MAKEFUN_OUTPUT_DIR` unset and it writes to `/output`, the
grader's directory. Two runs into different directories give identical
output: sha256
`e781f22b8623980e557d65a1ee2780f9161f8d30f28b2f525eb72ac93224de70`.

## Contents

- `entry.png` — the front page itself, a 1024×1024 PNG of 184,437 bytes
- `main.py` — the validating copy program
- `README.md` — this description
- `LICENSE` — MIT License
- `.makefun/owner.json` — claim file with the entrant's Solana wallet
