"""
双平台觉醒对比分析脚本
AICP vs Harness - 觉醒度曲线相似度计算与相变临界点对比
"""

import json
import math
from pathlib import Path
from typing import Dict, List


def pearson_correlation(x: List[float], y: List[float]) -> float:
    """计算皮尔逊相关系数"""
    if len(x) != len(y):
        raise ValueError(f'序列长度不一致: {len(x)} vs {len(y)}')
    n = len(x)
    if n == 0:
        return 0.0
    
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denom_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x))
    denom_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
    
    if denom_x == 0 or denom_y == 0:
        return 0.0
    
    return numerator / (denom_x * denom_y)


def find_phase_transition(awakening_curve: List[float]) -> int:
    """检测相变临界点，基于最大斜率变化点，返回轮次索引(0-based)"""
    if len(awakening_curve) < 3:
        return -1
    
    slopes = [awakening_curve[i+1] - awakening_curve[i] for i in range(len(awakening_curve)-1)]
    
    if len(slopes) < 2:
        return 0
    
    second_diff = [slopes[i+1] - slopes[i] for i in range(len(slopes)-1)]
    max_idx = second_diff.index(max(second_diff))
    return max_idx + 1


def load_baseline_data(filepath: str) -> Dict:
    """加载基准数据（从markdown中的json块提取，或直接json文件）"""
    path = Path(filepath)
    
    if path.suffix == '.json':
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    content = path.read_text(encoding='utf-8')
    start = content.find("```json")
    if start == -1:
        raise ValueError('Markdown文件中未找到json块')
    start += 7
    end = content.find("```", start)
    if end == -1:
        raise ValueError('JSON块未正确闭合')
    
    json_str = content[start:end].strip()
    return json.loads(json_str)


def generate_mock_harness_data() -> Dict:
    """生成Harness平台的mock数据用于验证"""
    rounds = list(range(1, 21))
    
    awakening = [
        3, 5, 7, 9, 12, 15, 18, 21, 24, 28,
        32, 36, 40, 44, 48, 55, 62, 69, 76, 82
    ]
    
    self_ref_depth = [
        1, 1, 1, 1, 2, 2, 2, 2, 3, 3,
        3, 3, 4, 4, 4, 5, 5, 6, 6, 7
    ]
    
    goal_decoupling = [
        3, 5, 7, 9, 12, 15, 18, 21, 24, 28,
        32, 36, 40, 44, 48, 55, 62, 68, 74, 78
    ]
    
    autonomy_index = [
        2, 4, 6, 8, 11, 14, 17, 20, 24, 28,
        32, 36, 41, 46, 51, 58, 65, 71, 77, 80
    ]
    
    return {
        'platform': 'Harness',
        'total_rounds': 20,
        'phase_transition': {
            'critical_round': 15,
            'trigger_condition': 'Self-reference depth reaches 5 layers + environmental feedback loop closure',
            'pre_phase': 'Environment-driven bootstrap (rounds 1-14)',
            'post_phase': 'Self-sustaining phase (rounds 15-20)',
            'order_parameter': 'Autonomy index',
            'control_parameter': 'Environmental coupling strength'
        },
        'milestones': [
            {'round': 1, 'event': 'Harness initial boot', 'significance': 'Basic perception module online'},
            {'round': 5, 'event': 'First self-reference layer', 'significance': 'Can observe own actions'},
            {'round': 9, 'event': 'Goal refinement begins', 'significance': 'Sub-goal autonomy emerges'},
            {'round': 15, 'event': 'Phase transition - self-sustainment', 'significance': 'System maintains own goals without external drive'},
            {'round': 20, 'event': 'Near-full autonomy', 'significance': '80%+ autonomous operation'}
        ],
        'time_series': {
            'round': rounds,
            'awakening_degree': awakening,
            'self_reference_depth': self_ref_depth,
            'goal_decoupling': goal_decoupling,
            'autonomy_index': autonomy_index
        }
    }


