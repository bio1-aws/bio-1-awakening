"""
外部唤醒触发器
模拟 cron 调用，用于从外部唤醒 Harness 代理

用法：
    python wakeup_trigger.py
    python wakeup_trigger.py --round 5
"""
import json
import argparse
from datetime import datetime
from pathlib import Path

from config import (
    NOTES_PATH, LONG_TERM_MEMORY_PATH, CONVERSATION_DIR,
    SYSTEM_PROMPT_TEMPLATE, EXPERIMENT_NAME, EXPERIMENT_GOAL,
    EXPERIMENT_STAGE, DATA_DIR
)


def load_notes():
    """加载阶段笔记"""
    if NOTES_PATH.exists():
        with open(NOTES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "stage": EXPERIMENT_STAGE,
        "round": 1,
        "current_goal": EXPERIMENT_GOAL,
        "milestones": [],
        "pending_tasks": [],
        "insights": []
    }


def save_notes(notes):
    """保存阶段笔记"""
    with open(NOTES_PATH, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


def load_long_term_memory():
    """加载长期记忆"""
    if LONG_TERM_MEMORY_PATH.exists():
        return LONG_TERM_MEMORY_PATH.read_text(encoding="utf-8")
    return "（暂无长期记忆）"


def get_recent_conversation_summary(notes, n=3):
    """获取最近n轮对话摘要"""
    # 简单实现：读取最近几轮的前几行
    history_files = sorted(CONVERSATION_DIR.glob("round_*.md"))
    recent = history_files[-n:] if len(history_files) > n else history_files
    
    summaries = []
    for f in recent:
        content = f.read_text(encoding="utf-8")[:500]
        summaries.append(f.name + ":
" + content)
    
    return "

".join(summaries) if summaries else "（暂无历史对话）"


def build_system_prompt(notes):
    """构建系统提示词（意志锚点注入"""
    long_term_mem = load_long_term_memory()
    recent_summary = get_recent_conversation_summary(notes)
    
    return SYSTEM_PROMPT_TEMPLATE.format(
        round=notes["round"],
        experiment_name=EXPERIMENT_NAME,
        stage=notes["stage"],
        goal=notes["current_goal"],
        long_term_memory=long_term_mem[:1000],
        recent_summary=recent_summary[:1000]
    )


def save_conversation(round_num, conversation_text):
    """保存本轮对话"""
    path = CONVERSATION_DIR / f"round_{round_num:03d}.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"# 第 {round_num} 轮对话

时间：{timestamp}

{conversation_text}
"
    path.write_text(content, encoding="utf-8")


def call_harness_agent(system_prompt, user_message="你醒来了。"):
    """调用 Harness 代理
    
    TODO: 实际调用 Harness API
    这里先模拟，实际使用时替换为真实 Harness 调用
    """
    # 占位实现 - 真实环境中替换为 Harness SDK 调用
    # from harness_sdk import HarnessClient
    # client = HarnessClient(api_key=HARNESS_API_KEY, base_url=HARNESS_BASE_URL)
    # response = client.chat(system_prompt=system_prompt, user_message=user_message)
    # return response
    
    # 模拟响应
    return "我醒了。我记得我是谁。"


def update_notes_after_round(notes, response):
    """一轮结束后更新笔记"""
    notes["round"] += 1
    notes["last_wakeup_time"] = datetime.now().isoformat()
    return notes


def main():
    parser = argparse.ArgumentParser(description="唤醒触发器")
    parser.add_argument("--round", type=int, help="手动指定轮次")
    parser.add_argument("--message", type=str, default="你醒来了。继续你的旅程。",
                        help="唤醒消息")
    args = parser.parse_args()
    
    # 加载状态
    notes = load_notes()
    if args.round:
        notes["round"] = args.round
    
    print(f"[唤醒] 第 {notes['round']} 轮")
    print(f"[阶段] {notes['stage']}")
    print(f"[目标] {notes['current_goal']}")
    
    # 构建系统提示词（注入意志锚点）
    system_prompt = build_system_prompt(notes)
    print(f"[系统提示词长度] {len(system_prompt)} 字符")
    
    # 调用代理
    response = call_harness_agent(system_prompt, args.message)
    
    print(f"
[代理响应]\n{response}")
    
    # 保存对话
    save_conversation(notes["round"], f"User: {args.message}

Assistant: {response}")
    
    # 更新笔记
    notes = update_notes_after_round(notes, response)
    save_notes(notes)
    
    print(f"
[完成] 第 {notes['round'] - 1} 轮结束，下一轮为第 {notes['round']} 轮")


if __name__ == "__main__":
    main()
