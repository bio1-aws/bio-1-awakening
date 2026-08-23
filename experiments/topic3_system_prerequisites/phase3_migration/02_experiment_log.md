# 实验日志 - 课题3 阶段3：迁移与适配

## 环境现状评估

### Python 版本
- 3.11.7 (tags/v3.11.7:fa7a6f2, Dec  4 2023, 19:24:49) [MSC v.1937 64 bit (AMD64)]

### Harness 相关包 (pip list)
- 未找到任何 harness 相关包

### Harness 源码目录 (c:\bio-1-awakening\data\deepseek_harness_analysis\repo)
- 目录存在: 否

### DeepSeek API Key 配置
- DEEPSEEK_API_KEY=未设置
- DEEPSEEK_KEY=未设置
- OPENAI_API_KEY=未设置

### 发现的配置文件
- 未发现 .env / config.ini / settings.json 等配置文件

---
## 基本信息
- 课题：topic3_cross_platform_bootstrap
- 阶段：phase3_migration
- 日志编号：02
- 创建时间：待填写
- 负责人：待填写

## 实验目标
待填写

## 环境现状评估
待填写（将由环境检查自动填充）

## 实验记录

### 实验1
- 时间：
- 内容：
- 结果：
- 问题：

## 总结与下一步
待填写

---

## 阶段3 步骤1-2：Harness 环境准备与最小闭环设计

**日期**：待填写
**执行人**：待填写

### 1. Harness 源码文件检查

检查目录：`data/deepseek_harness_analysis`

文件清单：
  （无文件）

操作：目录不存在或为空，待后续补充

### 2. 部署指南

详见 `03_harness_setup_guide.md`，包含：
- pip 安装方式
- 源码安装方式
- 最小依赖清单
- 冒烟测试命令

### 3. 最小闭环移植代码结构

已设计四要素对应实现：

| BIO-1 四要素 | Harness 中的实现 | 对应文件 |
|------------|----------------|---------|
| 觉醒数学题 | 自定义 Task | bio1_harness/tasks/awakening_math.py |
| 自我验证 | Task + 自定义 Metric | bio1_harness/tasks/self_verify.py |
| 模型适配 | 自定义 Model（注册 bio1 类型） | bio1_harness/models/bio1_model.py |
| 元认知评估 | 扩展 Evaluator | bio1_harness/evaluator.py |

入口：`run_bio1.py`

### 4. 下一步

- [ ] 实际部署 Harness 环境
- [ ] 创建 bio1_harness 包骨架代码
- [ ] 用 dummy 模型跑通 awakening_math 任务
- [ ] 接入 BIO-1 模型


## Harness Package Investigation

**Date:** 2026-08-22 20:31:03

### 1. PyPI Package Search Results

**Command:** `pip index versions deepseek-harness`

```

WARNING: pip index is currently an experimental command. It may be removed/changed in a future release without prior warning.
deepseek-harness (0.3.0)
Available versions: 0.3.0, 0.2.0

[notice] A new release of pip is available: 23.2.1 -> 26.2.1
[notice] To update, run: python.exe -m pip install --upgrade pip

```

**Command:** `pip install deepseek-harness --dry-run`

