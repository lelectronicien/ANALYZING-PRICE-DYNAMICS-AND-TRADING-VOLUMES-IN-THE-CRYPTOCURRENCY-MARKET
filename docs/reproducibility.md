# Reproducibility guide (daily UTC)

## Environment

Python 3.10+ recommended. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
```

Versions are bounded in `requirements.txt`, but not pinned. Before final results, generate a fully pinned lockfile and record Python/OS versions.

## Candidate data retrieval

```bash
python -m src.fetch_ohlcv --symbol BTCUSDT --start 2023-01-01 --end 2024-01-01 --output data/raw/BTCUSDT.csv
python -m src.fetch_ohlcv --symbol ETHUSDT --start 2023-01-01 --end 2024-01-01 --output data/raw/ETHUSDT.csv
```

Dates above are **illustrative**, not the approved study window. The end date is exclusive. Requests may fail because of API limits, restrictions, outages, or unavailable history. Do not circumvent access restrictions. Fetching is intentionally manual and makes no claim that data have already been collected.

The script rejects incomplete current-day bars and gaps; failures should be logged and investigated, not silently repaired. Raw files and provenance sidecars are saved locally under gitignored `data/raw/`. Keep provenance for the thesis even if raw data cannot be redistributed.

## Initial exploratory regressions

```bash
python -m src.analyze --input data/raw/BTCUSDT.csv --output results/btc
python -m src.analyze --input data/raw/ETHUSDT.csv --output results/eth
```

These simple HAC regressions estimate contemporaneous associations, not causality. Later versions should include controls, stationarity checks and additional diagnostics.

## Initial forecasting comparison

```bash
python -m src.forecast --input data/raw/BTCUSDT.csv --output results/btc_forecast.csv
python -m src.forecast --input data/raw/ETHUSDT.csv --output results/eth_forecast.csv
```

The baseline uses an 80/20 chronological split. Features at t predict absolute returns at t+1. No random split or contemporaneous target leakage. This is a single holdout baseline; rolling-origin evaluation, uncertainty estimates and volatility-model comparisons remain future work.

## Before publication

- Approve data provider, venue, symbol, period, license and timezone.
- Independently cross-check a subset of raw bars.
- Pin dependencies and record execution environment.
- Run tests and record their output.
- Inspect plots, missingness, residuals, model assumptions and sensitivity.
- Verify all results independently; never present unexecuted scripts as empirical findings.

## Confirmed 2018–2025 full-window commands

The earlier 2023–2024 examples are short smoke-test windows, **not** the thesis sample. For the full study period:

```bash
python -m src.fetch_ohlcv --symbol BTCUSDT --start 2018-01-01 --end 2026-01-01 --output data/raw/BTCUSDT.csv
python -m src.fetch_ohlcv --symbol ETHUSDT --start 2018-01-01 --end 2026-01-01 --output data/raw/ETHUSDT.csv
python -m src.coverage --input data/raw/BTCUSDT.csv --symbol BTCUSDT --output results/coverage_btc.json
python -m src.coverage --input data/raw/ETHUSDT.csv --symbol ETHUSDT --output results/coverage_eth.json
python -m src.walk_forward --input data/raw/BTCUSDT.csv --output-prefix results/btc_walk_forward --min-train 365 --step 1
python -m src.walk_forward --input data/raw/ETHUSDT.csv --output-prefix results/eth_walk_forward --min-train 365 --step 1
python -m src.robustness --input data/raw/BTCUSDT.csv --output results/btc_robustness.csv
python -m src.robustness --input data/raw/ETHUSDT.csv --output results/eth_robustness.csv
```

**Important:** The coverage audit should pass before running inference. Data-source permissions, full historical availability, independent cross-checks and empirical outputs remain unverified. Expanding-window forecasting refits at each origin and may take substantial computation time.
