#!/usr/bin/env python3
#
# finance-data-fetcher.py - 获取财经数据（完整版）
# 使用新浪财经API获取美股、A股、港股、商品全量数据
#

import sys
import subprocess
import json
import datetime
import os
import re

def get_template_path():
    """获取模板路径"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, '..', 'templates', 'finance-template.html')

def read_template():
    """读取模板文件"""
    template_path = get_template_path()
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"读取模板失败: {e}", file=sys.stderr)
        return None

def fetch_sina_data(symbols):
    """从新浪财经获取数据"""
    try:
        import requests
        url = f'https://hq.sinajs.cn/list={",".join(symbols)}'
        headers = {'Referer': 'https://finance.sina.com.cn'}
        resp = requests.get(url, headers=headers, timeout=10)
        return resp.text
    except Exception as e:
        print(f"新浪API请求失败: {e}", file=sys.stderr)
        return None

def parse_us_market(text):
    """解析美股数据"""
    data = {
        "dow": {"price": "—", "change": "—", "direction": "neutral"},
        "nasdaq": {"price": "—", "change": "—", "direction": "neutral"},
        "sp500": {"price": "—", "change": "—", "direction": "neutral"}
    }
    
    if not text:
        return data
    
    # 道指: var hq_str_int_dji="道琼斯,46247.29,299.97,0.65";
    if 'int_dji="' in text:
        match = re.search(r'int_dji=\"([^\"]+)\"', text)
        if match:
            parts = match.group(1).split(',')
            if len(parts) >= 4:
                data["dow"]["price"] = parts[1]
                change_val = float(parts[3])
                data["dow"]["change"] = f"{change_val:+.2f}%"
                data["dow"]["direction"] = "up" if change_val >= 0 else "down"
    
    # 纳指
    if 'int_nasdaq="' in text:
        match = re.search(r'int_nasdaq=\"([^\"]+)\"', text)
        if match:
            parts = match.group(1).split(',')
            if len(parts) >= 4:
                data["nasdaq"]["price"] = parts[1]
                change_val = float(parts[3])
                data["nasdaq"]["change"] = f"{change_val:+.2f}%"
                data["nasdaq"]["direction"] = "up" if change_val >= 0 else "down"
    
    # 标普500
    if 'int_sp500="' in text:
        match = re.search(r'int_sp500=\"([^\"]+)\"', text)
        if match:
            parts = match.group(1).split(',')
            if len(parts) >= 4:
                data["sp500"]["price"] = parts[1]
                change_val = float(parts[3])
                data["sp500"]["change"] = f"{change_val:+.2f}%"
                data["sp500"]["direction"] = "up" if change_val >= 0 else "down"
    
    return data

def parse_a_market(text):
    """解析A股数据"""
    data = {
        "shanghai": {"price": "—", "change": "—", "direction": "neutral"},
        "shenzhen": {"price": "—", "change": "—", "direction": "neutral"},
        "chinext": {"price": "—", "change": "—", "direction": "neutral"}
    }
    
    if not text:
        return data
    
    # 上证指数: var hq_str_s_sh000001="上证指数,4024.2298,-38.7546,-0.95,...";
    if 's_sh000001="' in text:
        match = re.search(r's_sh000001=\"([^\"]+)\"', text)
        if match:
            parts = match.group(1).split(',')
            if len(parts) >= 4:
                data["shanghai"]["price"] = parts[1]
                change_val = float(parts[3])
                data["shanghai"]["change"] = f"{change_val:+.2f}%"
                data["shanghai"]["direction"] = "up" if change_val >= 0 else "down"
    
    # 深证成指
    if 's_sz399001="' in text:
        match = re.search(r's_sz399001=\"([^\"]+)\"', text)
        if match:
            parts = match.group(1).split(',')
            if len(parts) >= 4:
                data["shenzhen"]["price"] = parts[1]
                change_val = float(parts[3])
                data["shenzhen"]["change"] = f"{change_val:+.2f}%"
                data["shenzhen"]["direction"] = "up" if change_val >= 0 else "down"
    
    # 创业板指
    if 's_sz399006="' in text:
        match = re.search(r's_sz399006=\"([^\"]+)\"', text)
        if match:
            parts = match.group(1).split(',')
            if len(parts) >= 4:
                data["chinext"]["price"] = parts[1]
                change_val = float(parts[3])
                data["chinext"]["change"] = f"{change_val:+.2f}%"
                data["chinext"]["direction"] = "up" if change_val >= 0 else "down"
    
    return data

def parse_hk_market(text):
    """解析港股数据"""
    data = {
        "hsi": {"price": "—", "change": "—", "direction": "neutral"},
        "hscei": {"price": "—", "change": "—", "direction": "neutral"}
    }
    
    if not text:
        return data
    
    # 恒生指数: var hq_str_rt_hkHSI="HSI,恒生指数,25550.560,26025.420,...,-1.660,...";
    if 'rt_hkHSI="' in text:
        match = re.search(r'rt_hkHSI=\"([^\"]+)\"', text)
        if match:
            parts = match.group(1).split(',')
            if len(parts) >= 10:
                data["hsi"]["price"] = parts[6]  # 当前价
                change_val = float(parts[8])
                data["hsi"]["change"] = f"{change_val:+.2f}%"
                data["hsi"]["direction"] = "up" if change_val >= 0 else "down"
    
    # 国企指数
    if 'rt_hkHSCEI="' in text:
        match = re.search(r'rt_hkHSCEI=\"([^\"]+)\"', text)
        if match:
            parts = match.group(1).split(',')
            if len(parts) >= 10:
                data["hscei"]["price"] = parts[6]
                change_val = float(parts[8])
                data["hscei"]["change"] = f"{change_val:+.2f}%"
                data["hscei"]["direction"] = "up" if change_val >= 0 else "down"
    
    return data

def parse_commodity(text_gold, text_oil):
    """解析大宗商品数据"""
    data = {
        "gold": {"price": "—", "change": "—", "direction": "neutral"},
        "oil": {"price": "—", "change": "—", "direction": "neutral"}
    }
    
    # 黄金: var hq_str_hf_GC="4858.235,,4857.200,4857.300,4868.700,4806.000,11:43:17,4896.200,4828.000,...";
    if text_gold and 'hf_GC="' in text_gold:
        match = re.search(r'hf_GC=\"([^\"]+)\"', text_gold)
        if match:
            parts = match.group(1).split(',')
            if len(parts) >= 14:
                price = parts[0]
                data["gold"]["price"] = f"{price} 美元/盎司"
                try:
                    prev_close = float(parts[7])
                    curr = float(price)
                    change_pct = ((curr - prev_close) / prev_close) * 100
                    data["gold"]["change"] = f"{change_pct:+.2f}%"
                    data["gold"]["direction"] = "up" if change_pct >= 0 else "down"
                except:
                    pass
    
    # 原油
    if text_oil and 'hf_CL="' in text_oil:
        match = re.search(r'hf_CL=\"([^\"]+)\"', text_oil)
        if match:
            parts = match.group(1).split(',')
            if len(parts) >= 14:
                price = parts[0]
                data["oil"]["price"] = f"{price} 美元/桶"
                try:
                    prev_close = float(parts[7])
                    curr = float(price)
                    change_pct = ((curr - prev_close) / prev_close) * 100
                    data["oil"]["change"] = f"{change_pct:+.2f}%"
                    data["oil"]["direction"] = "up" if change_pct >= 0 else "down"
                except:
                    pass
    
    return data

def search_finance_news():
    """搜索财经新闻用于宏观政策和后市展望"""
    try:
        result = subprocess.run([
            'curl', '-s', '-X', 'POST', 'http://127.0.0.1:8080/search',
            '-d', 'q=财经新闻+宏观政策+美联储+央行+2025&category_general=1&format=json'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            results = data.get('results', [])
            # 提取新闻标题和内容摘要
            news_items = []
            for r in results[:3]:
                title = r.get('title', '')
                summary = r.get('content', r.get('abstract', ''))[:100] + '...'
                if title:
                    news_items.append(f"• {title}")
            return news_items
    except Exception as e:
        print(f"新闻搜索失败: {e}", file=sys.stderr)
    
    return []

def get_color(direction):
    """获取涨跌颜色 - 中国股市：红涨绿跌"""
    colors = {
        "up": "#ff4757",
        "down": "#2ed573",
        "neutral": "#747d8c"
    }
    return colors.get(direction, colors["neutral"])

def generate_html(date_str, data):
    """使用模板生成HTML"""
    template = read_template()
    if not template:
        return None
    
    month_day = date_str[5:7] + "." + date_str[8:10]
    
    # 根据数据生成评论
    us_comment = "美股隔夜收盘，"
    if data['dow']['direction'] == 'up':
        us_comment += "三大指数集体上涨，市场情绪乐观。"
    elif data['dow']['direction'] == 'down':
        us_comment += "三大指数回调，投资者情绪谨慎。"
    else:
        us_comment += "市场震荡整理。"
    
    a_comment = "A股今日走势，"
    if data['shanghai']['direction'] == 'up':
        a_comment += "大盘收涨，资金流入积极。"
    elif data['shanghai']['direction'] == 'down':
        a_comment += "大盘承压，板块分化明显。"
    else:
        a_comment += "市场震荡，等待方向选择。"
    
    hk_comment = "港股表现，"
    if data['hsi']['direction'] == 'up':
        hk_comment += "恒指上涨，科技股引领反弹。"
    elif data['hsi']['direction'] == 'down':
        hk_comment += "恒指回调，南向资金观望。"
    else:
        hk_comment += "恒指震荡整理。"
    
    # 搜索新闻用于宏观政策
    news_items = search_finance_news()
    macro_content = ""
    if news_items:
        macro_content = "\n".join(news_items[:2])
    else:
        macro_content = "• 关注国内外宏观政策动向\n• 密切跟踪市场流动性变化"
    
    # 后市展望基于当前数据
    outlook_items = []
    if data['dow']['direction'] == 'up':
        outlook_items.append("美股：技术面向好，关注财报季表现")
    else:
        outlook_items.append("美股：短期或维持震荡，关注美联储政策")
    
    if data['shanghai']['direction'] == 'up':
        outlook_items.append("A股：情绪回暖，关注量能持续性")
    else:
        outlook_items.append("A股：结构性机会仍存，精选个股为主")
    
    if data['hsi']['direction'] == 'up':
        outlook_items.append("港股：估值修复持续，关注互联网板块")
    else:
        outlook_items.append("港股：等待企稳信号，关注南向资金动向")
    
    if data['gold']['direction'] == 'up':
        outlook_items.append("黄金：避险需求支撑，关注美联储利率路径")
    else:
        outlook_items.append("黄金：短期承压，中长期配置价值仍存")
    
    replacements = {
        '{{TITLE}}': '财经早报',
        '{{DATE}}': month_day,
        '{{WEEKDAY}}': '| 洞察出品',
        
        # 美股
        '{{DAQ_CHANGE}}': f"{data['dow']['price']} ({data['dow']['change']})",
        '{{NASDAQ_CHANGE}}': f"{data['nasdaq']['price']} ({data['nasdaq']['change']})",
        '{{SP500_CHANGE}}': f"{data['sp500']['price']} ({data['sp500']['change']})",
        '{{US_MARKET_COMMENT}}': us_comment,
        
        # A股
        '{{SH_INDEX}}': f"{data['shanghai']['price']} ({data['shanghai']['change']})",
        '{{SZ_INDEX}}': f"{data['shenzhen']['price']} ({data['shenzhen']['change']})",
        '{{CY_INDEX}}': f"{data['chinext']['price']} ({data['chinext']['change']})",
        '{{A_MARKET_COMMENT}}': a_comment,
        
        # 港股
        '{{HSI_CHANGE}}': f"{data['hsi']['price']} ({data['hsi']['change']})",
        '{{HSTECH_CHANGE}}': f"{data['hscei']['price']} ({data['hscei']['change']})",
        '{{SOUTHBOUND_FLOW}}': '关注南向资金流向',
        
        # 板块热点 - 简化为根据大盘表现判断
        '{{SECTOR_TAGS}}': generate_sector_tags(data),
        '{{SECTOR_COMMENT}}': generate_sector_comment(data),
        
        # 大宗商品
        '{{GOLD_PRICE}}': data['gold']['price'],
        '{{GOLD_CHANGE}}': data['gold']['change'],
        '{{GOLD_COLOR}}': get_color(data['gold']['direction']),
        '{{OIL_PRICE}}': data['oil']['price'],
        '{{OIL_CHANGE}}': data['oil']['change'],
        '{{OIL_COLOR}}': get_color(data['oil']['direction']),
        '{{COMMODITY_COMMENT}}': generate_commodity_comment(data),
        
        # 宏观政策
        '{{MACRO_POLICY_CONTENT}}': macro_content,
        
        # 后市展望
        '{{OUTLOOK_US}}': outlook_items[0] if len(outlook_items) > 0 else '美股：关注美联储政策和企业财报',
        '{{OUTLOOK_A}}': outlook_items[1] if len(outlook_items) > 1 else 'A股：关注国内经济数据和政策面变化',
        '{{OUTLOOK_HK}}': outlook_items[2] if len(outlook_items) > 2 else '港股：关注南向资金流向和科技股表现',
        '{{OUTLOOK_COMMODITY}}': outlook_items[3] if len(outlook_items) > 3 else '大宗商品：关注地缘风险和国际油价走势'
    }
    
    html = template
    for key, value in replacements.items():
        html = html.replace(key, value)
    
    return html

def generate_sector_tags(data):
    """生成板块标签"""
    tags = []
    
    # 根据市场走势生成相关板块提示
    if data['shanghai']['direction'] == 'up':
        tags.append('<span style="background: #ffebee; color: #c62828; padding: 5px 12px; border-radius: 15px; font-size: 13px;">金融 📈</span>')
    
    if data['chinext']['direction'] == 'up':
        tags.append('<span style="background: #ffebee; color: #c62828; padding: 5px 12px; border-radius: 15px; font-size: 13px;">科技成长 📈</span>')
    elif data['chinext']['direction'] == 'down':
        tags.append('<span style="background: #e8f5e9; color: #2e7d32; padding: 5px 12px; border-radius: 15px; font-size: 13px;">科技成长 📉</span>')
    
    if data['hsi']['direction'] == 'up':
        tags.append('<span style="background: #ffebee; color: #c62828; padding: 5px 12px; border-radius: 15px; font-size: 13px;">港股科技 📈</span>')
    
    if not tags:
        tags.append('<span style="background: #f5f5f5; color: #666; padding: 5px 12px; border-radius: 15px; font-size: 13px;">市场震荡 板块分化</span>')
    
    return '\n        '.join(tags)

def generate_sector_comment(data):
    """生成板块评论"""
    if data['shanghai']['direction'] == 'up' and data['chinext']['direction'] == 'up':
        return "大盘与创业板同步上涨，市场情绪回暖，板块轮动活跃。"
    elif data['shanghai']['direction'] == 'down' and data['chinext']['direction'] == 'down':
        return "市场整体承压，各板块普遍回调，建议控制仓位。"
    elif data['shanghai']['direction'] == 'up':
        return "权重股护盘，大盘收涨，但创业板相对较弱，结构性行情明显。"
    else:
        return "板块分化加剧，建议关注业绩确定性高的标的。"

def generate_commodity_comment(data):
    """生成商品评论"""
    comments = []
    if data['gold']['direction'] == 'up':
        comments.append("黄金上涨，避险需求升温")
    elif data['gold']['direction'] == 'down':
        comments.append("黄金回调，美元走强压制")
    
    if data['oil']['direction'] == 'up':
        comments.append("原油上涨，供应担忧支撑")
    elif data['oil']['direction'] == 'down':
        comments.append("原油承压，需求预期下调")
    
    return "；".join(comments) if comments else "大宗商品价格震荡，关注供需变化"

def main():
    date_str = sys.argv[1] if len(sys.argv) > 1 else "2026-03-19"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "/tmp/finance-content.html"
    
    print(f"正在获取 {date_str} 的完整财经数据...", file=sys.stderr)
    
    # 获取美股数据
    print("  获取美股数据...", file=sys.stderr)
    us_text = fetch_sina_data(['int_dji', 'int_nasdaq', 'int_sp500'])
    us_data = parse_us_market(us_text)
    
    # 获取A股数据
    print("  获取A股数据...", file=sys.stderr)
    a_text = fetch_sina_data(['s_sh000001', 's_sz399001', 's_sz399006'])
    a_data = parse_a_market(a_text)
    
    # 获取港股数据
    print("  获取港股数据...", file=sys.stderr)
    hk_text = fetch_sina_data(['rt_hkHSI', 'rt_hkHSCEI'])
    hk_data = parse_hk_market(hk_text)
    
    # 获取大宗商品
    print("  获取大宗商品数据...", file=sys.stderr)
    gold_text = fetch_sina_data(['hf_GC'])
    oil_text = fetch_sina_data(['hf_CL'])
    commodity_data = parse_commodity(gold_text, oil_text)
    
    # 合并数据
    data = {**us_data, **a_data, **hk_data, **commodity_data}
    
    print(f"\n数据获取完成:", file=sys.stderr)
    print(f"  美股: 道指{data['dow']['price']}, 纳指{data['nasdaq']['price']}, 标普{data['sp500']['price']}", file=sys.stderr)
    print(f"  A股: 上证{data['shanghai']['price']}, 深证{data['shenzhen']['price']}, 创业板{data['chinext']['price']}", file=sys.stderr)
    print(f"  港股: 恒指{data['hsi']['price']}, 国企{data['hscei']['price']}", file=sys.stderr)
    print(f"  商品: 黄金{data['gold']['price']}, 原油{data['oil']['price']}", file=sys.stderr)
    
    html = generate_html(date_str, data)
    
    if html:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"\n财经早报内容已生成: {output_file}")
    else:
        print("生成失败")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
