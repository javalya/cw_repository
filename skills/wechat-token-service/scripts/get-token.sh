#!/bin/bash
# get-token.sh - 获取微信公众号access_token（只需AppID，自动读取配置）
# 用法: bash get-token.sh <AppID>
# 返回: access_token 或空字符串

APP_ID="$1"
ACCOUNTS_FILE="/root/.openclaw/workspace/config/wechat_accounts.conf"
CACHE_DIR="/root/.openclaw/workspace/config/wechat_tokens"
CACHE_FILE="$CACHE_DIR/${APP_ID}.json"

# 参数检查
if [ -z "$APP_ID" ]; then
    echo ""
    exit 1
fi

# 从配置文件读取AppSecret
APP_SECRET=$(grep "^${APP_ID}|" "$ACCOUNTS_FILE" 2>/dev/null | cut -d'|' -f2)

if [ -z "$APP_SECRET" ]; then
    echo ""
    exit 1
fi

# 创建缓存目录
mkdir -p "$CACHE_DIR"

# 获取当前时间戳
NOW=$(date +%s)

# 检查缓存文件是否存在且有效
if [ -f "$CACHE_FILE" ]; then
    # 读取缓存
    CACHE_CONTENT=$(cat "$CACHE_FILE")
    ACCESS_TOKEN=$(echo "$CACHE_CONTENT" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    EXPIRES_AT=$(echo "$CACHE_CONTENT" | grep -o '"expires_at":[0-9]*' | cut -d':' -f2)
    
    # 检查是否过期（预留300秒缓冲）
    if [ -n "$ACCESS_TOKEN" ] && [ -n "$EXPIRES_AT" ]; then
        BUFFER_TIME=$((EXPIRES_AT - 300))
        if [ "$NOW" -lt "$BUFFER_TIME" ]; then
            # Token有效，直接返回
            echo "$ACCESS_TOKEN"
            exit 0
        fi
    fi
fi

# Token不存在或已过期，需要重新获取
RESPONSE=$(curl -s "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${APP_ID}&secret=${APP_SECRET}")

# 解析响应
NEW_TOKEN=$(echo "$RESPONSE" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
EXPIRES_IN=$(echo "$RESPONSE" | grep -o '"expires_in":[0-9]*' | cut -d':' -f2)

# 检查是否获取成功
if [ -z "$NEW_TOKEN" ] || [ -z "$EXPIRES_IN" ]; then
    echo ""
    exit 1
fi

# 计算过期时间
NEW_EXPIRES_AT=$((NOW + EXPIRES_IN))

# 保存到缓存
echo "{\"access_token\":\"$NEW_TOKEN\",\"expires_at\":$NEW_EXPIRES_AT,\"created_at\":$NOW}" > "$CACHE_FILE"

# 返回新token
echo "$NEW_TOKEN"
exit 0
