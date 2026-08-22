import sys, traceback
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from simulation_engine import NetworkSimulation

sim = NetworkSimulation(N=10, topology='fully_connected', g=2.0, seed_count=1, threshold=0.5, seed=42)

print('=== reset前 ===')
print('_state:', sim._state if hasattr(sim, '_state') else 'NO _state')
print('_newly_awakened:', sim._newly_awakened if hasattr(sim, '_newly_awakened') else 'NO')
print('_history:', sim._history if hasattr(sim, '_history') else 'NO')

sim.reset()

print('\n=== reset后 ===')
print('_state type:', type(sim._state))
print('_state:', sim._state)
print('_state sum (觉醒数):', sum(sim._state))
print('_newly_awakened:', sim._newly_awakened)

# 手动执行一步，看中间过程
print('\n=== 执行step 1 ===')
try:
    # 先看step方法源码
    import inspect
    print('step方法源码:')
    print(inspect.getsource(sim.step))
except Exception as e:
    print('getsource error:', e)

print('\n=== 逐步执行 ===')
for i in range(5):
    before = sum(sim._state)
    result = sim.step()
    after = sum(sim._state)
    print(f'Step {i+1}: 觉醒数 {before} -> {after}, newly={result.get("newly_awakened", "?")}, done={result.get("done", "?")}')
    if result.get('done'):
        print('已收敛，停止')
        break

print('\n=== 最终状态 ===')
print('final_fraction:', sum(sim._state) / len(sim._state))
