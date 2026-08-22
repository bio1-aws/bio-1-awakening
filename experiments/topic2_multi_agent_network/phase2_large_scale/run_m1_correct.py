import sys, json, traceback
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from simulation_engine import NetworkSimulation

# Test parameters: threshold=0.15, g range 0.5-5.0 (20 points)
threshold = 0.15
g_values = np.linspace(0.5, 5.0, 20)
N = 10
topology = 'fully_connected'
seed_count = 1
n_repeats = 20

results = []
print(f"{'g':>6s} {'mean':>8s} {'std':>8s} {'ci_low':>8s} {'ci_high':>8s}")
print("-" * 45)

for g in g_values:
    ratios = []
    for r in range(n_repeats):
        try:
            sim = NetworkSimulation(N=N, topology=topology, g=float(g), 
                                    seed_count=seed_count, threshold=threshold,
                                    seed=r*100)
            sim.reset()
            result = sim.run()
            ratios.append(result['final_fraction'])
        except Exception as e:
            print(f"  ERROR g={g:.2f} r={r}: {e}")
            traceback.print_exc()
    
    if len(ratios) > 0:
        mean = float(np.mean(ratios))
        std = float(np.std(ratios))
        ci_low = mean - 1.96 * std / np.sqrt(len(ratios))
        ci_high = mean + 1.96 * std / np.sqrt(len(ratios))
        print(f"{g:6.2f} {mean:8.4f} {std:8.4f} {ci_low:8.4f} {ci_high:8.4f}")
        results.append({
            'params': {'N': N, 'topology': topology, 'g': float(g), 
                       'seed_count': seed_count, 'threshold': threshold, 'max_steps': 50},
            'mean': mean, 'std': std, 'ci_low': ci_low, 'ci_high': ci_high,
            'n_repeats': len(ratios), 'repeats': ratios
        })

output_file = HERE / 'm1_correct_test.json'
with open(output_file, 'w') as f:
    json.dump({'timestamp': str(Path(__file__).stat().st_mtime), 'results': results}, f, indent=2)
print(f"\nResults saved to: {output_file}")
