# Research methodology: cryptocurrency price dynamics and trading volumes

**Status:** Initial research design (provisional; subject to supervisor review and data feasibility).

## 1. Research aim

Examine the contemporaneous and predictive relationships between cryptocurrency trading activity, price returns, and volatility using transparent, reproducible quantitative methods.

## 2. Research questions

- **RQ1:** What is the contemporaneous association between trading volume and cryptocurrency returns (including absolute returns)?
- **RQ2:** How is trading volume related to realized and conditional price volatility?
- **RQ3:** Does lagged volume contain incremental information for forecasting returns or volatility beyond their own histories?
- **RQ4 (extension):** Do the relationships differ across cryptocurrencies and market regimes?

## 3. Hypotheses

- **H1:** Trading volume is positively associated with the magnitude of returns (absolute returns), controlling for other factors.
- **H2:** Higher trading volume is associated with higher contemporaneous volatility.
- **H3:** Lagged volume improves out-of-sample forecasts of volatility relative to a benchmark without volume.
- **H4 (exploratory):** Volume–price relationships vary between high- and low-volatility regimes.

Directional return predictability is a separate, more demanding question and should not be assumed from H1–H3.

## 4. Proposed scope and sampling

- **Assets (provisional):** Bitcoin (BTC) and Ethereum (ETH), with other liquid assets considered for robustness.
- **Unit of observation:** Daily observations initially; intraday observations as an optional extension.
- **Study window (confirmed):** 2018-01-01 through 2025-12-31 inclusive (2,922 UTC daily observations expected per continuously traded asset). Verify coverage and document gaps before analysis.
- **Trading venue:** Use a documented exchange and consistent spot trading pairs (e.g., BTC/USDT, ETH/USDT), or a clearly defined aggregate provider; avoid mixing unlike volume definitions.
- **Time convention:** Daily UTC bars with explicit open/close boundaries.
- **Sampling:** Consecutive trading days, with transparent treatment of missing data, zero-volume records, delistings and exchange outages.

## 5. Variables and operational definitions

Let \(P_t\) denote the daily closing price and \(V_t\) the traded volume in a clearly stated unit.

- **Log return:** \(r_t = \ln(P_t/P_{t-1})\).
- **Absolute return:** \(|r_t|\), a simple volatility proxy.
- **Squared return:** \(r_t^2\), an alternative volatility proxy.
- **Log volume:** \(v_t = \ln(1+V_t)\), using \(1+V_t\) to accommodate zero observations.
- **Volume change:** \(\Delta v_t = v_t-v_{t-1}\).
- **Rolling realized proxy:** rolling sum of squared daily returns, labeled clearly as a daily-frequency proxy, not high-frequency realized volatility.
- **Optional controls:** lagged returns, lagged volatility, day-of-week indicators, market-wide returns, and market regime indicators.

Volume in base units, quote units, and USD-equivalent turnover are not interchangeable. The chosen measure and any conversions must be documented.

## 6. Empirical strategy

### 6.1 Descriptive analysis

Plot prices, returns, volume and rolling volatility. Report summary statistics, skewness, kurtosis, missingness, outliers, and correlations. Inspect distributional tails and stationarity using complementary tests (e.g., ADF and KPSS), noting their limitations.

### 6.2 Contemporaneous relationships

Estimate associations such as:

\[
|r_t| = \alpha + \beta v_t + \gamma' X_t + \epsilon_t.
\]

Use heteroskedasticity/autocorrelation-robust inference (e.g., Newey–West HAC) where appropriate. Compare alternative volume transformations and volatility measures. Interpret \(\beta\) as an association, not a causal effect.

### 6.3 Lead–lag relationships

Examine cross-correlations, distributed-lag models and VAR specifications for stationary series. Lag selection must be justified (information criteria and residual diagnostics). Granger-causality tests assess incremental predictive content under a model, **not structural causation**.

### 6.4 Volatility modeling and forecasting

Start with historical/rolling-volatility benchmarks, then estimate ARCH/GARCH-family specifications where suitable. Compare a benchmark model with a volume-augmented model, taking care not to use future or same-period information when forecasting. Evaluate one-step-ahead predictions in a chronological holdout or rolling-origin design, with metrics such as MAE, RMSE or QLIKE (if the volatility target is appropriate).

### 6.5 Robustness

- Repeat with alternative volume definitions, volatility proxies and lag lengths.
- Test BTC and ETH separately; compare results without presuming identical mechanisms.
- Evaluate sensitivity to extreme observations, market regimes and major market disruptions.
- Check residual diagnostics, multicollinearity, parameter stability and multiple-testing concerns.
- Consider exchange-specific effects and possible wash trading/volume-quality problems.

## 7. Data handling and reproducibility

Record data source, endpoint, license/terms, symbol, exchange, market type, bar interval, timezone, extraction timestamp, pagination, cleaning rules and dataset checksum. Keep raw data immutable locally when feasible; commit only redistributable data and metadata. Use versioned scripts and a pinned dependency environment.

## 8. Limitations and ethics

Observational analysis cannot identify causality without a defensible identification strategy. Cryptocurrency data may exhibit market manipulation, exchange outages, survivorship bias, inconsistent volumes, nonstationarity and structural breaks. Avoid claims of investment profitability from in-sample correlations. No personal data are required for the proposed design.

## 9. Decisions pending

1. Supervisor-approved research questions and hypotheses.
2. Exact assets, trading pairs, exchanges/provider, volume unit and data access permissions.
3. Study period and frequency confirmed: 2018–2025, daily UTC; verify data availability and daily boundaries.
4. Main outcome and primary hypothesis to reduce specification searching.
5. Software stack and expected deliverables.

See [analysis plan](analysis-plan.md) for implementation and evaluation steps.

## Confirmed temporal protocol

See [2018–2025 empirical protocol](2018-2025-protocol.md) for the fixed sample window, coverage gate, expanding-window forecasts, and robustness grid.
