import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import numpy as np
from simulation_engine import NetworkSimulation

# 参数设置
N = 10
topology = 'fully_connected'
seed_count = 1
threshold = 0.5
max_steps = 50
n_repeats = 20
g_values = np.linspace(0.2, 3.0, 15)

print(f'N={N}, topology={topology}, seed_count={seed_count}, threshold={threshold}')
print(f'{"g":>6} {"mean":>8} {"std":>8}')
print('-' * 30)

results = []
for g in g_values:
    ratios = []
    for r in range(n_repeats):
        sim = NetworkSimulation(N=N, topology=topology, g=g, 
                                seed_count=seed_count, threshold=threshold,
                                max_steps=max_steps, seed=r)
        final_ratio = sim.run()
        ratios.append(final_ratio)
    mean_r = np.mean(ratios)
    std_r = np.std(ratios)
    results.append({'g': float(g), 'mean': float(mean_r), 'std': float(std_r)})
    print(f'{g:6.2f} {mean_r:8.4f} {std_r:8.4f}')

import json
out_path = HERE / 'm1_v2_results.json'
with open(out_path, 'w') as f:
    json.dump({'N': N, 'topology': topology, 'threshold': threshold,
               'seed_count': seed_count, 'results': results}, f, indent=2)
print(f'\nResults saved to {out_path}')
