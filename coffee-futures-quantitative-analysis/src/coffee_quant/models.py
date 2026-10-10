"""Analytical pricing models under explicit educational assumptions."""
from __future__ import annotations
from math import exp, log, sqrt
from scipy.stats import norm


def futures_cost_of_carry(spot: float, rate: float, storage: float,
                          maturity: float, convenience_yield: float = 0.0) -> float:
    """F = S * exp((r + u - y)*T); storage as an annual proportional carry rate."""
    if spot <= 0 or maturity < 0:
        raise ValueError("Spot must be positive and maturity nonnegative")
    return spot * exp((rate + storage - convenience_yield) * maturity)


def black_scholes_spot_call(spot: float, strike: float, rate: float,
                            maturity: float, volatility: float) -> float:
    """European call under Black-Scholes *spot* convention (training guide)."""
    if spot <= 0 or strike <= 0 or maturity < 0 or volatility < 0:
        raise ValueError("Invalid option inputs")
    if maturity == 0:
        return max(spot - strike, 0.0)
    if volatility == 0:
        return max(spot - strike * exp(-rate * maturity), 0.0)
    d1 = (log(spot / strike) + (rate + 0.5 * volatility**2) * maturity) / (volatility * sqrt(maturity))
    d2 = d1 - volatility * sqrt(maturity)
    return spot * norm.cdf(d1) - strike * exp(-rate * maturity) * norm.cdf(d2)


def black76_futures_call(futures: float, strike: float, rate: float,
                         maturity: float, volatility: float) -> float:
    """European call on futures (Black-76), discounted terminal futures payoff."""
    if futures <= 0 or strike <= 0 or maturity < 0 or volatility < 0:
        raise ValueError("Invalid option inputs")
    if maturity == 0:
        return max(futures - strike, 0.0)
    if volatility == 0:
        return exp(-rate * maturity) * max(futures - strike, 0.0)
    d1 = (log(futures / strike) + 0.5 * volatility**2 * maturity) / (volatility * sqrt(maturity))
    d2 = d1 - volatility * sqrt(maturity)
    return exp(-rate * maturity) * (futures * norm.cdf(d1) - strike * norm.cdf(d2))


def black76_futures_put(futures: float, strike: float, rate: float,
                        maturity: float, volatility: float) -> float:
    """Black-76 put via put-call parity, with roundoff protection."""
    call = black76_futures_call(futures, strike, rate, maturity, volatility)
    return max(0.0, call - exp(-rate * maturity) * (futures - strike))
