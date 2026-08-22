import sys, traceback
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

try:
    from simulation_engine import NetworkSimulation
    print('Import OK')
    
    sim = NetworkSimulation(N=10, topology='fully_connected', g=1.0,
                            seed_count=1, threshold=0.5, max_steps=50, random_seed=0)
    print('Sim created OK')
    print(f'Initial awakened: {sim.awakened}')
    print(f'Initial ratio: {sim.get_awakened_ratio()}')
    
    sim.run()
    print(f'After run awakened: {sim.awakened}')
    print(f'After run ratio: {sim.get_awakened_ratio()}')
    print(f'Steps taken: {sim.step}')
    
except Exception as e:
    print(f'ERROR: {e}')
    traceback.print_exc()
