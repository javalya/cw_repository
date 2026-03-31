#!/bin/bash
# check-token.sh - 检查token状态（不自动刷新）
# 用法: bash check-token.sh <AppID>
# 返回: JSON格式的token状态

APP_ID="$1"
CACHE_DIR="/root/.openclaw/workspace/config/wechat_tokens"
CACHE_FILE="$CACHE_DIR/${APP_ID}.json"
NOW=$(date +%s)

if [ -z "$APP_ID" ]; then
    echo '{"exists":false,"error":"AppID is required"}'
    exit 1
fi

if [ ! -f "$CACHE_FILE" ]; then
    echo '{"exists":false,"expired":true}'
    exit 0
fi

CACHE_CONTENT=$(cat "$CACHE_FILE")
ACCESS_TOKEN=$(echo "$CACHE_CONTENT" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
EXPIRES_AT=$(echo "$CACHE_CONTENT" | grep -o '"expires_at":[0-9]*' | cut -d':' -f2)

if [ -z "$ACCESS_TOKEN" ] || [ -z "$EXPIRES_AT" ]; then
    echo '{"exists":false,"expired":true,"error":"invalid cache format"}'
    exit 0
fi

BUFFER_TIME=$((EXPIRES_AT - 300))
if [ "$NOW" -lt "$BUFFER_TIME" ]; then
    # 未过期
    REMAINING=$((EXPIRES_AT - NOW))
    echo "{\"exists\":true,\"expired\":false,\"expires_at\":$EXPIRES_AT,\"remaining_seconds\":$REMAINING,\"token\":\"$ACCESS_TOKEN\"}"
else
    # 已过期
    echo "{\"exists\":true,\"expired\":true,\"expires_at\":$EXPIRES_AT,\"token\":\"$ACCESS_TOKEN\"}"
fi
