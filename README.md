# Avellaneda-Stoikov Market Making Simulator

Educational Python implementation of a market-making simulator inspired by the
Avellaneda-Stoikov framework for optimal bid and ask quoting under inventory
risk.

The project compares simple benchmark agents against an inventory-aware
Avellaneda-Stoikov style agent in a simulated limit order book environment.

## Project Status

This project is in an early but runnable stage. The core simulator, stochastic
price process, and trading agents are separated into Python modules under
`src/`, with exploratory analysis in Jupyter notebooks.

Current focus:

- simulate a mid-price process using Brownian motion
- model order arrivals with distance-dependent fill intensity
- compare constant, symmetric, and inventory-aware quoting agents
- track cash, inventory, total portfolio value, and exponential utility

## Motivation

Market makers quote both bid and ask prices. They earn the spread when orders
are filled, but they also accumulate inventory risk when buy and sell fills are
unbalanced.

The Avellaneda-Stoikov model adjusts quotes dynamically based on inventory,
volatility, time remaining, and risk aversion. The key idea is that a market
maker with positive inventory should quote more aggressively on the ask side and
less aggressively on the bid side, reducing inventory exposure.

## Repository Structure

```text
.
+-- src/
|   +-- config.py                # Simulation parameters
|   +-- market_makers.py         # Trading agent definitions
|   +-- simulator.py             # Main simulation loop
|   +-- stochastic_processes.py  # Price and order-arrival processes
+-- 02_Simulation.ipynb          # Main exploratory simulation notebook
+-- Playground_Avellaneda...ipynb# Early exploratory notebook
+-- main.py                      # Placeholder script
```

## Trading Agents

The simulator is designed around a common agent interface:

```python
class TradingAgent:
    def quote(self, state: MarketState) -> tuple[float, float]:
        """Return bid_delta, ask_delta."""
```

Implemented agents:

- `ConstantSpreadAgent`: fixed bid and ask deltas
- `SymmetricAgent`: Avellaneda-Stoikov spread without inventory skew
- `ASModelAgent`: inventory-aware Avellaneda-Stoikov style quoting

The current AS-style quote uses:

```python
spread = gamma * sigma**2 * (T - t) + 2 * log(1 + gamma / k) / gamma
skew = inventory * gamma * sigma**2 * (T - t) / T

bid_delta = spread / 2 + skew
ask_delta = spread / 2 - skew
```

## Quick Start

Create and activate a virtual environment, then install the basic dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install numpy matplotlib jupyter
```

Run the notebook:

```powershell
jupyter notebook 02_Simulation.ipynb
```

Or run a small simulation directly from Python:

```python
import numpy as np

from src.config import SimParams
from src import stochastic_processes
from src.simulator import simulation
from src.market_makers import ConstantSpreadAgent, SymmetricAgent, ASModelAgent

np.random.seed(42)

params = SimParams()
prices = stochastic_processes.BM_stock(
    params.S0,
    params.m,
    params.T,
    mu=0,
    sigma=params.sigma,
)

ask_orders = stochastic_processes.buys(params.T, params.m)
bid_orders = stochastic_processes.buys(params.T, params.m)

agents = {
    "constant": ConstantSpreadAgent(bid_delta=1.0, ask_delta=1.0),
    "symmetric": SymmetricAgent(),
    "avellaneda_stoikov": ASModelAgent(),
}

for name, agent in agents.items():
    result = simulation(params, prices, ask_orders, bid_orders, agent)
    final_pnl = result["TotalValue"][-1] - params.money
    final_inventory = result["q_stocks"][-1]
    print(f"{name:20s} pnl={final_pnl:8.2f} inventory={final_inventory:5.1f}")
```

## Model Components

### Mid-Price Process

The mid-price is simulated as a Brownian motion:

```python
S_t = S_0 + sigma * W_t
```

This is currently implemented in `src/stochastic_processes.py`.

### Fill Intensity

Order-fill intensity decreases exponentially with the distance between the
quoted price and the mid-price:

```python
lambda(delta) = A * exp(-k * delta)
```

where:

- `A` controls baseline order arrival intensity
- `k` controls how quickly fill probability decreases with quote distance
- `delta` is the bid or ask distance from the mid-price

### Portfolio Value

The simulator tracks:

```python
portfolio_value = cash + inventory * mid_price
```

It also computes exponential utility:

```python
utility = -exp(-gamma * pnl)
```

## Current Limitations

- The project is still research/prototype code rather than a packaged library.
- There is not yet a command-line experiment runner.
- There are no automated tests yet.
- The execution model is simplified and does not use real order book data.
- Transaction costs, latency, queue position, and adverse selection are not yet
  modeled.
- `main.py` is still a placeholder and should be replaced or removed before
  publishing.

## Roadmap

Planned technical improvements:

- add `requirements.txt` or `pyproject.toml`
- add `.gitignore` for `.venv/`, `.idea/`, caches, and notebook checkpoints
- add tests for agents, quote behavior, and simulator output shapes
- add a reproducible experiment script, for example `python -m src.run_experiment`
- add summary metrics: mean PnL, PnL standard deviation, utility, inventory risk
- clean naming and docstrings across the codebase
- add plots and result tables to the README
- compare results against the qualitative findings from the Avellaneda-Stoikov
  paper

## Reference

Avellaneda, M. and Stoikov, S. (2008). High-frequency trading in a limit order
book. Quantitative Finance, 8(3), 217-224.
