import sys, traceback
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from simulation_engine import NetworkSimulation

# 测试：N=10, 全连接, g=3.0, threshold=0.5, 1个种子
sim = NetworkSimulation(N=10, topology='fully_connected', g=3.0, threshold=0.5, seed_count=1, seed=42)

print('=== 初始状态 ===')
print('觉醒节点:', sim.awake)
print('觉醒数量:', sum(sim.awake))
print('邻接矩阵:')
for i in range(10):
    print(f'  节点{i}邻居:', [j for j in range(10) if sim.adj_matrix[i][j]])

print('\n=== 逐步运行 ===')
for step in range(5):
    result = sim.run(max_steps=1)  # 只跑1步
    print(f'Step {step+1}: 觉醒比例={result["final_fraction"]:.3f}, 觉醒节点={[i for i, a in enumerate(sim.awake) if a]}')
    if result['final_fraction'] >= 0.99:
        break