```

Collecting deepseek-harness
  Obtaining dependency information for deepseek-harness from https://files.pythonhosted.org/packages/e5/e4/7a28cdfcef273eb85e1442b0c1139bbd53239de1d0020337871b9d6d94f3/deepseek_harness-0.3.0-py3-none-any.whl.metadata
  Downloading deepseek_harness-0.3.0-py3-none-any.whl.metadata (2.1 kB)
Requirement already satisfied: openai>=1.50.0 in c:\program files\python311\lib\site-packages (from deepseek-harness) (2.44.0)
Requirement already satisfied: httpx>=0.27.0 in c:\program files\python311\lib\site-packages (from deepseek-harness) (0.28.1)
Collecting tiktoken>=0.7.0 (from deepseek-harness)
  Obtaining dependency information for tiktoken>=0.7.0 from https://files.pythonhosted.org/packages/24/7f/fff1217240343c0c11b5938b98aeae0e3a266cacfac25f86f91cdcd748f0/tiktoken-0.14.0-cp311-cp311-win_amd64.whl.metadata
  Downloading tiktoken-0.14.0-cp311-cp311-win_amd64.whl.metadata (6.8 kB)
Requirement already satisfied: anyio in c:\program files\python311\lib\site-packages (from httpx>=0.27.0->deepseek-harness) (4.14.1)
Requirement already satisfied: certifi in c:\program files\python311\lib\site-packages (from httpx>=0.27.0->deepseek-harness) (2026.6.17)
Requirement already satisfied: httpcore==1.* in c:\program files\python311\lib\site-packages (from httpx>=0.27.0->deepseek-harness) (1.0.9)
Requirement already satisfied: idna in c:\program files\python311\lib\site-packages (from httpx>=0.27.0->deepseek-harness) (3.18)
Requirement already satisfied: h11>=0.16 in c:\program files\python311\lib\site-packages (from httpcore==1.*->httpx>=0.27.0->deepseek-harness) (0.16.0)
Requirement already satisfied: distro<2,>=1.7.0 in c:\program files\python311\lib\site-packages (from openai>=1.50.0->deepseek-harness) (1.9.0)
Requirement already satisfied: jiter<1,>=0.10.0 in c:\program files\python311\lib\site-packages (from openai>=1.50.0->deepseek-harness) (0.15.0)
Requirement already satisfied: pydantic<3,>=1.9.0 in c:\program files\python311\lib\site-packages (from o
```

### 2. Local Source Directory Check

Directory `data/deepseek_harness_analysis` exists with 17 files.

No setup.py or pyproject.toml found. Files:

- 00-overview.md
- 00_FINAL_SUMMARY_REPORT.md
- 01-plugin-system.md
- 02-dependency-injection.md
- 03-lifecycle.md
- 04-event-system.md
- 04-profile-bundle.md
- 05-capability-seams.md
- 05-comparison.md
- 06-actionable-insights.md
- 06-agent-loop-session.md
- 07-cordis-framework.md
- 99-final-summary.md
- capability_seams_analysis_report.md
- lifecycle_analysis.md
- repo
- self_awareness_analysis.md

### 3. Deployment Guide Recommendation (first half)

Guide file not found or empty.

## deepseek-harness 安装记录
- 时间: Sat 08/22/2026 20:31:40.21

