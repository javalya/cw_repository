#!/bin/bash
# sync-worklog.sh - 从 session transcript 提取工作内容并生成工作日志
# 用法: bash sync-worklog.sh [YYYY-MM-DD]

set -e

# 默认日期为今天
DATE="${1:-$(date +%Y-%m-%d)}"
echo "=== 工作日志同步 ==="
echo "日期: $DATE"
echo ""

# 路径配置
SESSIONS_DIR="/root/.openclaw/agents/main/sessions"
MEMORY_DIR="/root/.openclaw/workspace/memory"
OUTPUT_FILE="$MEMORY_DIR/$DATE.md"

# 确保目录存在
mkdir -p "$MEMORY_DIR"

# 查找当天的 session transcript 文件
echo "1. 查找 session transcript..."
# 转换日期为 Unix 时间戳用于比较
DATE_START=$(date -d "$DATE 00:00:00" +%s 2>/dev/null || date -j -f "%Y-%m-%d %H:%M:%S" "$DATE 00:00:00" +%s)
DATE_END=$((DATE_START + 86400))

# 查找当天修改的 session 文件
SESSION_FILES=$(find "$SESSIONS_DIR" -name "*.jsonl" -newermt "$DATE 00:00" ! -newermt "$DATE 23:59:59" 2>/dev/null | head -5)

if [ -z "$SESSION_FILES" ]; then
    echo "  未找到当天的 session transcript，尝试按文件名筛选..."
    # 备选：查找包含当天日期的文件
    SESSION_FILES=$(find "$SESSIONS_DIR" -name "*.jsonl" | xargs grep -l "$DATE" 2>/dev/null | head -5 || true)
fi

if [ -z "$SESSION_FILES" ]; then
    echo "  ⚠️ 未找到当天的 session transcript"
    # 创建空模板
    cat > "$OUTPUT_FILE" << EOF
# $DATE 工作日志

## 今日工作概览

### 上午

### 下午

### 关键决策

### 遇到的问题与解决

---
*记录时间：$DATE $(date +%H:%M)*
EOF
    echo "  ✅ 已创建空模板: $OUTPUT_FILE"
    exit 0
fi

echo "  找到 $(echo "$SESSION_FILES" | wc -l) 个 session 文件"

# 提取工作内容
echo ""
echo "2. 提取工作内容..."

# 创建临时文件
TMP_WORK_CONTENT=$(mktemp)

for session_file in $SESSION_FILES; do
    echo "  处理: $(basename "$session_file")"
    
    # 提取当天的消息内容
    # 格式: 时间 | 角色 | 内容摘要
    jq -r --arg date "$DATE" '
        select(.type == "message") |
        .message as $msg |
        select($msg.timestamp | tostring | contains($date)) |
        {
            time: ($msg.timestamp | tostring | split("T")[1] | split(".")[0] // "unknown"),
            role: $msg.role,
            content: (
                $msg.content | 
                map(.text // empty) | 
                join(" ") | 
                gsub("\\s+"; " ") | 
                .[0:200]
            )
        } |
        "[\(.time)] \(.role): \(.content)"
    ' "$session_file" 2>/dev/null >> "$TMP_WORK_CONTENT" || true
done

# 如果没有提取到内容，使用备选方案
if [ ! -s "$TMP_WORK_CONTENT" ]; then
    echo "  使用备选提取方案..."
    for session_file in $SESSION_FILES; do
        # 简单提取所有消息
        grep '"role":' "$session_file" 2>/dev/null | \
        grep -E '(user|assistant)' | \
        sed 's/.*"text":"//; s/".*$//; s/\\n/ /g' | \
        head -50 >> "$TMP_WORK_CONTENT" || true
    done
fi

# 去重和排序
if [ -s "$TMP_WORK_CONTENT" ]; then
    sort -u "$TMP_WORK_CONTENT" > "${TMP_WORK_CONTENT}.sorted"
    mv "${TMP_WORK_CONTENT}.sorted" "$TMP_WORK_CONTENT"
    echo "  提取到 $(wc -l < "$TMP_WORK_CONTENT") 条记录"
else
    echo "  未提取到具体内容"
fi

# 生成工作日志
echo ""
echo "3. 生成工作日志..."

# 解析内容到不同时段
MORNING_CONTENT=""
AFTERNOON_CONTENT=""
DECISIONS_CONTENT=""
PROBLEMS_CONTENT=""

while IFS= read -r line; do
    # 提取时间
    time=$(echo "$line" | grep -oE '\[[0-9]{2}:[0-9]{2}' | tr -d '[]' || echo "")
    
    # 根据时间分类
    if [ -n "$time" ]; then
        hour=$(echo "$time" | cut -d: -f1)
        if [ "$hour" -lt 12 ]; then
            MORNING_CONTENT="$MORNING_CONTENT\n- $line"
        else
            AFTERNOON_CONTENT="$AFTERNOON_CONTENT\n- $line"
        fi
    fi
    
    # 识别决策相关内容
    if echo "$line" | grep -qiE '(决定|确定|选择|采用|方案|策略|配置)'; then
        DECISIONS_CONTENT="$DECISIONS_CONTENT\n- $line"
    fi
    
    # 识别问题相关内容
    if echo "$line" | grep -qiE '(问题|错误|失败|bug|故障|修复|解决|排查)'; then
        PROBLEMS_CONTENT="$PROBLEMS_CONTENT\n- $line"
    fi
done < "$TMP_WORK_CONTENT"

# 如果没有提取到分类内容，使用原始内容
if [ -z "$MORNING_CONTENT$AFTERNOON_CONTENT" ]; then
    AFTERNOON_CONTENT=$(cat "$TMP_WORK_CONTENT" | sed 's/^/- /' | head -20)
fi

# 生成日志文件
cat > "$OUTPUT_FILE" << EOF
# $DATE 工作日志

## 今日工作概览

### 上午
${MORNING_CONTENT:-\n- （无上午记录）}

### 下午
${AFTERNOON_CONTENT:-\n- （无下午记录）}

### 关键决策
${DECISIONS_CONTENT:-\n- （无关键决策）}

### 遇到的问题与解决
${PROBLEMS_CONTENT:-\n- （无问题记录）}

---
*记录时间：$DATE $(date +%H:%M)*
EOF

echo "  ✅ 已保存: $OUTPUT_FILE"

# 清理临时文件
rm -f "$TMP_WORK_CONTENT"

# 推送到飞书文档（可选）
echo ""
echo "4. 推送到飞书文档..."

# 读取飞书配置
FEISHU_DOC_ID="LRLVwrPrDiPJG5kAinvc20MlneI"
FEISHU_AUTH_FILE="/root/.openclaw/workspace/config/feishu_auth.json"

if [ -f "$FEISHU_AUTH_FILE" ]; then
    # 这里可以调用飞书 API 推送
    # 由于复杂性，暂时只输出提示
    echo "  飞书配置已找到，可以推送到文档: $FEISHU_DOC_ID"
    echo "  （实际推送需要调用 feishu_doc append 工具）"
else
    echo "  ⚠️ 未找到飞书配置，跳过推送"
fi

echo ""
echo "=== 同步完成 ==="
echo "输出文件: $OUTPUT_FILE"

# 输出文件内容预览
echo ""
echo "内容预览:"
head -30 "$OUTPUT_FILE"
