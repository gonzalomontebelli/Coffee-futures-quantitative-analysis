# Data Dictionary and Provenance

- [`inputs.json`](inputs.json) records the **numerical assumptions from the Citi/Forage learning exercise**: coffee spot price $1.20/lb; annual risk-free rate 2%; annual storage rate 1%; maturity six months; strike $1.25/lb; annual volatility 25%.
- The same file also records **analyst-created educational assumptions**: convenience yield zero, position exposure of 100,000 lb, note principal/coupon/participation, credit-risk assumptions, VaR horizon, and Monte Carlo configuration.
- [`illustrative_scenarios.csv`](illustrative_scenarios.csv) contains one baseline and five **hypothetical**, analyst-chosen price/volatility scenarios. These are neither observed market outcomes nor calibrated empirical estimates of drought, demand, harvest, or geopolitical events.

## Excluded data

There are **no** actual historical coffee-price observations, exchange market feeds, real client trades, proprietary institutional records, true supplier credit files, or actual hedging results in this repository.

## Units and conventions

- Asset prices: USD per pound (`USD/lb`).
- Rates and volatility: annual decimals (e.g., `0.25` means 25% per year).
- Tenor: years (e.g., `0.5` for six months).
- `notional_lb = 100000` is an **illustrative aggregate exposure**, not a claim about an exchange contract lot size.
- `confidence_level=0.95` and `var_horizon_years=1/12` define the parametric VaR approximation.

See [Data provenance and limitations](../docs/07_data_provenance_and_limitations.md).
