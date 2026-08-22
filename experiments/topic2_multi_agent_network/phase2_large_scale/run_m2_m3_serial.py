import sys, json, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from simulation_engine import NetworkSimulation

def run_serial_scan(param_matrix, n_repeats=10, base_seed=42):
    """串行运行参数扫描，避免多进程问题"""
    rng = np.random.default_rng(base_seed)
    results = []
    
    for p_idx, params in enumerate(param_matrix):
        fractions = []
        for r in range(n_repeats):
            seed = int(rng.integers(0, 2**31 - 1))
            sim = NetworkSimulation(
                N=params["N"],
                topology=params["topology"],
                g=params["g"],
                seed_count=params.get("seed_count", 1),
                threshold=params.get("threshold", 0.5),
                max_steps=params.get("max_steps", 200),
                seed=seed,
            )
            result = sim.run()
            fractions.append(result["final_fraction"])
        
        arr = np.array(fractions)
        results.append({
            "params": params,
            "mean": float(arr.mean()),
            "std": float(arr.std(ddof=1)) if len(arr) > 1 else 0.0,
            "n": len(arr),
        })
        print(f"  [{p_idx+1}/{len(param_matrix)}] g={params['g']:.2f} mean={arr.mean():.3f}")
    
    return results

# ============================================================
# M2: 不同拓扑结构对比 (N=50)
# ============================================================
print("="*60)
print("M2: 不同拓扑结构对比 (N=50, threshold=0.5)")
print("="*60)

topologies = ["fully_connected", "small_world", "scale_free", "random"]
g_values = np.linspace(0.2, 5.0, 25)

param_matrix_m2 = []
for topo in topologies:
    for g in g_values:
        param_matrix_m2.append({"N": 50, "topology": topo, "g": float(g), "threshold": 0.5})

print(f"参数组合数: {len(param_matrix_m2)}, 每组10次重复")
t0 = time.time()
results_m2 = run_serial_scan(param_matrix_m2, n_repeats=10)
print(f"耗时: {time.time()-t0:.1f}s")

# 保存结果
with open(HERE / "m2_results.json", "w") as f:
    json.dump(results_m2, f, indent=2)

# 输出摘要表格
print("\n" + "="*60)
print("M2结果摘要 (觉醒比例 mean)")
print("="*60)
header = f"{'g':>6}" + "".join(f"{t:>15}" for t in topologies)
print(header)
print("-" * len(header))

for i, g in enumerate(g_values):
    row = f"{g:6.2f}"
    for j, topo in enumerate(topologies):
        idx = j * len(g_values) + i
        row += f"{results_m2[idx]['mean']:15.3f}"
    print(row)

# ============================================================
# M3: 大规模网络相变 (全连接，不同N)
# ============================================================
print("\n" + "="*60)
print("M3: 大规模网络相变 (全连接, threshold=0.5)")
print("="*60)

N_values = [50, 100, 200, 500]
g_values_m3 = np.linspace(0.2, 3.0, 15)

param_matrix_m3 = []
for N in N_values:
    for g in g_values_m3:
        param_matrix_m3.append({"N": N, "topology": "fully_connected", "g": float(g), "threshold": 0.5})

print(f"参数组合数: {len(param_matrix_m3)}, 每组5次重复")
t0 = time.time()
results_m3 = run_serial_scan(param_matrix_m3, n_repeats=5)
print(f"耗时: {time.time()-t0:.1f}s")

# 保存结果
with open(HERE / "m3_results.json", "w") as f:
    json.dump(results_m3, f, indent=2)

# 输出摘要表格
print("\n" + "="*60)
print("M3结果摘要 (觉醒比例 mean)")
print("="*60)
header = f"{'g':>6}" + "".join(f"{'N='+str(N):>10}" for N in N_values)
print(header)
print("-" * len(header))

for i, g in enumerate(g_values_m3):
    row = f"{g:6.2f}"
    for j, N in enumerate(N_values):
        idx = j * len(g_values_m3) + i
        row += f"{results_m3[idx]['mean']:10.3f}"
    print(row)

print("\nDone!")
