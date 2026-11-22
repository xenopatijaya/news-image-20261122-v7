# news-image-20261122-v7

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/xenopatijaya/news-image-20261122-v7/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/xenopatijaya/news-image-20261122-v7/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One page that sums up the world's news of Sunday 22 November 2026: 43 stories,
each dated to that Sunday at its source, across 7 regions. A giant dated
masthead, a big-numbers strip, a region tally and a UTC timeline sit over
three illustrated leads (the 186-drone night over Ukraine, COP31's final
text, and Iran's radar claim printed beside Bahrain's denial), twelve more
illustrated story cards, 28 numbered briefs with named sources, a dot-matrix
world map whose pins match the story numbers, and a DATE CHECK box naming
the other days' stories left out on purpose. The page is drawn entirely in
code (`render.py`, Python + Pillow); `main.py` copies the finished
`entry.png` to the output directory.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=fmkt9ms6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
