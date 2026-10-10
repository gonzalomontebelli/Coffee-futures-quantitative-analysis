"""Risk metrics and illustrative hedges; no live market feed."""
from __future__ import annotations
from math import sqrt
from scipy.stats import norm


def parametric_var(exposure_usd: float, vol_annual: float, confidence: float,
                   horizon_years: float) -> float:
    """Zero-mean linear normal P&L approximation; quantile, NOT max possible loss."""
    if exposure_usd < 0 or vol_annual < 0 or horizon_years < 0 or not (0.5 < confidence < 1):
        raise ValueError("Invalid VaR parameters")
    return exposure_usd * vol_annual * sqrt(horizon_years) * norm.ppf(confidence)


def expected_credit_loss(pd: float, lgd: float, ead: float) -> float:
    if not (0 <= pd <= 1 and 0 <= lgd <= 1) or ead < 0:
        raise ValueError("Invalid PD / LGD / EAD")
    return pd * lgd * ead


def procurement_costs(terminal_spot: float, quantity_lb: float,
                      futures_entry: float, call_strike: float, call_premium: float) -> dict:
    """Hypothetical fully matched physical/futures terminal fixing, no basis/costs."""
    if min(terminal_spot, quantity_lb, futures_entry, call_strike, call_premium) < 0:
        raise ValueError("Negative market input")
    return {
        "no_hedge": quantity_lb * terminal_spot,
        "long_futures": quantity_lb * futures_entry,
        "long_call": quantity_lb * (terminal_spot - max(terminal_spot-call_strike, 0.0) + call_premium),
    }
