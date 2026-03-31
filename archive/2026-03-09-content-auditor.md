# 2026-03-09 内容审核机制建立

## 背景
首次测试运行时出现严重事实错误（编造"DeepSeek V4已发布"虚假内容），建立双重审核机制避免再次发生。

## 新增角色: 内容审核师（Content Auditor）

**路径**: `skills/content-auditor/`
**职责**: 事实核查、来源验证、合规审查
**核心原则**: "宁可不发，也不能发错"

### 审核红线 (一票否决)
- 虚假事实（如编造产品发布）
- 无法验证的信息（"据内部人士透露"无具名来源）
- 过时信息（使用旧数据不标注时间）
- 侵权/违规内容

### 新工作流程
```
内容策划师撰写 → 内容审核师核实 → 刘总终审 → 发布
```

### 审核标准
- 关键事实必须2个独立信源确认
- 官方发布必须引用官网/官方账号
- 数据必须标注时间和出处
- "预计"/"传言"类信息必须明确标注

## 文件位置
- 角色定义: `skills/content-auditor/SKILL.md`
- 工作流程: `skills/content-auditor/WORKFLOW.md`

---

# 2026-03-09 日报推送最终修复

## 问题现象
- 3月9日 7:30 和 7:40 的定时任务只是原样输出了 payload 文本，没有真正执行推送

## 根本原因
1. `sessionTarget: "main"` + `payload.kind: "systemEvent"` 只是把文本注入主会话，不会触发AI执行工具
2. 之前的方案试图让主会话"理解"指令并执行，但 systemEvent 不具备 agentTurn 的执行能力

## 最终解决方案
创建**独立的bash脚本** `daily-push-agent.sh`，完整封装推送流程:
- 获取微信Token → 获取封面图 → 生成HTML文章 → 推送到草稿箱
- 定时任务只需要执行这个脚本，不依赖AI理解或调用工具

## 测试验证 (3月9日 7:49)
- ✅ AI日报推送成功
- ✅ 财经早报推送成功

## 脚本路径
`skills/wechat-daily-push/scripts/daily-push-agent.sh`

---

# 2026-03-09 INSIGHT AI STUDIO 架构确立

**定位**: "AI一人公司实战日记" - 记录用 OpenClaw 搭建自动化业务的完整过程

## 核心角色 (3个)

1. **内容总监（Content Lead）**
   - 路径: `skills/content-lead/`
   - 每日9:00输出选题建议
   - 每周日输出下周选题规划

2. **增长黑客（Growth Hacker）**
   - 路径: `skills/growth-hacker/`
   - 负责小红书/即刻/X/知乎分发
   - 设计引流资料和裂变活动

3. **产品分析师（Product Analyst）**
   - 路径: `skills/product-analyst/`
   - 每周输出竞品分析、用户反馈、数据洞察报告

## 内容策略 (4:3:2:1)
- 40% OpenClaw实战实录
- 30% AI工具实测
- 20% 一人公司/副业案例
- 10% 数据复盘/思考

## 冷启动目标 (第1个月)
- 公众号300粉
- 小红书200粉
- 即刻100粉
- 产出20篇原创内容

**启动指南**: `skills/INSIGHT_AI_STUDIO/STARTUP_GUIDE.md`
