# Knowledge Checks and Learning Decisions

This chapter summarizes the **questions and answers discussed during the simulation**. Original questions are paraphrased rather than reproduced verbatim.

## Project introduction: two checks

| Concept being assessed | Best answer | Reason |
|---|---|---|
| Why design standardized coffee futures? | Hedge price fluctuations | Producers and traders can manage price exposure using standardized contracts. |
| Why is a coffee futures contract needed? | Unpredictable price fluctuations | Climate, crop supply, shipping constraints and other economic shocks affect prices. |

## Task 1 — Financial mathematics: open response

The exercise asked which mathematics should be applied to **futures pricing**, **securities structuring**, and **risk management**. A strong response combines no-arbitrage carry pricing; statistical/regression and time-series methods; stochastic processes; discounted option payoffs; and VaR, Expected Shortfall and hedging.

The reference solution also emphasized regression, **geometric Brownian motion** and **GARCH**. These are discussed here but were **not fitted to observed time series**.

## Task 2 — Commodity pricing: open responses

- **Supply and demand:** large harvests typically loosen supply and put downward pressure on price; weak harvests often have the opposite effect, all else equal.
- **Weather:** drought, frost, crop disease and excess rain can reduce crop quantity or quality.
- **Geopolitics:** export restrictions, conflict, tariffs and FX shifts can alter trade flows and market prices.
- **Cost of carry:** `F = S * exp((r + u - y) * T)` under documented carry assumptions.
- **Options:** the learning guide demonstrates spot Black-Scholes; a call written on futures is typically treated with Black-76.
- **Monte Carlo:** simulate possible terminal outcomes to approximate a discounted payoff under risk-neutral model assumptions. Illustrative spot/volatility shocks are not measured event impacts.

The open task was submitted as an independent English pricing report; see [Task 2 PDF](../reports/Task_2_Coffee_Futures_Valuation.pdf).

## Task 3 — Hedging: three multiple-choice checks

| Question focus | Correct answer | Rationale |
|---|---|---|
| Limit downside from a decline in coffee prices | **Purchase put options** | Long puts preserve a minimum gross selling level while retaining upside, net of premium. Short futures may also hedge prices but change upside exposure. |
| When might an interest-rate swap help? | **Strong correlation between coffee prices and interest rates** | This was the best listed answer in the course. The swap actually hedges rate-sensitive funding cash flows, **not coffee price directly**. |
| Essential hedging governance | **Monitor developments and adjust strategies** | Hedging must reflect volatility, liquidity, basis and changing client exposures. |

The practical Task 3 prompt allowed **one of four client scenarios**. This project selected a moderate-risk structured note. The example answer selected high-risk **digital calls**. Both choices are consistent with the exercise when suitably risk-disclosed.

## Task 4 — Market risk: three multiple-choice checks

| Question focus | Correct answer | Rationale |
|---|---|---|
| Quantile-based potential portfolio loss | **Value at Risk (VaR)** | Reports a selected quantile of the modeled loss distribution, not an absolute maximum. |
| Purpose of stress testing | **Evaluate resilience and vulnerabilities** | Tests severe yet plausible market and liquidity shocks. |
| Vary one risk-factor input | **Sensitivity analysis** | Quantifies portfolio-value changes when rates, prices, volatility or other selected variables move. |

The final applied exercise required risk mitigation for: **a weather-driven coffee price increase**, **a risky new supplier**, and **manual execution errors**. Proposed answers use long futures/calls plus stress testing; supplier credit screening with collateral and performance guarantees; and automated pre-trade controls, reconciliations and incident response.

## What the project actually implements

- Reproducible futures, spot-call and futures-call pricing.
- Risk-neutral Monte Carlo consistency check.
- Hypothetical market scenarios, hedging cost comparison and note payoff.
- Parametric VaR and expected credit loss examples.
- Quantitative plots, documented limitations and tests.

**Not implemented:** empirical supplier credit scoring, live portfolio optimization, real GARCH calibration, production trade execution, or historical backtesting.
