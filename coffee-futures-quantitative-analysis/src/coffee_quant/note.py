"""Illustrative structured-note payoff and valuation budget for Task 3."""
from __future__ import annotations
from math import exp


def structured_note_payoff(terminal_coffee: float, principal: float,
                           coupon_rate: float, participation: float, strike: float) -> float:
    """Principal + maturity coupon + participation on positive relative rise over K.

    Ignores issuer default, fees, taxes, funding spreads and early-sale discounts.
    """
    if min(terminal_coffee, principal, coupon_rate, participation, strike) < 0 or strike == 0:
        raise ValueError("Invalid note inputs")
    return principal * (1 + coupon_rate + participation * max((terminal_coffee-strike)/strike, 0.0))


def note_budget(principal: float, coupon_rate: float, participation: float,
                strike: float, call_pv_per_lb: float, rate: float, maturity: float) -> dict:
    """Indicative idealized budget at risk-free discounting, before all real costs."""
    principal_pv = principal * exp(-rate*maturity)
    coupon_pv = principal*coupon_rate*exp(-rate*maturity)
    upside_pv = principal*participation/strike * call_pv_per_lb
    return {
        "principal_pv": principal_pv,
        "coupon_pv": coupon_pv,
        "embedded_option_pv": upside_pv,
        "total_pv": principal_pv+coupon_pv+upside_pv,
        "headroom_before_costs": principal-(principal_pv+coupon_pv+upside_pv),
    }
