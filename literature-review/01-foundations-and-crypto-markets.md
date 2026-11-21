# Literature review: price dynamics, volume and cryptocurrency markets

**Status:** First-pass thematic synthesis. Bibliographic details and interpretation should be verified against publisher records and full texts before thesis submission. No empirical results from this project are claimed here.

## 1. Purpose and framing

This review connects classic research on the price–volume relationship to the distinctive microstructure of cryptocurrency markets. The aim is to explain *why* volume may covary with returns and volatility, *whether* it has predictive content, and *how* such claims can be tested without conflating correlation with causation.

## 2. Theoretical foundations of price–volume relationships

**Karpoff (1987)** surveys empirical work on relationships between trading volume and price changes in financial markets. The central methodological lesson for this thesis is to distinguish the *direction* of returns from their *magnitude*, and to treat volume as a measure of trading activity whose economic meaning depends on the venue and market.

**Clark (1973)** develops a subordinated stochastic process view of price changes. Information arrival and the underlying rate of trading activity offer a possible common mechanism for movements in volume and return variability. This motivates testing volume–volatility associations, while not treating the model as direct evidence for cryptocurrencies.

**Lamoureux and Lastrapes (1990)** investigate heteroskedasticity in stock returns and the volume–volatility connection. Their work motivates examining whether a volume variable changes estimated volatility persistence, with careful attention to model specification.

**Bollerslev (1986)** introduces the generalized autoregressive conditional heteroskedasticity (GARCH) framework. Because financial returns often exhibit volatility clustering, GARCH-type models are useful candidate benchmarks, but their suitability for any particular crypto sample requires diagnostics.

## 3. Market efficiency and cryptocurrency-specific dynamics

**Urquhart (2016)** examines Bitcoin market efficiency, illustrating why efficiency and predictability are relevant empirical questions rather than settled assumptions. Any conclusion depends on the market, time period, test and definition of efficiency.

**Katsiampa (2017)** investigates volatility estimation for Bitcoin, offering a cryptocurrency-specific starting point for comparing conditional-volatility specifications.

**Corbet et al. (2019)** survey cryptocurrencies as financial assets, providing a broader context for market behavior, volatility, and the evolving empirical literature. Because the market has changed substantially since publication, this survey should be paired with more recent evidence.

## 4. Volume quality, liquidity and market microstructure

Reported trading volume is not a uniform construct. Exchange-specific rules, market type (spot vs derivatives), quote currency, aggregation procedures, liquidity and possible wash trading can distort comparisons. A credible study must document exactly what each volume observation measures and test whether conclusions survive changes in exchange or volume definition.

This issue also limits causal interpretation: market-wide news, volatility shocks and shifts in liquidity can jointly affect both prices and volumes.

## 5. Synthesis and research gap

The literature suggests a coherent set of mechanisms and empirical methods, but it does not justify assuming that volume forecasts the *sign* of cryptocurrency returns. This thesis can contribute by:

1. Separating contemporaneous volume–absolute-return and volume–volatility associations from predictive tests.
2. Applying consistent definitions to BTC and ETH using a documented venue and daily UTC observations.
3. Testing whether lagged volume adds *out-of-sample* forecasting value beyond autoregressive or volatility benchmarks.
4. Checking sensitivity to volume units, sample periods, extreme events and market regimes.

These are **proposed contribution areas**, not claims that no prior study has addressed them. A systematic search of recent work is needed before finalizing novelty.

## 6. Literature-search protocol (to execute)

**Databases:** Google Scholar, Scopus, Web of Science, SSRN and publisher databases, subject to institutional access.

**Example search strings:**
- `("cryptocurrency" OR bitcoin OR ethereum) AND ("trading volume" OR turnover) AND (volatility OR "price dynamics")`
- `("bitcoin" OR "ethereum") AND ("volume" OR liquidity) AND ("Granger causality" OR "predictability")`
- `("cryptocurrency" AND "volume" AND "GARCH")`
- `("crypto exchange" AND ("wash trading" OR "reported volume" OR "data quality"))`

**Selection principles:** prioritize peer-reviewed studies and seminal methods papers; record publication year, market, sample, venue, frequency, variables, identification strategy, findings and limitations. Include recent studies and contradictory findings; use backward/forward citation chaining. Avoid treating preprints as peer-reviewed evidence.

**Screening log fields:** citation key, DOI/URL, database, search date, search string, inclusion/exclusion reason, methods, asset, sample window, venue, key finding and caveats.

## 7. Provisional references

- Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. *Journal of Econometrics, 31*(3), 307–327. https://doi.org/10.1016/0304-4076(86)90063-1
- Clark, P. K. (1973). A subordinated stochastic process model with finite variance for speculative prices. *Econometrica, 41*(1), 135–155. https://doi.org/10.2307/1913889
- Corbet, S., Lucey, B., Urquhart, A., & Yarovaya, L. (2019). Cryptocurrencies as a financial asset: A systematic analysis. *International Review of Financial Analysis, 62*, 182–199. https://doi.org/10.1016/j.irfa.2018.09.003
- Karpoff, J. M. (1987). The relation between price changes and trading volume: A survey. *Journal of Financial and Quantitative Analysis, 22*(1), 109–126. https://doi.org/10.2307/2330874
- Katsiampa, P. (2017). Volatility estimation for Bitcoin: A comparison of GARCH models. *Economics Letters, 158*, 3–6. https://doi.org/10.1016/j.econlet.2017.06.023
- Lamoureux, C. G., & Lastrapes, W. D. (1990). Heteroskedasticity in stock return data: Volume versus GARCH effects. *The Journal of Finance, 45*(1), 221–229. https://doi.org/10.1111/j.1540-6261.1990.tb05088.x
- Urquhart, A. (2016). The inefficiency of Bitcoin. *Economics Letters, 148*, 80–82. https://doi.org/10.1016/j.econlet.2016.09.019

**Verification note:** These entries are a starting bibliography, not a completed systematic review. Check DOI metadata, page ranges, and claims before final citation.
