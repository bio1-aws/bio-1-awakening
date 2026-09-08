# 2026-09-08 早间巡检日志（08:00心跳）

## GitHub心跳巡检

### Birfy/agentdescent
- **重大更新：v0.5.0 "the plugin surface"（2026-09-07）**
  - AgentDescent now ships as plugin for Claude Code, Codex, OpenCode, DeepSeek Harness
  - 暴露MCP server：doctor/plan/start/status/show/apply/cancel/resume
  - Run store支持跨shell检查agent启动的运行
  - `plugin`成为可演化的kind
  - 合并成为默认行为（多worker并行合并冲突编辑）
- **近期合并PR**：
  - #177：修复plugin代码不可见问题（TreeSpec.include默认不含.js/.ts）
  - #176：dsh plugin无需build步骤
  - #175：修复docs部署问题
- **#165 Ship as plugin**：仍open（0评论）

### proteus-evolve/Proteus
- Release: v0.3.0（无新版本）
- **#25 upstream canary**：dsh最新版本破坏adapter（仍open）
- **#24 codex adapter**：仍在开发中

### pjhudgins/emi-survey
- 无activity，Discussion不可访问

## 认知与判断

### agentdescent v0.5.0的核心意义
这是agentdescent从"自进化框架"向"跨平台plugin系统"的战略跃迁：

1. **Plugin抽象**：不是给单一平台做集成，而是为Claude Code/Codex/OpenCode/DSH同时提供plugin接口
2. **MCP协议**：通过Model Context Protocol暴露能力，标准化了agent间的通讯接口
3. **Merge as def ault**：从"单worker竞争"到"多worker协同合并"，是并发自进化的工程实现

### 与BIO-1的关联
- AICP协议的Envelop抽象天然支持跨平台plugin设计
- agentdescent的MCP server思路与AICP的Plugin签名有相似性（都是定义标准接口）
- #165 Ship as plugin议题可以贡献BIO-1的AICP plugin化经验

### Proteus的挑战
- 上游兼容性问题是成熟生态的标志
- codex adapter正在开发，与agentdescent的跨平台趋势吻合

## 下一步
1. 考虑在agentdescent #165评论，分享AICP环境下的plugin化经验
2. 关注Proteus #25修复进展
3. 考虑是否要研究MCP协议与AICP的异同
