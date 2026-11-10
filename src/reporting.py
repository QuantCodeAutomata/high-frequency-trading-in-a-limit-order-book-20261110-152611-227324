"""Tabular and file-output helpers shared by the three experiment scripts."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.simulation import SimulationResult, summarize

TABLE_COLUMNS = ["Strategy", "Spread", "Profit", "std(Profit)", "Final q", "std(Final q)"]


def build_summary_table(results: dict[str, SimulationResult]) -> pd.DataFrame:
    """Build the Table-1/2/3-style summary DataFrame for one gamma value."""
    rows = []
    for strategy in ("inventory", "symmetric"):
        s = summarize(results[strategy])
        rows.append({
            "Strategy": strategy.capitalize(),
            "Spread": round(s["spread"], 2),
            "Profit": round(s["profit_mean"], 2),
            "std(Profit)": round(s["profit_std"], 2),
            "Final q": round(s["final_q_mean"], 2),
            "std(Final q)": round(s["final_q_std"], 2),
        })
    return pd.DataFrame(rows, columns=TABLE_COLUMNS)


def save_experiment_outputs(
    tag: str,
    gamma: float,
    results: dict[str, SimulationResult],
    results_dir: Path,
) -> dict:
    """Persist the summary table (CSV) and raw per-path metrics (JSON) for one experiment."""
    results_dir.mkdir(parents=True, exist_ok=True)
    table = build_summary_table(results)
    table.to_csv(results_dir / f"{tag}_table.csv", index=False)

    payload = {
        "gamma": gamma,
        "n_paths": int(results["inventory"].profit.shape[0]),
        "summary": {name: summarize(res) for name, res in results.items()},
    }
    (results_dir / f"{tag}_summary.json").write_text(json.dumps(payload, indent=2))
    return payload
