import json
import numpy as np
from pathlib import Path
from simulation_engine import NetworkSimulation

def single_run(params, repeat_seed):
    sim = NetworkSimulation(
        N=params["N"],
        topology=params["topology"],
        g=params["g"],
        seed_count=params.get("seed_count", 1),
        threshold=params.get("threshold", 0.5),
        max_steps=params.get("max_steps", 200),
        seed=repeat_seed,
    )
    result = sim.run()
    return result["final_fraction"]

def run_serial(param_matrix, n_repeats, base_seed=42):
    rng = np.random.default_rng(base_seed)
    results = []
    for p_idx, params in enumerate(param_matrix):
        repeats = []
        for r in range(n_repeats):
            seed = int(rng.integers(0, 2**31 - 1))
            repeats.append(single_run(params, seed))
        arr = np.array(repeats)
        results.append({
            "params": params,
            "mean": float(arr.mean()),
            "std": float(arr.std(ddof=1)) if len(arr) > 1 else 0.0,
            "n": len(arr),
            "repeats": repeats,
        })
        print(f"  [{p_idx+1}/{len(param_matrix)}] N={params['N']} g={params['g']:.2f} mean={arr.mean():.4f}")
    return results

# M3 v2: 小世界网络，不同规模的相变
print("="*70)
print("M3 v2: 小世界网络大规模相变 (threshold=0.5)")
print("="*70)

network_sizes = [50, 100, 200, 500]
g_values = [round(0.2 + i*0.15, 2) for i in range(20)]  # 0.2 to 3.05
n_repeats = 10

param_matrix_m3 = []
for N in network_sizes:
    for g in g_values:
        param_matrix_m3.append({"N": N, "topology": "small_world", "g": g, "threshold": 0.5})

print(f"参数组合数: {len(param_matrix_m3)}, 每组{n_repeats}次重复")
results_m3 = run_serial(param_matrix_m3, n_repeats=n_repeats, base_seed=123)

# 保存结果
with open("m3_v2_results.json", "w") as f:
    json.dump(results_m3, f, indent=2)

# 分析
print("\n" + "="*70)
print("M3 v2 结果摘要 (小世界网络, 觉醒比例 mean)")
print("="*70)
print(f"{'g':>6}", end="")
for N in network_sizes:
    print(f"{f'N={N}':>12}", end="")
print()
print("-" * (6 + 12*len(network_sizes)))

for g in g_values:
    print(f"{g:6.2f}", end="")
    for N in network_sizes:
        key = (N, g)
        val = next((r["mean"] for r in results_m3 if r["params"]["N"]==N and abs(r["params"]["g"]-g)<0.001), 0)
        print(f"{val:12.4f}", end="")
    print()

# 临界g值分析
print("\n" + "="*70)
print("M3 v2 临界g值与相变陡度")
print("="*70)
for N in network_sizes:
    means = [(r["params"]["g"], r["mean"]) for r in results_m3 if r["params"]["N"]==N]
    means.sort()
    # 找临界g（mean>0.5）
    g_crit = None
    for g, m in means:
        if m > 0.5:
            g_crit = g
            break
    # 相变宽度（0.1到0.9的g差）
    g_01 = next((g for g, m in means if m > 0.1), None)
    g_09 = next((g for g, m in means if m > 0.9), None)
    width = g_09 - g_01 if g_01 and g_09 else None
    print(f"N={N:4d}: 临界g={g_crit}, 相变宽度(0.1-0.9)={width}")

# 有限尺寸标度：临界g随N的变化
print("\n" + "="*70)
print("有限尺寸标度分析: g_c(N) ~ N^(-1/nu)")
print("="*70)
print("如果 g_c 随 N 增大而减小，说明大网络更容易传播（小世界效应）")
print("如果 g_c 随 N 增大而增大，说明大网络更难传播（稀释效应）")

print("\nDone. Results saved to m3_v2_results.json")
