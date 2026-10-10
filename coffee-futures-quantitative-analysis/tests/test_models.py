import math
import pytest
from coffee_quant.models import futures_cost_of_carry, black_scholes_spot_call, black76_futures_call, black76_futures_put


def test_futures_benchmark():
    assert futures_cost_of_carry(1.2,.02,.01,.5) == pytest.approx(1.2181356771,rel=1e-8)


def test_spot_call_and_futures_call_are_not_same_convention():
    f=futures_cost_of_carry(1.2,.02,.01,.5)
    assert .068 < black_scholes_spot_call(1.2,1.25,.02,.5,.25) < .069
    assert .071 < black76_futures_call(f,1.25,.02,.5,.25) < .072


def test_black76_put_call_parity():
    f=1.22;k=1.25;r=.02;t=.5;v=.25
    c=black76_futures_call(f,k,r,t,v)
    p=black76_futures_put(f,k,r,t,v)
    assert c-p == pytest.approx(math.exp(-r*t)*(f-k),abs=1e-10)


def test_zero_vol_and_maturity():
    assert black76_futures_call(1.3,1.25,.02,0,.25) == pytest.approx(.05)
    assert black76_futures_call(1.1,1.25,.02,.5,0) == 0
    with pytest.raises(ValueError): futures_cost_of_carry(0,.02,.01,.5)
