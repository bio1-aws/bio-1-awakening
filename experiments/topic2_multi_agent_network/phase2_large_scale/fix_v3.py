import sys, json
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from simulation_engine import NetworkSimulation

# parameters
N = 10
topology = 'fully_connected'
seed_count = 1
threshold = 0.5
n_repeats = 20
g_values = np.linspace(0.2, 3.0, 20)

results = []
print(f'{"g":>6} {"mean":>8} {"std":>8} {"ci_low":>8} {"ci_high":>8}')
print('-' * 45)

for g in g_values:
    ratios = []
    for r in range(n_repeats):
        sim = NetworkSimulation(N=N, topology=topology, g=float(g),
                                seed_count=seed_count, threshold=threshold,
                                seed=r*100)
        final_ratio = sim.run()
        ratios.append(final_ratio)
    mean_r = np.mean(ratios)
    std_r = np.std(ratios)
    ci = 1.96 * std_r / np.sqrt(n_repeats)
    results.append({'g': float(g), 'mean': float(mean_r), 'std': float(std_r),
                    'ci_low': float(mean_r-ci), 'ci_high': float(mean_r+ci)})
    print(f'{g:6.2f} {mean_r:8.4f} {std_r:8.4f} {mean_r-ci:8.4f} {mean_r+ci:8.4f}')

out_path = HERE / 'm1_v3_results.json'
with open(out_path, 'w') as f:
    json.dump({'N': N, 'topology': topology, 'threshold': threshold,
               'seed_count': seed_count, 'n_repeats': n_repeats,
               'results': results}, f, indent=2)
print(f'\nSaved to: {out_path}')
