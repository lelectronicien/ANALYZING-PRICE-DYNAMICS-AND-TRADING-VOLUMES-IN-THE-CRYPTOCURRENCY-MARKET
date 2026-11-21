# Daily spot OHLCV data dictionary

| Field | Type | Meaning |
| --- | --- | --- |
| symbol | string | Exchange symbol, e.g. BTCUSDT |
| open_time | UTC datetime | Start of daily candle |
| close_time | UTC datetime | Exchange-reported candle close |
| open | float | Opening trade price, quote units/base unit |
| high | float | Maximum trade price |
| low | float | Minimum trade price |
| close | float | Closing trade price |
| volume_base | float | Traded quantity in base asset (BTC or ETH) |
| volume_quote | float | Traded turnover in quote asset (USDT) |
| trades | integer | Exchange-reported number of trades |
| log_return | float | ln(close_t/close_{t-1}) |
| abs_return | float | Absolute log return |
| squared_return | float | Squared log return |
| log_volume_quote | float | ln(1 + quote turnover) |
| log_volume_change | float | Difference in log quote turnover |
| realized_var_7d | float | Rolling 7-day sum of squared daily returns; daily proxy |

Quote-asset turnover in USDT is **not guaranteed to equal USD-denominated turnover**. No aggregation across exchanges or market types is assumed. UTC day boundaries and source metadata are mandatory.
