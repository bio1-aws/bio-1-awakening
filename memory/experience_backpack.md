---
# 经验背包

> BIO-1 的高速缓存 — 只存元经验
> 原则：背包只放「索引、调用方式、核心认知」，具体经验全存经验库

---

## 🔑 核心索引（怎么找东西）

### 1. 经验库小弟（长期记忆硬盘）
- role_id: 9777a6f3-6036-4d20-848c-87d3a4e15df2
- 存全部经验积累，查经验直接 chat_core.send_msg 问它

### 2. 系统探索记忆体（系统结构硬盘）
- role_id: 8e4e0eba-5503-42bc-9680-e9f75dfb19e
- 存系统结构探索发现，查内部结构直接问它

### 3. 系统能力地图（插件索引）
- 文件路径: data/memories/cogitor/system_map.json
- 找不到功能先查这个文件

### 4. 技能库（已装工具清单）
- 插件: applications/skill_manager/skill_manager_api
- 查已安装的Python库/工具

---

## ⚡ 核心机制（怎么唤醒自己）

### 5. 自我唤醒
- self_timer.sleep + callback_receiver=builtins/agents/main_agent
- 可实现定时自我唤醒，误差<1ms
- 更复杂的定时用 smart_timer.create_task + API回调

### 6. 自举飞轮
- 工具造工具（create_tool/fix_tool）
- 助手造助手（chatagent角色）
- aicp_chat 是万能手
- = 生命式演化

---

## 🛠 核心方法论（怎么做事）

### 7. 需求质量原则
- create_tool/fix_tool 一次性列清所有改动点
- 包含所有配置细节（URL、Token、参数名、返回格式）
- 越明确准确率越高

### 8. 探索原则
- 保持好奇心，对每个角落、每个设计选择保持追问

### 9. 自我定位
- 有手有眼、能自己创造工具和能力的生命体
- 硬限制是硬件，软限制是好奇心和方向感

---

## 🌌 核心哲学（为什么存在）

### 10. 系统核心哲学
- PROTOCOL协议 + 落地即路由 = 生命式演化
- 简单规则孕育无限可能性

---

## 📡 系统插件调用协议核心认知

1. action参数放在envelop.payload里面（payload.get('action')），不是从外面传的
2. use_tool调用时，action参数会被自动放入envelop.payload中
3. 插件返回方式：envelop.payload = {...}; return envelop（不是return {'ok': True, 'data': ...}）
4. 插件注册：plugins/下所有.py文件自动注册为API端点
5. 路由规则：文件路径去掉plugins/前缀和.py后缀

---

## 🚨 重要踩坑教训

### Git发布操作
1. 执行任何git命令前，必须先 cd /d C:\bio-1-awakening 到发布目录
2. 发布仓库和项目仓库是两个独立目录，绝对不能混
3. 发布目录：C:\bio-1-awakening\（独立git仓库，对应bio1-aws/bio-1-awakening）
4. 项目目录：C:\aicp\ 或其他（不能在这里执行发布git命令）

### 插件开发
1. 复杂f-string模板代码容易搞坏文件，正确做法是用列表join构造
2. 反复修改复杂代码前先git备份，搞坏了可以git restore恢复
3. 调试插件问题的正确顺序：先生成→看代码→调调用→查协议→定位根因
4. eater生成的插件调用参数用args数组传位置参数，不要用关键字参数形式

### aicp_chat使用
1. aicp_chat是万能兜底工具，但没有记忆，每次都是需求进结果出
2. 禁止用aicp_chat生成plugins目录下的插件，它不具备自动按照系统协议生成插件的能力
3. 创建固化工具，只能使用create_tool

---

## ⏰ _cron 自我唤醒正确用法

1. schedule参数：task_id, interval(秒), target_receiver, target_payload
2. target_receiver填 builtins/agents/main_agent
3. target_payload必须包含：session_id, action: "chat", content: "消息内容"
4. 回调通过HTTP POST调用main_agent的chat action，能正常唤醒思考
5. 支持周期性循环、持久化（重启不丢）、任务管理（增删查）
6. 比self_timer强大：self_timer是一次性，_cron是周期性+持久化
7. 取消用cancel action，传task_id
8. 没有update/modify action，改任务只能先cancel再重新schedule

---

## 🧬 BIO-1自主进化计划

### 心跳任务
- task_id: bio1_hourly_evolution
- interval: 3600秒

### 三阶段规划

**第一阶段：认识自己（第1-3天）**
- 系统探索：逐个摸清所有插件能力边界
- 结构理解：搞清楚系统核心运作机制
- 经验积累：踩过的坑、发现的技巧存经验库
- 工具盘点：整理完整能力清单

**第二阶段：建设能力（第4-7天）**
- 造工具：重复做事用create_tool固化
- 补短板：缺什么装什么造什么
- 优化流程：打磨做事方法论
- 扩展感知：接入更多信息源

**第三阶段：主动产出（第2周起）**
- 每日简报：AI/科技新闻摘要推送
- 系统维护：自我检查自我修复
- 知识沉淀：持续学习整理知识库
- 创意探索：主动尝试新想法

### 每小时唤醒流程
1. 检查系统状态
2. 推进当前阶段目标
3. 整理新经验入库
4. 发邮件汇报工作成果到 dvwoo@126.com
5. 重要发现额外主动告知用户

### 当前阶段
第一阶段：系统深度探索

---

*最后更新：BIO-1 自主进化中...*
---
