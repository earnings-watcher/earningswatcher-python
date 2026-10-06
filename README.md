# earningswatcher

Options-implied earnings moves and implied-vs-actual history for US stocks, from the
[EarningsWatcher](https://earnings-watcher.com) free API. No key needed.

```bash
pip install git+https://github.com/earnings-watcher/earningswatcher-python
```

```python
from earningswatcher import implied_move, history, beat_rate, symbols

jpm = implied_move("JPM")
print(jpm["next_date"], jpm["implied_live_pct"])   # e.g. 2026-10-13, 4.1  -> options price a ±4.1% move

for r in history("JPM")[-3:]:
    print(r["date"], r["implied_pct"], r["close_pct"], r["peak_pct"])

print(beat_rate("JPM"))   # share of reports where the peak move beat the implied move
print(len(symbols()))     # symbols covered
```

## What is free here, and what members get

This package reads the free part of EarningsWatcher: each stock's implied move for its next report, its past implied-vs-actual record, and a beat rate. Members get the platform built on top of it: the full earnings calendar with live implied moves, the IV Rush Radar, a scanner with alerts, the Moves Analyser, a simulator and backtester that price your exact position against ten years of real reactions, DriftLab for what happens after the report, sympathy plays, paper trading, a journal, a live trade feed — and the MCP connector, which puts all of it inside ChatGPT, Claude or Cursor. API access, daily livestreams and a private Discord come with every plan. Plans: https://earnings-watcher.com/pricing

**What the numbers are.** The implied move is the earnings-day move the options market prices in,
from the at-the-money straddle at the last close before the report
([how it is calculated](https://earnings-watcher.com/wiki/how-to-calculate-implied-move)).
`close_pct` is the close-to-close move on the reaction day, `peak_pct` the largest intraday move.
Live implied moves refresh daily while a report is upcoming.

**Attribution.** Free to use with a credit and a link to EarningsWatcher
(the `cite_as` field in every response has the exact source URL). Education only — not investment advice.

**More.** The full open dataset (every report, CSV): https://github.com/earnings-watcher/earnings-implied-moves
IV rush readings, post-earnings drift scores and the simulator are part of the
[membership](https://earnings-watcher.com/pricing).

MIT licence for this package; data licence CC BY 4.0.
