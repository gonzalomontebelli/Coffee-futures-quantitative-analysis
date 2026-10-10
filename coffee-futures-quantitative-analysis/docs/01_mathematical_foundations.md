# Task 1 — Mathematical Foundations for Quantitative Finance

## Objective

Understand how **probability, statistics, calculus, linear algebra and stochastic processes** support pricing, portfolio management, structuring, forecasting, and risk measurement.

| Discipline | Financial application | Coffee case application |
|---|---|---|
| Probability | Random variables, probability distributions, Bayes' rule | Alternative supply and price outcomes |
| Statistical inference | Confidence intervals, hypothesis testing, p-values | Volatility estimation and model validation |
| Linear algebra | Covariance matrices, optimization, factor exposures | Cross-asset covariance between coffee, energy and FX |
| Differential calculus | Partial derivatives and sensitivities | Option delta, vega, and rate sensitivities |
| Differential equations | Dynamic models and PDEs | Theoretical foundation of Black-Scholes |
| Stochastic calculus | Brownian motion and SDEs | Random asset-price dynamics |
| Time series | ARIMA and GARCH | Trends and volatility clustering |

## Core models and their use

- **Linear regression:** estimate associations between coffee prices and measurable drivers; associations alone do not establish causation.
- **ARIMA:** model time-series dependence for statistical forecasting under validated assumptions.
- **GARCH:** describe time-varying conditional volatility and volatility clustering.
- **Geometric Brownian motion:** a simple continuous positive-price model used for simulation and introductory derivatives pricing.
- **Black-Scholes:** a benchmark European option formula under idealized assumptions.
- **Black-76:** a closely related formula for options on futures.
- **Monte Carlo:** approximate expected discounted derivative payoffs or simulated loss distributions via random sampling.
- **Value at Risk / Expected Shortfall:** characterize different aspects of loss distributions, provided the model and horizon are clearly stated.

## Brownian price dynamics

An educational stochastic model may be written as

$$dS_t = \mu S_t\,dt + \sigma S_t\,dW_t.$$

Here `S_t` denotes price, `mu` a selected drift, `sigma` annualized volatility, and `W_t` Brownian motion. The drift depends on whether the objective is **physical forecasting** or **risk-neutral pricing**. These are different modeling tasks.

## Knowledge-check context

The exercise asked for the mathematics behind **futures pricing**, **structured product design**, and **risk measurement**. An appropriate answer connects cost-of-carry, option pricing, regression and stochastic simulation with VaR/CVaR, hedging and controls. No ARIMA or GARCH model was actually fitted to real price history in this repository.

Continue to [Task 2: Coffee pricing](02_commodity_pricing.md).
