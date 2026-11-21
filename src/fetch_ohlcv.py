"""Fetch closed UTC daily Binance spot klines (candidate data source).

Example:
  python -m src.fetch_ohlcv --symbol BTCUSDT --start 2023-01-01 --end 2023-01-10 --output data/raw/BTCUSDT.csv

--end is EXCLUSIVE. API availability and jurisdiction restrictions apply.
"""
import argparse
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import time
import requests
import pandas as pd

API = "https://api.binance.com/api/v3/klines"
DAY_MS = 86_400_000
COLUMNS = ["open_time_ms", "open", "high", "low", "close", "volume_base",
           "close_time_ms", "volume_quote", "trades", "taker_base",
           "taker_quote", "ignore"]


def utc_ms(date_string):
    return int(datetime.strptime(date_string, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)


def fetch_daily(symbol, start, end, session=None):
    """Return complete daily bars in [start, end), with strict continuity checks."""
    symbol = symbol.upper()
    if symbol not in {"BTCUSDT", "ETHUSDT"}:
        raise ValueError("Only BTCUSDT and ETHUSDT are enabled in the initial study.")
    start_ms, end_ms = utc_ms(start), utc_ms(end)
    now_day_ms = int(datetime.now(timezone.utc).timestamp() * 1000) // DAY_MS * DAY_MS
    if not (start_ms < end_ms <= now_day_ms):
        raise ValueError("Require start < end and end <= current UTC day's start; end is exclusive.")
    http = session or requests.Session()
    rows = []
    cursor = start_ms
    while cursor < end_ms:
        params = {"symbol": symbol, "interval": "1d", "startTime": cursor,
                  "endTime": end_ms - 1, "limit": 1000}
        response = http.get(API, params=params, timeout=30)
        response.raise_for_status()
        batch = response.json()
        if not isinstance(batch, list):
            raise ValueError(f"Unexpected API response: {batch}")
        if not batch:
            break
        rows.extend(batch)
        next_cursor = int(batch[-1][0]) + DAY_MS
        if next_cursor <= cursor:
            raise ValueError("API pagination failed to advance.")
        cursor = next_cursor
        time.sleep(0.2)
    if not rows:
        raise ValueError("No bars returned; check symbol, dates and API availability.")
    frame = pd.DataFrame(rows, columns=COLUMNS)
    frame["open_time_ms"] = pd.to_numeric(frame["open_time_ms"], errors="raise").astype("int64")
    frame["close_time_ms"] = pd.to_numeric(frame["close_time_ms"], errors="raise").astype("int64")
    for col in ["open", "high", "low", "close", "volume_base", "volume_quote"]:
        frame[col] = pd.to_numeric(frame[col], errors="raise")
    frame["trades"] = pd.to_numeric(frame["trades"], errors="raise").astype("int64")
    frame = frame[(frame.open_time_ms >= start_ms) & (frame.open_time_ms < end_ms)]
    frame = frame.sort_values("open_time_ms").reset_index(drop=True)
    expected = list(range(start_ms, end_ms, DAY_MS))
    if frame.open_time_ms.tolist() != expected:
        raise ValueError("Missing, duplicate, or non-daily bars; inspect source before proceeding.")
    if ((frame[["open", "high", "low", "close"]] <= 0).any().any()
        or (frame[["volume_base", "volume_quote"]] < 0).any().any()
        or (frame["low"] > frame[["open", "close"]].min(axis=1)).any()
        or (frame["high"] < frame[["open", "close"]].max(axis=1)).any()
        or (frame["high"] < frame["low"]).any()
        or (frame["close_time_ms"] != frame["open_time_ms"] + DAY_MS - 1).any()):
        raise ValueError("OHLCV validation failed.")
    frame.insert(0, "symbol", symbol)
    frame["open_time"] = pd.to_datetime(frame.open_time_ms, unit="ms", utc=True)
    frame["close_time"] = pd.to_datetime(frame.close_time_ms, unit="ms", utc=True)
    return frame[["symbol", "open_time", "close_time", "open", "high", "low", "close",
                  "volume_base", "volume_quote", "trades"]]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True, choices=["BTCUSDT", "ETHUSDT"])
    parser.add_argument("--start", required=True, help="Inclusive UTC YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="Exclusive UTC YYYY-MM-DD")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    frame = fetch_daily(args.symbol, args.start, args.end)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    metadata = {"source": API, "market_type": "spot", "symbol": args.symbol,
                "interval": "1d", "timezone": "UTC", "start_inclusive": args.start,
                "end_exclusive": args.end, "rows": len(frame), "sha256": digest,
                "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                "volume_base_unit": args.symbol.replace("USDT", ""),
                "volume_quote_unit": "USDT"}
    output.with_suffix(".provenance.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Saved {len(frame)} rows to {output}; sha256={digest}")


if __name__ == "__main__":
    main()
