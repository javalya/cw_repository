#!/bin/bash
# set-config.sh - 写入workspace配置文件
# 用法: bash set-config.sh <文件名> '<JSON内容>'

FILE_NAME="$1"
CONTENT="$2"
BASE_DIR="/root/.openclaw/workspace"
CONFIG_DIR="$BASE_DIR/config"

if [ -z "$FILE_NAME" ]; then
    echo "{"error": "请提供文件名"}"
    exit 1
fi

if [ -z "$CONTENT" ]; then
    echo "{"error": "请提供内容"}"
    exit 1
fi

# 安全检查：防止目录遍历攻击
if [[ "$FILE_NAME" == *".."* ]]; then
    echo "{"error": "非法文件名"}"
    exit 1
fi

# 确保config目录存在
mkdir -p "$CONFIG_DIR"

# 写入文件
FILE_PATH="$CONFIG_DIR/$FILE_NAME"
echo "$CONTENT" > "$FILE_PATH"

if [ $? -eq 0 ]; then
    echo "{"success": true, "file": "$FILE_PATH"}"
else
    echo "{"error": "写入失败"}"
    exit 1
fi
