"""
Communication Layer for Multi-Agent Network
Handles message passing: broadcast, peer-to-peer, and delay simulation.
"""
import random
from typing import Dict, List, Tuple
from agent_prototype import Agent


class CommunicationLayer:
    """Manages signal propagation between agents."""

    def __init__(self, agents: Dict[int, Agent], topology: str = "full",
                 signal_strength: float = 0.3, delay_steps: int = 0,
                 noise_std: float = 0.0):
        self.agents = agents
        self.signal_strength = signal_strength
        self.delay_steps = delay_steps
        self.noise_std = noise_std
        # message queue: key = step_to_deliver, value = list of (to_id, signal)
        self.message_queue: Dict[int, List[Tuple[int, float]]] = {}

    def broadcast_from(self, agent_id: int, current_step: int) -> int:
        """Broadcast signal from an awakened agent to all neighbors."""
        agent = self.agents[agent_id]
        if not agent.awakened:
            return 0

        signal = self._noisy_signal(self.signal_strength)
        deliver_step = current_step + self.delay_steps

        if deliver_step not in self.message_queue:
            self.message_queue[deliver_step] = []

        count = 0
        for neighbor_id in agent.neighbors:
            self.message_queue[deliver_step].append((neighbor_id, signal))
            count += 1
        return count

    def deliver_messages(self, step: int) -> int:
        """Deliver all messages queued for this step."""
        if step not in self.message_queue:
            return 0

        count = 0
        for to_id, signal in self.message_queue[step]:
            self.agents[to_id].receive_signal(signal)
            count += 1

        del self.message_queue[step]
        return count

    def _noisy_signal(self, base_signal: float) -> float:
        """Add Gaussian noise to signal if noise_std > 0."""
        if self.noise_std <= 0:
            return base_signal
        return max(0.0, base_signal + random.gauss(0, self.noise_std))

    def send_direct(self, from_id: int, to_id: int, signal: float, current_step: int) -> None:
        """Send a peer-to-peer message."""
        deliver_step = current_step + self.delay_steps
        if deliver_step not in self.message_queue:
            self.message_queue[deliver_step] = []
        self.message_queue[deliver_step].append((to_id, self._noisy_signal(signal)))

    def build_topology(self, topology: str = "full") -> None:
        """Build neighbor connections according to topology type."""
        ids = list(self.agents.keys())
        n = len(ids)

        if topology == "full":
            # Fully connected: every agent connected to every other
            for aid in ids:
                self.agents[aid].neighbors = [x for x in ids if x != aid]
        elif topology == "ring":
            for i, aid in enumerate(ids):
                left = ids[(i - 1) % n]
                right = ids[(i + 1) % n]
                self.agents[aid].neighbors = [left, right]
        elif topology == "random":
            # Random sparse graph, each agent connects to ~3 others
            import random
            for aid in ids:
                candidates = [x for x in ids if x != aid]
                k = min(3, len(candidates))
                self.agents[aid].neighbors = random.sample(candidates, k)
                # Make symmetric
                for nb in self.agents[aid].neighbors:
                    if aid not in self.agents[nb].neighbors:
                        self.agents[nb].neighbors.append(aid)
