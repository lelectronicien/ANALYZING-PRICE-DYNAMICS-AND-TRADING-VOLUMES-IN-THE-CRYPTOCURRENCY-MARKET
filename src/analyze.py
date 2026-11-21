"""Descriptive analysis and baseline volume-volatility regressions.

Example:
  python -m src.analyze --input data/raw/BTCUSDT.csv --output results/btc
"""
import argparse
from pathlib import Path
import pandas as pd
import statsmodels.api as sm
from src.features import make_features


def run_analysis(data, output):
    df = make_features(data)
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    df.describe(include="all").to_csv(out / "descriptives.csv")
    for symbol, part in df.groupby("symbol"):
        part = part.dropna(subset=["abs_return", "log_volume_quote"]).copy()
        if len(part) < 30:
            raise ValueError("Need at least 30 usable observations per symbol.")
        # Contemporaneous association only, NOT a causal or forecasting model.
        X = sm.add_constant(part[["log_volume_quote"]])
        model = sm.OLS(part["abs_return"], X).fit(cov_type="HAC", cov_kwds={"maxlags": 7})
        (out / f"{symbol}_hac_summary.txt").write_text(model.summary().as_text())
        part.to_csv(out / f"{symbol}_features.csv", index=False)
    return df


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    run_analysis(pd.read_csv(args.input), args.output)


if __name__ == "__main__":
    main()
