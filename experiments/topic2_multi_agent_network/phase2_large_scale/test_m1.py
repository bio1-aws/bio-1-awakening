"""
Quick validation test for Phase 2 M1 milestone.
Runs N=10, fully-connected, g from 0.1 to 1.0.
Saves output to phase2_m1_test_v2.json.
"""

import sys
from pathlib import Path

# Ensure the local package is importable
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from parameter_scan import run_scan, save_results


def main():
    N = 10
    topology = "fully_connected"
    g_values = [round(0.1 * i, 1) for i in range(1, 11)]  # 0.1..1.0

    param_matrix = [
        {"N": N, "topology": topology, "g": g,
         "seed_count": 1, "threshold": 1.0, "max_steps": 50}
        for g in g_values
    ]

    results = run_scan(param_matrix, n_repeats=20, n_workers=4, base_seed=42)

    out_path = HERE / "phase2_m1_test_v2.json"
    save_results(results, out_path)

    # Print summary table
    print(f"{'g':>5s}  {'mean':>8s}  {'std':>8s}  {'ci_low':>8s}  {'ci_high':>8s}")
    print("-" * 45)
    for r in results:
        g = r["params"]["g"]
        print(f"{g:5.2f}  {r['mean']:8.4f}  {r['std']:8.4f}  "
              f"{r['ci_low']:8.4f}  {r['ci_high']:8.4f}")

    print(f"\nResults saved to: {out_path}")


if __name__ == "__main__":
    main()
