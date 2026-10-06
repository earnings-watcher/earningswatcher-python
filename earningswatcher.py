"""earningswatcher — options-implied earnings moves from EarningsWatcher's free API.

    from earningswatcher import implied_move, symbols
    jpm = implied_move("JPM")
    jpm["implied_live_pct"], jpm["next_date"], jpm["implied_history"]

Data: https://earnings-watcher.com · free to use with attribution and a link to the source URL.
Education only — not investment advice.
"""
from __future__ import annotations

import json
import ssl
import urllib.request

try:  # python.org builds on macOS ship without system CA bundles; certifi fixes that when present
    import certifi
    _CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:  # pragma: no cover
    _CTX = ssl.create_default_context()

__version__ = "0.1.0"
BASE = "https://earnings-watcher.com/api/implied"
_UA = f"earningswatcher-python/{__version__} (+https://earnings-watcher.com)"


def _get(url: str, timeout: float = 15.0) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": _UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout, context=_CTX) as r:  # noqa: S310 — fixed https host
        return json.load(r)


def symbols() -> list[str]:
    """Every symbol the free API covers."""
    idx = _get(f"{BASE}/index.json")
    syms = idx.get("symbols") or []
    return [s["symbol"] if isinstance(s, dict) else s for s in syms]


def implied_move(symbol: str) -> dict:
    """One stock: live implied move (when a report is upcoming), next report date and session,
    10-year average move, and `implied_history` — per past report the implied move, close move and
    peak move. Keys and units are documented at the `docs` URL inside the response."""
    return _get(f"{BASE}/{symbol.upper().strip()}.json")


def history(symbol: str) -> list[dict]:
    """Past reports for one stock: [{date, implied_pct, close_pct, peak_pct}, ...], oldest first."""
    return list(implied_move(symbol).get("implied_history") or [])


def beat_rate(symbol: str) -> float | None:
    """Share of past reports where the peak intraday move exceeded the implied move (0–1)."""
    rows = [h for h in history(symbol) if h.get("implied_pct") is not None and h.get("peak_pct") is not None]
    if not rows:
        return None
    return sum(abs(h["peak_pct"]) >= h["implied_pct"] for h in rows) / len(rows)
