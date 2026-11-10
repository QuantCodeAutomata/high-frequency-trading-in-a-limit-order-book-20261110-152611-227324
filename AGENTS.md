# AGENTS.md

Guide for coding agents and contributors working on this repository.

## What this repository implements

A replication of the Monte Carlo experiments in Section 3.3 ("Numerical
simulations") of Marco Avellaneda & Sasha Stoikov, "High-frequency trading in
a limit order book" (October 5, 2006): a market maker quoting around an
inventory-adjusted indifference price (Eqs. 3.17-3.18) is compared, over
1000 simulated price paths, to a benchmark that quotes the same spread
symmetrically around the mid-price, for three risk-aversion levels
(gamma = 0.1, 0.01, 0.5 — Tables 1-3, Figures 2-4). No external market data
is used: the experiments run entirely on simulated mid-price paths and
synthetic Poisson order arrivals.

## Layout

```
src/     closed-form quoting formulas (market_making.py), the Monte Carlo
         engine (simulation.py), table/JSON output (reporting.py), plots
         (visualization.py), and shared parameters (config.py)
data/    synthetic input generation: price shocks and order-arrival draws
         (generate_synthetic.py); no market data loader is needed
exp/     one script per experiment: exp1.py (gamma=0.1), exp2.py
         (gamma=0.01), exp3.py (gamma=0.5)
tests/   pytest unit tests for src/ and data/
results/ tables, summary JSON files and histogram plots written by the
         experiments, plus RESULTS.md
```

## Commands

Setup:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Tests:

```bash
python -m pytest
```

Experiments (run from the repository root):

```bash
python -m exp.exp1
python -m exp.exp2
python -m exp.exp3
```

Both the number of Monte Carlo paths and the random seed can be overridden,
e.g. `python -m exp.exp1 --n-paths 1000 --seed 20061005`; the paper's own
sample size (1000 paths per strategy) is already the default and is not
reduced anywhere in this repository.

`bash reproduce.sh` runs the tests followed by all three experiments.

## Conventions

- All experiment and simulation parameters live in `src/config.py` as
  module-level, upper-case variables, each with a comment naming its
  meaning, unit, and paper section. No parameter is hardcoded in `exp/` or
  `src/` modules.
- The Monte Carlo engine (`src/simulation.py`) and the quoting formulas
  (`src/market_making.py`) are the single shared implementation used by all
  three experiments; `exp/exp1.py`, `exp/exp2.py` and `exp/exp3.py` differ
  only in the `gamma` value they pass in.
- Synthetic random inputs (price shocks, order-arrival uniforms) are
  generated only in `data/generate_synthetic.py`; no experiment or `src/`
  module draws random numbers of its own.
- Tests run on small, deterministic configurations (synthetic inputs with a
  fixed seed) and check the paper's qualitative properties (signs, absence
  of look-ahead, shrinking of the inventory effect as gamma decreases), not
  only array shapes. Run the full suite with
  `python -m pytest`.
- No API keys are needed anywhere in this repository; it contains no
  `.env.example` because no external data service is used.
- Re-running the experiment commands overwrites the files in `results/`.
  After a rerun, the numbers and verdicts in `results/RESULTS.md` must be
  checked against the newly written `results/*_summary.json` and
  `results/*_table.csv` files and updated by hand if they changed.
