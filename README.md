# Avellaneda-Stoikov Market Making Simulator

Python implementation of a market-making simulator inspired by the
Avellaneda-Stoikov framework for optimal bid and ask quoting under inventory
risk.

The project compares simple benchmark agents against an inventory-aware
Avellaneda-Stoikov style agent in a simulated limit order book environment.

## Motivation

Market makers quote both bid and ask prices. They earn the spread when orders
are filled, but they also accumulate inventory risk when buy and sell fills are
unbalanced.

The Avellaneda-Stoikov model adjusts quotes dynamically based on inventory,
volatility, time remaining, and risk aversion. The key idea is that a market
maker with positive inventory should quote more aggressively on the ask side and
less aggressively on the bid side, reducing inventory exposure.



## Quick Start
To run the experiment in python open the terminal, fist install the requirements by 
pip install -r requirements.txt
Then the experiment can be run by the command 
python run_experiment.py --nsims 1000
which creates the file simulation_results. By the command 

python run_experiment.py --nsims 1000
one can simulate the simulation done in simulation_results_example.pdf




## Repository Structure

```text
.
+-- src/
|   +-- config.py                # Simulation parameters
|   +-- market_makers.py         # Trading agent definitions
|   +-- simulator.py             # Main simulation loop
|   +-- stochastic_processes.py  # Price and order-arrival processes
+-- run_experiment.py            # Runs Monte Carlo experiment and creates report
+-- experiment_results/          # Generated CSV and plot outputs
+-- report.pdf                   # Generated PDF report
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
- `ASModelAgent`: inventory-aware Avellaneda-Stoikov style quoting to reduce risk

The current AS-style quote uses:

```python
spread = gamma * sigma**2 * (T - t) + 2 * log(1 + gamma / k) / gamma
skew = inventory * gamma * sigma**2 * (T - t) / T

bid_delta = spread / 2 + skew
ask_delta = spread / 2 - skew
```

## Model Components

### Mid-Price Process

For the fair market setting, the mid-price is simulated as a Brownian motion:

```python
S_t = S_0 + sigma * W_t
```

This is currently implemented in `src/stochastic_processes.py`.

The project also contains an experimental `insider` market condition. In this
mode, event jumps are added to the price path and order-arrival samples are
modified around jump events. This is still an early extension.

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

The current experiment table reports final PnL summary statistics by agent.
Inventory-risk metrics are a planned next step because the AS-style strategy is
primarily designed to manage inventory exposure, not simply maximize raw PnL in
every sample path.

## Current Limitations

-


## Reference

Avellaneda, M. and Stoikov, S. (2008). High-frequency trading in a limit order
book. Quantitative Finance, 8(3), 217-224.
