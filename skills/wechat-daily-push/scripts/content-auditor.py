#!/usr/bin/env python3
#
# content-auditor.py - 内容审核师
# 审核日报内容的事实准确性、数据真实性
#

import sys
import re

def audit_ai_content(content):
    """审核AI日报内容"""
    issues = []
    warnings = []
    
    # 审核清单 - 已发布/已证实的内容不再拦截
    check_items = [
        # (关键词, 问题描述, 严重程度: error/warning)
        # 注意：Claude 4 已正式发布（claude-sonnet-4-20250514），不再拦截
        (r'DeepSeek\s*V4', 'DeepSeek V4 尚未正式发布，请核实', 'error'),
        (r'GPT-5', 'GPT-5 尚未正式发布，请核实', 'error'),
        (r'Gemini\s*3|Gemini-3', 'Gemini 3 尚未正式发布，请核实', 'warning'),
        (r'已经发布.*V5|V5.*已经发布', 'V5版本发布信息可能不实', 'error'),
        (r'突破.*物理.*定律|违反.*物理', '夸张不实描述', 'error'),
        (r'独家.*内部消息|内部人士透露', '无法验证的信息来源', 'warning'),
        (r'数据获取中|暂无可信来源', '数据来源缺失', 'warning'),
        # 新增：检测未证实的AI能力宣称
        (r'实现永生|永生了|永生技术', '永生相关宣称通常不实', 'error'),
        (r'突破.*图灵测试.*100%|完全通过.*图灵测试', '过度夸张的性能宣称', 'warning'),
        (r'超越人类.*所有领域|全面超越人类', '过度夸张的AI能力描述', 'warning'),
    ]
    
    for pattern, desc, level in check_items:
        if re.search(pattern, content, re.IGNORECASE):
            if level == 'error':
                issues.append(f"❌ {desc}")
            else:
                warnings.append(f"⚠️ {desc}")
    
    # 检查是否有数据来源标注
    if '来源' not in content and '数据来源' not in content:
        warnings.append("⚠️ 缺少数据来源标注")
    
    # 检查免责声明
    if '仅供参考' not in content and '自动生成' not in content:
        warnings.append("⚠️ 缺少免责声明")
    
    return issues, warnings

def audit_finance_content(content):
    """审核财经早报内容"""
    issues = []
    warnings = []
    
    # 审核清单
    check_items = [
        # 数据真实性检查
        (r'41,850\.00|41,850\.0{1,2}', '道指数据疑似使用模拟值，请核实', 'warning'),
        (r'17,650\.00|17,650\.0{1,2}', '纳指数据疑似使用模拟值，请核实', 'warning'),
        (r'5,780\.00|5,780\.0{1,2}', '标普500数据疑似使用模拟值，请核实', 'warning'),
        (r'2,985\.00', '黄金价格疑似使用模拟值，请核实', 'warning'),
        (r'73\.50', '原油价格疑似使用模拟值，请核实', 'warning'),
        
        # 格式检查
        (r'—.*—', '多处数据缺失（—）', 'warning'),
        (r'数据获取中', '数据获取失败', 'warning'),
    ]
    
    for pattern, desc, level in check_items:
        if re.search(pattern, content):
            if level == 'error':
                issues.append(f"❌ {desc}")
            else:
                warnings.append(f"⚠️ {desc}")
    
    # 检查是否有免责声明
    if '投资需谨慎' not in content:
        warnings.append("⚠️ 缺少投资风险提示")
    
    if '仅供参考' not in content:
        warnings.append("⚠️ 缺少数据免责声明")
    
    # 检查涨跌幅颜色是否正确（中国股市红涨绿跌）
    if 'up' in content and 'down' in content:
        # 检查是否有颜色定义
        if 'color: #ff4757' not in content and 'color: #2ed573' not in content:
            warnings.append("⚠️ 涨跌幅颜色可能不正确")
    
    return issues, warnings

def generate_report(content_type, issues, warnings):
    """生成审核报告"""
    status = "✅ 通过" if not issues else "❌ 不通过"
    
    report = f"""
========================================
📋 内容审核报告 ({content_type})
========================================

审核结果: {status}

"""
    
    if issues:
        report += "【严重问题 - 必须修复】\n"
        for issue in issues:
            report += f"  {issue}\n"
        report += "\n"
    
    if warnings:
        report += "【警告 - 建议优化】\n"
        for warning in warnings:
            report += f"  {warning}\n"
        report += "\n"
    
    if not issues and not warnings:
        report += "✅ 未发现明显问题\n\n"
    
    report += "========================================\n"
    
    return report, len(issues) == 0

def main():
    if len(sys.argv) < 2:
        print("用法: python3 content-auditor.py <html文件路径> [ai|finance]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    content_type = sys.argv[2] if len(sys.argv) > 2 else "auto"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 无法读取文件: {e}")
        sys.exit(1)
    
    # 自动判断类型
    if content_type == "auto":
        if "AI日报" in content or "🤖" in content:
            content_type = "ai"
        elif "财经早报" in content or "📊" in content:
            content_type = "finance"
        else:
            print("❌ 无法自动判断内容类型，请手动指定 ai 或 finance")
            sys.exit(1)
    
    # 执行审核
    if content_type == "ai":
        issues, warnings = audit_ai_content(content)
    else:
        issues, warnings = audit_finance_content(content)
    
    # 生成报告
    report, passed = generate_report(content_type.upper() + "日报", issues, warnings)
    print(report)
    
    # 返回状态码
    sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
