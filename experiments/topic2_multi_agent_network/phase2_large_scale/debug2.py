import sys, traceback
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from simulation_engine import NetworkSimulation

print('=== Test 1: Create simulation ===')
try:
    sim = NetworkSimulation(N=10, topology='fully_connected', seed_count=1, threshold=0.5, seed=42)
    print('Created OK')
    print('Methods:', [m for m in dir(sim) if not m.startswith('_')])
except Exception as e:
    print('Create ERROR:', e)
    traceback.print_exc()

print('\n=== Test 2: Run simulation ===')
try:
    result = sim.run(g=1.0)
    print('Run OK, result type:', type(result))
    print('Result:', result)
except Exception as e:
    print('Run ERROR:', e)
    traceback.print_exc()
