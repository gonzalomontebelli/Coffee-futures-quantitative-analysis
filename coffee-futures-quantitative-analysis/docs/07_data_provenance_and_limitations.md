# Data Provenance, Model Assumptions and Limitations

## Evidence classification

| Input or claim | Provenance | Status |
|---|---|---|
| Spot $1.20/lb; risk-free 2%; storage 1%; tenor 0.5 years; strike $1.25/lb; volatility 25% | Numerical exercise supplied by Citi/Forage during the conversation | **Provided educational assumptions** |
| Cost-of-carry, Black-Scholes, Monte Carlo and risk-management concepts | Educational tasks and the provided step-by-step study guide | **Training concepts**, with transparent extensions |
| Futures price, option premiums, Monte Carlo and VaR values | Locally computed in `src/` and `scripts/` | **Model outputs** under stated assumptions |
| Drought/harvest/consumption/geopolitical spot and volatility shocks | Analyst-designed scenario values | **Hypotheses**, not observations or measured causal effects |
| Note principal $100, coupon 0.20%, participation 10%, six-month tenor | Analyst-designed product scenario | **Illustrative hypothetical product** |
| 100,000-lb exposure; supplier PD 5%, LGD 60%, EAD $120,000 | Analyst-designed risk inputs | **Hypothetical quantities** |
| Task 2–4 PDF and Word reports | Prepared during the educational case study | **Archived educational deliverables** |
| Archived Word-document generators | Historical local scripts | **Process record**; contains original absolute paths |

## Excluded source materials

The original *Step by step guide.docx* and the Forage template are **not redistributed**. They were used to understand the assignment and conventions. Public text links to the virtual case are included for attribution; proprietary source datasets are not present.

## Key modeling caveats

1. **Cost of carry:** The model treats storage as a proportional annual rate and convenience yield as zero. Real physical contracts require warehouse, deliverable grade, location, quality, delivery restrictions and commodity-specific market conventions.
2. **Option conventions:** The teaching guide uses standard spot Black-Scholes, although the assignment speaks of options on futures. This repository explicitly distinguishes the spot benchmark from Black-76 futures option pricing.
3. **GBM Monte Carlo:** Terminal GBM prices are generated under **risk-neutral assumptions** to reproduce a discounted option payoff. They are not physical coffee-price forecasts.
4. **Original guide timing:** The guide's path count and time increments were slightly inconsistent. This project explicitly creates 126 increments over six months and retains both the initial and the exact terminal observation (127 prices per path).
5. **VaR:** A parametric normal VaR is a selected tail threshold, not the worst conceivable outcome or a stress-test replacement.
6. **Structured note:** Contractual capital repayment does not eliminate **issuer insolvency**, secondary-market mark-to-market losses, liquidity, fees or taxation.
7. **Physical supplier exposure:** A financial CDS is not necessarily available or suitable as a guarantee of physical performance. A bank guarantee, performance bond, letter of credit or escrow may be more relevant.
8. **No market calibration:** The project does not contain observed prices, an empirical volatility surface, real historic correlations, broker execution quotes, live counterparty files, or out-of-sample performance tests.

## Reproducibility and integrity

- Fixed random seeds permit deterministic results for a given library environment.
- All assumptions and scenario classifications are readable in plain-text input files.
- Unit tests check model parity, option bounds, zero-volatility cases, hedging mechanics, expected loss and simulation properties.
- Continuous integration executes the tests and reruns the plotting pipeline.
- Potential numerical differences caused by NumPy/SciPy versions are acceptable within test tolerances.

## Attribution and professional disclosure

This is independent **portfolio research for a Citi/Forage virtual job simulation**, not employment, a Citi-approved client analysis, live trading, or a recommendation. The author is responsible for the independent implementations and explanatory notes. For real transactions, consult binding exchange specifications, execution quotes, risk policies and an appropriately qualified professional.
