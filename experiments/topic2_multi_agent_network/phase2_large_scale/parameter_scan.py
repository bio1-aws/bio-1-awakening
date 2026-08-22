"""
Parameter Scan Module
=====================
Runs NetworkSimulation over a matrix of parameter combinations,
with multiple repeats for statistical robustness.

Results are collected with mean / std / 95% confidence interval
of the final awakened fraction, and optionally the full time series.
"""

import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np

from simulation_engine import NetworkSimulation


# ----------------------------------------------------------------------
# helper that runs one simulation (must be top-level for pickling)
# ----------------------------------------------------------------------
def _single_run(params: dict, repeat_seed: int) -> dict:
    """Run a single simulation repeat and return its final fraction."""
    sim = NetworkSimulation(
        N=params["N"],
        topology=params["topology"],
        g=params["g"],
        seed_count=params.get("seed_count", 1),
        threshold=params.get("threshold", 1.0),
        max_steps=params.get("max_steps", 200),
        seed=repeat_seed,
    )
    result = sim.run()
    return {"final_fraction": result["final_fraction"],
            "steps": result["steps"],
            "converged": result["converged"]}


# ----------------------------------------------------------------------
# public API
# ----------------------------------------------------------------------
def run_scan(param_matrix: list[dict], n_repeats: int = 20,
             n_workers: int | None = None,
             base_seed: int = 42) -> list[dict]:
    """
    Run a parameter scan.

    Args:
        param_matrix : list of parameter dicts (each gets n_repeats runs)
        n_repeats    : number of independent repeats per parameter set
        n_workers    : number of parallel workers (None = cpu_count)
        base_seed    : master seed for repeat seeds

    Returns:
        list of result dicts, one per parameter set, with keys:
            params, mean, std, ci_low, ci_high, n, repeats
    """
    rng = np.random.default_rng(base_seed)

    # Build all tasks
    tasks = []
    for p_idx, params in enumerate(param_matrix):
        for r in range(n_repeats):
            seed = int(rng.integers(0, 2**31 - 1))
            tasks.append((p_idx, params, seed))

    results: list[dict] = [{"params": p, "repeats": []} for p in param_matrix]

    with ProcessPoolExecutor(max_workers=n_workers) as pool:
        future_map = {
            pool.submit(_single_run, params, seed): p_idx
            for p_idx, params, seed in tasks
        }
        for future in as_completed(future_map):
            p_idx = future_map[future]
            single = future.result()
            results[p_idx]["repeats"].append(single["final_fraction"])

    # Compute statistics
    out = []
    for entry in results:
        arr = np.array(entry["repeats"])
        n = len(arr)
        mean = float(arr.mean())
        std = float(arr.std(ddof=1)) if n > 1 else 0.0
        # 95% CI via t-distribution (approx with 1.96 for n>=20)
        ci = 1.96 * std / np.sqrt(n) if n > 1 else 0.0
        out.append({
            "params": entry["params"],
            "mean": mean,
            "std": std,
            "ci_low": mean - ci,
            "ci_high": mean + ci,
            "n_repeats": n,
            "repeats": entry["repeats"],
        })

    return out


def save_results(results: list[dict], path: str | Path):
    """Save scan results to a JSON file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    serializable = []
    for r in results:
        entry = {
            "params": r["params"],
            "mean": r["mean"],
            "std": r["std"],
            "ci_low": r["ci_low"],
            "ci_high": r["ci_high"],
            "n_repeats": r["n_repeats"],
            "repeats": r["repeats"],
        }
        serializable.append(entry)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": serializable,
        }, f, indent=2, ensure_ascii=False)
    return path
