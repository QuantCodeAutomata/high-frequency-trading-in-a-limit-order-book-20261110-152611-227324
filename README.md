# High-Frequency Trading in a Limit Order Book — Replication

Marco Avellaneda & Sasha Stoikov, "High-frequency trading in a limit order
book" (October 5, 2006).

This repository reproduces the Monte Carlo simulations of Section 3.3
("Numerical simulations") of the paper: a market maker quoting bid and ask
prices around an inventory-adjusted indifference (reservation) price is
compared, over 1000 simulated price paths, to a benchmark that quotes the
same spread symmetrically around the mid-price. Three risk-aversion levels
are reproduced:

* `exp1` — gamma = 0.1 (Table 1, Figure 2)
* `exp2` — gamma = 0.01, close to risk-neutral (Table 2, Figure 3)
* `exp3` — gamma = 0.5, highly risk-averse (Table 3, Figure 4)

No market data is used: the experiments rely entirely on simulated mid-price
paths and synthetic Poisson order arrivals, as stated in Section 3.3.

## Repository layout

```
src/    closed-form quoting formulas and the Monte Carlo simulation engine
data/   synthetic input generation (price shocks, order-arrival draws)
exp/    one script per experiment (exp1, exp2, exp3)
tests/  pytest unit tests for src/ and data/
results/ tables, summary JSON files and histogram plots written by the experiments
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

No API keys are required: this replication uses no external market data.

## Running the tests

```bash
python -m pytest
```

## Running the experiments

From the repository root:

```bash
python -m exp.exp1
python -m exp.exp2
python -m exp.exp3
```

Each script runs 1000 Monte Carlo paths per strategy (the paper's sample
size, Section 3.3), prints the summary table, and writes to `results/`:

* `expN_gamma_<g>_table.csv` — the Table 1/2/3-style summary
* `expN_gamma_<g>_summary.json` — the same summary in machine-readable form
* `expN_gamma_<g>_profit_hist.png` — overlaid P&L histograms (Figures 2-4)
* `expN_gamma_<g>_inventory_hist.png` — overlaid final-inventory histograms

The number of paths and the random seed can be overridden, e.g.
`python -m exp.exp1 --n-paths 1000 --seed 20061005`.

## Reproduce everything

```bash
bash reproduce.sh
```

runs the test suite followed by the three experiments.

See `results/RESULTS.md` for the comparison against the paper's reported
values, deviations, and unreproduced items.
