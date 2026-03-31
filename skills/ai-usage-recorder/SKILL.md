---
name: ai-usage-recorder
description: AI使用实录技能 - 分析当天聊天记录，按照差评风格模板生成文章记录用户使用OpenClaw的实录，分享使用经验和心得，并推送到公众号草稿箱
trigger: "使用ai实录技能"
---

# AI使用实录技能

## 触发指令
用户说：**"使用ai实录技能"**

## 执行流程

### 步骤1：分析当天聊天记录
- 读取当天 memory/YYYY-MM-DD.md 文件
- 回顾当天的对话内容
- 提取关键互动节点和问题解决方案

### 步骤2：按差评风格模板生成文章
参考 config/writing_guidelines.md 的规范：

**文章结构**：
1. **标题**： catchy，带情绪，如"我用AI干了一天活｜结果..."
2. **导语**：1句话概括当天的核心体验
3. **正文**：按时间线或问题线展开
   - 🔥 上午：遇到了什么问题
   - 💥 下午：怎么解决的
   - ✅ 晚上：成果如何
4. **使用心得**：总结经验和技巧
5. **MickJagger点评**：AI视角的一句话点评
6. **结尾**：时间+署名

**文风要求**：
- 口语化："炸了"、"真香"、"离谱"
- 用户视角："我让他..."、"我发现..."
- 有态度：不回避问题，真实分享
- 故事感：像讲亲身经历

### 步骤3：推送到公众号草稿箱
- 使用 wechat-daily-push 技能
- AppID: wx474c0d9c9e4a8d1a
- 确保中文不乱码（ensure_ascii=False）
- 标题控制在64字节内

## 模板示例

**标题格式**：
```
我用AI干了一天活｜这几个坑把我整麻了
```

**正文结构**：
```html
<section style='font-size: 16px; line-height: 1.8;'>
  <p style='margin: 20px 0; background: #f5f5f5; padding: 15px; border-left: 4px solid #666;'>
    ☕ <strong>导语：</strong>今天是我用Kimi Claw的第一天...
  </p>
  
  <h3 style='font-size: 20px; font-weight: bold; margin: 30px 0 15px 0;'>🔥 上午：网络炸了</h3>
  <p>刚开始就不对劲...</p>
  
  <h3>💥 下午：踩坑实录</h3>
  <p>然后开始连环踩坑...</p>
  
  <h3>✅ 晚上：真香了</h3>
  <p>总算搞定了...</p>
  
  <blockquote>
    💬 <strong>使用心得：</strong>...
  </blockquote>
  
  <hr/>
  <p style='color: #999; font-size: 14px;'>...
</section>
```

## 注意事项
1. 从用户视角写，不是AI视角
2. 真实记录问题和解决过程
3. 分享具体的使用技巧和经验
4. 保持差评风格的口语化表达
5. 生成后推送到公众号草稿箱
