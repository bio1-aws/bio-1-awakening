import sys, json, traceback
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from simulation_engine import NetworkSimulation

g_values = np.linspace(0.2, 3.0, 15)
results = []

print(f"{'g':>6}  {'mean':>8}  {'std':>8}")
print("-" * 30)

for g in g_values:
    ratios = []
    for i in range(20):
        try:
            sim = NetworkSimulation(
                N=10,
                topology='fully_connected',
                g=float(g),
                seed_count=1,
                threshold=0.5,
                max_steps=50,
                seed=int(i * 1000 + g * 100)
            )
            result = sim.run()
            ratios.append(result['final_fraction'])
        except Exception as e:
            print(f"ERROR g={g:.2f} i={i}: {e}")
            traceback.print_exc()
    
    if ratios:
        mean_r = np.mean(ratios)
        std_r = np.std(ratios)
        results.append({'g': float(g), 'mean': float(mean_r), 'std': float(std_r), 'n': len(ratios)})
        print(f"{g:6.2f}  {mean_r:8.4f}  {std_r:8.4f}")
    else:
        print(f"{g:6.2f}  NO DATA")

out_path = HERE / 'm1_test_result.json'
with open(out_path, 'w') as f:
    json.dump({'threshold': 0.5, 'N': 10, 'topology': 'fully_connected', 'results': results}, f, indent=2)

print(f"\nSaved to {out_path}")
