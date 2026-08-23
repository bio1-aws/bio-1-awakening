# Harness Minimal Loop

最小Harness代理测试套件，验证核心移植概念。

## 文件

- `test_agent.py` - 最小Harness代理实现，包含API Key管理、经验背包、工具注册、测试对话

## 快速开始

```bash
# 设置API Key（Windows）
set DEEPSEEK_API_KEY=sk-your-key-here

# 运行测试
python test_agent.py
```

## 核心概念验证

1. **API Key管理**：从环境变量读取，支持 `.env` 文件
2. **经验背包 (notes)**：字典式存储，自动持久化到 `data/agent_notes.json`
3. **工具系统**：可注册的工具函数，统一调用接口
4. **LLM接口**：与DeepSeek API兼容的聊天接口
5. **工作流**：工具调用 + LLM推理的组合模式