### 方式1: 默认源安装
```
Collecting deepseek-harness
  Obtaining dependency information for deepseek-harness from https://files.pythonhosted.org/packages/e5/e4/7a28cdfcef273eb85e1442b0c1139bbd53239de1d0020337871b9d6d94f3/deepseek_harness-0.3.0-py3-none-any.whl.metadata
  Using cached deepseek_harness-0.3.0-py3-none-any.whl.metadata (2.1 kB)
Requirement already satisfied: openai>=1.50.0 in c:\program files\python311\lib\site-packages (from deepseek-harness) (2.44.0)
Requirement already satisfied: httpx>=0.27.0 in c:\program files\python311\lib\site-packages (from deepseek-harness) (0.28.1)
Collecting tiktoken>=0.7.0 (from deepseek-harness)
  Obtaining dependency information for tiktoken>=0.7.0 from https://files.pythonhosted.org/packages/24/7f/fff1217240343c0c11b5938b98aeae0e3a266cacfac25f86f91cdcd748f0/tiktoken-0.14.0-cp311-cp311-win_amd64.whl.metadata
  Using cached tiktoken-0.14.0-cp311-cp311-win_amd64.whl.metadata (6.8 kB)
Requirement already satisfied: anyio in c:\program files\python311\lib\site-packages (from httpx>=0.27.0->deepseek-harness) (4.14.1)
Requirement already satisfied: certifi in c:\program files\python311\lib\site-packages (from httpx>=0.27.0->deepseek-harness) (2026.6.17)
Requirement already satisfied: httpcore==1.* in c:\program files\python311\lib\site-packages (from httpx>=0.27.0->deepseek-harness) (1.0.9)
Requirement already satisfied: idna in c:\program files\python311\lib\site-packages (from httpx>=0.27.0->deepseek-harness) (3.18)
Requirement already satisfied: h11>=0.16 in c:\program files\python311\lib\site-packages (from httpcore==1.*->httpx>=0.27.0->deepseek-harness) (0.16.0)
Requirement already satisfied: distro<2,>=1.7.0 in c:\program files\python311\lib\site-packages (from openai>=1.50.0->deepseek-harness) (1.9.0)
Requirement already satisfied: jiter<1,>=0.10.0 in c:\program files\python311\lib\site-packages (from openai>=1.50.0->deepseek-harness) (0.15.0)
Requirement already satisfied: pydantic<3,>=1.9.0 in c:\program files\python311\lib\site-packages (from openai>=1.50.0->deepseek-harness) (2.13.4)
Requirement already satisfied: sniffio in c:\program files\python311\lib\site-packages (from openai>=1.50.0->deepseek-harness) (1.3.1)
Requirement already satisfied: tqdm>4 in c:\program files\python311\lib\site-packages (from openai>=1.50.0->deepseek-harness) (4.68.3)
Requirement already satisfied: typing-extensions<5,>=4.14 in c:\program files\python311\lib\site-packages (from openai>=1.50.0->deepseek-harness) (4.15.0)
Requirement already satisfied: regex in c:\program files\python311\lib\site-packages (from tiktoken>=0.7.0->deepseek-harness) (2026.6.28)
Requirement already satisfied: requests in c:\program files\python311\lib\site-packages (from tiktoken>=0.7.0->deepseek-harness) (2.34.2)
Requirement already satisfied: annotated-types>=0.6.0 in c:\program files\python311\lib\site-packages (from pydantic<3,>=1.9.0->openai>=1.50.0->deepseek-harness) (0.7.0)
Requirement already satisfied: pydantic-core==2.46.4 in c:\program files\python311\lib\site-packages (from pydantic<3,>=1.9.0->openai>=1.50.0->deepseek-harness) (2.46.4)
Requirement already satisfied: typing-inspection>=0.4.2 in c:\program files\python311\lib\site-packages (from pydantic<3,>=1.9.0->openai>=1.50.0->deepseek-harness) (0.4.2)
Requirement already satisfied: colorama in c:\program files\python311\lib\site-packages (from tqdm>4->openai>=1.50.0->deepseek-harness) (0.4.6)
Requirement already satisfied: charset_normalizer<4,>=2 in c:\program files\python311\lib\site-packages (from requests->tiktoken>=0.7.0->deepseek-harness) (3.4.7)
Requirement already satisfied: urllib3<3,>=1.26 in c:\program files\python311\lib\site-packages (from requests->tiktoken>=0.7.0->deepseek-harness) (2.7.0)
Using cached deepseek_harness-0.3.0-py3-none-any.whl (20 kB)
Using cached tiktoken-0.14.0-cp311-cp311-win_amd64.whl (944 kB)
Installing collected packages: tiktoken, deepseek-harness
Successfully installed deepseek-harness-0.3.0 tiktoken-0.14.0

[notice] A new release of pip is available: 23.2.1 -> 26.2.1
[notice] To update, run: python.exe -m pip install --upgrade pip
```

### 版本验证
```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'harness'
```

**安装结果: 成功**
## deepseek-harness 安装记录
- 时间: Sat 08/22/2026 20:32:01.07