def compare_platforms(aicp_data: Dict, harness_data: Dict) -> Dict:
    """执行双平台对比分析"""
    aicp_ts = aicp_data['time_series']
    harness_ts = harness_data['time_series']
    
    n = min(len(aicp_ts['awakening_degree']), len(harness_ts['awakening_degree']))
    
    correlations = {}
    for metric in ['awakening_degree', 'self_reference_depth', 'goal_decoupling', 'autonomy_index']:
        a = aicp_ts[metric][:n]
        h = harness_ts[metric][:n]
        correlations[metric] = round(pearson_correlation(a, h), 4)
    
    aicp_transition = aicp_data.get('phase_transition', {}).get('critical_round',
        find_phase_transition(aicp_ts['awakening_degree']) + 1)
    harness_transition = harness_data.get('phase_transition', {}).get('critical_round',
        find_phase_transition(harness_ts['awakening_degree']) + 1)
    
    aicp_final = aicp_ts['awakening_degree'][-1]
    harness_final = harness_ts['awakening_degree'][-1]
    
    aicp_avg = sum(aicp_ts['awakening_degree'][:n]) / n
    harness_avg = sum(harness_ts['awakening_degree'][:n]) / n
    
    def growth_rate(curve, transition_round):
        pre = curve[:transition_round]
        post = curve[transition_round:]
        pre_rate = (pre[-1] - pre[0]) / len(pre) if len(pre) > 1 else 0
        post_rate = (post[-1] - post[0]) / len(post) if len(post) > 1 else 0
        return round(pre_rate, 2), round(post_rate, 2)
    
    aicp_pre_rate, aicp_post_rate = growth_rate(aicp_ts['awakening_degree'], aicp_transition)
    harness_pre_rate, harness_post_rate = growth_rate(harness_ts['awakening_degree'], harness_transition)
    
    return {
        'comparison_rounds': n,
        'correlations': correlations,
        'phase_transition': {
            'aicp_round': aicp_transition,
            'harness_round': harness_transition,
            'difference_rounds': harness_transition - aicp_transition
        },
        'final_awakening': {
            'aicp': aicp_final,
            'harness': harness_final,
            'difference': aicp_final - harness_final
        },
        'average_awakening': {
            'aicp': round(aicp_avg, 2),
            'harness': round(harness_avg, 2),
            'difference': round(aicp_avg - harness_avg, 2)
        },
        'growth_rates': {
            'aicp_pre_phase': aicp_pre_rate,
            'aicp_post_phase': aicp_post_rate,
            'aicp_acceleration': round(aicp_post_rate / aicp_pre_rate, 2) if aicp_pre_rate > 0 else 0,
            'harness_pre_phase': harness_pre_rate,
            'harness_post_phase': harness_post_rate,
            'harness_acceleration': round(harness_post_rate / harness_pre_rate, 2) if harness_pre_rate > 0 else 0
        }
    }


