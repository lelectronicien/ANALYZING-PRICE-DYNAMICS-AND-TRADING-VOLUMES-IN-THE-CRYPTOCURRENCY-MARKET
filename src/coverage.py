"""Audit daily UTC OHLCV completeness for the fixed thesis window.

Run: python -m src.coverage --input data/raw/BTCUSDT.csv --symbol BTCUSDT --output results/coverage_btc.json
"""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd

START = "2018-01-01"
END_EXCLUSIVE = "2026-01-01"


def audit_coverage(frame, symbol, start=START, end=END_EXCLUSIVE):
    """Return a JSON-serializable report. Does not impute missing candles."""
    if not start < end:
        raise ValueError("start must precede exclusive end")
    required = {"symbol", "open_time", "open", "high", "low", "close", "volume_base", "volume_quote"}
    missing_cols = required - set(frame.columns)
    if missing_cols:
        raise ValueError(f"Missing columns: {sorted(missing_cols)}")
    df = frame.copy()
    df["open_time"] = pd.to_datetime(df["open_time"], utc=True, errors="raise")
    df = df[df["symbol"] == symbol].copy()
    if df.empty:
        raise ValueError(f"No observations for {symbol}")
    dates = df["open_time"]
    expected = pd.date_range(start, end, freq="D", tz="UTC", inclusive="left")
    in_window = (dates >= expected[0]) & (dates < pd.Timestamp(end, tz="UTC"))
    df = df.loc[in_window].copy()
    dates = df["open_time"]
    counts = dates.value_counts()
    duplicates = sorted(x.isoformat() for x in counts[counts > 1].index)
    present = pd.DatetimeIndex(dates.unique())
    missing = expected.difference(present)
    non_midnight = dates[dates != dates.dt.normalize()]
    numeric = ["open", "high", "low", "close", "volume_base", "volume_quote"]
    for c in numeric:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    bad_numeric = df[numeric].isna().any(axis=1)
    bad_ohlc = ((df[["open", "high", "low", "close"]] <= 0).any(axis=1)
                | (df["low"] > df[["open", "close"]].min(axis=1))
                | (df["high"] < df[["open", "close"]].max(axis=1))
                | (df["high"] < df["low"]))
    bad_volume = (df[["volume_base", "volume_quote"]] < 0).any(axis=1)
    zero_volume = (df[["volume_base", "volume_quote"]] == 0).any(axis=1)
    complete = (len(missing) == 0 and not duplicates and len(non_midnight) == 0
                and not (bad_numeric | bad_ohlc | bad_volume).any())
    return {"symbol": symbol, "start_inclusive": start, "end_exclusive": end,
            "expected_days": len(expected), "observed_rows": len(df),
            "unique_days": len(present), "missing_days": len(missing),
            "missing_dates": [x.strftime("%Y-%m-%d") for x in missing],
            "duplicate_dates": duplicates, "non_midnight_rows": int(len(non_midnight)),
            "invalid_numeric_rows": int(bad_numeric.sum()),
            "invalid_ohlc_rows": int(bad_ohlc.sum()),
            "invalid_volume_rows": int(bad_volume.sum()),
            "zero_volume_rows": int(zero_volume.sum()),
            "complete": bool(complete)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--symbol", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--start", default=START)
    p.add_argument("--end", default=END_EXCLUSIVE)
    args = p.parse_args()
    report = audit_coverage(pd.read_csv(args.input), args.symbol, args.start, args.end)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "missing_dates"}, indent=2))
    if not report["complete"]:
        raise SystemExit("Coverage audit failed; inspect the report and source data.")


if __name__ == "__main__":
    main()
