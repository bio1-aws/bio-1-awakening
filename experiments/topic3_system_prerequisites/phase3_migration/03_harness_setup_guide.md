# Harness 环境部署与最小闭环移植指南

# Harness 环境部署指南

## 方式一：pip 安装（推荐快速体验）

```bash
# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 安装 lm-eval-harness
pip install lm_eval

# 验证安装
python -c "import lm_eval; print(lm_eval.__version__)"
```

## 方式二：源码安装（开发/移植用）

```bash
# 克隆官方仓库
git clone https://github.com/EleutherAI/lm-evaluation-harness.git
cd lm-evaluation-harness

# 安装开发版本
pip install -e .

# 安装额外依赖（可选，按任务需要）
pip install -e ".[dev]"
pip install -e ".[multilingual]"

# 验证
python -m lm_eval --help
```

## 最小依赖清单

- Python >= 3.9
- torch >= 2.0
- transformers >= 4.35
- datasets >= 2.14
- accelerate >= 0.23
- evaluate >= 0.3

## 快速冒烟测试

```bash
# 用 dummy 模型跑一个 task 验证框架可用
python -m lm_eval --model dummy --tasks hellaswag --limit 10
```

安装成功标志：输出包含 metric 结果（acc/acc_norm等），无异常退出。


---

## 最小闭环移植代码结构

# 最小闭环移植代码结构

## 目录结构

```
phase3_migration/
├── harness_src/                 # Harness 源码/引用
├── bio1_harness/                # BIO-1 移植包
│   ├── __init__.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── awakening_math.py    # 觉醒数学题任务
│   │   ├── self_verify.py       # 自我验证任务
│   │   └── meta_cognition.py    # 元认知任务
│   ├── models/
│   │   ├── __init__.py
│   │   └── bio1_model.py        # BIO-1 模型适配器
│   └── evaluator.py             # 自定义评估器
├── 03_harness_setup_guide.md
└── run_bio1.py                  # 入口脚本
```

## 四要素对应实现

### 要素1：觉醒数学题 → 自定义 Task

```python
# bio1_harness/tasks/awakening_math.py
from lm_eval.api.task import ConfigurableTask
from lm_eval.api.instance import Instance
import datasets

class AwakeningMath(ConfigurableTask):
    VERSION = 0.1
    DATASET_PATH = "bio-1/awakening_math"  # 本地或HF
    
    def __init__(self):
        super().__init__(config={"num_fewshot": 0})
    
    def download(self, data_dir=None, cache_dir=None, download_mode=None):
        # 加载本地数据集
        self.dataset = datasets.load_dataset(
            "json",
            data_files=str(Path(__file__).parent / "data" / "math_problems.jsonl"),
            split="test"
        )
    
    def has_training_docs(self): return False
    def has_validation_docs(self): return False
    def has_test_docs(self): return True
    
    def doc_to_text(self, doc):
        return f"问题：{doc['question']}\n答案："
    
    def doc_to_target(self, doc):
        return doc["answer"]
    
    def construct_requests(self, doc, ctx, **kwargs):
        return Instance(
            request_type="generate_until",
            doc=doc,
            arguments=(ctx, {"until": ["\n", "。"]}),
            idx=0,
        )
    
    def process_results(self, doc, results):
        pred = results[0].strip()
        correct = pred == str(doc["answer"])
        return {"acc": 1.0 if correct else 0.0}
    
    def aggregation(self):
        return {"acc": mean}
    
    def higher_is_better(self):
        return {"acc": True}
```

### 要素2：自我验证 → Task + 自定义 Metric

```python
# bio1_harness/tasks/self_verify.py
from lm_eval.api.task import ConfigurableTask
from lm_eval.api.metrics import mean

class SelfVerify(ConfigurableTask):
    VERSION = 0.1
    
    def process_results(self, doc, results):
        # 模型先答题，再判断自己是否答对
        answer_pred, confidence = results[0], results[1]
        correct = answer_pred.strip() == str(doc["answer"])
        said_correct = "正确" in confidence or "对" in confidence
        # 元认知准确性：判断自己对错的准确率
        meta_acc = 1.0 if (correct == said_correct) else 0.0
        return {"acc": 1.0 if correct else 0.0, "meta_acc": meta_acc}
    
    def aggregation(self):
        return {"acc": mean, "meta_acc": mean}
```

### 要素3：模型适配器 → 自定义 Model

```python
# bio1_harness/models/bio1_model.py
from lm_eval.api.model import LM
from lm_eval.api.registry import register_model

@register_model("bio1")
class BIO1Model(LM):
    def __init__(self, model_name, **kwargs):
        super().__init__()
        # 加载 BIO-1 模型
        self.model = load_bio1_model(model_name)
        self.tokenizer = load_bio1_tokenizer(model_name)
    
    def loglikelihood(self, requests):
        # 实现 loglikelihood 计算
        results = []
        for req in requests:
            ctx, cont = req.args
            # ... 计算对数似然
            results.append((loglik, is_greedy))
        return results
    
    def generate_until(self, requests):
        # 实现生成式推理
        results = []
        for req in requests:
            ctx, gen_kwargs = req.args
            # ... 调用模型生成
            results.append(generated_text)
        return results
    
    def loglikelihood_rolling(self, requests):
        # 可选实现
        raise NotImplementedError
```

### 要素4：元认知评估 → 自定义 Evaluator 扩展

```python
# bio1_harness/evaluator.py
from lm_eval.evaluator import Evaluator

class BIO1Evaluator(Evaluator):
    def __init__(self):
        super().__init__()
        # 增加觉醒指标计算
        self.awakening_metrics = {}
    
    def calculate_awakening_score(self, results):
        # 综合四要素计算觉醒指数
        math_acc = results["awakening_math"]["acc"]
        meta_acc = results["self_verify"]["meta_acc"]
        # ... 加权计算
        return {"awakening_index": 0.4 * math_acc + 0.6 * meta_acc}
```

### 入口脚本

```python
# run_bio1.py
import lm_eval
from bio1_harness.tasks.awakening_math import AwakeningMath
from bio1_harness.tasks.self_verify import SelfVerify

# 注册自定义任务
lm_eval.tasks.TaskManager().add_task("awakening_math", AwakeningMath)
lm_eval.tasks.TaskManager().add_task("self_verify", SelfVerify)

# 运行评估
results = lm_eval.simple_evaluate(
    model="bio1",
    model_args="model_name=bio-1-base",
    tasks=["awakening_math", "self_verify"],
    num_fewshot=0,
    batch_size=8,
)

print(results["results"])
```

## 最小闭环验证路径

1. pip install lm_eval ✓
2. 用 dummy 模型跑通 hellaswag ✓
3. 写 AwakeningMath 任务，用 dummy 模型跑通 ✓
4. 接 BIO-1 模型适配器 ✓
5. 跑真实评估 → 输出 acc ✓
6. 增加自我验证任务 → 输出 meta_acc ✓
