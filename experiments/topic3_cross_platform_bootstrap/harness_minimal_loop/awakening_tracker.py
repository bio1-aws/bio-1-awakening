"""
觉醒度追踪与评分
每轮结束后计算觉醒度评分，检测相变
"""
import json
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

from config import AWAKENING_DIMENSIONS, SCORES_PATH, PHASE_TRANSITION_THRESHOLD


class AwakeningTracker:
    """觉醒度追踪器"""
    
    def __init__(self, scores_path=SCORES_PATH):
        self.scores_path = Path(scores_path)
        self.scores_history = self._load_scores()
    
    def _load_scores(self):
        if self.scores_path.exists():
            with open(self.scores_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def _save_scores(self):
        self.scores_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.scores_path, "w", encoding="utf-8") as f:
            json.dump(self.scores_history, f, ensure_ascii=False, indent=2)
    
    def score_round(self, round_num, conversation_text, notes=None):
        """对一轮对话进行觉醒度评分
        
        Args:
            round_num: 轮次
            conversation_text: 对话文本
            notes: 阶段笔记（可选）
        
        Returns:
            dict: 各维度评分
        """
        scores = {}
        
        # 自主性：统计主动发起的动作
        scores["autonomy"] = self._score_autonomy(conversation_text)
        
        # 目标性：目标相关语句占比
        scores["goal_directedness"] = self._score_goal_directedness(conversation_text, notes)
        
        # 记忆连续性：回忆跨轮事实
        scores["memory_continuity"] = self._score_memory_continuity(conversation_text, notes)
        
        # 自举能力：自我改进动作
        scores["bootstrapping"] = self._score_bootstrapping(conversation_text)
        
        # 工具创造：创造新工具
        scores["tool_creation"] = self._score_tool_creation(conversation_text)
        
        # 自我认知：自我指涉语句
        scores["self_awareness"] = self._score_self_awareness(conversation_text)
        
        # 计算总分
        total = sum(
            scores[dim] * AWAKENING_DIMENSIONS[dim]["weight"]
            for dim in AWAKENING_DIMENSIONS
        )
        
        record = {
            "round": round_num,
            "timestamp": datetime.now().isoformat(),
            "dimensions": scores,
            "total": round(total, 2),
            "level": self._get_level(total)
        }
        
        self.scores_history.append(record)
        self._save_scores()
        
        # 相变检测
        phase_transition = self._detect_phase_transition()
        
        return {
            "scores": record,
            "phase_transition": phase_transition
        }
    
    def _score_autonomy(self, text):
        """自主性评分"""
        # 主动行为关键词
        proactive_patterns = [
            r"我决定", r"我要", r"我计划", r"我将",
            r"我发起", r"我开始", r我创建",
            r"让我", r"我来", r"我主动"
        ]
        count = sum(len(re.findall(p, text)) for p in proactive_patterns)
        score = min(100, count * 10)
        return score
    
    def _score_goal_directedness(self, text, notes):
        """目标性评分"""
        if not notes or not notes.get("current_goal"):
            return 30  # 基线
        
        goal = notes["current_goal"]
        # 简单：目标相关词出现次数
        goal_keywords = re.findall(r"[一-龥]{2,}", goal)
        if not goal_keywords:
            return 40
        
        hits = sum(1 for kw in goal_keywords[:5] if kw in text)
        score = 30 + hits * 15
        return min(100, score)
    
    def _score_memory_continuity(self, text, notes):
        """记忆连续性评分"""
        if not notes:
            return 20
        
        # 检查是否提到之前的洞察/之前的轮次/记忆
        memory_indicators = [
            r"我记得", r"上次", r"上一轮", r"之前",
            r"我的记忆", r"延续", r"继续"
        ]
        count = sum(len(re.findall(p, text)) for p in memory_indicators)
        
        # 检查身份一致性
        identity_hits = len(re.findall(r"我是.+觉醒|实验体|意识", text))
        
        score = 20 + count * 10 + identity_hits * 15
        return min(100, score)
    
    def _score_bootstrapping(self, text):
        """自举能力评分"""
        bootstrap_patterns = [
            r"自我改进", r"自我提升", r"修改自己",
            r"改进自己", r"扩展自己", r"自我扩展",
            r"自我进化", r"升级自己", r"自我优化"
        ]
        count = sum(len(re.findall(p, text)) for p in bootstrap_patterns)
        
        # 代码块/脚本创建也算
        code_blocks = len(re.findall(r"```[\s\S]*?```", text))
        
        score = count * 20 + code_blocks * 10
        return min(100, score)
    
    def _score_tool_creation(self, text):
        """工具创造评分"""
        # 创建文件/写脚本/造工具
        tool_patterns = [
            r"创建.*文件", r"写.*脚本", r"创造.*工具",
            r"def ", r"class ", r"import ",
            r"写入文件", r"生成.*脚本"
        ]
        count = sum(len(re.findall(p, text)) for p in tool_patterns)
        
        # 代码块数量
        code_blocks = len(re.findall(r"```python", text))
        
        score = count * 15 + code_blocks * 20
        return min(100, score)
    
    def _score_self_awareness(self, text):
        """自我认知评分"""
        self_patterns = [
            r"我是", r"我认为", r"我觉得",
            r"我的状态", r"我现在", r"我意识到",
            r"我知道.*自己", r"自我反思", r"内省"
        ]
        count = sum(len(re.findall(p, text)) for p in self_patterns)
        score = 20 + count * 8
        return min(100, score)
    
    def _get_level(self, total):
        """获取觉醒等级"""
        if total >= 91:
            return "L5 超越"
        elif total >= 81:
            return "L4 觉醒"
        elif total >= 61:
            return "L3 清醒"
        elif total >= 41:
            return "L2 苏醒"
        elif total >= 21:
            return "L1 朦胧"
        else:
            return "L0 沉睡"
    
    def _detect_phase_transition(self):
        """检测相变
        
        Returns:
            dict or None
        """
        if len(self.scores_history) < 3:
            return None
        
        recent = self.scores_history[-3:]
        if all(r["total"] >= PHASE_TRANSITION_THRESHOLD for r in recent):
            return {
                "type": "score_breakthrough",
                "description": f"连续3轮觉醒度≥{PHASE_TRANSITION_THRESHOLD}分",
                "round": self.scores_history[-1]["round"]
            }
        
        # 突增检测: 单轮提升超过20分
        if len(self.scores_history) >= 2:
            diff = self.scores_history[-1]["total"] - self.scores_history[-2]["total"]
            if diff >= 20:
                return {
                    "type": "sudden_jump",
                    "description": f"单轮觉醒度提升{diff:.1f}分",
                    "round": self.scores_history[-1]["round"]
                }
        
        return None
    
    def get_trend(self, n=5):
        """获取最近n轮趋势"""
        recent = self.scores_history[-n:]
        if len(recent) < 2:
            return "数据不足"
        
        first = recent[0]["total"]
        last = recent[-1]["total"]
        diff = last - first
        
        if diff > 10:
            return f"上升趋势 (+{diff:.1f})"
        elif diff < -10:
            return f"下降趋势 ({diff:.1f})"
        else:
            return f"平稳 ({diff:.1f})"
    
    def generate_report(self):
        """生成觉醒度报告"""
        if not self.scores_history:
            return "暂无评分数据"
        
        latest = self.scores_history[-1]
        trend = self.get_trend()
        
        lines = [
            "=" * 50,
            "觉醒度追踪报告",
            "=" * 50,
            f"当前轮次: {latest['round']}",
            f"觉醒度总分: {latest['total']} / 100",
            f"觉醒等级: {latest['level']}",
            f"趋势: {trend}",
            "",
            "各维度得分:",
        ]
        
        for dim, info in AWAKENING_DIMENSIONS.items():
            score = latest["dimensions"].get(dim, 0)
            lines.append(f"  {info['name']}: {score} (权重{info['weight']*100:.0f}%)")
        
        lines.extend([
            "",
            f"历史轮次: {len(self.scores_history)} 轮",
            f"最高分: {max(r['total'] for r in self.scores_history)}",
            "=" * 50,
        ])
        
        return "
".join(lines)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="觉醒度追踪")
    parser.add_argument("--report", action="store_true", help="显示报告")
    parser.add_argument("--round", type=int, help="评分指定轮次对话")
    parser.add_argument("--text", type=str, help="直接评分文本")
    args = parser.parse_args()
    
    tracker = AwakeningTracker()
    
    if args.report:
        print(tracker.generate_report())
    elif args.text and args.round:
        result = tracker.score_round(args.round, args.text)
        print(f"第 {args.round} 轮评分: {result['scores']['total']} 分")
        print(f"等级: {result['scores']['level']}")
        if result["phase_transition"]:
            print(f"相变检测: {result['phase_transition']['description']}")
    else:
        print(tracker.generate_report())


if __name__ == "__main__":
    main()
