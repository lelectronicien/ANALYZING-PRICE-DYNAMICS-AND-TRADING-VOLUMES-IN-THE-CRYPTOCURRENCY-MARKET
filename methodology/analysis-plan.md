# Empirical analysis plan

**Status:** Planned, not executed.

## Phase A — Data acquisition and validation

1. Select documented spot-market OHLCV data for BTC and ETH covering **2018-01-01 to 2025-12-31 inclusive** (exclusive endpoint **2026-01-01**).
2. Define exchange, quote currency, UTC daily boundaries, study period and licensing.
3. Run `python -m src.coverage` for each asset: require 2,922 unique UTC-midnight daily timestamps, continuity, positive prices, nonnegative volumes, and consistent units.
4. Log missing bars and exceptional observations; avoid silently forward-filling returns or volumes.
5. Produce a data dictionary and a provenance record.

**Deliverable:** reproducible ingestion/cleaning scripts and a data-quality report.

## Phase B — Exploratory analysis

1. Compute log returns, absolute/squared returns, log volume and log-volume changes.
2. Report summary statistics and price/volume/volatility plots.
3. Inspect distributional features, autocorrelation, volatility clustering and structural breaks.
4. Assess stationarity with complementary diagnostics and choose stationary specifications.

**Deliverable:** EDA figures, descriptive tables and variable definitions.

## Phase C — Hypothesis testing

| Hypothesis | Candidate approach | Primary interpretation |
| --- | --- | --- |
| H1 | HAC regression of absolute returns on volume and controls | Contemporaneous association |
| H2 | HAC regression and conditional-volatility specifications | Volume–volatility association |
| H3 | Chronological out-of-sample benchmark vs volume-augmented forecasts | Incremental predictive value |
| H4 (exploratory) | Regime interactions/subsample sensitivity | Heterogeneity, not causal regime effects |

Preselect the main specification and outcomes before reviewing results where practical.

## Phase D — Predictive validation

- Split data chronologically; never random-shuffle time-series observations.
- Fit transformations and model parameters on training data only.
- Use expanding-window one-day-ahead forecasts from `src/walk_forward.py`; compare same-date benchmark and volume-augmented predictions. Add rolling fixed-width windows as a future sensitivity check.
- Compare against a simple persistence or historical volatility benchmark.
- Report errors, uncertainty and negative findings, not just significant results.

## Phase E — Robustness and reporting

- Check alternative volumes, return/volatility definitions and sample windows.
- Diagnose residual dependence, instability and influential observations.
- Distinguish statistical significance from economic importance.
- Publish tables/figures with scripts, seeds and environment specifications.

## Suggested directory usage

- `data/`: dictionary, provenance, allowable derived data
- `src/`: ingestion, validation, features, models, evaluation
- `experiments/`: specifications, experiment notes
- `results/`: tables, diagnostics, out-of-sample metrics
- `figures/`: plots for the thesis

No empirical findings are claimed in this plan.

## Implemented exploratory robustness

Run `src/robustness.py` for two volatility proxies (absolute and squared returns), two volume measures (log turnover and its change), and full/2018–2021/2022–2025 subsamples. These are exploratory, multiple-comparison p-values are unadjusted, and conclusions must be independently verified.
