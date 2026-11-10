"""Experiment 3: inventory vs. symmetric strategy, gamma = 0.5 (paper Table 3, Figure 4).

A large gamma represents a very risk-averse investor: the inventory
strategy is expected to avoid accumulating inventory much more aggressively,
trading lower variance for lower mean profit. Run from the repository root
with: python -m exp.exp3
"""
from __future__ import annotations

import argparse
from pathlib import Path

from src import config
from src.reporting import save_experiment_outputs
from src.simulation import run_gamma_experiment
from src.visualization import plot_inventory_histograms, plot_profit_histograms

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
TAG = "exp3_gamma_0.5"


def main(gamma: float = config.GAMMA_EXP3, n_paths: int = config.N_PATHS, seed: int = config.SEED) -> dict:
    results = run_gamma_experiment(
        gamma=gamma, sigma=config.SIGMA, k=config.K, A=config.A, T=config.T, dt=config.DT,
        s0=config.S0, q0=config.Q0, n_paths=n_paths, seed=seed,
    )
    payload = save_experiment_outputs(TAG, gamma, results, RESULTS_DIR)

    plot_profit_histograms(
        results["inventory"].profit, results["symmetric"].profit, gamma,
        results["inventory"].spread, RESULTS_DIR / f"{TAG}_profit_hist.png",
    )
    plot_inventory_histograms(
        results["inventory"].final_inventory, results["symmetric"].final_inventory, gamma,
        RESULTS_DIR / f"{TAG}_inventory_hist.png",
    )

    table = Path(RESULTS_DIR / f"{TAG}_table.csv").read_text()
    print(f"Experiment 3 (gamma={gamma}) summary table:\n{table}")
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-paths", type=int, default=config.N_PATHS,
                         help="Number of Monte Carlo paths per strategy (paper: 1000)")
    parser.add_argument("--seed", type=int, default=config.SEED, help="Random seed")
    args = parser.parse_args()
    main(n_paths=args.n_paths, seed=args.seed)
