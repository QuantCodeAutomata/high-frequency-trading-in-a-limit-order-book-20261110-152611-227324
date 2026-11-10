"""Plots for the market-making Monte Carlo experiments.

Reproduces the profit-distribution histograms of Section 3.3 (Figures 2-4),
comparing the "inventory" and "symmetric" strategies for a given gamma.
matplotlib is used directly: no histogram/backtest-plot library in the
standard quantitative stack (vectorbt, quantstats) exposes a generic
two-sample P&L histogram, so this is a thin, direct matplotlib call rather
than a custom statistical routine.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def plot_profit_histograms(
    inventory_profit: np.ndarray,
    symmetric_profit: np.ndarray,
    gamma: float,
    spread: float,
    output_path: Path,
    n_bins: int = 25,
) -> None:
    """Overlaid histograms of final P&L for both strategies (paper Figures 2-4)."""
    combined = np.concatenate([inventory_profit, symmetric_profit])
    bin_edges = np.linspace(combined.min(), combined.max(), n_bins + 1)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(inventory_profit, bins=bin_edges, alpha=0.6, label="Inventory strategy", color="tab:blue")
    ax.hist(symmetric_profit, bins=bin_edges, alpha=0.6, label="Symmetric strategy", color="tab:orange")
    ax.set_title(f"P&L distribution, gamma = {gamma} (constant spread = {spread:.2f})")
    ax.set_xlabel("Final profit")
    ax.set_ylabel("Number of simulated paths")
    ax.legend()
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_inventory_histograms(
    inventory_final_q: np.ndarray,
    symmetric_final_q: np.ndarray,
    gamma: float,
    output_path: Path,
    n_bins: int = 25,
) -> None:
    """Overlaid histograms of final inventory q_T for both strategies."""
    combined = np.concatenate([inventory_final_q, symmetric_final_q])
    bin_edges = np.linspace(combined.min(), combined.max(), n_bins + 1)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(inventory_final_q, bins=bin_edges, alpha=0.6, label="Inventory strategy", color="tab:blue")
    ax.hist(symmetric_final_q, bins=bin_edges, alpha=0.6, label="Symmetric strategy", color="tab:orange")
    ax.set_title(f"Final inventory distribution, gamma = {gamma}")
    ax.set_xlabel("Final inventory q_T")
    ax.set_ylabel("Number of simulated paths")
    ax.legend()
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
