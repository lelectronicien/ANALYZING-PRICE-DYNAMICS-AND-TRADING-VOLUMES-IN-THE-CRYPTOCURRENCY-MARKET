"""Chronological one-step-ahead volatility-proxy forecast benchmark.

Forecast target: next day's absolute log return. At date t, only data
available through t are used. This is a *baseline*, not a final thesis model.
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from src.features import make_features


def compare_forecasts(frame, train_fraction=0.8):
    if not 0.5 <= train_fraction < 1:
        raise ValueError("train_fraction must be in [0.5, 1).")
    df = make_features(frame)
    rows = []
    for symbol, part in df.groupby("symbol"):
        part = part.sort_values("open_time").copy()
        part["target_next_abs_return"] = part["abs_return"].shift(-1)
        part["lag_abs_return"] = part["abs_return"]
        part["lag_volume"] = part["log_volume_quote"]
        part = part.dropna(subset=["target_next_abs_return", "lag_abs_return", "lag_volume"])
        if len(part) < 100:
            raise ValueError(f"{symbol}: need at least 100 usable observations.")
        cut = int(len(part) * train_fraction)
        train, test = part.iloc[:cut], part.iloc[cut:]
        target = "target_next_abs_return"
        for label, features in [("autoregressive", ["lag_abs_return"]),
                                ("volume_augmented", ["lag_abs_return", "lag_volume"])]:
            Xtrain = sm.add_constant(train[features], has_constant="add")
            Xtest = sm.add_constant(test[features], has_constant="add")
            model = sm.OLS(train[target], Xtrain).fit()
            pred = np.maximum(model.predict(Xtest).to_numpy(), 0)
            truth = test[target].to_numpy()
            rows.append({"symbol": symbol, "model": label, "n_train": len(train),
                         "n_test": len(test), "mae": float(np.mean(np.abs(truth-pred))),
                         "rmse": float(np.sqrt(np.mean((truth-pred)**2)))})
    return pd.DataFrame(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    scores = compare_forecasts(pd.read_csv(args.input))
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    scores.to_csv(path, index=False)
    print(scores.to_string(index=False))


if __name__ == "__main__":
    main()
