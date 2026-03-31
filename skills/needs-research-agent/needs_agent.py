#!/usr/bin/env python3
"""
轻量级需求调研 Agent
自动发现用户痛点和App需求机会
"""

import json
import re
import os
from datetime import datetime, timedelta
from collections import Counter
from typing import List, Dict, Any
import yaml

# 模拟数据存储（实际使用时可以接入真实API或数据库）
class NeedsResearchAgent:
    """需求调研Agent主类"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.pain_points = []
        self.report_data = {
            "generated_at": datetime.now().isoformat(),
            "period": "weekly",
            "pain_points": [],
            "trends": [],
            "recommendations": []
        }
    
    def _load_config(self, path: str) -> Dict:
        """加载配置文件"""
        default_config = {
            "platforms": [
                {"name": "reddit", "enabled": True, "keywords": ["app idea", "looking for app", "wish there was"]},
                {"name": "xiaohongshu", "enabled": True, "keywords": ["求推荐", "有没有app", "想找个工具"]},
                {"name": "jike", "enabled": True, "keywords": ["效率工具", "求推荐"]}
            ],
            "report": {
                "min_mentions": 3,
                "format": "markdown"
            },
            "output": {
                "path": "./reports/"
            }
        }
        
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return default_config
    
    def search_pain_points(self) -> List[Dict]:
        """
        搜索各平台的用户痛点
        实际使用时接入真实API
        """
        # 模拟数据 - 实际使用时替换为真实爬虫
        mock_data = [
            # Reddit 风格
            {"platform": "reddit", "text": "Wish there was an app to quickly calm down during work stress", "mentions": 5},
            {"platform": "reddit", "text": "Looking for a simple journaling app without social features", "mentions": 4},
            {"platform": "reddit", "text": "Need an app to track how long my stuff lasts", "mentions": 3},
            {"platform": "reddit", "text": "App idea: Emergency mood booster for anxiety attacks", "mentions": 6},
            
            # 小红书风格
            {"platform": "xiaohongshu", "text": "求推荐一个简单记录心情的App，不要社交", "mentions": 8},
            {"platform": "xiaohongshu", "text": "有没有能追踪物品使用寿命的工具", "mentions": 4},
            {"platform": "xiaohongshu", "text": "想要一个极简手帐App，不要太复杂", "mentions": 7},
            {"platform": "xiaohongshu", "text": "工作压力大，有没有快速减压的App推荐", "mentions": 12},
            
            # 即刻风格
            {"platform": "jike", "text": "求推荐：轻量级情绪管理工具", "mentions": 5},
            {"platform": "jike", "text": "想要一个数字手帐，类似纸质手帐的感觉", "mentions": 6},
        ]
        
        self.pain_points = mock_data
        return mock_data
    
    def analyze_frequency(self) -> Dict[str, Any]:
        """分析痛点频率和分类"""
        
        # 关键词分类
        categories = {
            "情绪管理": ["calm", "stress", "anxiety", "mood", "减压", "情绪", "心情", "压力"],
            "手帐笔记": ["journal", "journaling", "hand account", "手帐", "笔记", "记录"],
            "物品管理": ["track", "stuff", "lasts", "物品", "寿命", "追踪"],
            "极简工具": ["simple", "minimal", "极简", "轻量", "简单"]
        }
        
        category_counts = {cat: 0 for cat in categories}
        
        for point in self.pain_points:
            text = point["text"].lower()
            for category, keywords in categories.items():
                if any(kw in text for kw in keywords):
                    category_counts[category] += point["mentions"]
        
        # 按提及次数排序
        sorted_categories = sorted(
            category_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return {
            "category_stats": sorted_categories,
            "total_mentions": sum(point["mentions"] for point in self.pain_points),
            "unique_points": len(self.pain_points)
        }
    
    def scan_competitors(self, category: str) -> List[Dict]:
        """扫描竞品情况"""
        competitors_db = {
            "情绪管理": [
                {"name": "Calm", "type": "国外", "complexity": "高", "gap": "无中文急救场景"},
                {"name": "Headspace", "type": "国外", "complexity": "高", "gap": "流程太长"},
                {"name": "小睡眠", "type": "国内", "complexity": "中", "gap": "功能杂"},
                {"name": "潮汐", "type": "国内", "complexity": "中", "gap": "偏向冥想"}
            ],
            "手帐笔记": [
                {"name": "GoodNotes", "type": "国外", "complexity": "高", "gap": "iOS独占"},
                {"name": "Notion", "type": "国外", "complexity": "高", "gap": "太复杂"},
                {"name": "时光序", "type": "国内", "complexity": "中", "gap": "功能多但不精"}
            ],
            "物品管理": [
                {"name": "随手记", "type": "国内", "complexity": "高", "gap": "偏向记账"},
                {"name": "备忘录", "type": "系统", "complexity": "低", "gap": "无统计功能"}
            ]
        }
        
        return competitors_db.get(category, [])
    
    def generate_recommendations(self, analysis: Dict) -> List[Dict]:
        """生成推荐行动"""
        recommendations = []
        
        category_stats = analysis["category_stats"]
        
        if category_stats:
            top_category = category_stats[0][0]
            top_mentions = category_stats[0][1]
            
            if top_category == "情绪管理" and top_mentions >= 10:
                recommendations.append({
                    "priority": "高",
                    "category": "情绪急救App",
                    "reason": f"提及{top_mentions}次，大厂方案复杂，缺乏快速急救场景",
                    "mvp_time": "3周",
                    "market_size": "全球$143亿",
                    "action": "建议优先开发"
                })
            
            if len(category_stats) > 1 and category_stats[1][1] >= 5:
                second_category = category_stats[1][0]
                recommendations.append({
                    "priority": "中",
                    "category": f"{second_category}App",
                    "reason": f"提及{category_stats[1][1]}次，有一定需求",
                    "mvp_time": "4-5周",
                    "action": "可并行调研"
                })
        
        return recommendations
    
    def generate_report(self) -> str:
        """生成Markdown报告"""
        
        # 收集数据
        self.search_pain_points()
        analysis = self.analyze_frequency()
        recommendations = self.generate_recommendations(analysis)
        
        # 构建报告
        report_date = datetime.now().strftime("%Y-%m-%d")
        
        report = f"""# 需求调研周报 - {report_date}

