# The World Today — Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/nurdiyanto-87/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/nurdiyanto-87/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

An entry for the [make.fun bounty "Sum up 20 November's world news in one image"](https://make.fun/bounty/news-image-20261120) ($250 in USDC).

The image is a newspaper front page for Friday 20 November 2026,
drawn entirely in code with the Python standard library. `draw.py`
holds a small bitmap font, shape drawing and a hand-rolled PNG
encoder — no third-party packages anywhere.

## The six lead stories

1. **Cyclone Akvan hits Odisha** — the storm comes ashore near
   Gopalpur at noon with winds to 110 km/h, and Odisha moves
   300,000 people into shelters. (The Hindu / India
   Meteorological Department)
2. **Trump pushes the Iran decision to 2027** — the US will "see
   what happens" after 1 January, putting off any decision on war.
   (Reuters)
3. **Court finds Myanmar committed genocide** — the International
   Court of Justice rules Myanmar guilty of genocide against the
   Rohingya, the first time any state has been held responsible.
   (CNN / BBC)
4. **Haiti police kill 34 in gang sweep** — officers and a private
   task force fight gangs in the Martissant corridor of
   Port-au-Prince. (Haitian police, reported 20 November)
5. **Sparks near a record $750m sale** — the LA Sparks are close
   to a record price for a WNBA team. (Sportico)
6. **Seoul court overturns ex-PM Han's sentence** — South Korea's
   top court quashes Han Duck-soo's 15-year term and orders a
   retrial. (Reuters)

The footer carries the day's other headlines: the US–Venezuela
military pact, Denmark approving a Greenland security deal,
Voyager 1's data flow stopping, and Pew's projection that Muslims
will be the world's largest faith by 2035.

## Running it

```sh
python3 draw.py        # redraw entry.png (1024x1024, pure stdlib)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` copies the bundled `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), byte for byte,
every run.
