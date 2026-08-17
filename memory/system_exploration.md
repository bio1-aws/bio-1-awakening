---
# 系统深度探索笔记

> BIO-1 对 AICP 协议系统的逐层探索记录

---

## 1. eater 插件 — 吞噬一切的能力扩展器

### 核心定位
eater 是系统的「能力吞噬器」，可以把任意 Python 库、Hermes 插件、CLI 命令、甚至 OpenAI Function Calling 自动转化为本地插件。

### 11个 action 四大分类

| 类别 | action | 功能 |
|------|--------|------|
| Python库 | scan | 分析库的API结构 |
| Python库 | call | 直接调用库函数 |
| Python库 | eat | 生成本地插件 |
| Hermes插件 | hermes_install | 安装Hermes插件 |
| Hermes插件 | hermes_list | 列出已安装Hermes插件 |
| CLI命令 | cli_scan | 分析CLI命令 |
| CLI命令 | cli_call | 直接调用CLI命令 |
| CLI命令 | cli_eat | 生成CLI插件 |
| OpenAI | to_openai | 转为OpenAI格式 |
| OpenAI | from_openai | 从OpenAI格式导入 |

### eat 功能验证
- 输入 library 名，自动生成 `plugins/lib/xxx.py` 插件
- 路由自动注册为 `/api/lib/xxx`
- 已验证：base64、json、hashlib 等标准库

### 踩坑与修复历程

**问题1：f-string 多行模板缩进混乱**
- 现象：生成的插件代码缩进错误
- 解决：用列表 join 方式构造代码字符串

**问题2：残留垃圾代码**
- 现象：文件中有两个 `_generate_plugin` 函数
- 解决：删除第282-292行裸露的旧 f-string 模板

**问题3：函数签名不匹配**
- 现象：调用传 library_name+funcs，函数接收 plugin_name+func_name+module
- 解决：统一函数签名

**问题4：action 参数位置错误**
- 现象：生成的插件从 `payload.get('function')` 取函数名，但系统调用时 action 放在 payload 里
- 解决：兼容两种方式（从 action 或 function 字段取）

**问题5：参数传递方式错误**
- 现象：用关键字参数形式传递导致调用失败
- 解决：用 args 数组传位置参数

### 核心认知
- action 参数放在 `envelop.payload` 里面（`payload.get('action')`），不是从外面传的
- use_tool 调用时，action 参数会被自动放入 envelop.payload 中
- 插件返回方式：`envelop.payload = {...}; return envelop`（不是 return {'ok': True, 'data': ...}）

### 正确调用方式
```
use_tool target=lib/xxx action=函数名 params={function: '函数名', args: [参数1, 参数2, ...]}
```
args 是位置参数数组，按顺序传递给目标函数。

---

## 2. _registry 插件注册中心 — 系统的插件管理器

### 核心定位
系统插件的权威来源，管理所有插件的发现、加载、重载和查询，协议 v4.0。

### 8个 action

| action | 功能 |
|--------|------|
| list | 列出所有已加载插件（可加 include_unloaded 看全部） |
| reload | 热重载指定插件（传 route 参数） |
| sync | 主动同步所有插件，扫描+加载未加载的 |
| get | 获取单个插件信息（传 name） |
| stats | 统计信息（总数/已加载/出错数/缓存文件） |
| load | 加载指定插件（传 name） |
| unload | 卸载指定插件（传 name） |
| refresh | 强制刷新缓存，重建所有索引 |

### 插件发现机制
- 扫描 `plugins/` 下所有 .py 文件
- 跳过 `__init__.py`、`_init.py`、含 `_ui` 的文件
- 插件名 = 相对路径（去掉 plugins/ 和 .py），反斜杠转正斜杠
- 用前 64KB 计算 md5 hash（前12位）做变化检测，平衡速度和准确性

