"""
Network Simulation Engine
=========================
Core engine for multi-agent awakening dynamics on various network topologies.

Update rule:
    For each un-awakened agent i:
        if (fraction of awakened neighbors) * g >= threshold:
            agent i becomes awakened

Parameters:
    N           : int, number of nodes
    topology    : str, one of 'fully_connected', 'random', 'small_world', 'scale_free'
    g           : float, coupling strength
    seed_count  : int, initial number of awakened seeds
    threshold   : float, awakening threshold
    max_steps   : int, maximum simulation steps
"""

import networkx as nx
import numpy as np


class NetworkSimulation:
    """Discrete-time networked awakening simulation."""

    def __init__(self, N: int, topology: str, g: float,
                 seed_count: int = 1, threshold: float = 1.0,
                 max_steps: int = 200, seed: int | None = None):
        self.N = N
        self.topology = topology
        self.g = g
        self.seed_count = seed_count
        self.threshold = threshold
        self.max_steps = max_steps
        self.seed = seed
        self.rng = np.random.default_rng(seed)

        self.graph = self._build_graph()
        self._state: np.ndarray | None = None  # 0=asleep, 1=awakened
        self._history: list[float] = []
        self._newly_awakened: list[list[int]] = []

    # ------------------------------------------------------------------
    # topology builders
    # ------------------------------------------------------------------
    def _build_graph(self) -> nx.Graph:
        """Generate a NetworkX graph of the requested topology."""
        topo = self.topology.lower()
        n = self.N
        seed_int = int(self.rng.integers(0, 2**31 - 1))

        if topo == "fully_connected":
            return nx.complete_graph(n)

        if topo == "random":
            # Erdos-Renyi with average degree ~ 4 (tunable default)
            p = 4.0 / max(n - 1, 1)
            return nx.erdos_renyi_graph(n, p, seed=seed_int)

        if topo == "small_world":
            # Watts-Strogatz: k=4 neighbours, rewiring prob 0.1
            k = min(4, n - 1)
            k = max(k, 2)  # WS requires k >= 2
            return nx.watts_strogatz_graph(n, k=k, p=0.1, seed=seed_int)

        if topo == "scale_free":
            # Barabasi-Albert with m=2 attachments per new node
            m = min(2, n - 1)
            m = max(m, 1)
            return nx.barabasi_albert_graph(n, m=m, seed=seed_int)

        raise ValueError(f"Unknown topology: {self.topology}")

    # ------------------------------------------------------------------
    # simulation core
    # ------------------------------------------------------------------
    def reset(self):
        """Reset state and pick new random seeds."""
        self._state = np.zeros(self.N, dtype=np.int8)
        seeds = self.rng.choice(self.N, size=self.seed_count, replace=False)
        self._state[seeds] = 1
        self._history = [float(self._state.mean())]
        self._newly_awakened = [list(seeds.tolist())]

    def step(self) -> bool:
        """
        Advance the simulation by one step (synchronous update).
        Returns True if at least one new node awakened, False otherwise.
        """
        assert self._state is not None, "Call reset() before step()."

        new_state = self._state.copy()
        newly_awakened: list[int] = []

        # Precompute adjacency list for speed
        adj = {node: list(self.graph.neighbors(node))
               for node in range(self.N)}

        for i in range(self.N):
            if self._state[i] == 1:
                continue  # already awakened
            neighbors = adj[i]
            if len(neighbors) == 0:
                continue  # isolated node, never awakens
            awakened_neighbors = sum(int(self._state[j]) for j in neighbors)
            fraction = awakened_neighbors / len(neighbors)
            if fraction * self.g >= self.threshold:
                new_state[i] = 1
                newly_awakened.append(i)

        self._state = new_state
        self._history.append(float(self._state.mean()))
        self._newly_awakened.append(newly_awakened)

        return len(newly_awakened) > 0

    def run(self) -> dict:
        """
        Run the full simulation until convergence or max_steps.
        Returns a results dict with:
            - fraction_series : list[float], awakened fraction per step
            - final_fraction  : float
            - new_per_step    : list[list[int]], newly awakened nodes per step
            - steps           : int
            - converged       : bool
        """
        self.reset()
        converged = False
        steps = 0
        for _ in range(self.max_steps):
            changed = self.step()
            steps += 1
            if not changed:
                converged = True
                break
            if self._state.mean() >= 1.0:
                converged = True
                break

        return {
            "fraction_series": self._history,
            "final_fraction": float(self._state.mean()),
            "new_per_step": self._newly_awakened,
            "steps": steps,
            "converged": converged,
        }
