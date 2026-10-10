#!/usr/bin/env python3
"""Regenerate datasets, metrics, and charts using the inputs in data/inputs.json.

Usage: python scripts/run_analysis.py
     python scripts/run_analysis.py --n-simulations 200000 --seed 42
"""
from __future__ import annotations
import argparse
import csv
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from coffee_quant.models import futures_cost_of_carry, black_scholes_spot_call, black76_futures_call
from coffee_quant.simulation import risk_neutral_terminal
from coffee_quant.risk import parametric_var, expected_credit_loss, procurement_costs
from coffee_quant.note import note_budget, structured_note_payoff
from coffee_quant.visualizations import render_all


def build(inputs: dict, scenarios_input: list[dict], n: int, seed: int):
    s=inputs["spot_price"];r=inputs["risk_free_rate_annual"];u=inputs["storage_cost_rate_annual"]
    y=inputs["convenience_yield_annual"];t=inputs["maturity_years"];k=inputs["strike_price"]
    vol=inputs["volatility_annual"]
    f=futures_cost_of_carry(s,r,u,t,y)
    bsm=black_scholes_spot_call(s,k,r,t,vol)
    b76=black76_futures_call(f,k,r,t,vol)
    sim=risk_neutral_terminal(s,r,u,t,vol,k,n,seed,y)
    qty=inputs["notional_lb"];exposure=s*qty
    var=parametric_var(exposure,vol,inputs["confidence_level"],inputs["var_horizon_years"])
    sc=inputs["supplier_credit_example"]
    expected_loss=expected_credit_loss(sc["probability_of_default"],sc["loss_given_default"],sc["exposure_at_default_usd"])
    note=inputs["structured_note"]
    budget=note_budget(note["principal"],note["fixed_coupon_rate_six_months"],note["upside_participation"],k,b76,r,t)
    metrics={
        "unit":"USD per lb except where specified",
        "market_data_status":"Instructional inputs; no live quotes or historical market data",
        "futures_usd_per_lb":f,"black_scholes_spot_call_usd_per_lb":bsm,
        "black76_call_usd_per_lb":b76,"mc_call_usd_per_lb":sim.call_price,
        "mc_call_standard_error":sim.call_standard_error,
        "mc_call_95_ci_low":sim.ci_95_low,"mc_call_95_ci_high":sim.ci_95_high,
        "mc_terminal_mean_usd_per_lb":sim.mean_terminal_price,
        "mc_simulations":n,"mc_seed":seed,
        "one_month_95pct_parametric_var_usd":var,
        "illustrative_supplier_expected_credit_loss_usd":expected_loss,
        "structured_note_budget_per_100usd":budget,
    }
    scenarios=[]
    for row in scenarios_input:
        sv=float(row["spot_price"]);vv=float(row["volatility_annual"])
        sf=futures_cost_of_carry(sv,r,u,t,y)
        scenarios.append({**row,"spot_price":sv,"volatility_annual":vv,
                          "futures":sf,"call":black76_futures_call(sf,k,r,t,vv)})
    return metrics,scenarios,sim


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n-simulations",type=int,default=None,help="MC n; default from inputs.json")
    ap.add_argument("--seed",type=int,default=None,help="Random seed; default from inputs.json")
    ap.add_argument("--output-dir",type=Path,default=ROOT / "results")
    ap.add_argument("--figures-dir",type=Path,default=ROOT / "assets" / "figures")
    args=ap.parse_args()
    inputs=json.loads((ROOT/"data"/"inputs.json").read_text(encoding="utf-8"))
    with (ROOT/"data"/"illustrative_scenarios.csv").open(newline="",encoding="utf-8") as f:
        scenarios_input=list(csv.DictReader(f))
    n=args.n_simulations if args.n_simulations is not None else inputs["simulation_n"]
    seed=args.seed if args.seed is not None else inputs["simulation_seed"]
    metrics,scenarios,sim=build(inputs,scenarios_input,n,seed)
    args.output_dir.mkdir(exist_ok=True,parents=True)
    args.figures_dir.mkdir(exist_ok=True,parents=True)
    (args.output_dir/"metrics.json").write_text(json.dumps(metrics,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    with (args.output_dir/"scenario_valuations.csv").open("w",newline="",encoding="utf-8") as f:
        cols=["scenario","classification","spot_price","volatility_annual","futures","call","interpretation"]
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows({k:row[k] for k in cols} for row in scenarios)
    with (args.output_dir/"hedging_comparison.csv").open("w",newline="",encoding="utf-8") as f:
        cols=["terminal_price_usd_per_lb","no_hedge_usd","long_futures_usd","long_call_usd"]
        writer=csv.writer(f);writer.writerow(cols)
        for v in [0.96,1.20,1.44]:
            outcome=procurement_costs(v,inputs["notional_lb"],metrics["futures_usd_per_lb"],inputs["strike_price"],metrics["black76_call_usd_per_lb"])
            writer.writerow([v,outcome["no_hedge"],outcome["long_futures"],outcome["long_call"]])
    with (args.output_dir/"structured_note_payoff.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.writer(f);writer.writerow(["terminal_coffee_usd_per_lb","payout_per_100usd"])
        note=inputs["structured_note"]
        for v in [.95,1.20,1.25,1.40,1.60]:
            writer.writerow([v,structured_note_payoff(v,note["principal"],note["fixed_coupon_rate_six_months"],note["upside_participation"],inputs["strike_price"])])
    render_all(inputs,scenarios,sim,metrics,args.figures_dir)
    print(f"Futures: ${metrics['futures_usd_per_lb']:.5f}/lb")
    print(f"Call spot Black-Scholes: ${metrics['black_scholes_spot_call_usd_per_lb']:.5f}/lb")
    print(f"Call Black-76: ${metrics['black76_call_usd_per_lb']:.5f}/lb")
    print(f"Call Monte Carlo: ${metrics['mc_call_usd_per_lb']:.5f}/lb, n={n}, seed={seed}")
    print(f"One-month 95% VaR: ${metrics['one_month_95pct_parametric_var_usd']:,.0f}")
    print(f"Illustrative expected credit loss: ${metrics['illustrative_supplier_expected_credit_loss_usd']:,.0f}")
    print(f"Results -> {args.output_dir}")
    print(f"Charts    -> {args.figures_dir}")


if __name__ == "__main__":
    main()
