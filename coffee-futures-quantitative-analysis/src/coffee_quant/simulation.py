"""Monte Carlo consistent with simplified cost-of-carry pricing and Black-76."""
from __future__ import annotations
from dataclasses import dataclass
from math import exp, sqrt
import numpy as np


@dataclass(frozen=True)
class SimulationResult:
    terminal_prices: np.ndarray
    call_price: float
    call_standard_error: float
    mean_terminal_price: float
    ci_95_low: float
    ci_95_high: float


def risk_neutral_terminal(spot: float, rate: float, storage: float, maturity: float,
                          volatility: float, strike: float, n: int = 200000,
                          seed: int = 42, convenience_yield: float = 0) -> SimulationResult:
    """Uses drift r+storage-y to match model futures and prices call via discounting.

    This is an educational model-consistency check, not a real-world forecast.
    """
    if n < 2 or spot <= 0 or strike <= 0 or volatility < 0 or maturity < 0:
        raise ValueError("Invalid simulation parameters")
    rng = np.random.default_rng(seed)
    z = rng.standard_normal(n)
    drift = (rate + storage - convenience_yield - 0.5 * volatility**2) * maturity
    terminal = spot * np.exp(drift + volatility * sqrt(maturity) * z)
    payoff_pv = exp(-rate * maturity) * np.maximum(terminal - strike, 0)
    price = float(payoff_pv.mean())
    se = float(payoff_pv.std(ddof=1) / sqrt(n))
    return SimulationResult(terminal, price, se, float(terminal.mean()),
                            price - 1.96 * se, price + 1.96 * se)


def sample_price_paths(spot: float, rate: float, storage: float,
                       maturity: float, volatility: float, steps: int = 126,
                       n_paths: int = 30, seed: int = 43,
                       convenience_yield: float = 0.0) -> np.ndarray:
    """Return array of shape (steps+1, n_paths), including t=0 and EXACT t=T."""
    if steps < 1 or n_paths < 1 or maturity <= 0:
        raise ValueError("Expected positive steps, n_paths and maturity")
    dt = maturity / steps
    rng = np.random.default_rng(seed)
    shocks = rng.standard_normal((steps, n_paths))
    increments = (rate + storage - convenience_yield - 0.5*volatility**2)*dt + volatility*sqrt(dt)*shocks
    paths = np.concatenate([np.zeros((1, n_paths)), np.cumsum(increments, axis=0)], axis=0)
    return spot * np.exp(paths)
