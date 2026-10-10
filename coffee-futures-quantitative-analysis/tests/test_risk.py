import pytest
from coffee_quant.risk import expected_credit_loss, parametric_var, procurement_costs
from coffee_quant.note import structured_note_payoff, note_budget


def test_credit():
    assert expected_credit_loss(.05,.60,120000) == pytest.approx(3600)


def test_var():
    assert parametric_var(120000,.25,.95,1/12) == pytest.approx(14245.87,rel=.001)


def test_hedge():
    results=procurement_costs(1.44,100000,1.218135677,1.25,.07119)
    assert results['no_hedge'] == pytest.approx(144000)
    assert results['long_futures'] == pytest.approx(121813.5677)
    assert results['long_call'] == pytest.approx(132119,abs=1)


def test_note_payoff():
    assert structured_note_payoff(1.2,100,.002,.1,1.25) == pytest.approx(100.2)
    assert structured_note_payoff(1.4,100,.002,.1,1.25) == pytest.approx(101.4)
    assert structured_note_payoff(1.6,100,.002,.1,1.25) == pytest.approx(103)
    b=note_budget(100,.002,.1,1.25,.07119,.02,.5)
    assert 0 < b['headroom_before_costs'] < 2
