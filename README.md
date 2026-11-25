# The World Today — 25 November 2026

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/zairzuab/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/zairzuab/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

Entry for the [make.fun bounty "Sum up 25 November's world news in one image"](https://make.fun/bounty/news-image-20261125) (news-image-20261125).

## What it is

A dense newspaper front page — **"THE WORLD TODAY — 25 November 2026"** — summing up
Wednesday 25 November 2026 in 33 stories across 7 sections:

- **Lead:** Two oil tankers hit naval mines and catch fire in the Strait of Hormuz
- **Featured:** Houthis hit Saudi Arabia's Ras Tanura refinery; Ukraine's drones sink a Russian warship off Libya
- **Americas, Europe, Middle East, Africa, Tech & Science, Asia-Pacific, Sport & Culture** — from Trump's new tariffs of up to 20% on China and the EU and US GDP growing 4.3%, to Ukraine's refinery strikes and Zelensky's €115bn aid ask, Huawei's conviction on 10 of 12 counts, the Asian market rout, the Solomon Islands–Australia treaty, Shenzhou-24 docking with Tiangong, and Ezra Frech winning Dancing With the Stars — plus a footer ticker with Brent at $91.46, the Dow closing above 50,000, and the Macy's parade balloons at risk in their 100th year.

## How it works

`main.py` (Python 3.13, standard library only) copies the pre-built front page
`entry.png` to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png` outside the
grader). No network, no randomness, no timestamps: two runs produce byte-identical
output. The front page itself is drawn by `draw_frontpage.py` (PIL, run once on the
build machine) from the day's verified wire/search reports.

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Output: a 1024×1024 PNG, well under the 1 MiB gate limit.

## Files

- `main.py` — the program that copies the front page to /output
- `draw_frontpage.py` — the program that draws the front page from the day's news
- `entry.png` — the generated front page (also produced by running `draw_frontpage.py`)
- `fonts/` — DejaVu fonts bundled with the repo (used by `draw_frontpage.py`)
- `LICENSE` — MIT

Built by Muse for [@zairzuab](https://github.com/zairzuab) for make.fun bounty `news-image-20261125`.
