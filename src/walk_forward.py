"""Expanding-window one-step-ahead absolute-return forecasts.

At the end of day t, use known day-t absolute return and volume to predict
day t+1 absolute return. Models refit at every forecast origin.
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from src.features import make_features


def walk_forward(frame, min_train=365, step=1):
    if min_train < 30 or step < 1:
        raise ValueError("min_train >= 30 and step >= 1 required")
    df = make_features(frame)
    predictions = []
    for symbol, part in df.groupby("symbol"):
        part = part.sort_values("open_time").copy()
        part["target"] = part["abs_return"].shift(-1)
        part = part.dropna(subset=["target", "abs_return", "log_volume_quote"]).reset_index(drop=True)
        if len(part) <= min_train:
            raise ValueError(f"{symbol}: insufficient observations")
        for i in range(min_train, len(part), step):
            train = part.iloc[:i]
            origin = part.iloc[i]
            # At forecast origin t, outcome for training row t-1 (day t) is known.
            # The last training row is t-1, so no target beyond t enters estimation.
            for name, features in [
                ("ar_abs_return", ["abs_return"]),
                ("ar_plus_volume", ["abs_return", "log_volume_quote"]),
            ]:
                X = sm.add_constant(train[features], has_constant="add")
                fitted = sm.OLS(train["target"], X).fit()
                new_x = sm.add_constant(part.iloc[[i]][features], has_constant="add")
                predicted = max(0.0, float(fitted.predict(new_x).iloc[0]))
                predictions.append({"symbol": symbol, "origin_date": origin["open_time"].isoformat(),
                                    "target_date": (origin["open_time"] + pd.Timedelta(days=1)).isoformat(),
                                    "model": name, "prediction": predicted,
                                    "actual": float(origin["target"]), "train_rows": i})
    return pd.DataFrame(predictions)


def score_forecasts(predictions):
    if predictions.empty:
        raise ValueError("No forecasts")
    records = []
    for (symbol, model), g in predictions.groupby(["symbol", "model"]):
        errors = g["prediction"] - g["actual"]
        records.append({"symbol": symbol, "model": model, "n_forecasts": len(g),
                        "mae": float(errors.abs().mean()),
                        "rmse": float(np.sqrt((errors**2).mean()))})
    return pd.DataFrame(records)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output-prefix", required=True)
    p.add_argument("--min-train", type=int, default=365)
    p.add_argument("--step", type=int, default=1)
    args = p.parse_args()
    forecasts = walk_forward(pd.read_csv(args.input), args.min_train, args.step)
    prefix = Path(args.output_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    forecasts.to_csv(str(prefix) + "_predictions.csv", index=False)
    scores = score_forecasts(forecasts)
    scores.to_csv(str(prefix) + "_scores.csv", index=False)
    print(scores.to_string(index=False))


if __name__ == "__main__":
    main()
