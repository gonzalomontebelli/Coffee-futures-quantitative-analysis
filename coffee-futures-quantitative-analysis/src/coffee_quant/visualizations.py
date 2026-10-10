"""Research charts; all values are based on simulated scenarios."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .models import futures_cost_of_carry, black76_futures_call
from .risk import procurement_costs
from .note import structured_note_payoff
from .simulation import sample_price_paths

INK="#172a45"; BLUE="#2664aa"; TEAL="#087e8b"; CORAL="#d75a4a"; LIGHT="#e2e8f0"; MUTED="#62758b"


def setup():
    plt.rcParams.update({
        "font.family":"DejaVu Sans", "font.size":10, "axes.titlesize":14,
        "axes.labelcolor":INK,"axes.edgecolor":LIGHT,"axes.titleweight":"bold",
        "text.color":INK,"xtick.color":MUTED,"ytick.color":MUTED,
        "grid.color":LIGHT,"figure.facecolor":"white","axes.spines.top":False,
        "axes.spines.right":False, "savefig.facecolor":"white",
    })


def save(fig, name: str, outdir: Path):
    fig.tight_layout(pad=2.0)
    fig.savefig(outdir / f"{name}.png", dpi=155, bbox_inches="tight")
    fig.savefig(outdir / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)


def render_all(inputs, scenarios, sim, metrics, figures_dir: Path):
    setup(); figures_dir.mkdir(parents=True,exist_ok=True)
    s=inputs["spot_price"];r=inputs["risk_free_rate_annual"];u=inputs["storage_cost_rate_annual"]
    y=inputs["convenience_yield_annual"];t=inputs["maturity_years"];k=inputs["strike_price"]
    vol=inputs["volatility_annual"];qty=inputs["notional_lb"]
    # 1 analytical sensitivity curve
    x=np.linspace(.8,1.6,150)
    fv=np.array([futures_cost_of_carry(float(i),r,u,t,y) for i in x])
    calls=np.array([black76_futures_call(float(i),k,r,t,vol) for i in fv])
    fig,ax=plt.subplots(figsize=(9,4.1))
    ax.plot(x, calls, lw=2.5,color=BLUE,label="Black-76 (σ = 25 %)")
    ax.scatter([s],[metrics["black76_call_usd_per_lb"]],color=CORAL,zorder=5,s=72,label="Baseline")
    ax.set(xlabel="Coffee spot price (USD/lb)",ylabel="Theoretical call premium (USD/lb)",
           title="Coffee call option price sensitivity")
    ax.grid(alpha=.6);ax.legend(frameon=False)
    save(fig,"01_option_sensitivity",figures_dir)
    # 2 futures and options shown on separate, explicitly labeled scales
    ordered = list(scenarios)
    labels = [item["scenario"].replace(" / ", "\n/").replace(" global ", "\nglobal ")
              for item in ordered]
    ix = np.arange(len(labels))
    futures_values = [item["futures"] for item in ordered]
    option_values = [item["call"] for item in ordered]
    fig, ax = plt.subplots(figsize=(11.5, 5.0))
    bars = ax.bar(ix, futures_values, width=0.58, color=BLUE, alpha=0.88,
                  label="Six-month futures (left axis)")
    ax.set_ylabel("Futures price (USD/lb)", color=BLUE)
    ax.tick_params(axis="y", labelcolor=BLUE)
    ax.set_xticks(ix, labels, fontsize=8.5)
    ax.set_ylim(0, max(futures_values) * 1.23)
    ax.grid(axis="y", alpha=0.40)
    ax.set_axisbelow(True)
    ax2 = ax.twinx()
    ax2.plot(ix, option_values, marker="o", markersize=8, linewidth=2.6,
             color=TEAL, label="Black-76 call (right axis)")
    ax2.set_ylabel("Call premium (USD/lb)", color=TEAL)
    ax2.tick_params(axis="y", labelcolor=TEAL)
    ax2.set_ylim(0, max(option_values) * 1.45)
    ax2.spines["top"].set_visible(False)
    ax.set_title("Illustrative market scenarios: futures and call valuation")
    handles_a, labels_a = ax.get_legend_handles_labels()
    handles_b, labels_b = ax2.get_legend_handles_labels()
    ax.legend(handles_a + handles_b, labels_a + labels_b, frameon=False, loc="upper left")
    save(fig, "02_market_scenarios", figures_dir)
    # 3 MC density
    terminals=sim.terminal_prices
    fig,ax=plt.subplots(figsize=(9,4))
    ax.hist(terminals,bins=75,color=TEAL,alpha=.84,density=True)
    ax.axvline(metrics["futures_usd_per_lb"],lw=2,color=CORAL,label="Cost-of-carry futures")
    ax.axvline(k,lw=1.8,color=BLUE,ls="--",label="Option strike")
    ax.set(xlabel="Simulated terminal price (USD/lb)",ylabel="Probability density",
           title="Monte Carlo: risk-neutral terminal price distribution")
    ax.grid(axis="y",alpha=.5);ax.legend(frameon=False)
    save(fig,"03_monte_carlo_distribution",figures_dir)
    # 4 sample path fanchart (paths span exactly T)
    paths=sample_price_paths(s,r,u,t,vol,steps=inputs["simulation_path_steps"],n_paths=45,seed=43,convenience_yield=y)
    tt=np.linspace(0,t,paths.shape[0])
    fig,ax=plt.subplots(figsize=(9,4))
    for i in range(paths.shape[1]):
        ax.plot(tt*12,paths[:,i],lw=.8,color=BLUE,alpha=.12)
    ax.plot(tt*12,paths.mean(axis=1),lw=2.5,color=TEAL,label="Mean of displayed paths")
    ax.axhline(s,ls="--",color=MUTED,lw=1)
    ax.set(xlabel="Months",ylabel="Simulated price (USD/lb)",title="45 illustrative simulated coffee price paths")
    ax.grid(alpha=.5);ax.legend(frameon=False)
    save(fig,"04_monte_carlo_paths",figures_dir)
    # 5 hedges costs
    prices=np.linspace(.65,1.7,160)
    value=[procurement_costs(float(p),qty,metrics["futures_usd_per_lb"],k,metrics["black76_call_usd_per_lb"]) for p in prices]
    fig,ax=plt.subplots(figsize=(9,4.2))
    for key,lab,col in [("no_hedge","Unhedged",CORAL),
                        ("long_futures","Long futures",BLUE),
                        ("long_call","Long call",TEAL)]:
        ax.plot(prices,[x[key]/1000 for x in value],label=lab,color=col,lw=2.4)
    ax.set(xlabel="Terminal coffee price (USD/lb)",ylabel="Procurement cost (USD thousands)",
           title="Coffee procurement costs: 100,000 lb under different hedges")
    ax.grid(alpha=.5);ax.legend(frameon=False)
    save(fig,"05_hedging_cost_comparison",figures_dir)
    # 6 note payoffs
    note=inputs["structured_note"];pc=note["principal"];cp=note["fixed_coupon_rate_six_months"];p=note["upside_participation"]
    prices=np.linspace(.65,1.8,120)
    fig,ax=plt.subplots(figsize=(9,4.1))
    ax.plot(prices,[structured_note_payoff(float(z),pc,cp,p,k) for z in prices],lw=2.7,color=TEAL,label="Contractual payoff")
    ax.axhline(pc,ls="--",color=MUTED,label="$100 principal")
    ax.axvline(k,color=CORAL,ls=":",label="Strike $1.25")
    ax.set(xlabel="Terminal coffee price (USD/lb)",ylabel="Payoff (USD per $100 principal)",
           title="Coffee-linked structured note: illustrative maturity payoff")
    ax.grid(alpha=.5);ax.legend(frameon=False)
    save(fig,"06_structured_note_payoff",figures_dir)
    # 7 market stress net cost (example)
    shocks=np.array([-.30,-.20,-.10,0,.10,.20,.30]); terminal=s*(1+shocks)
    costs=np.array([procurement_costs(float(z),qty,metrics["futures_usd_per_lb"],k,
                                        metrics["black76_call_usd_per_lb"])["no_hedge"] for z in terminal])
    fig,ax=plt.subplots(figsize=(9,4.1))
    ax.bar([f"{int(sh*100):+d}%" for sh in shocks],costs/1000,color=[CORAL if sh>0 else TEAL for sh in shocks])
    ax.axhline(s*qty/1000,color=BLUE,ls="--",label="Baseline cost")
    ax.set(xlabel="Spot price shock",ylabel="Procurement cost (USD thousands)",
           title="Stress test: unhedged coffee buyer")
    ax.grid(axis="y",alpha=.5);ax.set_axisbelow(True);ax.legend(frameon=False)
    save(fig,"07_stress_test",figures_dir)
