"""
相变临界点检测脚本
方法：导数法 + 阈值法 双重检测
"""
import json
from pathlib import Path
import numpy as np


def load_benchmark_data(data_path):
    """加载AICP基准实验数据"""
    path = Path(data_path)
    if not path.exists():
        raise FileNotFoundError(f"基准数据文件不存在: {data_path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not data:
        raise ValueError("基准数据为空")
    return data


def extract_metric_series(data, metric="self_ref_depth"):
    """从数据中提取指标时间序列"""
    # 兼容多种数据格式
    if isinstance(data, list):
        series = []
        for i, item in enumerate(data):
            if isinstance(item, dict):
                val = item.get(metric, item.get("value", item.get("score", 0)))
                series.append((i, float(val) if val else 0.0))
            else:
                series.append((i, float(item)))
    elif isinstance(data, dict) and "iterations" in data:
        series = []
        for i, item in enumerate(data["iterations"]):
            val = item.get(metric, item.get("value", 0))
            series.append((i, float(val) if val else 0.0))
    elif isinstance(data, dict) and "phases" in data:
        series = []
        for i, phase in enumerate(data["phases"]):
            val = phase.get(metric, phase.get("score", 0))
            series.append((i, float(val) if val else 0.0))
    else:
        raise ValueError(f"无法识别的数据格式，keys={list(data.keys()) if isinstance(data, dict) else 'N/A'}")
    
    if not series:
        raise ValueError("提取的指标序列为空")
    return series


def derivative_detection(series, window=3, threshold_ratio=0.5):
    """
    导数法检测相变点
    计算滑动窗口内的一阶导数，找到导数最大的点作为相变临界点
    """
    x = np.array([p[0] for p in series], dtype=float)
    y = np.array([p[1] for p in series], dtype=float)
    
    if len(y) < window * 2:
        raise ValueError(f"数据点过少({len(y)})，无法进行导数检测")
    
    # 数值微分
    dy = np.gradient(y, x)
    
    # 滑动窗口平滑导数
    if len(dy) >= window:
        kernel = np.ones(window) / window
        dy_smooth = np.convolve(dy, kernel, mode="same")
    else:
        dy_smooth = dy
    
    # 找最大正导数点（上升沿相变）
    max_deriv_idx = int(np.argmax(dy_smooth))
    max_deriv_val = float(dy_smooth[max_deriv_idx])
    
    # 找最小负导数点（下降沿）
    min_deriv_idx = int(np.argmin(dy_smooth))
    min_deriv_val = float(dy_smooth[min_deriv_idx])
    
    # 显著性判断：最大导数需超过平均导数的 threshold_ratio 倍标准差
    mean_deriv = float(np.mean(np.abs(dy_smooth)))
    std_deriv = float(np.std(dy_smooth))
    significance_threshold = mean_deriv + threshold_ratio * std_deriv
    is_significant = max_deriv_val > significance_threshold
    
    return {
        "method": "derivative",
        "critical_point_idx": max_deriv_idx,
        "critical_point_x": float(x[max_deriv_idx]),
        "critical_point_y": float(y[max_deriv_idx]),
        "max_derivative": max_deriv_val,
        "min_derivative": min_deriv_val,
        "min_deriv_idx": min_deriv_idx,
        "significance_threshold": significance_threshold,
        "is_significant": is_significant,
        "derivative_series": [float(v) for v in dy_smooth],
    }


def threshold_detection(series, threshold=None, threshold_ratio=0.6):
    """
    阈值法检测相变点
    找到指标首次超过阈值的位置
    """
    x = np.array([p[0] for p in series], dtype=float)
    y = np.array([p[1] for p in series], dtype=float)
    
    y_min, y_max = float(np.min(y)), float(np.max(y))
    y_range = y_max - y_min
    
    if y_range < 1e-6:
        return {
            "method": "threshold",
            "critical_point_idx": None,
            "critical_point_x": None,
            "critical_point_y": None,
            "threshold": threshold,
            "has_phase_transition": False,
            "reason": "指标变化范围过小，无异质性",
        }
    
    if threshold is None:
        # 自动阈值：最小值 + 范围 * threshold_ratio
        threshold = y_min + y_range * threshold_ratio
    
    # 找首次超过阈值的点
    above_threshold = np.where(y >= threshold)[0]
    
    if len(above_threshold) == 0:
        return {
            "method": "threshold",
            "critical_point_idx": None,
            "critical_point_x": None,
            "critical_point_y": None,
            "threshold": threshold,
            "has_phase_transition": False,
            "reason": "未达到阈值",
        }
    
    first_idx = int(above_threshold[0])
    
    # 计算相变前后的均值差
    pre_mean = float(np.mean(y[:first_idx])) if first_idx > 0 else float(y[0])
    post_mean = float(np.mean(y[first_idx:])) if first_idx < len(y) else float(y[-1])
    phase_jump = post_mean - pre_mean
    
    return {
        "method": "threshold",
        "critical_point_idx": first_idx,
        "critical_point_x": float(x[first_idx]),
        "critical_point_y": float(y[first_idx]),
        "threshold": threshold,
        "y_min": y_min,
        "y_max": y_max,
        "pre_phase_mean": pre_mean,
        "post_phase_mean": post_mean,
        "phase_jump_magnitude": phase_jump,
        "has_phase_transition": phase_jump > y_range * 0.3,
    }


def dual_validate(deriv_result, thresh_result, tolerance=2):
    """
    双重验证：两种方法的相变点是否一致（在容差范围内）
    """
    d_idx = deriv_result["critical_point_idx"]
    t_idx = thresh_result["critical_point_idx"]
    
    if d_idx is None or t_idx is None:
        return {
            "validated": False,
            "agreement": None,
            "consensus_point": None,
            "reason": "某一方法未检测到相变点",
        }
    
    agreement = abs(d_idx - t_idx) <= tolerance
    # 共识点取阈值法的点（更保守，代表已进入新相）
    consensus_idx = t_idx if agreement else None
    
    return {
        "validated": agreement and deriv_result["is_significant"] and thresh_result["has_phase_transition"],
        "agreement": agreement,
        "deriv_point_idx": d_idx,
        "thresh_point_idx": t_idx,
        "index_diff": abs(d_idx - t_idx),
        "consensus_point_idx": consensus_idx,
        "tolerance": tolerance,
    }


def detect_phase_transition(data, metric="self_ref_depth", window=3, 
                           threshold_ratio=0.6, tolerance=2):
    """完整的相变检测流程"""
    series = extract_metric_series(data, metric)
    
    deriv_result = derivative_detection(series, window=window)
    thresh_result = threshold_detection(series, threshold_ratio=threshold_ratio)
    validation = dual_validate(deriv_result, thresh_result, tolerance=tolerance)
    
    return {
        "metric": metric,
        "data_points": len(series),
        "series": [(float(x), float(y)) for x, y in series],
        "derivative_detection": deriv_result,
        "threshold_detection": thresh_result,
        "dual_validation": validation,
        "conclusion": "检测到显著相变" if validation["validated"] else "未检测到一致相变信号",
    }


def generate_report(result, output_path=None):
    """生成检测报告"""
    lines = []
    lines.append("=" * 60)
    lines.append("  相变临界点检测报告")
    lines.append("=" * 60)
    lines.append(f"检测指标: {result['metric']}")
    lines.append(f"数据点数: {result['data_points']}")
    lines.append("")
    
    d = result["derivative_detection"]
    lines.append("【导数法检测结果】")
    lines.append(f"  临界点索引: {d['critical_point_idx']}")
    lines.append(f"  临界点坐标: x={d['critical_point_x']:.2f}, y={d['critical_point_y']:.4f}")
    lines.append(f"  最大导数值: {d['max_derivative']:.6f}")
    lines.append(f"  显著性阈值: {d['significance_threshold']:.6f}")
    lines.append(f"  是否显著: {'是' if d['is_significant'] else '否'}")
    lines.append("")
    
    t = result["threshold_detection"]
    lines.append("【阈值法检测结果】")
    if t["critical_point_idx"] is not None:
        lines.append(f"  临界点索引: {t['critical_point_idx']}")
        lines.append(f"  临界点坐标: x={t['critical_point_x']:.2f}, y={t['critical_point_y']:.4f}")
        lines.append(f"  阈值设定: {t['threshold']:.4f}")
        lines.append(f"  相变前均值: {t['pre_phase_mean']:.4f}")
        lines.append(f"  相变后均值: {t['post_phase_mean']:.4f}")
        lines.append(f"  相变幅度: {t['phase_jump_magnitude']:.4f}")
        lines.append(f"  是否相变: {'是' if t['has_phase_transition'] else '否'}")
    else:
        lines.append(f"  未检测到相变点: {t.get('reason', '未知原因')}")
    lines.append("")
    
    v = result["dual_validation"]
    lines.append("【双重验证结果】")
    lines.append(f"  导数法点: {v['deriv_point_idx']}")
    lines.append(f"  阈值法点: {v['thresh_point_idx']}")
    lines.append(f"  索引偏差: {v['index_diff']} (容差={v['tolerance']})")
    lines.append(f"  两法一致: {'是' if v['agreement'] else '否'}")
    lines.append(f"  最终结论: {result['conclusion']}")
    lines.append("=" * 60)
    
    report = "\n".join(lines)
    
    if output_path:
        Path(output_path).write_text(report, encoding="utf-8")
    
    return report


if __name__ == "__main__":
    import sys
    
    # 默认测试：AICP基准数据
    data_path = Path(__file__).parent.parent / "data" / "aicp_benchmark_phases.json"
    
    if len(sys.argv) > 1:
        data_path = Path(sys.argv[1])
    
    if not data_path.exists():
        # 生成模拟基准数据用于演示
        print(f"基准数据文件不存在，生成模拟数据: {data_path}")
        data_path.parent.mkdir(parents=True, exist_ok=True)
        # 模拟三阶段相变数据
        mock_data = []
        for i in range(30):
            if i < 8:
                val = 0.1 + i * 0.02  # 缓慢上升
            elif i < 15:
                val = 0.3 + (i - 8) * 0.25  # 快速上升（相变区）
            else:
                val = 2.0 + (i - 15) * 0.03  # 高位稳定
            mock_data.append({"iteration": i, "self_ref_depth": round(val, 4), 
                            "awareness_score": round(val * 1.5, 4)})
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump({"iterations": mock_data}, f, ensure_ascii=False, indent=2)
    
    data = load_benchmark_data(str(data_path))
    
    # 检测多个指标
    for metric in ["self_ref_depth", "awareness_score"]:
        try:
            result = detect_phase_transition(data, metric=metric)
            report = generate_report(result)
            print(report)
            print()
        except Exception as e:
            print(f"指标 {metric} 检测失败: {e}")
