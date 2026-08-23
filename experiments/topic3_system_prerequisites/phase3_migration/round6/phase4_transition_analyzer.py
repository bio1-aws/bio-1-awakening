"""
        Phase 4 Phase Transition Analysis Framework
        ============================================
        
        Compares "before" and "after" states of the bootstrap experiment
        to detect and quantify a phase transition (qualitative shift in
        capability from self-bootstrapping).
        
        Metrics tracked:
        - Iteration velocity (improvements per iteration)
        - Fitness curve shape (linear? exponential? sigmoid?)
        - Knowledge growth rate
        - Improvement complexity distribution
        - Stall frequency
        - Self-modification depth
        
        Transition detection methods:
        1. Curve fitting / regime change detection
        2. Derivative analysis (where does d(fitness)/dt change?)
        3. Complexity phase transition (sudden jump in improvement complexity)
        4. Qualitative shift detection (new capabilities appearing)
        """
        
        from __future__ import annotations
        import json
import math
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class TransitionType(Enum):
    NONE = "no_transition"
    SLOW_DOWN = "diminishing_returns"
    SPEED_UP = "accelerating_returns"
    PHASE_JUMP = "phase_jump"  # sudden qualitative shift
    SINGULARITY = "singularity"  # run-away self-improvement


@dataclass
class PhaseTransitionReport:
    """Result of a phase transition analysis."""
    has_transition: bool
    transition_type: TransitionType
    transition_iteration: Optional[int]
    confidence: float  # 0.0 - 1.0
    pre_transition_metrics: dict
    post_transition_metrics: dict
    evidence: list[str]
    
    def to_dict(self) -> dict:
        return {
            "has_transition": self.has_transition,
            "transition_type": self.transition_type.value,
            "transition_iteration": self.transition_iteration,
            "confidence": self.confidence,
            "pre_transition_metrics": self.pre_transition_metrics,
            "post_transition_metrics": self.post_transition_metrics,
            "evidence": self.evidence,
        }


