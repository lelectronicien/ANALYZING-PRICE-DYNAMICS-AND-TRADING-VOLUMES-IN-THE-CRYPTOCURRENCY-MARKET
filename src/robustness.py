"""Exploratory robustness grid for contemporaneous volume associations.

Comparisons use HAC inference. They are not causal tests, and unadjusted
p-values from multiple exploratory models should not be read as confirmatory.
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from src.features import make_features


def robustness_grid(frame):
    df = make_features(frame)
    results = []
    for symbol, part in df.groupby("symbol"):
        part = part.sort_values("open_time").copy()
        part["year"] = part["open_time"].dt.year
        for period, subset in [
            ("full", part),
            ("2018-2021", part[part["year"].between(2018, 2021)]),
            ("2022-2025", part[part["year"].between(2022, 2025)]),
        ]:
            for outcome in ["abs_return", "squared_return"]:
                for volume in ["log_volume_quote", "log_volume_change"]:
                    work = subset[[outcome, volume]].replace([np.inf, -np.inf], np.nan).dropna()
                    if len(work) < 60 or work[volume].nunique() < 2:
                        continue
                    X = sm.add_constant(work[[volume]], has_constant="add")
                    fitted = sm.OLS(work[outcome], X).fit(cov_type="HAC", cov_kwds={"maxlags": 7})
                    results.append({"symbol": symbol, "period": period, "outcome": outcome,
                                    "volume_variable": volume, "n": len(work),
                                    "coefficient": float(fitted.params[volume]),
                                    "std_error_hac": float(fitted.bse[volume]),
                                    "p_value_unadjusted": float(fitted.pvalues[volume]),
                                    "r_squared": float(fitted.rsquared)})
    return pd.DataFrame(results)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    result = robustness_grid(pd.read_csv(args.input))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False)
    print(f"Saved {len(result)} exploratory specifications to {output}")


if __name__ == "__main__":
    main()
