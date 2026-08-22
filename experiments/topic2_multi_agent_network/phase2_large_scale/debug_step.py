import sys, traceback
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from simulation_engine import NetworkSimulation

# N=10全连接，1个种子，g=3.0（最大），threshold=0.5
sim = NetworkSimulation(N=10, topology='fully_connected', g=3.0, seed_count=1, threshold=0.5, seed=42)

print('=== 所有属性 ===')
print(dir(sim))

print('\n=== 初始状态 ===')
if hasattr(sim, 'nodes'):
    print('nodes:', sim.nodes)
if hasattr(sim, 'states'):
    print('states:', sim.states)
if hasattr(sim, 'awake_nodes'):
    print('awake_nodes:', sim.awake_nodes)
if hasattr(sim, 'awake_count'):
    print('awake_count:', sim.awake_count)

print('\n=== 运行1步 ===')
try:
    result = sim.step()
    print('step result:', result)
except Exception as e:
    print('step error:', e)
    traceback.print_exc()

print('\n=== 1步后状态 ===')
if hasattr(sim, 'nodes'):
    print('nodes:', sim.nodes)
if hasattr(sim, 'states'):
    print('states:', sim.states)

print('\n=== 运行5步 ===')
for i in range(5):
    try:
        r = sim.step()
        print(f'step {i+2}: {r}')
    except Exception as e:
        print(f'step {i+2} error: {e}')
        break

print('\n=== 最终状态 ===')
if hasattr(sim, 'nodes'):
    print('nodes:', sim.nodes)
if hasattr(sim, 'states'):
    print('states:', sim.states)
