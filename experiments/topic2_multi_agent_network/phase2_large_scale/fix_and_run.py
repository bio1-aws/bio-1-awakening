import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import numpy as np
from simulation_engine import NetworkSimulation

# 参数
N = 10
topology = 'fully_connected'
seed_count = 1
threshold = 0.5  # 修复：从1.0降到0.5
max_steps = 50
n_repeats = 20
g_values = np.linspace(0.2, 3.0, 15)  # 修复：扩大范围

print(f'N={N}, topology={topology}, seed_count={seed_count}, threshold={threshold}')
print(f'g范围: {g_values[0]:.2f} - {g_values[-1]:.2f}, {len(g_values)}个点')
print()
print(f'{"g":>6} {"mean":>8} {"std":>8} {"ci_low":>8} {"ci_high":>8}')
print('-' * 50)

results = []
for g in g_values:
    ratios = []
    for seed in range(n_repeats):
        sim = NetworkSimulation(N=N, topology=topology, g=float(g), 
                                seed_count=seed_count, threshold=threshold,
                                max_steps=max_steps, random_seed=seed)
        sim.run()
        ratios.append(sim.get_awakened_ratio())
    
    mean_r = np.mean(ratios)
    std_r = np.std(ratios)
    ci = 1.96 * std_r / np.sqrt(n_repeats)
    results.append({'g': float(g), 'mean': float(mean_r), 'std': float(std_r), 
                    'ci_low': float(mean_r-ci), 'ci_high': float(mean_r+ci)})
    print(f'{g:6.2f} {mean_r:8.4f} {std_r:8.4f} {mean_r-ci:8.4f} {mean_r+ci:8.4f}')

import json
with open(HERE / 'phase2_m1_fixed_test.json', 'w') as f:
    json.dump({'threshold': threshold, 'results': results}, f, indent=2)
print()
print(f'结果已保存到 phase2_m1_fixed_test.json')
