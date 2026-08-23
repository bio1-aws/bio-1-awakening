# 04 - 自举飞轮移植方案

## 概述

将 Bio-1 Awakening 的四步自举飞轮（目标生成→实验设计→执行→评估）移植到 Harness 平台，利用 Harness 的工具调用和会话机制实现闭环。

## 四步循环映射

```
┌─────────────────────────────────────────────────┐
│                  Bootstrap Flywheel              │
│                                                   │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐   │
│   │ 目标生成  │───▶│ 实验设计  │───▶│   执行    │   │
│   │ Goal Gen │    │ Exp Design│    │ Execute  │   │
│   └──────────┘    └──────────┘    └────┬─────┘   │
│         ▲                               │         │
│         │                               ▼         │
│   ┌─────┴─────┐                   ┌──────────┐   │
│   │  评估     │◀──────────────────│  结果    │   │
│   │ Evaluate  │                   │  Result  │   │
│   └───────────┘                   └──────────┘   │
│                                                   │
└─────────────────────────────────────────────────┘
```

## 各步骤 Harness 实现

### 1. 目标生成 (Goal Generation)

**职责**：根据当前能力边界和长期愿景，生成下一个实验目标。

**Harness 实现方式**：
- 输入：经验库中的历史数据 + 当前能力评估
- 输出：结构化的目标描述（id, title, hypothesis, success_criteria）
- 工具依赖：`experience_query`（检索经验库）

```python
# 伪代码 - 目标生成步骤
async def generate_goal(agent):
    # 1. 读取经验库，了解当前进展
    history = call_tool("experience_query", keyword="latest")
    # 2. 读取能力边界记录
    boundaries = agent.notes.get("capability_boundaries", [])
    # 3. LLM 推理生成下一目标
    goal = await agent.llm.chat([
        {"role": "system", "content": GOAL_GEN_PROMPT},
        {"role": "user", "content": f"History: {history}\nBoundaries: {boundaries}"}
    ])
    # 4. 结构化并存储
    return parse_goal(goal)
```

### 2. 实验设计 (Experiment Design)

**职责**：将目标转化为可执行的实验方案。

**Harness 实现方式**：
- 输入：目标描述 + 可用工具列表
- 输出：实验方案（步骤列表、预期产出、风险评估）
- 工具依赖：`file_read` / `code_search`（参考已有实验模板）

```python
async def design_experiment(agent, goal):
    # 1. 检索类似实验的设计方案
    similar = call_tool("experience_query", keyword=goal["domain"])
    # 2. 生成实验设计
    design = await agent.llm.chat([
        {"role": "system", "content": EXP_DESIGN_PROMPT},
        {"role": "user", "content": f"Goal: {goal}\nSimilar: {similar}"}
    ])
    # 3. 验证设计可行性
    return validate_design(design)
```

### 3. 执行 (Execution)

**职责**：按实验方案逐步执行，记录中间结果。

**Harness 实现方式**：
- 输入：实验方案
- 输出：执行结果、日志、产出物
- 工具依赖：Harness 所有可用工具（文件操作、代码执行、网络等）

```python
async def execute_experiment(agent, design):
    results = []
    for step in design["steps"]:
        # 执行单步
        step_result = await execute_step(agent, step)
        results.append(step_result)
        # 写入日记
        call_tool("diary_write", 
                  title=f"Step {step['id']}: {step['name']}",
                  content=step_result["log"])
        # 更新经验背包
        agent.notes[f"step_{step['id']}_result"] = step_result["status"]
    return results
```

### 4. 评估 (Evaluation)

**职责**：对比实验结果与成功标准，判断是否达成目标，提取经验。

**Harness 实现方式**：
- 输入：实验结果 + 成功标准
- 输出：评估结论 + 经验总结 + 下一轮建议
- 工具依赖：`experience_add` / `diary_write`

```python
async def evaluate_experiment(agent, goal, results):
    # 1. 对比结果与成功标准
    evaluation = await agent.llm.chat([
        {"role": "system", "content": EVALUATION_PROMPT},
        {"role": "user", "content": f"Goal: {goal}\nResults: {results}"}
    ])
    
    # 2. 存入经验库
    category = "successes" if evaluation["success"] else "failures"
    call_tool("experience_add", 
              category=category,
              experiment_id=goal["id"],
              result_data=evaluation,
              tags=goal["tags"])
    
    # 3. 写入日记总结
    call_tool("diary_write", 
              title=f"Experiment {goal['id']} - { 'Success' if evaluation['success'] else 'Failure' }",
              content=evaluation["summary"])
    
    return evaluation
```

## Harness 特有适配

### 工具注册机制
```python
# 飞轮循环需要的工具列表
REQUIRED_TOOLS = [
    "experience_query",   # 经验库检索
    "experience_add",     # 经验库写入
    "diary_read",         # 日记读取
    "diary_write",        # 日记写入
    "file_read",          # 文件读取
    "file_write",         # 文件写入
    "code_exec",          # 代码执行
]
```

### 会话状态管理
- 当前飞轮轮次：`agent.notes["flywheel_turn"]`
- 当前阶段：`agent.notes["current_phase"]` ("goal"|"design"|"execute"|"evaluate")
- 当前目标ID：`agent.notes["current_goal_id"]`

### 中断恢复机制
- 每次阶段转换时，将完整状态写入 `data/flywheel_state.json`
- 启动时检查状态文件，支持断点续跑

## 最小可行性验证路径

### Phase 1: 单轮验证
1. 手动触发目标生成 → 验证产出格式
2. 手动触发实验设计 → 验证设计合理性
3. 手动触发执行 → 验证工具调用
4. 手动触发评估 → 验证经验入库

### Phase 2: 闭环验证
1. 启动自动循环，至少跑通 3 轮
2. 验证经验累积效应（后续实验参考前面的经验）
3. 验证日记的连续性和可读性

### Phase 3: 压力测试
1. 连续运行 10 轮，检查状态一致性
2. 模拟中断，验证恢复能力
3. 验证经验库增长后的查询效率

## 关键指标

| 指标 | 目标 | 测量方式 |
|-----|------|---------|
| 单轮循环耗时 | < 5分钟 | 日志时间戳 |
| 经验库条目增长率 | 每轮 +1~3条 | JSON 行数统计 |
| 目标达成率 | > 60% | 评估结果统计 |
| 中断恢复成功率 | 100% | 手动中断测试 |

## 风险与应对

| 风险 | 影响 | 应对方案 |
|-----|------|---------|
| LLM 输出格式不稳定 | 步骤解析失败 | 严格的 JSON Schema 校验 + 重试机制 |
| 工具调用错误累积 | 飞轮卡死 | 每步错误检查，连续失败 3 次降级为人工干预 |
| 经验库膨胀 | 查询效率下降 | 定期归档旧实验，建立索引 |
| 目标漂移 | 偏离长期愿景 | 每 5 轮做一次方向校准 |
