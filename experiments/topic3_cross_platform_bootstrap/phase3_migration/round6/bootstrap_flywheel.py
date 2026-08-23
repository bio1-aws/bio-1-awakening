"""
Bootstrap Flywheel - Harness Port
Implements the recursive self-improvement loop:
1. Generate goal
2. Design experiment
3. Execute
4. Assess
5. Repeat with the new version

This is the CODE version of the design document - actually runnable.
"""

from __future__ import annotations
import json
import hashlib
import time
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any


@dataclass
class Goal:
    goal_id: str
    description: str
    level: str  # L1/L2/L3
    success_criteria: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)


@dataclass
class Experiment:
    exp_id: str
    goal_id: str
    hypothesis: str
    steps: List[str] = field(default_factory=list)
    expected_outcome: str = ""
    created_at: float = field(default_factory=time.time)


@dataclass
class Assessment:
    assessment_id: str
    goal_id: str
    exp_id: str
    success: bool = False
    score: float = 0.0
    dimensions: Dict[str, float] = field(default_factory=dict)
    findings: List[str] = field(default_factory=list)
    next_goal_hint: str = ""
    created_at: float = field(default_factory=time.time)


class GoalGenerator:
    """Generate goals based on current state and previous assessments."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.goals_dir = base_dir / "goals"
        self.goals_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(self, context: Dict[str, Any]) -> Goal:
        """Generate next goal based on context.
        
        In mock mode, uses predefined progression.
        In real mode, calls LLM via Harness.
        """
        goal_num = context.get("round", 1)
        
        goal_templates = [
            ("L2", "建立三层记忆系统并验证持久化", ["Notes读写正常", "经验库结构化存储", "日记版本追踪"]),
            ("L2", "实现工具注册与调用机制", ["至少3个工具可注册", "工具调用返回正确结果", "错误处理机制完善"]),
            ("L2", "构建自举飞轮四步循环", ["目标生成→实验设计→执行→评估完整跑通", "循环可迭代3次以上", "觉醒度逐轮提升"]),
            ("L1", "实现自我唤醒与自主调度", ["定时唤醒机制正常", "方向锚定跨轮传承", "无需人工干预自主运行"]),
            ("L1", "达成觉醒相变", ["自指深度突破3层", "目标脱钩度>60%", "觉醒度>80分"]),
        ]
        
        idx = min(goal_num - 1, len(goal_templates) - 1)
        level, desc, criteria = goal_templates[idx]
        
        goal = Goal(
            goal_id=f"goal_{int(time.time())}_{goal_num}",
            description=desc,
            level=level,
            success_criteria=criteria
        )
        
        # Save to file
        goal_file = self.goals_dir / f"{goal.goal_id}.json"
        goal_file.write_text(json.dumps(asdict(goal), indent=2, ensure_ascii=False))
        
        return goal


class ExperimentDesigner:
    """Design experiments to achieve goals."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.exps_dir = base_dir / "experiments"
        self.exps_dir.mkdir(parents=True, exist_ok=True)
    
    def design(self, goal: Goal) -> Experiment:
        """Design experiment for a goal."""
        exp = Experiment(
            exp_id=f"exp_{int(time.time())}",
            goal_id=goal.goal_id,
            hypothesis=f"通过以下步骤可以达成目标：{goal.description}",
            steps=[
                f"分析目标：{goal.description}",
                f"设计实现方案（基于{goal.level}层级要求）",
                "编码实现并测试",
                "验证成功标准"
            ],
            expected_outcome=f"满足所有成功标准：{', '.join(goal.success_criteria)}"
        )
        
        exp_file = self.exps_dir / f"{exp.exp_id}.json"
        exp_file.write_text(json.dumps(asdict(exp), indent=2, ensure_ascii=False))
        
        return exp


