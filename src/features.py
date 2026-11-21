"""Deterministic daily price/volume feature engineering."""
import numpy as np
import pandas as pd


def make_features(frame):
    required = {"symbol", "open_time", "close", "volume_quote"}
    if not required.issubset(frame.columns):
        raise ValueError(f"Missing columns: {sorted(required - set(frame.columns))}")
    df = frame.copy()
    df["open_time"] = pd.to_datetime(df["open_time"], utc=True)
    df = df.sort_values(["symbol", "open_time"]).reset_index(drop=True)
    if df.duplicated(["symbol", "open_time"]).any():
        raise ValueError("Duplicate symbol/date observations.")
    if (df["close"] <= 0).any() or (df["volume_quote"] < 0).any():
        raise ValueError("Prices must be positive and quote volume nonnegative.")
    group = df.groupby("symbol", sort=False)
    df["log_return"] = group["close"].transform(lambda x: np.log(x).diff())
    df["abs_return"] = df["log_return"].abs()
    df["squared_return"] = df["log_return"] ** 2
    df["log_volume_quote"] = np.log1p(df["volume_quote"])
    df["log_volume_change"] = df.groupby("symbol")["log_volume_quote"].diff()
    df["realized_var_7d"] = df.groupby("symbol")["squared_return"].transform(
        lambda x: x.rolling(7, min_periods=7).sum())
    return df
