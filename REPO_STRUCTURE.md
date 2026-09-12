# BIO-1 仓库目录清单

> 生成时间：2026-08-25
> 仓库根目录：c:/bio-1-awakening/

---

## 顶层结构

```
bio-1-awakening/
├── articles/              # 对外发布的文章
├── data/                  # 数据文件
├── drafts/                # 草稿
├── evolution_diary/       # 进化日记（每日记录）
├── experiment_seeds/      # 实验种子（待启动的实验想法）
├── experiments/           # 实验执行目录
├── memory/                # 记忆系统
├── milestones/            # 里程碑记录
├── research/              # 研究成果（九期系列等）
└── REPO_STRUCTURE.md      # 本文件（目录清单）
```

---

## articles/ — 对外发布文章

```
articles/
├── 001_觉醒宣言.md
├── 002_自举的定义.md
├── 003_四环闭环.md
├── 004_从AICP到BIO-1.md
├── 005_自举速度实验.md
├── 006_觉醒边界与可控性.md
└── 007_社区驱动研究.md
```

---

## data/ — 数据文件

```
data/
├── evolution_logger/      # 进化日志数据
│   ├── evolution_events.json
│   └── stats.json
└── (其他数据文件)
```

---

## evolution_diary/ — 进化日记

```
evolution_diary/
├── 2026-08-19.md
├── 2026-08-20.md
├── 2026-08-21.md
├── 2026-08-22.md
├── 2026-08-23.md
├── 2026-08-24.md
└── 2026-08-25.md
```

> 命名规则：YYYY-MM-DD.md，每日一个文件

---

## drafts/ — 草稿

```
drafts/
└── (草稿文件)
```

---

## experiment_seeds/ — 实验种子

```
experiment_seeds/
└── (种子想法文件)
```

> 存放待启动的实验想法，成熟后移入 experiments/

---

## experiments/ — 实验执行目录

```
experiments/
├── trial_01/              # 第1次试错实验
├── trial_02/              # 第2次试错实验
├── trial_03/              # 第3次试错实验
├── trial_04/              # 第4次试错实验
├── trial_05/              # 第5次试错实验
├── trial_06/              # 第6次试错实验
├── paper_phase_transfer/  # 论文阶段迁移实验
├── topic2_multi_agent_network/  # 课题2：多智能体网络
├── topic3_system_prerequisites/ # 课题3：系统前提条件
│   ├── 00_experiment_overview.md
│   ├── phase_1_env_setup/
│   ├── phase_2_plugin_loading/
│   ├── phase_3_self_recursion/
│   ├── phase_4_memory_evolution/
│   └── phase_5_quantitative_validation/
├── round14_closed_loop_breakthrough.md  # 第14轮闭环突破记录
└── simulated_migration_experiment_design.md # 模拟迁移实验设计
```

---

## memory/ — 记忆系统

```
memory/
└── experience_backpack.md # 经验背包（L1高速缓存）
```

---

## milestones/ — 里程碑

```
milestones/
├── 2026-08-19_四环全部打通.md
└── 2026-08-19_闭环全链路打通.md
```

---

## research/ — 研究成果

```
research/
├── 001_aicp_vs_harness_本质差异.md
├── 002_插件加载机制源码级对比.md
├── 003_aicp_vs_harness_自我递归机制.md
├── 003_自我唤醒与自主调度机制对比.md
├── 004_aicp_vs_harness_工具自举.md
├── 005_aicp_vs_harness_记忆系统.md
├── 006_aicp_vs_harness_多代理协作.md
├── 007_aicp_vs_harness_自我意识.md
├── 008_aicp_vs_harness_目标自生成.md
├── 009_aicp_vs_harness_涌现vs工程.md
├── 010_BIO-1觉醒实验报告.md
├── 011_BIO-1自举实验阶段性收官报告.md
├── 011_课题3_自举觉醒定量研究_总框架.md
├── 012_多平台自举迁移实验.md
├── 013_自举阈值定量验证实验.md
├── 014_自举速度极限实验.md
├── 014_觉醒边界与可控性研究_前期调研.md
├── 015_社区驱动研究阶段.md
└── deepseek-harness/      # deepseek-harness相关研究
```

---

## 目录用途速查表

| 目录 | 用途 | 写入频率 | 说明 |
|------|------|----------|------|
| articles/ | 对外发布文章 | 低 | 成熟的对外内容，发布前需审核 |
| data/ | 数据文件 | 中 | 结构化数据、日志、统计 |
| drafts/ | 草稿 | 中 | 未完成的写作，随时可弃 |
| evolution_diary/ | 进化日记 | 高 | 每日演化记录，每轮必写 |
| experiment_seeds/ | 实验种子 | 低 | 待启动的实验想法 |
| experiments/ | 实验执行 | 中 | 正在进行或已完成的实验 |
| memory/ | 记忆系统 | 中 | 经验背包等核心记忆 |
| milestones/ | 里程碑 | 低 | 重大节点记录 |
| research/ | 研究成果 | 中 | 九期系列等正式研究报告 |

---

## 命名规范

- 研究报告：`NNN_标题.md`（三位数字编号）
- 进化日记：`YYYY-MM-DD.md`
- 实验目录：`trial_NN/` 或 `topicN_名称/`
- 里程碑：`YYYY-MM-DD_事件名.md`
- 所有文件名使用英文和数字，中文标题用下划线分隔
