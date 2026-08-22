
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from parameter_scan import run_scan

# 快速测试5组参数x2次重复
import numpy as np
g_vals = np.linspace(0.2, 5.0, 5)
params = [{'N': 50, 'topology': 'scale_free', 'g': float(g), 'seed_count': 1, 'threshold': 0.5, 'max_steps': 200} for g in g_vals]

t0 = time.time()
results = run_scan(params, n_repeats=2, n_workers=4)
t1 = time.time()
total = t1 - t0
per_sim = total / (5 * 2)
print(f"总耗时: {total:.2f}s, 单次模拟约: {per_sim:.3f}s")
print(f"M2(100组x20次)预估: {per_sim*100*20:.1f}s")
print(f"M3(60组x10次)预估: {per_sim*60*10:.1f}s")
