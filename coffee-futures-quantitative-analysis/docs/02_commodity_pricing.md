# Task 2 — Pricing Coffee Futures and Options

## The question

Price a six-month coffee futures contract, value a call option and explore how supply/demand, weather, and geopolitical news may influence future prices. Compare the class's Black-Scholes demonstration with a futures-specific option formula.

## Given inputs

| Parameter | Instructional value | Units |
|---|---:|---|
| Spot coffee price, `S` | 1.20 | USD/lb |
| Risk-free financing rate, `r` | 2% | Annual continuous rate |
| Storage rate, `u` | 1% | Annual proportional carry |
| Convenience yield, `y` | 0% | Analyst assumption |
| Tenor, `T` | 0.50 | Years |
| Strike, `K` | 1.25 | USD/lb |
| Annual volatility, `sigma` | 25% | Annual |

These are **teaching assumptions**, not independently observed coffee market quotations.

## 1. Cost-of-carry futures valuation

$$F_0 = S_0 e^{(r+u-y)T}.$$

Using the exercise values:

$$F_0 = 1.20\,e^{(0.02+0.01)\times0.5}=\boxed{1.21813568\ \mathrm{USD/lb}}.$$

The expression assumes proportional continuously compounded carry and zero convenience yield. Physical coffee requires additional scrutiny of warehouse rates, transportation, quality, delivery location, contract specifications, and the observed forward curve.

## 2. European spot call under Black-Scholes

The original exercise introduces:

$$C_{BS}=S_0N(d_1)-Ke^{-rT}N(d_2),$$
$$d_1=\frac{\ln(S_0/K)+(r+\sigma^2/2)T}{\sigma\sqrt T},\quad d_2=d_1-\sigma\sqrt T.$$

**Result: $0.06835799/lb.** This is a **spot-based** teaching comparison, not the preferred model for an option written on a futures reference.

## 3. European call on futures under Black-76

$$C_{76}=e^{-rT}\left[F_0N(d_1)-KN(d_2)\right],$$
$$d_1=\frac{\ln(F_0/K)+\sigma^2T/2}{\sigma\sqrt T},\quad d_2=d_1-\sigma\sqrt T.$$

**Result: $0.07119333/lb** using the theoretical futures level and 25% volatility. Real option valuation depends on the traded futures contract, implied volatility surface and market conventions.

## 4. Monte Carlo verification

Simulate 200,000 risk-neutral terminal prices using:

$$S_T=S_0\exp\left[(r+u-y-\sigma^2/2)T+\sigma\sqrt T\,Z\right],\quad Z\sim N(0,1).$$

Discount `max(S_T-K,0)` at the risk-free rate. The fixed-seed Monte Carlo call estimate is **approximately $0.07140520/lb**, with a numerical confidence interval encompassing the analytical Black-76 figure. The simulated terminal expectation is **approximately $1.21809059/lb**. These differences reflect sampling noise, not an empirical pricing advantage.

![Monte Carlo distribution](../assets/figures/03_monte_carlo_distribution.png)

## 5. Hypothetical supply, demand and geopolitical scenarios

| Shock | Economic channel | Typical directional pressure |
|---|---|---|
| Crop damage or drought | Lower expected harvest | Higher prices; potentially higher volatility |
| Exceptional harvest | Higher expected supply | Lower prices |
| Stronger consumer demand | Higher consumption | Higher prices |
| Demand slowdown | Weaker consumption | Lower prices |
| Trade restrictions | Shipping/export limitations | Higher localized or global supply risk |

Changes are illustrated with **assumed spot and volatility adjustments**, not measured causal estimates. The scenario CSV is transparent and editable.

![Scenario option and futures prices](../assets/figures/02_market_scenarios.png)

See [`models.py`](../src/coffee_quant/models.py) and [`simulation.py`](../src/coffee_quant/simulation.py).
