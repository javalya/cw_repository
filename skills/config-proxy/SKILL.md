---
name: config-proxy
description: 配置代理工具 - 允许子代理安全地读取和写入workspace中的配置文件。当任务需要访问config目录下的配置、模板或记忆文件时使用此skill。
---

# Config Proxy Skill

此skill提供了一个标准化的接口，让isolated session（子代理）能够安全地读取和写入workspace中的配置文件。

## 使用场景

- 子代理需要读取微信公众号API配置
- 子代理需要读取日报写作模板
- 子代理需要读取记忆文件
- 子代理需要写入token缓存文件

## 使用方法

### 1. 读取配置文件

```bash
bash /root/.openclaw/workspace/skills/config-proxy/scripts/get-config.sh <文件名>
```

示例：
```bash
# 读取公众号配置
bash /root/.openclaw/workspace/skills/config-proxy/scripts/get-config.sh wechat_official_account.md

# 读取token缓存
bash /root/.openclaw/workspace/skills/config-proxy/scripts/get-config.sh wechat_token.json

# 读取写作规范
bash /root/.openclaw/workspace/skills/config-proxy/scripts/get-config.sh writing_guidelines.md
```

### 2. 写入配置文件

```bash
bash /root/.openclaw/workspace/skills/config-proxy/scripts/set-config.sh <文件名> '<JSON内容>'
```

示例：
```bash
# 写入token缓存
bash /root/.openclaw/workspace/skills/config-proxy/scripts/set-config.sh wechat_token.json '{"access_token":"xxx","expires_at":1234567890}'
```

## 支持读取的文件路径

- `config/wechat_official_account.md` - 公众号配置
- `config/wechat_token.json` - Token缓存
- `config/writing_guidelines.md` - 写作规范
- `config/daily_report_guidelines.md` - 日报写作规范
- `memory/*.md` - 记忆文件
- `SOUL.md` - 人格配置
- `USER.md` - 用户信息

## 注意事项

1. 所有路径都相对于 `/root/.openclaw/workspace/` 
2. 只能访问workspace目录下的文件
3. 写入操作会覆盖原有文件，请谨慎使用
4. 如果文件不存在，读取会返回空
