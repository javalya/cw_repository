# 公众号配置

## 洞察 INNOV.LINK

- **公众号名称**：洞察 INNOV.LINK
- **AppID**：wx474c0d9c9e4a8d1a
- **AppSecret**：d0b6bdc9779543fff515bf64fd874cef

## Token 管理策略（已优化）

微信公众号 access_token 获取限制：
- 有效期：7200秒（2小时）
- 每日获取次数：2000次（所有公众号共用配额）
- **策略：缓存token，有效期内复用，避免频繁调用**

### Token缓存机制

**方案：本地文件缓存 + 定时刷新**

1. **缓存文件**：`config/wechat_token.json`
   - 存储内容：access_token、expires_in、获取时间戳
   - 检查时机：每次调用API前

2. **使用逻辑**：
```
调用API前：
  1. 读取缓存文件
  2. 检查是否过期（当前时间 < 获取时间 + 7000秒，预留200秒缓冲）
  3. 如果有效：使用缓存token
  4. 如果过期：重新获取 + 更新缓存文件
```

3. **定时刷新任务**：
   - 创建定时任务，每1.5小时自动刷新token
   - 任务时间：每偶数小时执行（00:00, 02:00, 04:00...）
   - 避免与日报推送时间冲突

4. **容错机制**：
   - 缓存读取失败 → 重新获取
   - API调用返回token过期 → 立即刷新并重试
   - 预留200秒缓冲期，避免临界过期

### API 调用流程（优化后）

```bash
# 1. 读取缓存token
TOKEN=$(cat config/wechat_token.json | jq -r '.access_token')
EXPIRES=$(cat config/wechat_token.json | jq -r '.expires_at')
NOW=$(date +%s)

# 2. 检查是否过期（预留200秒缓冲）
if [ $NOW -gt $((EXPIRES - 200)) ]; then
  # 重新获取
  RESPONSE=$(curl -s "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx474c0d9c9e4a8d1a&secret=d0b6bdc9779543fff515bf64fd874cef")
  TOKEN=$(echo $RESPONSE | jq -r '.access_token')
  EXPIRES=$((NOW + 7200))
  # 写入缓存
  echo "{\"access_token\":\"$TOKEN\",\"expires_at\":$EXPIRES}" > config/wechat_token.json
fi

# 3. 使用token调用API
curl -X POST "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=$TOKEN" ...
```

## API 接口

- 获取access_token：`GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET`
- 创建草稿：`POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token=ACCESS_TOKEN`

## 封面图片

- **文件名**：cover_img.jpg
- **media_id**：`M7mDzlQvkr9lyiE-5zgXyQv8HF1Ukmq8U2Ht9jLcMJHllhMO54rchvCPexkJZr8n`
- **用途**：AI日报/财经早报通用封面图
- **更新时间**：2026-03-04

## 注意事项

- Token需要妥善存储，定时刷新
- 封面图media_id已保存，可直接复用