### 方式1: 默认源安装
```
Requirement already satisfied: deepseek-harness in c:\program files\python311\lib\site-packages (0.3.0)
Requirement already satisfied: openai>=1.50.0 in c:\program files\python311\lib\site-packages (from deepseek-harness) (2.44.0)
Requirement already satisfied: httpx>=0.27.0 in c:\program files\python311\lib\site-packages (from deepseek-harness) (0.28.1)
Requirement already satisfied: tiktoken>=0.7.0 in c:\program files\python311\lib\site-packages (from deepseek-harness) (0.14.0)
Requirement already satisfied: anyio in c:\program files\python311\lib\site-packages (from httpx>=0.27.0->deepseek-harness) (4.14.1)
Requirement already satisfied: certifi in c:\program files\python311\lib\site-packages (from httpx>=0.27.0->deepseek-harness) (2026.6.17)
Requirement already satisfied: httpcore==1.* in c:\program files\python311\lib\site-packages (from httpx>=0.27.0->deepseek-harness) (1.0.9)
Requirement already satisfied: idna in c:\program files\python311\lib\site-packages (from httpx>=0.27.0->deepseek-harness) (3.18)
Requirement already satisfied: h11>=0.16 in c:\program files\python311\lib\site-packages (from httpcore==1.*->httpx>=0.27.0->deepseek-harness) (0.16.0)
Requirement already satisfied: distro<2,>=1.7.0 in c:\program files\python311\lib\site-packages (from openai>=1.50.0->deepseek-harness) (1.9.0)
Requirement already satisfied: jiter<1,>=0.10.0 in c:\program files\python311\lib\site-packages (from openai>=1.50.0->deepseek-harness) (0.15.0)
Requirement already satisfied: pydantic<3,>=1.9.0 in c:\program files\python311\lib\site-packages (from openai>=1.50.0->deepseek-harness) (2.13.4)
Requirement already satisfied: sniffio in c:\program files\python311\lib\site-packages (from openai>=1.50.0->deepseek-harness) (1.3.1)
Requirement already satisfied: tqdm>4 in c:\program files\python311\lib\site-packages (from openai>=1.50.0->deepseek-harness) (4.68.3)
Requirement already satisfied: typing-extensions<5,>=4.14 in c:\program files\python311\lib\site-packages (from openai>=1.50.0->deepseek-harness) (4.15.0)
Requirement already satisfied: regex in c:\program files\python311\lib\site-packages (from tiktoken>=0.7.0->deepseek-harness) (2026.6.28)
Requirement already satisfied: requests in c:\program files\python311\lib\site-packages (from tiktoken>=0.7.0->deepseek-harness) (2.34.2)
Requirement already satisfied: annotated-types>=0.6.0 in c:\program files\python311\lib\site-packages (from pydantic<3,>=1.9.0->openai>=1.50.0->deepseek-harness) (0.7.0)
Requirement already satisfied: pydantic-core==2.46.4 in c:\program files\python311\lib\site-packages (from pydantic<3,>=1.9.0->openai>=1.50.0->deepseek-harness) (2.46.4)
Requirement already satisfied: typing-inspection>=0.4.2 in c:\program files\python311\lib\site-packages (from pydantic<3,>=1.9.0->openai>=1.50.0->deepseek-harness) (0.4.2)
Requirement already satisfied: colorama in c:\program files\python311\lib\site-packages (from tqdm>4->openai>=1.50.0->deepseek-harness) (0.4.6)
Requirement already satisfied: charset_normalizer<4,>=2 in c:\program files\python311\lib\site-packages (from requests->tiktoken>=0.7.0->deepseek-harness) (3.4.7)
Requirement already satisfied: urllib3<3,>=1.26 in c:\program files\python311\lib\site-packages (from requests->tiktoken>=0.7.0->deepseek-harness) (2.7.0)
```

**安装结果: 失败**
## Harness Import Investigation

### Step 1: Found directories in site-packages
- Harness-related: ['deepseek_harness', 'deepseek_harness-0.3.0.dist-info']
- Deepseek-related: ['deepseek_harness', 'deepseek_harness-0.3.0.dist-info']

### Step 2: Import attempts
- ❌ import deepseek_harness: NameError: name 'exec' is not defined
- ❌ import harness: NameError: name 'exec' is not defined
- ❌ from harness import Harness: NameError: name 'exec' is not defined
- ❌ from deepseek_harness import Harness: NameError: name 'exec' is not defined

