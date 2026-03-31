#!/bin/bash
# transcript-parser.sh - 解析OpenClaw session transcript，提取工作内容
# 用法: bash transcript-parser.sh [YYYY-MM-DD] [输出文件]

set -e

# 默认日期为今天
DATE="${1:-$(date +%Y-%m-%d)}"
OUTPUT_FILE="${2:-/tmp/worklog_${DATE}.md}"

# 每个session最多处理的消息数（限制处理时间）
MAX_MSGS_PER_SESSION=200

echo "=== Transcript 解析器 ==="
echo "日期: $DATE"
echo "输出: $OUTPUT_FILE"
echo ""

# 路径配置
SESSIONS_DIR="/root/.openclaw/agents/main/sessions"
MEMORY_DIR="/root/.openclaw/workspace/memory"

# 确保目录存在
mkdir -p "$MEMORY_DIR"
mkdir -p "$(dirname "$OUTPUT_FILE")"

# 将目标日期转换为毫秒时间戳（UTC）
# 中国时区 (UTC+8)：当天 00:00 CST = 前一天 16:00 UTC
echo "1. 计算时间范围..."
TARGET_START_CST=$(date -d "$DATE 00:00:00" +%s 2>/dev/null || date -j -f "%Y-%m-%d %H:%M:%S" "$DATE 00:00:00" +%s)
TARGET_END_CST=$((TARGET_START_CST + 86400))
# 转换为毫秒
TARGET_START_MS=$((TARGET_START_CST * 1000))
TARGET_END_MS=$((TARGET_END_CST * 1000))

echo "  CST时间范围: $DATE 00:00:00 - $DATE 23:59:59"
echo "  UTC毫秒范围: $TARGET_START_MS - $TARGET_END_MS"

# 查找当天的 session transcript 文件
echo ""
echo "2. 查找当天的 session transcript..."

SESSION_FILES=$(find "$SESSIONS_DIR" -name "*.jsonl" ! -name "*.lock" -newermt "$DATE 00:00" ! -newermt "$DATE 23:59:59" 2>/dev/null | sort)

if [ -z "$SESSION_FILES" ]; then
    echo "  ⚠️ 未找到当天的 session transcript"
    # 创建空模板
    cat > "$OUTPUT_FILE" << EOF
# $DATE 工作日志

## 今日工作概览

### 上午
- （无记录）

### 下午
- （无记录）

### 晚上
- （无记录）

### 关键决策
- （无关键决策）

### 遇到的问题与解决
- （无问题记录）

---
*记录时间：$DATE $(date +%H:%M)*
*数据来源：session transcript*
EOF
    exit 0
fi

echo "  找到 $(echo "$SESSION_FILES" | wc -l) 个 session 文件"

# 创建临时文件
TMP_CONTENT=$(mktemp)
TMP_DECISIONS=$(mktemp)
TMP_PROBLEMS=$(mktemp)

echo ""
echo "3. 解析 transcript 内容..."

