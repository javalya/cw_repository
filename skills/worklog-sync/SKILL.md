---
name: worklog-sync
description: 工作日志同步技能 - 自动从 session transcript 提取工作内容并生成工作日志。用于定时任务中整理当天工作记录，支持保存到本地文件和推送到飞书文档。
---

# Worklog Sync Skill

自动从 OpenClaw session transcript 提取工作内容，生成结构化工作日志。

## 使用场景

- **定时任务**：每天22:30自动整理当天工作内容
- **手动触发**：随时同步最近的工作记录
- **多源汇总**：可处理多个 session 的 transcript

## 使用方法

### 方式1：直接执行脚本（推荐用于定时任务）

```bash
bash /root/.openclaw/workspace/skills/worklog-sync/scripts/sync-worklog.sh [日期]
```

**参数：**
- `日期`：可选，格式 YYYY-MM-DD，默认为今天

**示例：**
```bash
# 同步今天的工作日志
bash /root/.openclaw/workspace/skills/worklog-sync/scripts/sync-worklog.sh

# 同步指定日期的工作日志
bash /root/.openclaw/workspace/skills/worklog-sync/scripts/sync-worklog.sh 2026-03-05
```

### 方式2：子代理执行（复杂场景）

```bash
# 在子代理任务中调用
bash /root/.openclaw/workspace/skills/worklog-sync/scripts/sync-worklog.sh 2026-03-05
```

## 工作流程

1. **查找 Session Transcript**
   - 扫描 `~/.openclaw/agents/main/sessions/*.jsonl`
   - 筛选指定日期的 session 文件

2. **提取工作内容**
   - 解析 JSONL 格式的 transcript
   - 提取用户消息和助理回复
   - 识别工作任务、决策、问题等关键信息

3. **生成工作日志**
   - 按时间顺序整理
   - 分类：上午/下午/关键决策/问题与解决
   - 生成 Markdown 格式

4. **保存与同步**
   - 保存到 `memory/YYYY-MM-DD.md`
   - 推送到飞书文档（可选）

## 输出格式

生成的日志文件格式：

```markdown
# YYYY-MM-DD 工作日志

## 今日工作概览

### 上午
- [任务描述]
- [任务描述]

### 下午
- [任务描述]
- [任务描述]

### 关键决策
- [决策内容]

### 遇到的问题与解决
- [问题] → [解决方案]

---
*记录时间：YYYY-MM-DD HH:MM*
```

## 文件位置

- **Session Transcript**：`~/.openclaw/agents/main/sessions/*.jsonl`
- **输出日志**：`/root/.openclaw/workspace/memory/YYYY-MM-DD.md`
- **飞书文档**：通过 Feishu API 推送

## 依赖

- `jq`：JSON 解析
- `date`：日期处理
- `curl`：飞书 API 调用

## 注意事项

1. Session transcript 可能很大，脚本会智能筛选有效内容
2. 只提取与工作内容相关的对话，过滤闲聊
3. 如果当天没有工作记录，会生成空模板
4. 飞书文档推送需要配置 `config/feishu_auth.json`