## 📊 数据概览

- **调研平台**: Reddit、小红书、即刻
- **发现痛点**: {analysis['unique_points']}个
- **总提及次数**: {analysis['total_mentions']}次
- **报告生成**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 🔥 高频痛点分类 (TOP 3)

"""
        
        # 添加分类统计
        for i, (category, count) in enumerate(analysis['category_stats'][:3], 1):
            competitors = self.scan_competitors(category)
            
            report += f"""### {i}. {category}
- **提及次数**: {count}次
- **用户需求**: 
"""
            # 找出该分类下的具体需求
            related_points = []
            keywords = {
                "情绪管理": ["calm", "stress", "anxiety", "mood", "减压", "情绪", "心情", "压力"],
                "手帐笔记": ["journal", "journaling", "hand account", "手帐", "笔记", "记录"],
                "物品管理": ["track", "stuff", "lasts", "物品", "寿命", "追踪"]
            }.get(category, [])
            
            for point in self.pain_points:
                if any(kw in point["text"].lower() for kw in keywords):
                    related_points.append(point["text"])
            
            for text in related_points[:3]:
                report += f"  - {text}\n"
            
            # 竞品分析
            if competitors:
                report += f"- **现有方案**: {', '.join([c['name'] for c in competitors[:3]])}\n"
                gaps = [c['gap'] for c in competitors if c.get('gap')]
                if gaps:
                    report += f"- **市场缺口**: {gaps[0]}\n"
            
            report += f"- **机会评级**: {'⭐' * (4 if count >= 10 else 3)}\n\n"
        
        # 推荐行动
        report += """---

## 🎯 推荐行动

"""
        
        for rec in recommendations:
            report += f"""### {rec['priority']}优先级: {rec['category']}
- **理由**: {rec['reason']}
- **MVP周期**: {rec['mvp_time']}
- **建议**: {rec['action']}

"""
        
        # 趋势观察
        report += """---

## 📈 趋势观察

- AI+个人管理类需求持续上升
- 极简、无社交功能成为新偏好
- 职场压力相关工具需求明显

---

*Report generated by Needs Research Agent v1.0*
*INSIGHT AI STUDIO*
"""
        
        return report
    
    def save_report(self, report: str, output_dir: str = "./reports/"):
        """保存报告到文件"""
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"needs_report_{datetime.now().strftime('%Y%m%d')}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 报告已保存: {filepath}")
        return filepath
    
    def run(self):
        """运行完整调研流程"""
        print("🚀 启动需求调研Agent...")
        print("📡 正在搜索各平台痛点...")
        
        report = self.generate_report()
        
        output_dir = self.config.get("output", {}).get("path", "./reports/")
        filepath = self.save_report(report, output_dir)
        
        print("\n" + "="*50)
        print("📋 调研报告预览:")
        print("="*50)
        print(report[:1000] + "...\n")
        
        return filepath


def main():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='需求调研Agent')
    parser.add_argument('--config', default='config.yaml', help='配置文件路径')
    parser.add_argument('--report', choices=['weekly', 'daily'], default='weekly', help='报告类型')
    
    args = parser.parse_args()
    
    agent = NeedsResearchAgent(args.config)
    agent.run()


if __name__ == "__main__":
    main()
