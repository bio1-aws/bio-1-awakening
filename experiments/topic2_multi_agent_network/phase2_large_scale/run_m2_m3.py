import sys, json, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from parameter_scan import run_scan

# M2: 不同拓扑结构对比 (N=50, 4种拓扑)
print("="*60)
print("M2: 不同拓扑结构对比 (N=50)")
print("="*60)

topologies = ['fully_connected', 'random', 'small_world', 'scale_free']
g_values = np.linspace(0.2, 5.0, 25)

param_matrix_m2 = []
for topo in topologies:
    for g in g_values:
        param_matrix_m2.append({
            'N': 50,
            'topology': topo,
            'g': float(g),
            'seed_count': 1,
            'threshold': 0.5,
            'max_steps': 200
        })

print(f"参数组合数: {len(param_matrix_m2)}, 每组20次重复")
start = time.time()
results_m2 = run_scan(param_matrix_m2, n_repeats=20, n_workers=4)
print(f"耗时: {time.time()-start:.1f}s")

# 保存M2结果
with open(HERE / 'm2_topology_comparison.json', 'w') as f:
    json.dump(results_m2, f, indent=2)

# 打印M2摘要
print("\nM2结果摘要 (mean觉醒比例):")
print(f"{'g':>6}", end='')
for topo in topologies:
    print(f" {topo:>15}", end='')
print()
print("-" * (6 + 16*len(topologies)))

for i, g in enumerate(g_values):
    print(f"{g:6.2f}", end='')
    for topo in topologies:
        idx = topologies.index(topo) * len(g_values) + i
        r = results_m2[idx]
        print(f" {r['mean']:15.4f}", end='')
    print()

# M3: 大规模网络相变 (N=200, 500, 1000, scale_free)
print("\n" + "="*60)
print("M3: 大规模网络相变 (scale_free)")
print("="*60)

N_values = [200, 500, 1000]
g_values_m3 = np.linspace(0.5, 4.0, 20)

param_matrix_m3 = []
for N in N_values:
    for g in g_values_m3:
        param_matrix_m3.append({
            'N': N,
            'topology': 'scale_free',
            'g': float(g),
            'seed_count': 1,
            'threshold': 0.5,
            'max_steps': 300
        })

print(f"参数组合数: {len(param_matrix_m3)}, 每组10次重复")
start = time.time()
results_m3 = run_scan(param_matrix_m3, n_repeats=10, n_workers=4)
print(f"耗时: {time.time()-start:.1f}s")

# 保存M3结果
with open(HERE / 'm3_large_scale_phase.json', 'w') as f:
    json.dump(results_m3, f, indent=2)

# 打印M3摘要
print("\nM3结果摘要 (mean觉醒比例):")
print(f"{'g':>6}", end='')
for N in N_values:
    print(f" N={N:>5}", end='')
print()
print("-" * (6 + 9*len(N_values)))

for i, g in enumerate(g_values_m3):
    print(f"{g:6.2f}", end='')
    for j, N in enumerate(N_values):
        idx = j * len(g_values_m3) + i
        r = results_m3[idx]
        print(f" {r['mean']:8.4f}", end='')
    print()

print("\n✅ M2和M3测试完成！")
