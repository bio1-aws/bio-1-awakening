import sys, traceback
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from simulation_engine import NetworkSimulation

sim = NetworkSimulation(N=10, topology='fully_connected', g=2.0, seed_count=1, threshold=0.5, seed=42)

print('=== 对象属性 ===')
print(dir(sim))
print()
print('=== __init__源码 ===')
import inspect
print(inspect.getsource(sim.__init__))
print()
print('=== step源码 ===')
print(inspect.getsource(sim.step))
