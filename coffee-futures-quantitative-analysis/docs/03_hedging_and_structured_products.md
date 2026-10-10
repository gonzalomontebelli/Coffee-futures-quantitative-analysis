# Task 3 — Hedging and Structuring Securities

## Objective

Select derivatives and investment products tailored to **specific client exposures, risk tolerances, and desired cash flows**.

## Instruments reviewed

| Strategy | Example use case | Important trade-off |
|---|---|---|
| Long futures | Buyer locks an approximate purchase price | Gives up benefits of price declines; daily margin and basis risk |
| Short futures | Producer protects a sale price | Gives up benefits of price increases; margin and basis risk |
| Long call | Buyer hedges a sharp price increase | Pays premium; may still face basis risk |
| Long put | Producer hedges a price decline | Pays premium; retains upside subject to basis |
| Producer collar | Long put combined with short call | Lower net premium, but limits upside |
| Interest-rate swap | Stabilizes variable warehouse/inventory financing cost | Does not directly hedge physical coffee price |
| Digital option | Fixed payment if terminal condition is met | Discontinuous payoff, potential full loss of premium |

## Four client scenarios from the learning task

1. **Conservative investor:** commodity-linked bond with a fixed component and conditional coffee-price exposure; assess issuer risk and contract terms.
2. **Moderate-risk investor:** structured note with a fixed coupon and limited participation in price increases (**selected submission**).
3. **High-risk investor:** digital call options paying a fixed amount if coffee rises beyond a strike. The example answer in the training chose this alternative.
4. **Diversification seeker:** an ETF or fund referencing coffee futures, with roll yield, fees, tracking error, and concentration risk.

## Selected structure: six-month coffee-linked note

**All product terms below are illustrative and were designed for the assignment, not issued or quoted by Citi.**

| Term | Hypothetical choice |
|---|---|
| Principal | $100 |
| Term | 6 months |
| Fixed coupon over the term | 0.20% |
| Coffee reference strike | $1.25/lb |
| Upside participation | 10% |
| Contractual principal repayment | At maturity, subject to issuer performance |

For each $100 invested, an illustrative terminal cash payment is

$$\mathrm{Payoff}(C_T)=100\left[1+0.002+0.10\max\left(\frac{C_T-1.25}{1.25},0\right)\right].$$

| Terminal coffee fixing (USD/lb) | Payment per $100 principal (USD) |
|---:|---:|
| 0.95 | 100.20 |
| 1.20 | 100.20 |
| 1.25 | 100.20 |
| 1.40 | 101.40 |
| 1.60 | 103.00 |

Payments exclude fees, taxes, and issuer default. Selling early may realize less than par even when the issuer has not defaulted.

![Structured note illustrative payoff](../assets/figures/06_structured_note_payoff.png)

## Indicative replication and financing budget

Using the same theoretical futures curve and Black-76 premium ($0.07119333/lb):

| Component, per $100 | Present value (approx.) |
|---|---:|
| Discounted principal | $99.0050 |
| Discounted fixed coupon | $0.1980 |
| Upside participation | $0.5695 |
| Total theoretical cost | $99.7725 |
| Preliminary remainder | **$0.2275** |

**This remainder is not a bank margin or executable product spread.** It excludes issuer funding costs, credit risk, bid-ask spreads, hedging transaction costs, reserves, and structuring expenses.

## Issuer-side hedging and control

The issuer is short the embedded call option. A matching purchased call can offset its payoff if available; otherwise a dynamic **delta hedge** using the appropriate futures may be considered. Monitor vega, jumps, basis, funding, execution costs, and legal settlement terms. The protected principal depends on issuer solvency.

## Digital-option reference example

For a unit-paying European digital call, the payoff is `1{F_T > K}` and a Black-76-style risk-neutral present value is `exp(-rT) * N(d2)` under its distributional assumptions. `N(d2)` is a **risk-neutral probability**, not a real-world event forecast.

See [`note.py`](../src/coffee_quant/note.py) and the [Task 3 report](../reports/Task_3_Coffee_Structured_Note.pdf).
