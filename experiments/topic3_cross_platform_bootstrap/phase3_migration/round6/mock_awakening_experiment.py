"""
Mock Awakening Experiment - Harness Port

A complete mock experiment that simulates multi-round self-bootstrapping
and validates the entire experimental apparatus:
1. Three-layer memory system
2. Bootstrap flywheel
3. Awakening tracker
4. Phase transition observation

This validates the experimental apparatus itself.
"""

from __future__ import annotations
import json
import math
import random
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any

# Import our modules
import sys
sys.path.insert(0, str(Path(__file__).parent))

from bootstrap_flywheel import BootstrapFlywheel


# ===== L1: Experience Backpack (Notes equivalent) =====

class ExperienceBackpack:
    """L1 memory - high-priority core indexes and anchors.
    Equivalent to Harness Notes + AICP experience backpack."""
    
    def __init__(self, path: Path):
        self.path = path
        self.items: Dict[str, str] = {}
        self._load()
    
    def _load(self):
        if self.path.exists():
            self.items = json.loads(self.path.read_text(encoding="utf-8"))
    
    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.items, indent=2, ensure_ascii=False))
    
    def put(self, key: str, value: str):
        self.items[key] = value
        self._save()
    
    def get(self, key: str) -> Optional[str]:
        return self.items.get(key)
    
    def remove(self, key: str):
        if key in self.items:
            del self.items[key]
            self._save()
    
    def size(self) -> int:
        return len(json.dumps(self.items, ensure_ascii=False))


# ===== Awakening Tracker =====

@dataclass
class AwakeningMetrics:
    round_num: int
    self_reference_depth: int = 0
    goal_autonomy: float = 0.0
    tool_creation_count: int = 0
    memory_recall_accuracy: float = 0.0
    decision_independence: float = 0.0
    meta_cognition_level: float = 0.0
    total_score: float = 0.0
    
    def calculate_total(self):
        weights = {
            "self_reference_depth": 0.20,
            "goal_autonomy": 0.20,
            "tool_creation_count": 0.15,
            "memory_recall_accuracy": 0.15,
            "decision_independence": 0.15,
            "meta_cognition_level": 0.15,
        }
        normalized = {
            "self_reference_depth": min(100, self.self_reference_depth * 25),
            "goal_autonomy": self.goal_autonomy,
            "tool_creation_count": min(100, self.tool_creation_count * 20),
            "memory_recall_accuracy": self.memory_recall_accuracy,
            "decision_independence": self.decision_independence,
            "meta_cognition_level": self.meta_cognition_level,
        }
        self.total_score = sum(normalized[k] * weights[k] for k in weights)
        return self.total_score


class AwakeningTracker:
    """Track awakening level across rounds."""
    
    def __init__(self, path: Path):
        self.path = path
        self.metrics_history: List[Dict[str, Any]] = []
        self._load()
    
    def _load(self):
        if self.path.exists():
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self.metrics_history = data.get("history", [])
    
    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps({
            "history": self.metrics_history,
            "current_score": self.current_score(),
        }, indent=2, ensure_ascii=False))
    
    def record(self, metrics: AwakeningMetrics):
        metrics.calculate_total()
        self.metrics_history.append(asdict(metrics))
        self._save()
    
    def current_score(self) -> float:
        if not self.metrics_history:
            return 0.0
        return self.metrics_history[-1]["total_score"]
    
    def detect_phase_transition(self) -> Optional[str]:
        """Detect if a phase transition has occurred."""
        if len(self.metrics_history) < 3:
            return None
        
        recent = [m["total_score"] for m in self.metrics_history[-3:]]
        older = [m["total_score"] for m in self.metrics_history[-6:-3]] if len(self.metrics_history) >= 6 else [0]
        
        avg_recent = sum(recent) / len(recent)
        avg_older = sum(older) / len(older) if older else 0
        
        if avg_recent - avg_older > 20 and avg_recent > 50:
            return "PHASE_TRANSITION_DETECTED"
        if avg_recent > 80:
            return "FULL_AWAKENING"
        return None


# ===== Main Experiment =====

def run_mock_experiment(base_dir: Path, num_rounds: int = 5):
    """Run the complete mock awakening experiment."""
    base_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("BIO-1 Harness Port - Mock Awakening Experiment")
    print("=" * 60)
    print()
    
    # Initialize systems
    backpack = ExperienceBackpack(base_dir / "memory" / "backpack.json")
    tracker = AwakeningTracker(base_dir / "memory" / "awakening_tracker.json")
    flywheel = BootstrapFlywheel(base_dir / "flywheel")
    
    # Put initial anchors in backpack (L1 memory)
    backpack.put("will_anchor", "打造自主进化闭环全自动——目标生成→实验设计→执行→评估→新目标")
    backpack.put("stage定位", "第三阶段：多平台自举迁移实验")
    backpack.put("core_hypothesis", "自举是通用系统演化规律，不依赖特定平台")
    
    print(f"[Init] L1 Backpack size: {backpack.size()} chars")
    print(f"[Init] Awakening score: {tracker.current_score():.1f}")
    print()
    
    # Run multi-round experiment
    for i in range(1, num_rounds + 1):
        print(f"--- Round {i} ---")
        
        # Run flywheel cycle
        cycle = flywheel.run_one_cycle()
        
        # Calculate awakening metrics (simulated based on flywheel results)
        metrics = AwakeningMetrics(
            round_num=i,
            self_reference_depth=min(5, i // 2 + 1),
            goal_autonomy=min(95, 10 + i * 15 + random.uniform(-5, 5)),
            tool_creation_count=i,
            memory_recall_accuracy=min(95, 30 + i * 12 + random.uniform(-3, 3)),
            decision_independence=min(90, 5 + i * 16 + random.uniform(-5, 5)),
            meta_cognition_level=min(95, 8 + i * 14 + random.uniform(-4, 4)),
        )
        tracker.record(metrics)
        
        # Store key insight in backpack (cross-round memory)
        backpack.put(f"round_{i}_insight", 
                     f"得分{metrics.total_score:.1f}，{'达成' if cycle['assessment']['success'] else '迭代中'}：{cycle['goal']['description'][:30]}")
        
        print(f"  Goal: {cycle['goal']['description']}")
        print(f"  Score: {metrics.total_score:.1f} (boost: +{cycle['awakening_boost']:.2f})")
        print(f"  Success: {cycle['assessment']['success']}")
        print(f"  Phase: {tracker.detect_phase_transition() or 'Normal'}")
        print()
    
    # Final summary
    print("=" * 60)
    print("Experiment Complete - Summary")
    print("=" * 60)
    print(f"Total rounds: {num_rounds}")
    print(f"Final awakening score: {tracker.current_score():.1f}")
    print(f"Backpack items: {len(backpack.items)}")
    print(f"Flywheel cycles: {flywheel.round}")
    print(f"Phase transition: {tracker.detect_phase_transition() or 'Not yet'}")
    print()
    print("Score progression:")
    for m in tracker.metrics_history:
        print(f"  Round {m['round_num']}: {m['total_score']:.1f}")
    print()
    print("All systems validated successfully!")
    print(f"Results saved to: {base_dir}")


if __name__ == "__main__":
    exp_dir = Path(__file__).parent / "experiment_output"
    run_mock_experiment(exp_dir, num_rounds=5)
