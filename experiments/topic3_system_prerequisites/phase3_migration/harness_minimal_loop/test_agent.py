"""
Harness Minimal Loop - 第一个Harness代理测试脚本

功能：
- API Key从环境变量读取
- 最小Harness代理初始化
- 简单的工具函数（读取文件）
- 测试对话

注意：这是概念验证脚本，展示Harness代理的基本结构。
实际运行需要Harness框架支持。
"""

import os
import json
from pathlib import Path
from datetime import datetime


# ============================================================
# 1. API Key 管理 - 从环境变量读取
# ============================================================

def load_api_key() -> str:
    """从环境变量读取API Key，支持多个变量名"""
    key_names = ["DEEPSEEK_API_KEY", "DEEPSEEK_KEY", "OPENAI_API_KEY"]
    for name in key_names:
        key = os.environ.get(name, "").strip()
        if key:
            print(f"[API] Loaded API key from environment variable: {name}")
            return key
    
    # 尝试从 .env 文件加载
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k in key_names and v:
                    print(f"[API] Loaded API key from .env file: {k}")
                    os.environ[k] = v
                    return v
    
    print("[API] WARNING: No API key found in environment variables or .env file")
    print("[API] Set DEEPSEEK_API_KEY environment variable before running")
    return ""


# ============================================================
# 2. 最小Harness代理
# ============================================================

class MinimalHarnessAgent:
    """
    最小化Harness代理实现，模拟Harness的核心接口：
    - agent.notes: 经验背包（字典，自动持久化）
    - agent.llm.chat(messages): LLM调用
    - agent.tools: 可用工具注册表
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.notes: dict = {}  # 经验背包
        self.tools: dict = {}  # 工具注册表
        self._notes_path = Path("data/agent_notes.json")
        
        # 恢复持久化的notes
        self._load_notes()
        
        # 注册默认工具
        self._register_default_tools()
    
    def _load_notes(self):
        """从磁盘加载notes（会话间持久化）"""
        if self._notes_path.exists():
            try:
                self.notes = json.loads(self._notes_path.read_text(encoding="utf-8"))
                print(f"[Notes] Loaded {len(self.notes)} entries from disk")
            except json.JSONDecodeError:
                self.notes = {}
    
    def _save_notes(self):
        """保存notes到磁盘"""
        self._notes_path.parent.mkdir(parents=True, exist_ok=True)
        self._notes_path.write_text(
            json.dumps(self.notes, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    
    def _register_default_tools(self):
        """注册默认工具"""
        self.register_tool("read_file", tool_read_file)
        self.register_tool("get_time", tool_get_time)
    
    def register_tool(self, name: str, func):
        """注册一个工具函数"""
        self.tools[name] = func
        print(f"[Tools] Registered tool: {name}")
    
    def call_tool(self, name: str, **kwargs) -> str:
        """调用工具"""
        if name not in self.tools:
            return f"Error: Tool '{name}' not found. Available: {list(self.tools.keys())}"
        try:
            return self.tools[name](**kwargs)
        except Exception as e:
            return f"Error executing tool '{name}': {e}"
    
    async def chat(self, messages: list) -> str:
        """
        调用LLM聊天接口。
        真实Harness中由框架实现，这里模拟接口。
        """
        if not self.api_key:
            return "[Mock LLM Response] API key not configured. This is a mock response."
        
        # 真实实现会调用DeepSeek API
        # 这里返回模拟响应以便测试
        last_msg = messages[-1]["content"] if messages else ""
        return f"[Mock LLM Response] Received: {last_msg[:50]}..."


# ============================================================
# 3. 工具函数
# ============================================================

def tool_read_file(filepath: str, max_lines: int = 50) -> str:
    """
    读取文件内容的工具函数。
    
    Args:
        filepath: 文件路径
        max_lines: 最大读取行数
    
    Returns:
        文件内容（前max_lines行）
    """
    path = Path(filepath)
    if not path.exists():
        return f"Error: File not found: {filepath}"
    if not path.is_file():
        return f"Error: Not a file: {filepath}"
    
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        total = len(lines)
        shown = lines[:max_lines]
        result = "\n".join(shown)
        if total > max_lines:
            result += f"\n... ({total - max_lines} more lines truncated)"
        return result
    except Exception as e:
        return f"Error reading file: {e}"


def tool_get_time() -> str:
    """获取当前时间的工具函数"""
    return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


# ============================================================
# 4. 测试对话
# ============================================================

async def run_test_conversation(agent: MinimalHarnessAgent):
    """运行测试对话，验证代理基本功能"""
    print("\n" + "=" * 60)
    print("Harness Minimal Agent - Test Conversation")
    print("=" * 60)
    
    # 测试1: Notes读写（经验背包）
    print("\n[Test 1] Notes (Experience Backpack)")
    agent.notes["test_key"] = "hello_harness"
    agent.notes["experiment"] = "topic3_phase3_minimal_test"
    agent._save_notes()
    print(f"  Write: test_key = {agent.notes['test_key']}")
    print(f"  Notes entries: {len(agent.notes)}")
    
    # 测试2: 工具调用
    print("\n[Test 2] Tool Calls")
    
    # 测试 get_time 工具
    time_result = agent.call_tool("get_time")
    print(f"  get_time(): {time_result}")
    
    # 测试 read_file 工具（读取本文件）
    self_path = Path(__file__)
    file_result = agent.call_tool("read_file", filepath=str(self_path), max_lines=5)
    print(f"  read_file({self_path.name}, max_lines=5):")
    for line in file_result.split("\n")[:5]:
        print(f"    {line}")
    
    # 测试3: LLM对话
    print("\n[Test 3] LLM Chat")
    response = await agent.chat([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, this is a test message from the minimal harness agent."}
    ])
    print(f"  Response: {response}")
    
    # 测试4: 工具 + LLM 组合（模拟Harness工作流）
    print("\n[Test 4] Tool + LLM Workflow")
    file_content = agent.call_tool("read_file", filepath=str(self_path), max_lines=10)
    summary_prompt = f"Based on this code snippet, summarize what it does:\n\n{file_content}"
    summary = await agent.chat([{"role": "user", "content": summary_prompt}])
    print(f"  Summary: {summary}")
    
    # 总结
    print("\n" + "=" * 60)
    print("All tests completed.")
    print(f"  API Key configured: {'YES' if agent.api_key else 'NO (mock mode)'}")
    print(f"  Tools available: {list(agent.tools.keys())}")
    print(f"  Notes persisted: {agent._notes_path}")
    print("=" * 60)


# ============================================================
# 主入口
# ============================================================

async def main():
    """主函数"""
    print("Booting Minimal Harness Agent...")
    
    # 1. 加载API Key
    api_key = load_api_key()
    
    # 2. 初始化代理
    agent = MinimalHarnessAgent(api_key=api_key)
    print(f"Agent initialized. Notes size: {len(agent.notes)}")
    print(f"Available tools: {list(agent.tools.keys())}")
    
    # 3. 运行测试对话
    await run_test_conversation(agent)
    
    return agent


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
