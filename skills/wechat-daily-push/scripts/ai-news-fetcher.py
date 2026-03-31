#!/usr/bin/env python3
#
# ai-news-fetcher.py - 生成AI日报HTML内容（模板版）
# 读取模板文件并替换变量
#

import sys
import subprocess
import json
import re
import os

def get_template_path():
    """获取模板路径"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, '..', 'templates', 'ai-template.html')

def read_template():
    """读取模板文件"""
    template_path = get_template_path()
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"读取模板失败: {e}", file=sys.stderr)
        return None

def search_with_searxng(query):
    """使用本地SearXNG搜索"""
    try:
        result = subprocess.run([
            'curl', '-s', '-X', 'POST', 'http://127.0.0.1:8080/search',
            '-d', f'q={query}&category_general=1&format=json'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            return data.get('results', [])
        return []
    except Exception as e:
        print(f"SearXNG搜索失败: {e}", file=sys.stderr)
        return []

def search_ai_news():
    """搜索AI新闻"""
    queries = [
        "AI人工智能 OpenAI DeepSeek 大模型 最新",
        "Claude Anthropic Google Gemini AI新闻 最新",
        "Kimi 豆包 文心一言 智谱 AI更新 最新"
    ]
    
    all_results = []
    for query in queries:
        results = search_with_searxng(query)
        all_results.extend(results)
    
    # 去重
    seen_urls = set()
    unique_results = []
    for r in all_results:
        url = r.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(r)
    
    return unique_results[:10]

def verify_news(title, summary):
    """验证新闻真实性"""
    text = (title + " " + summary).lower()
    
    suspicious = [
        'deepseek v4', 'deepseek-v4', 'v4发布',
        'gpt-5', 'gpt5', 'gpt 5 发布',
        'claude 4', 'claude-4',
        '突破物理定律', '违反物理',
        '实现永生', '永生了',
    ]
    
    for s in suspicious:
        if s in text:
            return False, f"包含未证实信息: {s}"
    
    return True, "通过"

def filter_and_format_news(search_results):
    """过滤并格式化搜索结果"""
    headlines = []
    
    for item in search_results[:5]:
        title = item.get('title', '')
        summary = item.get('content', item.get('abstract', ''))[:180] + '...' if item.get('content') or item.get('abstract') else '...'
        source = item.get('url', '未知来源')
        
        # 验证真实性
        is_valid, reason = verify_news(title, summary)
        if not is_valid:
            print(f"过滤: {title[:30]}... ({reason})", file=sys.stderr)
            continue
        
        # 判断分类
        category = "资讯"
        title_lower = title.lower()
        if any(kw in title_lower for kw in ['deepseek', 'kimi', 'gpt', 'claude', 'llama', '大模型']):
            category = "大模型"
        elif any(kw in title_lower for kw in ['融资', '收购', '上市', '财报']):
            category = "商业"
        elif any(kw in title_lower for kw in ['产品', '发布', '更新', '上线']):
            category = "产品"
        
        headlines.append({
            "title": title,
            "summary": summary,
            "source": source,
            "category": category
        })
    
    return headlines

def generate_news_items_html(headlines):
    """生成新闻条目HTML"""
    if not headlines:
        return '<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; color: #666;">今日暂无经过验证的AI资讯</div>'
    
    html = ""
    for item in headlines:
        category = item.get("category", "资讯")
        title = item.get("title", "")
        summary = item.get("summary", "")
        source = item.get("source", "未知来源")
        
        html += f'''<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
    <div style="display: inline-block; background: #667eea; color: white; font-size: 12px; padding: 3px 10px; border-radius: 4px; margin-bottom: 10px;">{category}</div>
    <h3 style="color: #667eea; margin: 0 0 10px 0; font-size: 17px; font-weight: 600;">{title}</h3>
    <p style="margin: 0 0 8px 0; color: #333; line-height: 1.7; font-size: 15px;">{summary}</p>
    <p style="margin: 0; color: #999; font-size: 12px;">来源：{source}</p>
</div>
'''
    return html

def generate_html(date_str, data):
    """使用模板生成HTML"""
    template = read_template()
    if not template:
        print("无法读取模板，使用备用方案", file=sys.stderr)
        return None
    
    headlines = data.get("headlines", [])
    month_day = date_str[5:7] + "." + date_str[8:10]
    
    # 替换变量
    replacements = {
        '{{TITLE}}': 'AI日报',
        '{{DATE}}': month_day,
        '{{WEEKDAY}}': '| 洞察出品',
        '{{LEAD}}': f'👋 早上好！这里是 MickJagger，今天为你整理了 AI 领域的重要动态，5分钟看完，不错过任何值得关注的事。<br><br>📌 <strong>今日热点：</strong>今日AI行业共收集到 {len(headlines)} 条经过验证的重要资讯',
        '{{NEWS_ITEMS}}': generate_news_items_html(headlines),
        '{{COMMENT}}': 'AI行业持续演进，技术迭代与商业化并进。建议关注有实际产品落地的创新，避免被概念炒作迷惑。',
        '{{ENDING}}': '<span style="font-size: 24px;">👇</span><br><strong>你最期待AI在哪个领域的突破？</strong><br><span style="font-size: 13px; color: #666;">评论区留言，点赞最高的3位送「AI工具手册」</span>',
        '{{DATA_SOURCES}}': 'SearXNG搜索汇总'
    }
    
    html = template
    for key, value in replacements.items():
        html = html.replace(key, value)
    
    return html

def main():
    date_str = sys.argv[1] if len(sys.argv) > 1 else "2026-03-19"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "/tmp/ai-content.html"
    
    print(f"正在使用SearXNG搜索 {date_str} 的AI新闻...", file=sys.stderr)
    
    search_results = search_ai_news()
    
    if search_results:
        headlines = filter_and_format_news(search_results)
        if headlines:
            data = {"headlines": headlines}
            print(f"成功获取 {len(headlines)} 条新闻", file=sys.stderr)
        else:
            print("搜索到内容但验证未通过", file=sys.stderr)
            data = {"headlines": []}
    else:
        print("搜索失败", file=sys.stderr)
        data = {"headlines": []}
    
    html = generate_html(date_str, data)
    
    if html:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"AI日报内容已生成: {output_file}")
    else:
        print("生成失败")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