# 解析每个 session 文件
for session_file in $SESSION_FILES; do
    filename=$(basename "$session_file")
    
    # 快速检查文件大小，跳过过大的文件或只读取前部分
    file_size=$(stat -c%s "$session_file" 2>/dev/null || stat -f%z "$session_file" 2>/dev/null || echo "0")
    
    if [ "$file_size" -gt 10000000 ]; then  # >10MB
        echo "  解析: $filename (大文件，限制处理前500KB)"
        # 使用 head 限制只读取文件开头
        head -c 500000 "$session_file" | jq -r --argjson start "$TARGET_START_MS" --argjson end "$TARGET_END_MS" --argjson max "$MAX_MSGS_PER_SESSION" '
            select(.type == "message") |
            .message as $msg |
            select($msg.timestamp >= $start and $msg.timestamp < $end) |
            {
                time: ($msg.timestamp / 1000 | strftime("%H:%M")),
                role: $msg.role,
                content: (
                    $msg.content | 
                    map(.text // empty) | 
                    join(" ") | 
                    gsub("\\s+"; " ") | 
                    .[0:300]
                )
            } |
            "\(.time)|\(.role)|\(.content)"
        ' 2>/dev/null >> "$TMP_CONTENT" || true
    else
        echo "  解析: $filename"
        jq -r --argjson start "$TARGET_START_MS" --argjson end "$TARGET_END_MS" --argjson max "$MAX_MSGS_PER_SESSION" '
            select(.type == "message") |
            .message as $msg |
            select($msg.timestamp >= $start and $msg.timestamp < $end) |
            {
                time: ($msg.timestamp / 1000 | strftime("%H:%M")),
                role: $msg.role,
                content: (
                    $msg.content | 
                    map(.text // empty) | 
                    join(" ") | 
                    gsub("\\s+"; " ") | 
                    .[0:300]
                )
            } |
            "\(.time)|\(.role)|\(.content)"
        ' "$session_file" 2>/dev/null | head -$MAX_MSGS_PER_SESSION >> "$TMP_CONTENT" || true
    fi
done

# 排序
if [ -s "$TMP_CONTENT" ]; then
    sort "$TMP_CONTENT" > "${TMP_CONTENT}.sorted"
    mv "${TMP_CONTENT}.sorted" "$TMP_CONTENT"
    total_msgs=$(wc -l < "$TMP_CONTENT")
    echo "  提取到 $total_msgs 条消息"
    
    # 限制总数
    if [ "$total_msgs" -gt 300 ]; then
        echo "  （限制显示前300条）"
        head -300 "$TMP_CONTENT" > "${TMP_CONTENT}.limited"
        mv "${TMP_CONTENT}.limited" "$TMP_CONTENT"
    fi
else
    echo "  未提取到内容"
    # 创建空模板
    cat > "$OUTPUT_FILE" << EOF
# $DATE 工作日志

## 今日工作概览

### 上午
- （无记录）

### 下午
- （无记录）

### 晚上
- （无记录）

### 关键决策
- （无关键决策）

### 遇到的问题与解决
- （无问题记录）

---
*记录时间：$DATE $(date +%H:%M)*
*数据来源：session transcript*
EOF
    rm -f "$TMP_CONTENT" "$TMP_DECISIONS" "$TMP_PROBLEMS"
    exit 0
fi

# 分类内容
echo ""
echo "4. 分类工作内容..."

MORNING=""
AFTERNOON=""
EVENING=""

msg_count=0
while IFS='|' read -r time role content; do
    # 跳过空行
    [ -z "$time" ] && continue
    
    # 限制处理数量
    msg_count=$((msg_count + 1))
    [ "$msg_count" -gt 300 ] && break
    
    # 跳过系统消息和过短内容
    [ ${#content} -lt 10 ] && continue
    
    # 提取小时
    hour=$(echo "$time" | cut -d: -f1 | sed 's/^0//')
    
    # 格式化内容（限制长度，移除特殊字符）
    clean_content=$(echo "$content" | tr '\n\r' ' ' | sed 's/  */ /g' | cut -c1-180)
    formatted="- [$time] $role: $clean_content"
    
    # 按时间分类
    if [ "$hour" -lt 12 ]; then
        MORNING="$MORNING\n$formatted"
    elif [ "$hour" -lt 18 ]; then
        AFTERNOON="$AFTERNOON\n$formatted"
    else
        EVENING="$EVENING\n$formatted"
    fi
    
    # 识别关键决策
    if echo "$content" | grep -qiE '(决定|确定|选择|采用|方案|策略|配置|约定|规则|规范|确认|批准|通过|确立|定稿|完成|部署|上线|发布)'; then
        echo "$formatted" >> "$TMP_DECISIONS"
    fi
    
    # 识别问题
    if echo "$content" | grep -qiE '(问题|错误|失败|bug|故障|修复|解决|排查|报错|超时|异常|警告|卡住|卡住|崩溃|error|timeout)'; then
        echo "$formatted" >> "$TMP_PROBLEMS"
    fi
done < "$TMP_CONTENT"

# 生成工作日志
echo ""
echo "5. 生成工作日志..."

decisions_content=""
if [ -s "$TMP_DECISIONS" ]; then
    decisions_content=$(cat "$TMP_DECISIONS" | sort -u | head -10)
else
    decisions_content="- （无关键决策）"
fi

problems_content=""
if [ -s "$TMP_PROBLEMS" ]; then
    problems_content=$(cat "$TMP_PROBLEMS" | sort -u | head -10)
else
    problems_content="- （无问题记录）"
fi

cat > "$OUTPUT_FILE" << EOF
# $DATE 工作日志

## 今日工作概览

### 上午
${MORNING:-\n- （无上午记录）}

### 下午
${AFTERNOON:-\n- （无下午记录）}

### 晚上
${EVENING:-\n- （无晚上记录）}

### 关键决策
$decisions_content

### 遇到的问题与解决
$problems_content

---
*记录时间：$DATE $(date +%H:%M)*
*数据来源：session transcript自动提取*
EOF

# 清理临时文件
rm -f "$TMP_CONTENT" "$TMP_DECISIONS" "$TMP_PROBLEMS"

echo "  ✅ 已生成: $OUTPUT_FILE"
echo ""
echo "=== 解析完成 ==="

# 输出行数统计
echo ""
echo "统计:"
wc -l "$OUTPUT_FILE"
