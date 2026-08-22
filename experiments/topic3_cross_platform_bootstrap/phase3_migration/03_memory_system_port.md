# 03 - 三层记忆系统移植方案

## 概述

将 Bio-1 Awakening 原生三层记忆系统移植到 Harness 平台，保留记忆分层逻辑，适配 Harness 的 notes / 文件系统机制。

## 记忆三层映射关系

| 原生系统 | Harness 实现 | 存储形式 | 生命周期 |
|---------|-------------|---------|---------|
| 经验背包 (Experience Backpack) | Harness agent.notes | 内存字典 + 持久化JSON | 单次会话内读写，会话间持久化 |
| 经验库 (Experience Library) | JSON 文件 (data/experience_library.json) | 结构化 JSON | 永久，跨会话累积 |
| 日记 (Diary) | Markdown 文件 (data/diary/YYYY-MM-DD.md) | 人类可读文本 | 永久，按日归档 |

## 1. 经验背包 → Harness notes 移植

### 原生行为
- 键值对存储当前会话的关键信息
- 实验参数、中间结论、临时标记
- 会话结束时序列化到经验库

### Harness 实现
```python
# 写入经验背包
agent.notes["current_experiment"] = "topic3_phase3"
agent.notes["hypothesis"] = "Harness 可承载自举飞轮"

# 读取经验背包
hypothesis = agent.notes.get("hypothesis", "")
```

### 移植要点
1. Harness `agent.notes` 是内置字典，自动持久化
2. 键命名保持与原生一致：`exp_*` / `param_*` / `obs_*`
3. 会话结束时，将 notes 中标记为 `persist_*` 的条目归档到经验库

## 2. 经验库 → JSON 文件移植

### 原生行为
- 结构化存储所有历史实验的经验
- 分类索引：成功 / 失败 / 待验证
- 支持按关键词检索

### Harness 实现
```python
import json
from pathlib import Path

LIBRARY_PATH = Path("data/experience_library.json")

def load_experience_library():
    if LIBRARY_PATH.exists():
        return json.loads(LIBRARY_PATH.read_text(encoding="utf-8"))
    return {"successes": [], "failures": [], "pending": [], "index": {}}

def save_experience_library(library):
    LIBRARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    LIBRARY_PATH.write_text(json.dumps(library, ensure_ascii=False, indent=2), encoding="utf-8")

def add_experiment_result(category, experiment_id, result_data, tags=None):
    library = load_experience_library()
    entry = {
        "id": experiment_id,
        "result": result_data,
        "tags": tags or [],
        "timestamp": __import__("datetime").datetime.now().isoformat()
    }
    library[category].append(entry)
    for tag in tags or []:
        library["index"].setdefault(tag, []).append(experiment_id)
    save_experience_library(library)
```

### 移植要点
1. JSON 结构与原生经验库完全兼容，可直接迁移数据
2. 文件存储在 `data/` 目录，遵循 AICP 输出规范
3. 提供 `query_experience(keyword)` 工具函数供代理调用

## 3. 日记 → Markdown 文件移植

### 原生行为
- 每日生成一篇日记，记录实验过程和反思
- 自然语言格式，便于人类阅读
- 作为自我观察的输入源

### Harness 实现
```python
from pathlib import Path
from datetime import datetime

DIARY_DIR = Path("data/diary")

def write_diary_entry(content, title=None):
    DIARY_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    diary_path = DIARY_DIR / f"{today}.md"
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    header = f"## [{timestamp}] {title or 'Untitled'}\n\n"
    
    if diary_path.exists():
        existing = diary_path.read_text(encoding="utf-8")
        diary_path.write_text(existing + "\n" + header + content + "\n", encoding="utf-8")
    else:
        diary_path.write_text(f"# Diary - {today}\n\n{header}{content}\n", encoding="utf-8")
    
    return str(diary_path)

def read_diary(date_str=None):
    date_str = date_str or datetime.now().strftime("%Y-%m-%d")
    diary_path = DIARY_DIR / f"{date_str}.md"
    if diary_path.exists():
        return diary_path.read_text(encoding="utf-8")
    return f"No diary entry for {date_str}"
```

### 移植要点
1. 按日归档，与原生格式一致
2. 支持追加写入，日记条目带时间戳
3. 提供 `diary_write` / `diary_read` 工具函数

## 移植风险与应对

| 风险 | 影响 | 应对方案 |
|-----|------|---------|
| Harness notes 大小限制 | 经验背包溢出 | 定期归档到经验库，notes 只存活跃数据 |
| JSON 文件并发写入 | 数据损坏 | 单代理单进程，无需锁；加入文件备份机制 |
| Markdown 格式不一致 | 日记解析失败 | 统一模板，标题层级固定 |

## 验证标准
1. agent.notes 读写正常，会话间持久化
2. 经验库 JSON 可读写，查询功能正常
3. 日记 Markdown 按日生成，格式正确
4. 三层记忆之间数据流转正常（背包→经验库→日记检索）