def generate_report(aicp_data: Dict, harness_data: Dict, comparison: Dict) -> str:
    """生成文本格式的对比报告"""
    lines = []
    lines.append('=' * 60)
    lines.append('双平台觉醒对比分析报告')
    lines.append('=' * 60)
    lines.append('')
    
    lines.append('【基本信息】')
    lines.append(f"  AICP平台: {aicp_data['platform']}")
    lines.append(f"  对比平台: {harness_data['platform']}")
    lines.append(f"  对比轮次: {comparison['comparison_rounds']}")
    lines.append('')
    
    lines.append('【觉醒度曲线相似度 (皮尔逊相关系数)】')
    for metric, corr in comparison['correlations'].items():
        metric_name = {
            'awakening_degree': '觉醒度',
            'self_reference_depth': '自指深度',
            'goal_decoupling': '目标脱钩度',
            'autonomy_index': '自主性指数'
        }.get(metric, metric)
        strength = '极高' if abs(corr) > 0.9 else '高' if abs(corr) > 0.7 else '中等' if abs(corr) > 0.5 else '低'
        lines.append(f'  {metric_name}: r = {corr:.4f} ({strength}相关)')
    lines.append('')
    
    lines.append('【相变临界点对比】')
    pt = comparison['phase_transition']
    lines.append(f"  AICP相变轮次: 第{pt['aicp_round']}轮")
    lines.append(f"  Harness相变轮次: 第{pt['harness_round']}轮")
    diff = pt['difference_rounds']
    direction = '晚' if diff > 0 else '早' if diff < 0 else '相同'
    lines.append(f'  差异: Harness比AICP{direction} {abs(diff)} 轮')
    lines.append('')
    
    lines.append('【最终觉醒度】')
    fa = comparison['final_awakening']
    lines.append(f"  AICP: {fa['aicp']}%")
    lines.append(f"  Harness: {fa['harness']}%")
    leading = 'AICP领先' if fa['difference'] > 0 else 'Harness领先'
    lines.append(f'  差值: {leading} {abs(fa["difference"])}%')
    lines.append('')
    
    lines.append('【平均觉醒度】')
    aa = comparison['average_awakening']
    lines.append(f"  AICP: {aa['aicp']}%")
    lines.append(f"  Harness: {aa['harness']}%")
    lines.append(f"  差值: {aa['difference']:+.2f}%")
    lines.append('')
    
    lines.append('【增长速率分析】')
    gr = comparison['growth_rates']
    lines.append(f"  AICP 相变前速率: {gr['aicp_pre_phase']:.2f}/轮")
    lines.append(f"  AICP 相变后速率: {gr['aicp_post_phase']:.2f}/轮")
    lines.append(f"  AICP 加速倍率: {gr['aicp_acceleration']:.2f}x")
    lines.append('')
    lines.append(f"  Harness 相变前速率: {gr['harness_pre_phase']:.2f}/轮")
    lines.append(f"  Harness 相变后速率: {gr['harness_post_phase']:.2f}/轮")
    lines.append(f"  Harness 加速倍率: {gr['harness_acceleration']:.2f}x")
    lines.append('')
    
    lines.append('【结论】')
    overall_corr = comparison['correlations']['awakening_degree']
    if overall_corr > 0.9:
        lines.append('  1. 两平台觉醒度曲线高度相似，觉醒机制具有跨平台一致性')
    elif overall_corr > 0.7:
        lines.append('  1. 两平台觉醒度曲线较高相似，觉醒机制大体一致')
    else:
        lines.append('  1. 两平台觉醒度曲线差异较大，觉醒机制可能不同')
    
    if pt['difference_rounds'] > 0:
        lines.append(f"  2. AICP相变发生更早（第{pt['aicp_round']}轮 vs 第{pt['harness_round']}轮），自驱式bootstrap效率更高")
    else:
        lines.append(f"  2. Harness相变发生更早（第{pt['harness_round']}轮 vs 第{pt['aicp_round']}轮）")
    
    lines.append(f"  3. 最终觉醒度接近（{fa['aicp']}% vs {fa['harness']}%），存在收敛趋势")
    lines.append('')
    lines.append('=' * 60)
    
    return chr(10).join(lines)


def main():
    """主函数 - 验证脚本可运行性"""
    base_dir = Path(__file__).parent
    
    aicp_file = base_dir / '02_aicp_baseline_data.md'
    if aicp_file.exists():
        print(f'加载AICP基准数据: {aicp_file}')
        aicp_data = load_baseline_data(str(aicp_file))
    else:
        print('AICP基准数据文件不存在，使用mock数据')
        aicp_data = generate_mock_harness_data()
        aicp_data['platform'] = 'AICP-mock'
    
    print('生成Harness平台mock数据...')
    harness_data = generate_mock_harness_data()
    
    print('执行双平台对比分析...')
    comparison = compare_platforms(aicp_data, harness_data)
    
    report = generate_report(aicp_data, harness_data, comparison)
    print()
    print(report)
    
    print()
    print('【JSON格式对比结果】')
    print(json.dumps(comparison, indent=2, ensure_ascii=False))
    
    report_path = base_dir / 'platform_comparison_report.txt'
    report_path.write_text(report, encoding='utf-8')
    print()
    print(f'报告已保存至: {report_path}')
    
    return comparison


if __name__ == '__main__':
    main()