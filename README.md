# The World Today — Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/nurdiyanto-87/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/nurdiyanto-87/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Built for the [make.fun bounty "Sum up 20 November's world news in one image"](https://make.fun/bounty/news-image-20261120) ($250 in USDC).

A one-page newspaper front page summing up the world news of
Friday 20 November 2026, drawn entirely in code with the Python
standard library (see `draw.py`: a small bitmap font, shape drawing,
and a hand-rolled PNG encoder — no third-party packages).

Six stories lead the page:

1. **Cyclone Akvan hits Odisha** — landfall near Gopalpur at noon,
   winds to 110 km/h; Odisha moves 300,000 people to shelters.
   (The Hindu / India Meteorological Department)
2. **Trump pushes the Iran decision to 2027** — the US will "see
   what happens" after 1 January, putting off any war decision.
   (Reuters)
3. **Court finds Myanmar committed genocide** — the ICJ rules
   Myanmar guilty of genocide against the Rohingya, a first for
   any state. (CNN / BBC)
4. **Haiti police kill 34 in gang sweep** — officers and a task
   force fight gangs in the Martissant corridor of Port-au-Prince.
   (Haitian police, reported 20 November)
5. **Sparks near a record $750m sale** — the LA Sparks are close
   to a record price for a WNBA team. (Sportico)
6. **Seoul court overturns ex-PM Han's sentence** — South Korea's
   top court quashes Han Duck-soo's 15-year term and orders a
   retrial. (Reuters)

The footer adds the day's other headlines: the US–Venezuela
military pact, Denmark's Greenland security deal, Voyager 1's data
flow stopping, and Pew's projection that Muslims will be the
world's largest faith by 2035.

## Running

```sh
python3 draw.py        # regenerate entry.png (1024x1024, pure stdlib)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` simply copies the bundled `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), deterministically.
