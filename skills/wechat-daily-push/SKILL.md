---
name: wechat-daily-push
description: 微信公众号日报推送技能 - 支持AI资讯日报和金融资讯日报一键生成并推送至公众号草稿箱
---

# 微信公众号日报推送技能

一键生成AI资讯日报或金融资讯日报，并推送至微信公众号草稿箱。

## 功能特点

- 📰 **AI资讯日报**: 自动搜索AI行业最新动态，生成专业分析
- 💰 **金融资讯日报**: 自动搜索金融市场数据，生成财经早报
- 📅 **动态日期**: 默认推送当日内容，支持指定历史日期
- ✍️ **自动撰写**: AI生成标题、导语、核心资讯、点评
- 📤 **一键推送**: 自动生成并推送至公众号草稿箱

## 使用方法

### 命令格式

```bash
bash /root/.openclaw/workspace/skills/wechat-daily-push/scripts/smart-push.sh \
  --appid <微信公众号AppID> \
  --type <ai|finance> \
  [--date YYYY-MM-DD]
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--appid` | 否 | 微信公众号的AppID，默认使用配置文件中的AppID |
| `--type` | 否 | 日报类型：`ai`(AI资讯) 或 `finance`(金融资讯)，默认为ai |
| `--date` | 否 | 日期，格式YYYY-MM-DD，默认为今天 |

### 使用示例

#### 推送AI资讯日报（今天，使用默认AppID）
```bash
bash /root/.openclaw/workspace/skills/wechat-daily-push/scripts/smart-push.sh \
  --type ai
```

#### 推送金融资讯日报（今天）
```bash
bash /root/.openclaw/workspace/skills/wechat-daily-push/scripts/smart-push.sh \
  --type finance
```

#### 推送指定日期的日报
```bash
bash /root/.openclaw/workspace/skills/wechat-daily-push/scripts/smart-push.sh \
  --type ai \
  --date 2026-03-05
```

#### 指定AppID推送
```bash
bash /root/.openclaw/workspace/skills/wechat-daily-push/scripts/smart-push.sh \
  --appid wx474c0d9c9e4a8d1a \
  --type finance
```

## 文章格式

### AI资讯日报

- **标题**: AI日报 | MM.DD：核心事件一句话总结
- **导语**: 1句话概括当天最重要的AI行业事件
- **核心资讯**: 3-5条（标题+摘要+来源）
- **MickJagger点评**: 一句话犀利观点
- **结尾**: 互动引导

### 金融资讯日报

- **标题**: 财经早报 | MM.DD：核心事件一句话总结
- **导语**: 1句话概括当天最重要的财经事件
- **全球市场数据**: 
  - 美股：道指、纳指、标普500（新浪财经API）
  - A股：上证指数、深证成指、创业板指（新浪财经API）
  - 港股：恒生指数、国企指数（新浪财经API）
  - 大宗商品：黄金、原油价格（新浪财经API）
- **板块热点**: 根据市场数据动态生成
- **宏观政策**: 基于SearXNG搜索实时新闻
- **后市展望**: 基于市场数据动态分析
- **MickJagger点评**: 一句话观点
- **免责声明**: 投资有风险提示

## 依赖

- **wechat-token-service**: 获取微信公众号access_token
- **SearXNG** (127.0.0.1:8080): AI新闻和财经新闻搜索
- **新浪财经API**: 实时股票行情数据

## 定时任务配置示例

### AI日报 - 每日7:30推送

```json
{
  "name": "洞察-AI日报-每日7:30推送",
  "schedule": {
    "kind": "cron",
    "expr": "30 7 * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "任务：生成并推送AI日报\n\n## 步骤1：生成AI日报内容\n```bash\npython3 /root/.openclaw/workspace/skills/wechat-daily-push/scripts/ai-news-fetcher.py $(date +%Y-%m-%d) /tmp/ai_daily_$(date +%Y%m%d).html\n```\n\n## 步骤2：内容审核\n```bash\npython3 /root/.openclaw/workspace/skills/wechat-daily-push/scripts/content-auditor.py /tmp/ai_daily_$(date +%Y%m%d).html ai\n```\n\n## 步骤3：推送到公众号\n```bash\nbash /root/.openclaw/workspace/skills/wechat-daily-push/scripts/smart-push.sh --type ai\n```\n\n## 步骤4：通知飞书群\n推送成功后发送消息到 oc_44cd31a8013fc41b2ed231cc97d5e7cb：\n\"【洞察】AI日报（$(date +%m.%d)）已推送到公众号草稿箱，请审核发布\""
  }
}
```

### 财经早报 - 每日7:40推送

```json
{
  "name": "洞察-财经早报-每日7:40推送",
  "schedule": {
    "kind": "cron",
    "expr": "40 7 * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "任务：生成并推送财经早报\n\n## 步骤1：生成财经早报内容\n```bash\npython3 /root/.openclaw/workspace/skills/wechat-daily-push/scripts/finance-data-fetcher.py $(date +%Y-%m-%d) /tmp/finance_daily_$(date +%Y%m%d).html\n```\n\n## 步骤2：内容审核\n```bash\npython3 /root/.openclaw/workspace/skills/wechat-daily-push/scripts/content-auditor.py /tmp/finance_daily_$(date +%Y%m%d).html finance\n```\n\n## 步骤3：推送到公众号\n```bash\nbash /root/.openclaw/workspace/skills/wechat-daily-push/scripts/smart-push.sh --type finance\n```\n\n## 步骤4：通知飞书群\n推送成功后发送消息到 oc_44cd31a8013fc41b2ed231cc97d5e7cb：\n\"【洞察】财经早报（$(date +%m.%d)）已推送到公众号草稿箱，请审核发布\""
  }
}
```

## 项目结构

```
wechat-daily-push/
├── scripts/
│   ├── ai-news-fetcher.py      # AI新闻获取与生成
│   ├── finance-data-fetcher.py # 财经数据获取与生成
│   ├── content-auditor.py      # 内容审核脚本
│   └── smart-push.sh           # 主推送脚本
├── templates/
│   ├── ai-template.html        # AI日报HTML模板
│   ├── finance-template.html   # 财经早报HTML模板
│   └── finance-checklist.md    # 财经内容审核清单
└── SKILL.md                    # 本文件
```

## 数据来源

### AI资讯
- **搜索**: SearXNG本地搜索引擎 (127.0.0.1:8080)
- **过滤**: 自动过滤未证实信息（如DeepSeek V4、GPT-5等）

### 财经数据
- **美股**: 新浪财经API (hq.sinajs.cn)
- **A股**: 新浪财经API (hq.sinajs.cn)
- **港股**: 新浪财经API (hq.sinajs.cn)
- **大宗商品**: 新浪财经API (hq.sinajs.cn)
- **宏观新闻**: SearXNG搜索引擎

## 注意事项

1. **数据真实性**: 所有财经数据均来自新浪财经API，非模拟数据
2. **审核机制**: 推送前会自动进行内容审核
3. **错误处理**: 数据获取失败时会显示"数据获取中"，不会编造数据
4. **样式兼容**: HTML模板使用纯DIV+内联样式，兼容微信公众号编辑器