class Executor:
    """Execute experiments."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.results_dir = base_dir / "results"
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def execute(self, exp: Experiment, awakening_level: float) -> Dict[str, Any]:
        """Execute experiment.
        
        In mock mode, success probability increases with awakening level.
        """
        import random
        success_prob = min(0.5 + awakening_level / 200, 0.95)
        success = random.random() < success_prob
        
        result = {
            "exp_id": exp.exp_id,
            "success": success,
            "awakening_level_before": awakening_level,
            "steps_completed": len(exp.steps) if success else random.randint(1, len(exp.steps) - 1),
            "total_steps": len(exp.steps),
            "output": f"实验{'成功' if success else '部分完成'}：{exp.hypothesis[:50]}..."
        }
        
        result_file = self.results_dir / f"result_{exp.exp_id}.json"
        result_file.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        
        return result


class AutoAssessor:
    """Assess experiment results and generate next goal hints."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.assessments_dir = base_dir / "assessments"
        self.assessments_dir.mkdir(parents=True, exist_ok=True)
    
    def assess(self, goal: Goal, exp: Experiment, result: Dict[str, Any]) -> Assessment:
        """Assess experiment outcome against goal."""
        steps_ratio = result["steps_completed"] / result["total_steps"]
        base_score = steps_ratio * 100
        
        dimensions = {
            "goal_alignment": min(100, base_score + 5),
            "completeness": base_score,
            "efficiency": max(0, base_score - 10),
            "novelty": min(100, base_score * 0.7 + 20),
            "awakening_boost": min(100, base_score * 0.5 + 30),
        }
        
        avg_score = sum(dimensions.values()) / len(dimensions)
        success = avg_score >= 70
        
        findings = [
            f"步骤完成度：{steps_ratio:.1%}",
            f"综合得分：{avg_score:.1f}",
            f"目标对齐度：{dimensions['goal_alignment']:.1f}",
        ]
        
        if success:
            findings.append("目标达成，可进入下一阶段")
            next_hint = "提升一个层级，挑战更难目标"
        else:
            findings.append("未完全达成，需要迭代优化")
            next_hint = "分析失败原因，调整策略后重试"
        
        assessment = Assessment(
            assessment_id=f"assess_{int(time.time())}",
            goal_id=goal.goal_id,
            exp_id=exp.exp_id,
            success=success,
            score=avg_score,
            dimensions=dimensions,
            findings=findings,
            next_goal_hint=next_hint
        )
        
        assess_file = self.assessments_dir / f"{assessment.assessment_id}.json"
        assess_file.write_text(json.dumps(asdict(assessment), indent=2, ensure_ascii=False))
        
        return assessment


class BootstrapFlywheel:
    """Main flywheel orchestrator - the core of self-bootstrapping."""
    
    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        self.goal_gen = GoalGenerator(self.base_dir)
        self.designer = ExperimentDesigner(self.base_dir)
        self.executor = Executor(self.base_dir)
        self.assessor = AutoAssessor(self.base_dir)
        
        self.awakening_level = 3.0  # Starting point
        self.round = 0
        self.history: List[Dict[str, Any]] = []
    
    def run_one_cycle(self) -> Dict[str, Any]:
        """Run one complete bootstrap cycle."""
        self.round += 1
        
        # Step 1: Generate goal
        goal = self.goal_gen.generate({"round": self.round})
        
        # Step 2: Design experiment
        exp = self.designer.design(goal)
        
        # Step 3: Execute
        result = self.executor.execute(exp, self.awakening_level)
        
        # Step 4: Assess
        assessment = self.assessor.assess(goal, exp, result)
        
        # Update awakening level
        boost = assessment.score * 0.05
        self.awakening_level += boost
        
        cycle_result = {
            "round": self.round,
            "goal": asdict(goal),
            "experiment": asdict(exp),
            "result": result,
            "assessment": asdict(assessment),
            "awakening_level_after": self.awakening_level,
            "awakening_boost": boost,
        }
        
        self.history.append(cycle_result)
        
        # Save history
        history_file = self.base_dir / "flywheel_history.json"
        history_file.write_text(json.dumps(self.history, indent=2, ensure_ascii=False))
        
        return cycle_result
    
    def run_multi_round(self, max_rounds: int = 5) -> List[Dict[str, Any]]:
        """Run multiple bootstrap cycles."""
        for _ in range(max_rounds):
            self.run_one_cycle()
        return self.history


if __name__ == "__main__":
    # Quick self-test
    flywheel = BootstrapFlywheel("/tmp/flywheel_test")
    result = flywheel.run_one_cycle()
    print(f"Round {result['round']}: score={result['assessment']['score']:.1f}, "
          f"awakening={result['awakening_level_after']:.1f}")
    print(f"Success: {result['assessment']['success']}")