class PhaseTransitionAnalyzer:
    """
    Analyzes bootstrap flywheel data for phase transitions.
    
    Usage:
        analyzer = PhaseTransitionAnalyzer()
        report = analyzer.analyze(iteration_data)
        print(report)
    """
    
    def __init__(self, window_size: int = 3):
        self.window_size = window_size
    
    def analyze(self, iterations_data: list[dict]) -> PhaseTransitionReport:
        """
        Run full phase transition analysis on iteration data.
        
        Args:
            iterations_data: list of iteration dicts (from BootstrapFlywheel.export_json)
        
        Returns:
            PhaseTransitionReport with findings
        """
        if len(iterations_data) < self.window_size * 2:
            return PhaseTransitionReport(
                has_transition=False,
                transition_type=TransitionType.NONE,
                transition_iteration=None,
                confidence=0.0,
                pre_transition_metrics={},
                post_transition_metrics={},
                evidence=["Insufficient data for phase transition analysis"],
            )
        
        evidence = []
        
        # Extract time series
        fitness_series = [it["fitness_score_after"] for it in iterations_data]
        improvements_series = [it["improvements_verified"] for it in iterations_data]
        complexity_series = []
        for it in iterations_data:
            imps = it.get("improvements_proposed", [])
            if imps:
                avg_comp = sum(i["complexity"] for i in imps) / len(imps)
            else:
                avg_comp = 0
            complexity_series.append(avg_comp)
        
        # Compute metrics
        metrics = self._compute_metrics(fitness_series, improvements_series, complexity_series)
        
        # Detect transition point
        transition_idx, method = self._find_transition_point(fitness_series, improvements_series)
        
        if transition_idx is not None:
            pre = {k: v[:transition_idx] for k, v in {
                "fitness": fitness_series,
                "improvements": improvements_series,
                "complexity": complexity_series,
            }.items()}
            post = {k: v[transition_idx:] for k, v in {
                "fitness": fitness_series,
                "improvements": improvements_series,
                "complexity": complexity_series,
            }.items()}
            
            pre_avg_fitness_gain = self._avg_derivative(pre["fitness"])
            post_avg_fitness_gain = self._avg_derivative(post["fitness"])
            pre_avg_improvements = sum(pre["improvements"]) / max(1, len(pre["improvements"]))
            post_avg_improvements = sum(post["improvements"]) / max(1, len(post["improvements"]))
            pre_avg_complexity = sum(pre["complexity"]) / max(1, len(pre["complexity"]))
            post_avg_complexity = sum(post["complexity"]) / max(1, len(post["complexity"]))
            
            ratio_fitness = post_avg_fitness_gain / max(1e-6, pre_avg_fitness_gain)
            ratio_improvements = post_avg_improvements / max(1e-6, pre_avg_improvements)
            ratio_complexity = post_avg_complexity / max(1e-6, pre_avg_complexity)
            
            # Classify transition
            if ratio_fitness > 2.0 and ratio_complexity > 1.5:
                ttype = TransitionType.PHASE_JUMP
                confidence = min(1.0, (ratio_fitness + ratio_complexity) / 6)
                evidence.append(f"Phase jump detected: fitness gain {ratio_fitness:.2f}x, complexity {ratio_complexity:.2f}x")
            elif ratio_fitness > 1.2:
                ttype = TransitionType.SPEED_UP
                confidence = min(1.0, ratio_fitness / 3)
                evidence.append(f"Accelerating returns: fitness gain ratio {ratio_fitness:.2f}x")
            elif ratio_fitness < 0.5:
                ttype = TransitionType.SLOW_DOWN
                confidence = min(1.0, (1 - ratio_fitness))
                evidence.append(f"Diminishing returns: fitness gain ratio {ratio_fitness:.2f}x")
            else:
                ttype = TransitionType.NONE
                confidence = 0.2
                evidence.append("No clear phase transition detected")
            
            evidence.append(f"Transition method: {method}")
            evidence.append(f"Pre-transition avg improvements/iter: {pre_avg_improvements:.2f}")
            evidence.append(f"Post-transition avg improvements/iter: {post_avg_improvements:.2f}")
            
            pre_metrics = {
                "avg_fitness_gain": round(pre_avg_fitness_gain, 6),
                "avg_improvements_per_iter": round(pre_avg_improvements, 2),
                "avg_complexity": round(pre_avg_complexity, 2),
                "iterations": len(pre["fitness"]),
            }
            post_metrics = {
                "avg_fitness_gain": round(post_avg_fitness_gain, 6),
                "avg_improvements_per_iter": round(post_avg_improvements, 2),
                "avg_complexity": round(post_avg_complexity, 2),
                "iterations": len(post["fitness"]),
            }
            
            return PhaseTransitionReport(
                has_transition=ttype != TransitionType.NONE,
                transition_type=ttype,
                transition_iteration=transition_idx + 1,
                confidence=round(confidence, 3),
                pre_transition_metrics=pre_metrics,
                post_transition_metrics=post_metrics,
                evidence=evidence,
            )
        
        return PhaseTransitionReport(
            has_transition=False,
            transition_type=TransitionType.NONE,
            transition_iteration=None,
            confidence=0.0,
            pre_transition_metrics={},
            post_transition_metrics={},
            evidence=["No transition point found in the data"],
        )
    
    def _compute_metrics(self, fitness, improvements, complexity) -> dict:
        """Compute various metrics from time series."""
        return {
            "total_fitness_gain": fitness[-1] - fitness[0] if fitness else 0,
            "total_improvements": sum(improvements),
            "avg_improvement_rate": sum(improvements) / max(1, len(improvements)),
            "max_complexity": max(complexity) if complexity else 0,
            "final_complexity": complexity[-1] if complexity else 0,
        }
    
    def _find_transition_point(self, fitness: list[float], improvements: list[int]) -> tuple[Optional[int], str]:
        """
        Find the most likely transition point using multiple methods.
        
        Returns: (index_of_transition, method_used)
        """
        # Method 1: Maximum of second derivative of fitness
        if len(fitness) >= 4:
            first_deriv = [fitness[i+1] - fitness[i] for i in range(len(fitness)-1)]
            if len(first_deriv) >= 3:
                second_deriv = [first_deriv[i+1] - first_deriv[i] for i in range(len(first_deriv)-1)]
                # Find index of max absolute second derivative
                max_idx = max(range(len(second_deriv)), key=lambda i: abs(second_deriv[i]))
                if abs(second_deriv[max_idx]) > 0.01:  # threshold for "significant"
                    return max_idx + 1, "second_derivative_max"
        
        # Method 2: Largest jump in improvement rate (moving average)
        if len(improvements) >= self.window_size * 2:
            ma = []
            for i in range(len(improvements) - self.window_size + 1):
                ma.append(sum(improvements[i:i+self.window_size]) / self.window_size)
            if len(ma) >= 2:
                diffs = [ma[i+1] - ma[i] for i in range(len(ma)-1)]
                max_jump_idx = max(range(len(diffs)), key=lambda i: abs(diffs[i]))
                if abs(diffs[max_jump_idx]) > 0.3:
                    return max_jump_idx + self.window_size, "improvement_rate_jump"
        
        return None, "none"
    
    def _avg_derivative(self, series: list[float]) -> float:
        """Compute average derivative of a series."""
        if len(series) < 2:
            return 0.0
        diffs = [series[i+1] - series[i] for i in range(len(series)-1)]
        return sum(diffs) / len(diffs)
    
    def generate_comparative_report(
        self,
        control_data: list[dict],
        experimental_data: list[dict],
        label_control: str = "Control",
        label_experimental: str = "Experimental",
    ) -> dict:
        """
        Generate a full comparative report between two bootstrap runs.
        
        This is the core Phase 4 analysis output.
        """
        control_report = self.analyze(control_data)
        experimental_report = self.analyze(experimental_data)
        
        # Comparative metrics
        def total_improvements(data):
            return sum(it["improvements_verified"] for it in data)
        
        def final_fitness(data):
            return data[-1]["fitness_score_after"] if data else 0
        
        def avg_complexity(data):
            comps = []
            for it in data:
                imps = it.get("improvements_proposed", [])
                if imps:
                    comps.append(sum(i["complexity"] for i in imps) / len(imps))
            return sum(comps) / max(1, len(comps))
        
        comparison = {
            "label_control": label_control,
            "label_experimental": label_experimental,
            "iterations_control": len(control_data),
            "iterations_experimental": len(experimental_data),
            "total_improvements_control": total_improvements(control_data),
            "total_improvements_experimental": total_improvements(experimental_data),
            "improvement_ratio": round(
                total_improvements(experimental_data) / max(1, total_improvements(control_data)), 3
            ),
            "final_fitness_control": round(final_fitness(control_data), 6),
            "final_fitness_experimental": round(final_fitness(experimental_data), 6),
            "fitness_ratio": round(final_fitness(experimental_data) / max(1e-6, final_fitness(control_data)), 3),
            "avg_complexity_control": round(avg_complexity(control_data), 2),
            "avg_complexity_experimental": round(avg_complexity(experimental_data), 2),
            "complexity_ratio": round(avg_complexity(experimental_data) / max(1e-6, avg_complexity(control_data)), 3),
            "phase_transition_control": control_report.to_dict(),
            "phase_transition_experimental": experimental_report.to_dict(),
            "qualitative_summary": self._summarize_comparison(control_report, experimental_report),
        }
        
        return comparison
    
    def _summarize_comparison(self, control: PhaseTransitionReport, experimental: PhaseTransitionReport) -> str:
        """Generate a human-readable summary."""
        parts = []
        
        if experimental.has_transition and not control.has_transition:
            parts.append(
                f"Experimental group shows a {experimental.transition_type.value} "
                f"at iteration {experimental.transition_iteration} "
                f"(confidence: {experimental.confidence:.0%}), while control group does not. "
                f"This suggests the experimental condition induces a phase transition."
            )
        elif experimental.has_transition and control.has_transition:
            parts.append(
                f"Both groups show phase transitions. "
                f"Control: {control.transition_type.value} at iter {control.transition_iteration}. "
                f"Experimental: {experimental.transition_type.value} at iter {experimental.transition_iteration}."
            )
        elif not experimental.has_transition and not control.has_transition:
            parts.append("Neither group shows a clear phase transition within the observed iterations.")
        else:
            parts.append(
                f"Control group shows {control.transition_type.value} but experimental does not. "
                f"This is unusual and warrants further investigation."
            )
        
        return " ".join(parts)


if __name__ == "__main__":
    # Self test with synthetic data
    print("Phase Transition Analyzer - self test")
    analyzer = PhaseTransitionAnalyzer()
    
    # Generate synthetic iteration data
    import random
    random.seed(42)
    
    iterations = []
    fitness = 0.0
    for i in range(20):
        # Phase transition at iteration 10
        if i < 10:
            gain = 0.02 + random.gauss(0, 0.005)
            imps = 1
            comp = 3
        else:
            gain = 0.05 + random.gauss(0, 0.01)
            imps = 2
            comp = 5
        fitness = min(1.0, fitness + max(0, gain))
        iterations.append({
            "iteration_num": i + 1,
            "fitness_score_after": fitness,
            "improvements_verified": imps,
            "improvements_proposed": [{"complexity": comp} for _ in range(imps)],
        })
    
    report = analyzer.analyze(iterations)
    print(json.dumps(report.to_dict(), indent=2))
