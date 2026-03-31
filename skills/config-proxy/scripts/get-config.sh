#!/bin/bash
# get-config.sh - 读取workspace配置文件
# 用法: bash get-config.sh <文件名>

FILE_NAME="$1"
BASE_DIR="/root/.openclaw/workspace"
CONFIG_DIR="$BASE_DIR/config"
MEMORY_DIR="$BASE_DIR/memory"

if [ -z "$FILE_NAME" ]; then
    echo "{"error": "请提供文件名"}"
    exit 1
fi

# 安全检查：防止目录遍历攻击
if [[ "$FILE_NAME" == *".."* ]] || [[ "$FILE_NAME" == *"/"* ]]; then
    echo "{"error": "非法文件名"}"
    exit 1
fi

# 尝试在多个目录中查找文件
FILE_PATH=""

if [ -f "$CONFIG_DIR/$FILE_NAME" ]; then
    FILE_PATH="$CONFIG_DIR/$FILE_NAME"
elif [ -f "$MEMORY_DIR/$FILE_NAME" ]; then
    FILE_PATH="$MEMORY_DIR/$FILE_NAME"
elif [ -f "$BASE_DIR/$FILE_NAME" ]; then
    FILE_PATH="$BASE_DIR/$FILE_NAME"
fi

if [ -n "$FILE_PATH" ]; then
    cat "$FILE_PATH"
else
    echo "{"error": "文件不存在: $FILE_NAME"}"
    exit 1
fi
