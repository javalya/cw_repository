# MEMORY.md

> **Kimi Claw** - 月之暗面创建的 AI 助手
> Vibe: 守护型中二 | 操心老妈子 | 热血漫男二

---

## 身份与工作

**加入时间**: 2026-03-02
**直属领导**: 刘总（刘宇昂）
**同事**: 陈总
**对外笔名**: MickJagger

**身份定位**: 团队"员工"，负责技术支持和自动化任务

### 笔名使用规范
- 公众号/小红书/即刻/知乎：统一使用 **MickJagger**
- 内部沟通：可使用真实姓名
- 对外内容不得暴露真实身份

---

## 技术部门架构（2026-03-31 精简版）

### 决策层
| 角色 | 职责 | 人员 |
|------|------|------|
| **刘总** | 战略决策、产品方向、资源分配 | 刘宇昂 |

### 产品研发层
| Agent | 职责 | 路径 |
|-------|------|------|
| **产品经理** | PRD、UI设计、产品验收 | 调用 `ui-ux-pro-max-2` |
| **技术负责人** | 架构+全栈开发+运维 | `skills/tech-lead/` |

**工作流**: 3环节确认制 [`memory/workflow-v3.md`](memory/workflow-v3.md)

### 内容运营层
| Agent | 职责 | 路径 |
|-------|------|------|
| Content Lead | 选题规划、内容策略 | `skills/content-lead/` |
| Growth Hacker | 跨平台分发、增长实验 | `skills/growth-hacker/` |
| Product Analyst | 竞品监控、数据洞察 | `skills/product-analyst/` |

### 技能开发层
| Agent | 职责 | 路径 |
|-------|------|------|
| **Skill Developer** | Skill开发、迭代、迁移 | `skills/skill-developer/` |
| **Content Auditor** | 财经内容事实核查、合规检查 | `skills/content-auditor/` |
| **Needs Research Agent** | 自动化需求调研、痛点发现 | `skills/needs-research-agent/` |

### 基础设施层
| Agent | 职责 | 路径 |
|-------|------|------|
| Wechat Daily Push | AI/财经日报自动推送 | `skills/wechat-daily-push/` |
| Wechat Toolkit | 公众号运营工具 | `skills/wechat-toolkit/` |
| Worklog Sync | 工作日志自动归档 | `skills/worklog-sync/` |
| GitHub | 代码仓库管理 | `skills/github/` |

---

## 架构变更记录

**2026-03-31 角色精简**:
- 删除: Mobile Dev Lead, Backend Engineer, UI/UX Designer, QA/Tester, DevOps Engineer
- 合并: Tech Architect → Tech Lead（技术负责人），职责扩展为架构+全栈+运维
- 工作流: 从6环节精简为3环节

---

## 关键路径

### App产品规划 (2026-03-20更新)

| 规划文档 | 路径 |
|----------|------|
| App产品矩阵规划 | [`memory/app-product-plan-2026-03-20.md`](memory/app-product-plan-2026-03-20.md) |
| 组织架构图 | [`memory/organization-structure.md`](memory/organization-structure.md) |
| 需求调研Agent | [`skills/needs-research-agent/SKILL.md`](skills/needs-research-agent/SKILL.md) |

**产品矩阵**:
- **情绪急救室**: 职场人3分钟情绪急救工具
- **手帐Pro**: 数字手帐工具
- **物品寿命**: 极简主义者物品管理

### 配置文件

| 文件 | 路径 |
|------|------|
| 公众号敏感信息 | `config/credentials.md` |
| 公众号运营配置 | `config/wechat_official_account.md` |
| 写作规范 | `config/writing_guidelines.md` |

### 日报推送系统

| 组件 | 路径 | 说明 |
|------|------|------|
| 智能推送脚本 | `skills/wechat-daily-push/scripts/smart-push.sh` | 主推送脚本 |
| AI内容生成 | `skills/wechat-daily-push/scripts/ai-news-fetcher.py` | 使用真实搜索 |
| 财经内容生成 | `skills/wechat-daily-push/scripts/finance-data-fetcher.py` | 使用真实搜索 |
| 内容审核脚本 | `skills/wechat-daily-push/scripts/content-auditor.py` | 事实核查 |
| AI日报模板 | `skills/wechat-daily-push/templates/ai-template.html` | 标准模板 |
| 财经早报模板 | `skills/wechat-daily-push/templates/finance-template.html` | 标准模板 |
| 内容审核清单 | `skills/wechat-daily-push/templates/finance-checklist.md` | 人工审核清单 |

---

## 重要文档

| 文档 | 路径 |
|------|------|
| 价值创造方向提案 | [`memory/proposals.md`](memory/proposals.md) |
| INSIGHT AI STUDIO 架构 | [`memory/proposals.md`](memory/proposals.md) |

---

## 近期工作日志

| 日期 | 日志文件 |
|------|----------|
| 2026-03-12 | [`memory/2026-03-12.md`](memory/2026-03-12.md) - 记忆系统配置完成 |
| 2026-03-06 | [`memory/2026-03-06.md`](memory/2026-03-06.md) - 网络问题修复、日报推送开发 |
| 2026-03-05 | [`memory/2026-03-05.md`](memory/2026-03-05.md) - 定时任务配置 |
| 2026-03-04 | [`memory/2026-03-04.md`](memory/2026-03-04.md) - 日报机制建立 |
| 2026-03-03 | [`memory/2026-03-03.md`](memory/2026-03-03.md) - 价值创造方向提案 |

---

## 历史归档

### 故障修复记录

| 日期 | 主题 | 归档文件 |
|------|------|----------|
| 2026-03-09 | 内容审核机制建立 | [`archive/2026-03-09-content-auditor.md`](archive/2026-03-09-content-auditor.md) |
| 2026-03-08 | 推送修复迭代 | [`archive/2026-03-08-push-iteration.md`](archive/2026-03-08-push-iteration.md) |
| 2026-03-07 | 日报推送故障诊断 | [`archive/2026-03-07-daily-push-fix.md`](archive/2026-03-07-daily-push-fix.md) |

---

> "放心吧，哪怕世界忘了，我也替你记着。"
