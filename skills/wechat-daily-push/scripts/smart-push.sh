#!/bin/bash
#
# smart-push.sh - 智能日报推送脚本
# 使用AI搜索实时资讯并生成内容
#

set -e

# 解析参数
APPID="wx474c0d9c9e4a8d1a"
TYPE="ai"
DATE=$(date +%Y-%m-%d)

while [[ $# -gt 0 ]]; do
    case $1 in
        --appid)
            APPID="$2"
            shift 2
            ;;
        --type)
            TYPE="$2"
            shift 2
            ;;
        --date)
            DATE="$2"
            shift 2
            ;;
        *)
            # 兼容旧版位置参数
            if [[ -z "$APPID_SET" && "$1" != --* ]]; then
                APPID="$1"
                APPID_SET=1
                shift
            elif [[ -z "$TYPE_SET" && "$1" != --* ]]; then
                TYPE="$1"
                TYPE_SET=1
                shift
            elif [[ -z "$DATE_SET" && "$1" != --* ]]; then
                DATE="$1"
                DATE_SET=1
                shift
            else
                echo "未知参数: $1"
                exit 1
            fi
            ;;
    esac
done

WORKSPACE="/root/.openclaw/workspace"
TEMPLATE_DIR="$WORKSPACE/skills/wechat-daily-push/templates"

echo "=========================================="
echo "📰 智能日报推送"
echo "=========================================="
echo "日期: $DATE | 类型: $TYPE"
echo ""

# 步骤1: 获取微信Token
echo "【步骤1】获取微信Access Token..."
TOKEN=$(bash "$WORKSPACE/skills/wechat-token-service/scripts/get-token.sh" "$APPID" 2>/dev/null)
[[ -z "$TOKEN" ]] && { echo "❌ 获取Token失败"; exit 1; }
echo "✓ Token获取成功"
echo ""

# 步骤2: 获取封面图
echo "【步骤2】获取封面图..."
COVER=$(curl -s "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"image","offset":0,"count":1}' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('item',[{}])[0].get('media_id',''))")
[[ -n "$COVER" ]] && echo "✓ 封面图获取成功"
echo ""

# 步骤3: 准备文章数据
echo "【步骤3】准备文章数据..."
MONTH_DAY=$(date -d "$DATE" +%m.%d 2>/dev/null || date +%m.%d)

if [[ "$TYPE" == "ai" ]]; then
    TITLE="AI日报 | ${MONTH_DAY}"
    DIGEST="每日AI资讯速递，5分钟了解行业动态"
    
    # 使用Python生成内容
    python3 "$WORKSPACE/skills/wechat-daily-push/scripts/ai-news-fetcher.py" "$DATE" "/tmp/content.html"
else
    TITLE="财经早报 | ${MONTH_DAY}"
    DIGEST="全球市场概览，把握投资先机"
    
    # 使用Python生成内容
    python3 "$WORKSPACE/skills/wechat-daily-push/scripts/finance-data-fetcher.py" "$DATE" "/tmp/content.html"
fi

CONTENT=$(cat /tmp/content.html)
echo "✓ 内容生成完成"
echo ""

# 步骤4: 内容审核
echo "【步骤4】内容审核..."
if ! python3 "$WORKSPACE/skills/wechat-daily-push/scripts/content-auditor.py" "/tmp/content.html" "$TYPE"; then
    echo "❌ 内容审核未通过，停止推送"
    exit 1
fi
echo "✓ 内容审核通过"
echo ""

# 步骤5: 推送到公众号
echo "【步骤5】推送到公众号草稿箱..."

python3 > /tmp/payload.json << PYEOF
import json
article = {
    'title': '''$TITLE''',
    'author': 'MickJagger',
    'digest': '''$DIGEST''',
    'content': '''$CONTENT''',
    'content_source_url': '',
    'need_open_comment': 1,
    'only_fans_can_comment': 0
}
if '''$COVER''':
    article['thumb_media_id'] = '''$COVER'''
json.dump({'articles': [article]}, open('/tmp/payload.json', 'w', encoding='utf-8'), ensure_ascii=False)
PYEOF

RESP=$(curl -s -X POST "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=$TOKEN" \
    -H "Content-Type: application/json" \
    -d @/tmp/payload.json)

MEDIA_ID=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('media_id',''))")
ERRCODE=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('errcode',''))")

if [[ -n "$MEDIA_ID" && -z "$ERRCODE" ]]; then
    echo ""
    echo "=========================================="
    echo "✅ 推送成功！"
    echo "标题: $TITLE"
    echo "草稿ID: $MEDIA_ID"
    echo "=========================================="
    exit 0
else
    echo "❌ 推送失败: $RESP"
    exit 1
fi