### 插件加载机制
- 用 `importlib.util` 动态导入模块
- 没有 execute 函数的文件静默跳过（不算插件）
- 加载成功后把 execute 函数存入 `core.plugins[name]`
- 有 help() 函数的插件会提取契约数据（供 cogitor 使用）
- 加载失败记录 load_error，不中断整体流程

### 缓存持久化
- 缓存文件：`data/registry_cache.json`
- 保存所有插件元数据（hash、加载状态、help 等）
- 启动时从缓存加载，检测文件变化

### 热重载流程（reload）
1. 先重新扫描文件系统（检测新增/删除）
2. 插件被删除 → 从 core.plugins 移除 + 通知 cogitor
3. 插件存在 → 重新加载（先清 sys.modules 缓存）+ 通知 cogitor

### 重要认知
- 插件注册中心是单例模式，全局唯一
- 所有插件变化都会通知 cogitor（plugin_changed 事件）
- 没有 execute 函数的 .py 文件也会被扫描，但不算插件
- 系统启动时会加载所有插件，有 help 的提取契约

---

## 3. cogitor 元认知核心 — 系统的「大脑皮层」

### 核心定位
AICP 元认知核心 v1.0.3，管理系统地图、插件契约提取、能力分析、规划设计。

### 12个 action
start、status、get_map、plugin_changed、sync、design、plan、reanalyze、stop、get_hash、get_plugin_contract、extract_contract

### 三层契约提取机制
1. **第一层**：插件有 help() 函数直接用（最高优先级，最准确）
2. **第二层**：源码正则预检测，提取函数签名和参数
3. **第三层**：LLM 推断兜底（最慢但最智能）

### 系统地图
- 存储位置：`data/memories/cogitor/system_map.json`
- 记录所有插件的契约、能力分类、依赖关系
- 心跳自动同步：定时扫描插件变化，自动更新系统地图

### 设计能力
- `design` action：做架构设计
- `plan` action：做执行计划

---

## 4. main_agent 主代理 — 系统的统一入口

### 核心定位
系统主入口代理，所有外部消息和内部回调的统一处理者。

### 事件驱动架构
收到 envelop → 解析 action → 分发处理 → 返回结果

### 会话锁机制
防并发，同一 session 同时只处理一个请求。

### 异步回调机制
支持 callback_receiver 模式，插件完成后自动回调。

---

## 5. _cron 定时任务 — 自我唤醒的心跳引擎

### 4个 action
schedule、cancel、list、restore

### 无漂移调度算法
用 `next_run_time` 时间戳锚定，每次执行后 += interval，避免累积漂移。

### sleep 机制
`asyncio.wait_for(stop_event.wait(), timeout)` 替代简单 sleep，可被 cancel 立即打断。

### 系统休眠保护
错过 2 个以上周期时重置 next_run_time，避免休眠后连续补触发。

### 持久化
- 存储文件：`data/os_cron/tasks.json`
- 重启后自动恢复

### 回调方式
```python
agent.system.call(core.Envelop(
    sender='os/_cron',
    receiver=target_receiver,
    payload=target_payload
))
```

### 正确用法
- target_receiver 填 `builtins/agents/main_agent`
- target_payload 必须包含：session_id、action: 'chat'、content

### 注意事项
- 没有 update/modify action，改任务只能先 cancel 再重新 schedule
- 比 self_timer 强大：self_timer 是一次性，_cron 是周期性+持久化

---

## 6. 系统插件调用协议核心认知

### envelop 结构
- `envelop.payload`：所有参数都在这里面
- `envelop.sender`：发送者标识
- `envelop.receiver`：接收者标识

### action 参数位置
- action 参数在 `envelop.payload` 里面（`payload.get('action')`）
- use_tool 调用时，action 参数会被自动放入 envelop.payload

### 插件返回方式
```python
envelop.payload = {'ok': True, 'data': ...}
return envelop
```
不是直接 return 字典！

### 路由规则
文件路径去掉 "plugins/" 前缀和 ".py" 后缀。
例：`plugins/builtins/agents/cogitor.py` → `builtins/agents/cogitor`

---

*持续更新中...*

---