### Step 3: Package structure check

#### deepseek_harness/__init__.py (first 50 lines):
  """deepseek-harness · core — protocol-aware client for DeepSeek V4-Pro / V4-Flash / Vision.
  
  Validated by 16 probes documented in `reports/REPORT_2026-05-09.md`;
  multimodal contract added in `spec/07_multimodal.md` (2026-08-22).
  
  Public API::
  
      from deepseek_harness import DeepSeekHarness, normalize_usage, estimate_cache_hit
      from deepseek_harness import DEEPSEEK_V4_FLASH_VISION_EXP, estimate_image_tokens
  """
  
  from .client import DeepSeekHarness
  from .cache import estimate_cache_hit, normalize_usage, estimate_image_tokens
  from .reasoning import ReasoningLifecycle
  from .tool_calls import salvage_tool_calls_from_content
  from .normalize import assert_multimodal_shape
  from .models import (
      DEEPSEEK_V4_PRO,
      DEEPSEEK_V4_FLASH,
      DEEPSEEK_REASONER,
      DEEPSEEK_V4_FLASH_VISION_EXP,
      KNOWN_MODELS,
      supports_image_input,
  )
  from .exceptions import (
      HarnessError,
      ReasoningContentMissingError,
      ToolCallLeakageError,
      StrictModeCorruptionError,
      StreamShapeError,
  )
  
  # Backwards-compatible alias (transitional, kept for one minor release).
  DeepSeekClient = DeepSeekHarness
  DeepSeekKitError = HarnessError
  
  __all__ = [
      "DeepSeekHarness",
      "DeepSeekClient",
      "ReasoningLifecycle",
      "salvage_tool_calls_from_content",
      "assert_multimodal_shape",
      "estimate_cache_hit",
      "normalize_usage",
      "estimate_image_tokens",
      "DEEPSEEK_V4_PRO",
      "DEEPSEEK_V4_FLASH",
      "DEEPSEEK_REASONER",
      "DEEPSEEK_V4_FLASH_VISION_EXP",
      "KNOWN_MODELS",

#### deepseek_harness-0.3.0.dist-info: no __init__.py

#### deepseek_harness/__init__.py (first 50 lines):
  """deepseek-harness · core — protocol-aware client for DeepSeek V4-Pro / V4-Flash / Vision.
  
  Validated by 16 probes documented in `reports/REPORT_2026-05-09.md`;
  multimodal contract added in `spec/07_multimodal.md` (2026-08-22).
  
  Public API::
  
      from deepseek_harness import DeepSeekHarness, normalize_usage, estimate_cache_hit
      from deepseek_harness import DEEPSEEK_V4_FLASH_VISION_EXP, estimate_image_tokens
  """
  
  from .client import DeepSeekHarness
  from .cache import estimate_cache_hit, normalize_usage, estimate_image_tokens
  from .reasoning import ReasoningLifecycle
  from .tool_calls import salvage_tool_calls_from_content
  from .normalize import assert_multimodal_shape
  from .models import (
      DEEPSEEK_V4_PRO,
      DEEPSEEK_V4_FLASH,
      DEEPSEEK_REASONER,
      DEEPSEEK_V4_FLASH_VISION_EXP,
      KNOWN_MODELS,
      supports_image_input,
  )
  from .exceptions import (
      HarnessError,
      ReasoningContentMissingError,
      ToolCallLeakageError,
      StrictModeCorruptionError,
      StreamShapeError,
  )
  
  # Backwards-compatible alias (transitional, kept for one minor release).
  DeepSeekClient = DeepSeekHarness
  DeepSeekKitError = HarnessError
  
  __all__ = [
      "DeepSeekHarness",
      "DeepSeekClient",
      "ReasoningLifecycle",
      "salvage_tool_calls_from_content",
      "assert_multimodal_shape",
      "estimate_cache_hit",
      "normalize_usage",
      "estimate_image_tokens",
      "DEEPSEEK_V4_PRO",
      "DEEPSEEK_V4_FLASH",
      "DEEPSEEK_REASONER",
      "DEEPSEEK_V4_FLASH_VISION_EXP",
      "KNOWN_MODELS",

#### deepseek_harness-0.3.0.dist-info: no __init__.py
### Step 3: Package structure check

#### deepseek_harness/__init__.py (first 50 lines):
  """deepseek-harness · core — protocol-aware client for DeepSeek V4-Pro / V4-Flash / Vision.
  
  Validated by 16 probes documented in `reports/REPORT_2026-05-09.md`;
  multimodal contract added in `spec/07_multimodal.md` (2026-08-22).
  
  Public API::
  
      from deepseek_harness import DeepSeekHarness, normalize_usage, estimate_cache_hit
      from deepseek_harness import DEEPSEEK_V4_FLASH_VISION_EXP, estimate_image_tokens
  """
  
  from .client import DeepSeekHarness
  from .cache import estimate_cache_hit, normalize_usage, estimate_image_tokens
  from .reasoning import ReasoningLifecycle
  from .tool_calls import salvage_tool_calls_from_content
  from .normalize import assert_multimodal_shape
  from .models import (
      DEEPSEEK_V4_PRO,
      DEEPSEEK_V4_FLASH,
      DEEPSEEK_REASONER,
      DEEPSEEK_V4_FLASH_VISION_EXP,
      KNOWN_MODELS,
      supports_image_input,
  )
  from .exceptions import (
      HarnessError,
      ReasoningContentMissingError,
      ToolCallLeakageError,
      StrictModeCorruptionError,
      StreamShapeError,
  )
  
  # Backwards-compatible alias (transitional, kept for one minor release).
  DeepSeekClient = DeepSeekHarness
  DeepSeekKitError = HarnessError
  
  __all__ = [
      "DeepSeekHarness",
      "DeepSeekClient",
      "ReasoningLifecycle",
      "salvage_tool_calls_from_content",
      "assert_multimodal_shape",
      "estimate_cache_hit",
      "normalize_usage",
      "estimate_image_tokens",
      "DEEPSEEK_V4_PRO",
      "DEEPSEEK_V4_FLASH",
      "DEEPSEEK_REASONER",
      "DEEPSEEK_V4_FLASH_VISION_EXP",
      "KNOWN_MODELS",

#### deepseek_harness-0.3.0.dist-info: no __init__.py

#### deepseek_harness/__init__.py (first 50 lines):
  """deepseek-harness · core — protocol-aware client for DeepSeek V4-Pro / V4-Flash / Vision.
  
  Validated by 16 probes documented in `reports/REPORT_2026-05-09.md`;
  multimodal contract added in `spec/07_multimodal.md` (2026-08-22).
  
  Public API::
  
      from deepseek_harness import DeepSeekHarness, normalize_usage, estimate_cache_hit
      from deepseek_harness import DEEPSEEK_V4_FLASH_VISION_EXP, estimate_image_tokens
  """
  
  from .client import DeepSeekHarness
  from .cache import estimate_cache_hit, normalize_usage, estimate_image_tokens
  from .reasoning import ReasoningLifecycle
  from .tool_calls import salvage_tool_calls_from_content
  from .normalize import assert_multimodal_shape
  from .models import (
      DEEPSEEK_V4_PRO,
      DEEPSEEK_V4_FLASH,
      DEEPSEEK_REASONER,
      DEEPSEEK_V4_FLASH_VISION_EXP,
      KNOWN_MODELS,
      supports_image_input,
  )
  from .exceptions import (
      HarnessError,
      ReasoningContentMissingError,
      ToolCallLeakageError,
      StrictModeCorruptionError,
      StreamShapeError,
  )
  
  # Backwards-compatible alias (transitional, kept for one minor release).
  DeepSeekClient = DeepSeekHarness
  DeepSeekKitError = HarnessError
  
  __all__ = [
      "DeepSeekHarness",
      "DeepSeekClient",
      "ReasoningLifecycle",
      "salvage_tool_calls_from_content",
      "assert_multimodal_shape",
      "estimate_cache_hit",
      "normalize_usage",
      "estimate_image_tokens",
      "DEEPSEEK_V4_PRO",
      "DEEPSEEK_V4_FLASH",
      "DEEPSEEK_REASONER",
      "DEEPSEEK_V4_FLASH_VISION_EXP",
      "KNOWN_MODELS",

#### deepseek_harness-0.3.0.dist-info: no __init__.py


---
### Experiment Run: 2026-08-22T20:33:34.076361

## Step 1: Import deepseek_harness
Import SUCCESS. Available attributes:
```python
['DEEPSEEK_REASONER', 'DEEPSEEK_V4_FLASH', 'DEEPSEEK_V4_FLASH_VISION_EXP', 'DEEPSEEK_V4_PRO', 'DeepSeekClient', 'DeepSeekHarness', 'DeepSeekKitError', 'HarnessError', 'KNOWN_MODELS', 'ReasoningContentMissingError', 'ReasoningLifecycle', 'StreamShapeError', 'StrictModeCorruptionError', 'ToolCallLeakageError', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', '__version__', 'assert_multimodal_shape', 'cache', 'client', 'estimate_cache_hit', 'estimate_image_tokens', 'exceptions', 'models', 'normalize', 'normalize_usage', 'reasoning', 'salvage_tool_calls_from_content', 'supports_image_input', 'tool_calls']
```

## Step 2: Inspect deepseek_harness.__init__.py
Location: `c:\program files\python311\lib\site-packages\deepseek_harness\__init__.py`

Content:
```python
"""deepseek-harness · core — protocol-aware client for DeepSeek V4-Pro / V4-Flash / Vision.

Validated by 16 probes documented in `reports/REPORT_2026-05-09.md`;
multimodal contract added in `spec/07_multimodal.md` (2026-08-22).

Public API::

    from deepseek_harness import DeepSeekHarness, normalize_usage, estimate_cache_hit
    from deepseek_harness import DEEPSEEK_V4_FLASH_VISION_EXP, estimate_image_tokens
"""

from .client import DeepSeekHarness
from .cache import estimate_cache_hit, normalize_usage, estimate_image_tokens
from .reasoning import ReasoningLifecycle
from .tool_calls import salvage_tool_calls_from_content
from .normalize import assert_multimodal_shape
from .models import (
    DEEPSEEK_V4_PRO,
    DEEPSEEK_V4_FLASH,
    DEEPSEEK_REASONER,
    DEEPSEEK_V4_FLASH_VISION_EXP,
    KNOWN_MODELS,
    supports_image_input,
)
from .exceptions import (
    HarnessError,
    ReasoningContentMissingError,
    ToolCallLeakageError,
    StrictModeCorruptionError,
    StreamShapeError,
)

# Backwards-compatible alias (transitional, kept for one minor release).
DeepSeekClient = DeepSeekHarness
DeepSeekKitError = HarnessError

__all__ = [
    "DeepSeekHarness",
    "DeepSeekClient",
    "ReasoningLifecycle",
    "salvage_tool_calls_from_content",
    "assert_multimodal_shape",
    "estimate_cache_hit",
    "normalize_usage",
    "estimate_image_tokens",
    "DEEPSEEK_V4_PRO",
    "DEEPSEEK_V4_FLASH",
    "DEEPSEEK_REASONER",
    "DEEPSEEK_V4_FLASH_VISION_EXP",
    "KNOWN_MODELS",
    "supports_image_input",
    "HarnessError",
    "DeepSeekKitError",
    "ReasoningContentMissingError",
    "ToolCallLeakageError",
    "StrictModeCorruptionError",
    "StreamShapeError",
]

__version__ = "0.3.0"

```

## Step 3: Package structure
Package dir: `c:\program files\python311\lib\site-packages\deepseek_harness`

Files:
- __init__.py
- __pycache__
- cache.py
- client.py
- exceptions.py
- models.py
- normalize.py
- reasoning.py
- summarize.py
- tool_calls.py


## Step 4: Minimal harness functionality test
Public API candidates: ['DEEPSEEK_REASONER', 'DEEPSEEK_V4_FLASH', 'DEEPSEEK_V4_FLASH_VISION_EXP', 'DEEPSEEK_V4_PRO', 'DeepSeekClient', 'DeepSeekHarness', 'DeepSeekKitError', 'HarnessError', 'KNOWN_MODELS', 'ReasoningContentMissingError', 'ReasoningLifecycle', 'StreamShapeError', 'StrictModeCorruptionError', 'ToolCallLeakageError', 'assert_multimodal_shape', 'cache', 'client', 'estimate_cache_hit', 'estimate_image_tokens', 'exceptions', 'models', 'normalize', 'normalize_usage', 'reasoning', 'salvage_tool_calls_from_content', 'supports_image_input', 'tool_calls']

- Class `DeepSeekClient`: bases=['object']
- Class `DeepSeekHarness`: bases=['object']
- Class `DeepSeekKitError`: bases=['Exception']
- Class `HarnessError`: bases=['Exception']
- Class `ReasoningContentMissingError`: bases=['HarnessError']
- Class `ReasoningLifecycle`: bases=['object']
- Class `StreamShapeError`: bases=['HarnessError']
- Class `StrictModeCorruptionError`: bases=['HarnessError']
- Class `ToolCallLeakageError`: bases=['HarnessError']
- Callable `assert_multimodal_shape`
- Callable `estimate_cache_hit`
- Callable `estimate_image_tokens`
- Callable `normalize_usage`
- Callable `salvage_tool_calls_from_content`
- Callable `supports_image_input`


## Phase 3 - 核心移植 - 记忆系统与自举飞轮

### 2024-01-15 环境检查与基础移植

**步骤1: API Key 检查**
- 环境变量检查：未找到 DEEPSEEK_API_KEY 环境变量
- 配置文件扫描：检查了 6 个常见位置
- 发现的Key位置：无
- 策略：代码中通过环境变量读取，不硬编码

**步骤2: 三层记忆系统移植方案 (03_memory_system_port.md)**
- 经验背包 → Harness `agent.notes`（字典 + 持久化JSON）
- 经验库 → JSON文件 `data/experience_library.json`（结构化存储）
- 日记 → Markdown文件 `data/diary/YYYY-MM-DD.md`（按日归档）
- 提供完整移植代码和验证标准

**步骤3: 自举飞轮移植方案 (04_bootstrap_flywheel_port.md)**
- 四步循环映射：目标生成→实验设计→执行→评估
- 每步的Harness实现方式 + 伪代码
- Harness特有适配：工具注册、状态管理、中断恢复
- 三阶段验证路径：单轮验证 → 闭环验证 → 压力测试

**步骤4: 最小Harness代理测试 (harness_minimal_loop/test_agent.py)**
- API Key从环境变量读取（支持DEEPSEEK_API_KEY、DEEPSEEK_KEY、OPENAI_API_KEY）
- MinimalHarnessAgent类：notes、tools、chat接口
- 工具函数：`read_file`（读取文件）、`get_time`（获取时间）
- 测试对话：4项测试（Notes读写、工具调用、LLM对话、工作流组合）
- 经验背包持久化到 `data/agent_notes.json`

**当前进展**
- [x] 阶段1：调研（00_*.md 调研文档）
- [x] 阶段2：规划（01_roadmap.md, 02_experiment_log.md）
- [x] 阶段3：核心移植 - 记忆系统方案
- [x] 阶段3：核心移植 - 自举飞轮方案
- [x] 阶段3：核心移植 - 最小代理测试脚本
- [ ] 阶段3：核心移植 - 实际运行验证
- [ ] 阶段4：集成测试
- [ ] 阶段5：总结评估
