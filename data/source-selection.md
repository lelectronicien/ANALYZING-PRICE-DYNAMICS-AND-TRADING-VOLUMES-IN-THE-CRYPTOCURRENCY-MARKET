# Daily cryptocurrency market data: source selection

**Decision status:** Binance spot public historical klines API is a **candidate**, not an approved or validated source. Access and permitted usage must be checked from the researcher's location and institution before collection.

## Selection criteria

1. Documented and reproducible API or downloadable historical records.
2. BTC and ETH spot trading pairs with consistent daily UTC OHLCV.
3. Clearly defined base-asset volume and quote-asset turnover.
4. Sufficient historical coverage and transparent handling of exchange outages and delistings.
5. Data provenance, access terms, geographic restrictions, API limits and redistribution permissions.
6. Ability to replicate results using documented extraction dates and software versions.

## Candidate: Binance Spot API

- Documentation: https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints
- Endpoint: `GET https://api.binance.com/api/v3/klines`
- Parameters: `symbol=BTCUSDT` or `ETHUSDT`, `interval=1d`, `startTime`, `endTime`, `limit`.
- Each kline includes open time, OHLC, base-asset volume, close time, quote-asset volume, and trade count.
- Use UTC day boundaries (do not set a non-UTC timeZone); reject incomplete current-day candles.
- One exchange and USDT-quoted spot pairs are **not** equivalent to total cryptocurrency-market volume or USD turnover.
- API availability and exchange eligibility vary by jurisdiction; use an authorized alternative if this endpoint is blocked or unsuitable.

## Alternatives for evaluation

- **CoinGecko API:** aggregated price and volume series; check historical lookback and plan restrictions, aggregation methodology and timestamp conventions. https://docs.coingecko.com/
- **CryptoCompare:** market data aggregation; confirm endpoint access, historical coverage, constituent venues, and license. https://min-api.cryptocompare.com/documentation
- **Exchange-native historical exports:** exchange-specific records, subject to venue documentation and licensing.

Do not concatenate volume across exchanges without harmonizing units, trading pairs, time boundaries and methodology.

## Provisional scope

- BTCUSDT and ETHUSDT, spot, daily UTC.
- Study window: **2018-01-01 to 2025-12-31 inclusive**, with exclusive API end **2026-01-01**. Expect **2,922 daily bars per asset** if continuously covered; verify and record every gap.
- Keep a source log: retrieval UTC timestamp, API base URL, endpoint/parameters, response checksum, symbols, data license, and observed missing bars.

## Data-quality checks

- Unique ascending open timestamps and 86,400,000 ms spacing.
- Open/high/low/close positive, low <= min(open, close), high >= max(open, close).
- Nonnegative base/quote volume; zero volumes flagged for review.
- Closed daily candles only; no partial current-day observation.
- Explicitly report missing dates; do not fabricate or forward-fill candles.
- Verify quote turnover is not interpreted as base-asset volume.
- Cross-check a sample against another authorized provider before finalizing source.

## Public repository policy

`data/raw/` is gitignored. Commit data dictionaries, retrieval scripts, provenance records and permitted small derived examples only. Never commit credentials or datasets whose terms forbid redistribution.

## Coverage gate

Run `python -m src.coverage --input data/raw/BTCUSDT.csv --symbol BTCUSDT --output results/coverage_btc.json` (repeat for ETHUSDT). An incomplete report blocks inference until gaps are investigated and documented. A complete report is necessary but not sufficient for data reliability.
