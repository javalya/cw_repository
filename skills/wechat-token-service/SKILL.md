---
name: wechat-token-service
description: 微信公众号Token服务 - 按需获取有效的access_token。只需传入AppID，自动从配置文件读取AppSecret并获取token。支持自动缓存和过期刷新，供其他任务调用获取微信公众号access_token。
---

# 微信Token服务

按需获取微信公众号access_token，只需传入AppID，自动从配置文件读取密钥。

## 使用方法

### 获取Token（只需AppID）

```bash
bash /root/.openclaw/workspace/skills/wechat-token-service/scripts/get-token.sh <AppID>
```

**示例：**
```bash
# 获取洞察公众号的token
TOKEN=$(bash /root/.openclaw/workspace/skills/wechat-token-service/scripts/get-token.sh wx474c0d9c9e4a8d1a)
echo $TOKEN
# 输出: 101_xxxxxxxxxxxxxxxx
```

**返回：**
- 成功：返回access_token字符串
- 失败：返回空字符串

### 检查Token状态

```bash
bash /root/.openclaw/workspace/skills/wechat-token-service/scripts/check-token.sh <AppID>
```

**返回JSON：**
```json
{
  "exists": true,
  "expired": false,
  "expires_at": 1234567890,
  "remaining_seconds": 7179,
  "token": "101_xxxx"
}
```

## 配置管理

### 公众号配置文件

位置：`/root/.openclaw/workspace/config/wechat_accounts.conf`

格式：
```
# AppID | AppSecret | 公众号名称 | 备注

wx474c0d9c9e4a8d1a|d0b6bdc9779543fff515bf64fd874cef|洞察INNOV.LINK|主公众号
wx1234567890abcdef|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|其他公众号|备注说明
```

### 缓存文件位置

```
/root/.openclaw/workspace/config/wechat_tokens/
├── wx474c0d9c9e4a8d1a.json    # 洞察公众号token缓存
└── {appid}.json               # 其他公众号token缓存
```

## 工作原理

1. **读取配置**：根据AppID从`wechat_accounts.conf`读取AppSecret
2. **读取缓存**：查找对应AppID的token缓存
3. **检查过期**：比较当前时间与expires_at（预留300秒缓冲）
4. **返回有效token**：如未过期，直接返回缓存token
5. **自动刷新**：如过期或不存在，调用微信API获取新token
6. **保存缓存**：将新token写入缓存文件

## 在定时任务中使用

### AI日报任务示例

```bash
# 1. 获取有效token（只需AppID）
ACCESS_TOKEN=$(bash /root/.openclaw/workspace/skills/wechat-token-service/scripts/get-token.sh wx474c0d9c9e4a8d1a)

# 2. 使用token推送文章到公众号
curl -X POST "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=$ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{...文章数据...}'
```

### 多公众号支持

```bash
# 洞察公众号
TOKEN_1=$(bash .../get-token.sh wx474c0d9c9e4a8d1a)

# 其他公众号
TOKEN_2=$(bash .../get-token.sh wx1234567890abcdef)
```

## 添加新公众号

1. 编辑配置文件：`config/wechat_accounts.conf`
2. 添加一行：`AppID|AppSecret|公众号名称|备注`
3. 直接使用新AppID调用技能即可

## 优势

1. **密钥统一管理**：所有AppSecret集中存储在配置文件
2. **简化调用**：只需传入AppID，无需传递密钥
3. **按需获取**：只在需要token时才检查/刷新
4. **自动缓存**：有效token自动缓存，避免重复调用API
5. **过期自动刷新**：token过期时自动获取新token
6. **多公众号支持**：通过AppID区分不同公众号
7. **无需定时任务**：不再需要定时刷新token的cron job
