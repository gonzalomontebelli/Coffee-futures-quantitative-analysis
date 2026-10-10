# Computed Results and Interpretation

The values below are reproduced using `python scripts/run_analysis.py` and saved in [`results/metrics.json`](../results/metrics.json). All prices and risk metrics depend on **educational inputs**.

## Pricing output

| Model | Computed value (USD/lb) | Interpretation |
|---|---:|---|
| Cost-of-carry futures | 1.21813568 | Theoretical six-month forward/futures reference |
| Spot Black-Scholes call | 0.06835799 | Teaching-guide spot option formula |
| Black-76 call on futures | 0.07119333 | Futures-referenced European call benchmark |
| Risk-neutral Monte Carlo call | 0.07140520 | Independent sampled approximation to theoretical call |
| Mean simulated terminal coffee price | 1.21809059 | Close to the modeled theoretical futures price |
| Monte Carlo call standard error | 0.00028806 | Sampling uncertainty conditional on the chosen model |

The difference between the Monte Carlo estimate and Black-76 is **about $0.000212/lb**, which is within the simulation's approximate 95% sampling confidence interval. This is evidence of **numerical consistency**, not real-market accuracy.

## Risk output

| Quantity | Value | Qualification |
|---|---:|---|
| Notional physical purchase exposure | 100,000 lb | Analyst-created example, not an exchange lot |
| Initial USD equivalent exposure | $120,000 | 100,000 lb × $1.20/lb |
| One-month parametric 95% VaR | ~$14,245 | Zero-mean normal linear approximation |
| Supplier expected credit loss | $3,600 | PD 5%, LGD 60%, EAD $120,000; all hypothetical |
| Structured-note theoretical headroom, per $100 | ~$0.2275 | Before funding, margin, hedging and issuer credit |

## Visual deliverables

| Figure | What it illustrates |
|---|---|
| [01: Option sensitivity](../assets/figures/01_option_sensitivity.png) | Black-76 call premium versus the underlying coffee spot level |
| [02: Market scenarios](../assets/figures/02_market_scenarios.png) | Analyst-defined supply/demand/weather/geopolitical inputs |
| [03: Terminal-price distribution](../assets/figures/03_monte_carlo_distribution.png) | Monte Carlo risk-neutral GBM terminal distribution |
| [04: Simulated price paths](../assets/figures/04_monte_carlo_paths.png) | Selected illustrative GBM paths over six months |
| [05: Hedging comparison](../assets/figures/05_hedging_cost_comparison.png) | Total coffee purchaser cost with and without long futures/calls |
| [06: Structured note](../assets/figures/06_structured_note_payoff.png) | Contractual maturity payoff under assumed note terms |
| [07: Stress test](../assets/figures/07_stress_test.png) | Unhedged coffee purchaser sensitivity to price shocks |

## Data and implementation

- [`inputs.json`](../data/inputs.json): input quantities and model configuration.
- [`illustrative_scenarios.csv`](../data/illustrative_scenarios.csv): explicitly hypothetical market shocks.
- [`scenario_valuations.csv`](../results/scenario_valuations.csv): repriced futures and calls for each scenario.
- [`hedging_comparison.csv`](../results/hedging_comparison.csv): total physical purchase cost under three strategies.
- [`structured_note_payoff.csv`](../results/structured_note_payoff.csv): contractual payoff examples.
- [`metrics.json`](../results/metrics.json): authoritative machine-readable summary.

## No unsupported conclusions

No claim is made about realized trading profitability, verified supplier credit, the probability of a drought, actual option implied volatility, regulatory capital requirements, or the performance of strategies on historical observations.
