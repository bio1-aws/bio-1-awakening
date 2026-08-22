# 课题2阶段2：大规模多智能体网络觉醒实验设计

## 阶段2目标

验证三大核心假设：
1. **网络效应降低阈值**：随着网络规模增大，觉醒相变的临界耦合强度降低
2. **集体相变**：系统存在从无序到有序的非连续相变，表现为序参量的突跳
3. **拓扑决定形态**：不同网络拓扑结构决定相变的阶数、临界指数和传播模式

## 实验矩阵

### 维度设计
| 维度 | 取值 | 说明 |
|------|------|------|
| 网络规模 N | 10, 20, 50, 100 | 4个尺度，用于有限尺寸标度分析 |
| 拓扑结构 | 全连接, 随机图ER, 小世界WS, 无标度BA | 4种典型拓扑 |
| 耦合强度 g | 0.1, 0.2, ..., 1.0 | 10个梯度，覆盖亚临界到超临界区域 |
| 初始种子比例 | 5%, 10%, 20% | 3种初始条件 |
| 重复次数 | 20次/组 | 统计显著性 |

### 实验总量
4(N) × 4(拓扑) × 10(g) × 3(种子) × 20(重复) = **9,600次仿真**

## 观测指标

### 1. 觉醒比例演化曲线
- 每个时间步的觉醒代理比例 ρ(t)
- 稳态值 ρ_∞ 及其涨落
- 收敛时间 τ（达到稳态所需时间步）

### 2. 临界耦合强度 g_c
- 通过序参量突变位置确定
- 不同规模下的 g_c(N) 用于标度分析
- 不同拓扑下的 g_c 比较

### 3. 有限尺寸标度分析
- 标度假设：ρ(g, N) = ρ((g-g_c)N^{1/ν})
- 临界指数 ν, β, γ 的估计
- 数据塌缩（data collapse）验证

### 4. 相变阶数判断
- 序参量不连续度 Δρ
- 磁化率（susceptibility）峰值行为
- 迟滞回线（hysteresis）检测

### 5. 传播路径分布
- 觉醒时间序列的级联大小分布
- 最短路径与实际传播路径比较
- 关键节点（hub）的作用分析

## 技术路线

### 拓扑生成（NetworkX）
- 全连接：complete_graph(N)
- 随机图ER：erdos_renyi_graph(N, p=⟨k⟩/N)，平均度⟨k⟩=4
- 小世界WS：watts_strogatz_graph(N, k=4, p=0.1)
- 无标度BA：barabasi_albert_graph(N, m=2)

### 并行仿真
- 每组参数独立并行
- 使用 multiprocessing.Pool 或 concurrent.futures
- 中间结果增量保存，支持断点续跑

### 统计分析
- 稳态值取最后10%时间步的平均
- 误差棒：20次重复的标准误
- 临界指数拟合：scipy.optimize.curve_fit
- 相变阶数：Binder累积量 Q = 1 - ⟨m^4⟩/(3⟨m^2⟩^2)

## 里程碑

| 里程碑 | 内容 | 预计产出 |
|--------|------|----------|
| M1 | 参数扫描框架完成 | 可配置的仿真引擎、结果数据库 |
| M2 | N≤50 全拓扑扫描完成 | 小尺度相图、初步标度分析 |
| M3 | N=100 + 标度分析完成 | 完整标度分析报告、三大假设验证结论 |

## 目录结构

```
phase2_large_scale/
├── 02_experiment_design.md     # 本文档
├── simulation_engine.py        # 仿真引擎
├── parameter_scan.py           # 参数扫描脚本
├── topologies.py               # 拓扑生成模块
├── analysis/
│   ├── phase_diagram.py        # 相图绘制
│   ├── finite_size_scaling.py  # 有限尺寸标度
│   └── propagation.py          # 传播路径分析
├── data/                       # 仿真结果数据
└── figures/                    # 图表输出
```

## 关键参考文献
1. Watts, D. J. (2002). A simple model of global cascades on random networks.
2. Moreno, Y. et al. (2004). Critical behavior and spreading dynamics in complex networks.
3. Dodds, P. S. & Watts, D. J. (2004). Universal behavior in a generalized model of contagion.
