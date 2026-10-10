import numpy as np
import pytest
from coffee_quant.models import futures_cost_of_carry, black76_futures_call
from coffee_quant.simulation import risk_neutral_terminal, sample_price_paths


def test_monte_carlo_agrees_with_analytic_to_4_se():
    f=futures_cost_of_carry(1.2,.02,.01,.5)
    analytic=black76_futures_call(f,1.25,.02,.5,.25)
    result=risk_neutral_terminal(1.2,.02,.01,.5,.25,1.25,n=200000,seed=42)
    assert abs(result.call_price-analytic)<4*result.call_standard_error
    assert abs(result.mean_terminal_price-f)<.004


def test_reproducible_paths_include_zero_and_T():
    p1=sample_price_paths(1.2,.02,.01,.5,.25,steps=126,n_paths=10,seed=42)
    p2=sample_price_paths(1.2,.02,.01,.5,.25,steps=126,n_paths=10,seed=42)
    assert p1.shape==(127,10)
    assert np.allclose(p1[0],1.2)
    assert np.array_equal(p1,p2)
