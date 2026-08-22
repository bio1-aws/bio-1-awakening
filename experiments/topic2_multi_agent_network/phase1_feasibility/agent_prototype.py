"""
Agent Prototype for Topic 2: Multi-Agent Awakening Network
Minimal agent class with awakening state, threshold, neighbors, and signal processing.
"""
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Agent:
    agent_id: int
    threshold: float = 0.5  # awakening threshold
    activation: float = 0.0  # current activation level
    awakened: bool = False
    neighbors: List[int] = field(default_factory=list)
    received_signals: List[float] = field(default_factory=list)
    awaken_step: Optional[int] = None  # step when agent awakened

    def receive_signal(self, signal_strength: float) -> None:
        """Receive a signal from a neighbor."""
        self.received_signals.append(signal_strength)

    def update_state(self, step: int, decay: float = 0.1) -> bool:
        """
        Update activation based on received signals and decay.
        Returns True if agent awakens in this step.
        """
        if self.awakened:
            self.received_signals.clear()
            return False

        # Sum incoming signals, apply decay to existing activation
        total_input = sum(self.received_signals)
        self.activation = max(0.0, self.activation * (1 - decay) + total_input)
        self.received_signals.clear()

        if self.activation >= self.threshold:
            self.awakened = True
            self.awaken_step = step
            return True
        return False

    def output_signal(self) -> float:
        """Signal strength sent to neighbors when awakened."""
        return 1.0 if self.awakened else 0.0

    def reset(self) -> None:
        """Reset agent to initial state."""
        self.activation = 0.0
        self.awakened = False
        self.received_signals.clear()
        self.awaken_step = None
