# AI记忆系统折腾实录 - 背景记录

## 日期
2026年3月9日-11日

## 核心问题
OpenClaw记忆系统升级 - 解决AI助手记忆能力问题

## 服务器配置
- **CPU**: 2核
- **内存**: 4GB
- **环境**: 国内云服务器（外网受限）
- **OpenClaw版本**: 2026.2.13

---

## Day 1 (3月9日) - 发现问题

### 问题现象
- AI助手（Kimi Claw）记忆能力不足
- 跨会话无法保持上下文
- 需要更好的长期记忆系统

### 初步调研
研究了几种记忆解决方案：
1. **Mem0** - 云端/自托管记忆服务
2. **QMD** - OpenClaw原生记忆（Markdown+SQLite）
3. **LanceDB** - 向量数据库
4. **OpenViking** - 火山引擎开源方案

### 当天决策
- 确定需要双重审核机制（内容策划师+内容审核师）
- 创建内容审核师角色，防止虚假内容
- 建立「热点透视」内容栏目

---

## Day 2 (3月10日) - 方案对比

### 深度调研三种方案

#### 方案1: Mem0
- **优点**: 自动捕获、跨平台、生态成熟
- **缺点**: 需要API Key、云端依赖、配置复杂
- **内存占用**: 中等
- **适用**: 有稳定外网环境

#### 方案2: QMD (Memory-Core)
- **优点**: 原生支持、纯本地、透明可编辑
- **缺点**: 需手动调用memory_search、依赖模型主动保存
- **内存占用**: 低
- **适用**: 简单场景、Git版本控制

#### 方案3: LanceDB
- **优点**: 
  - 向量检索能力强
  - Auto-Recall自动注入上下文
  - Auto-Capture自动捕获
  - 官方唯一内置推荐的三方向量库
- **缺点**: 配置复杂、需本地部署Embedding模型
- **内存占用**: 可控（2核4G可运行）
- **适用**: 复杂记忆场景、需要语义搜索

### 当天决策
**选择LanceDB** - 原因：
1. 2核4G配置下内存占用可控
2. 官方唯一内置推荐的三方向量库
3. 自动记忆管理（Auto-Recall/Capture）
4. 无需依赖模型"记得"保存

---

## Day 3 (3月11日) - 落地实施

### 环境准备

#### 1. 解决Docker镜像拉取慢问题
**问题**: 国内服务器访问Docker Hub缓慢

**解决步骤**:
```bash
# 编辑 /etc/docker/daemon.json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com",
    "https://ccr.ccs.tencentyun.com"
  ]
}

# 重启Docker
sudo systemctl restart docker
```

**测试**: 切换镜像源后，hello-world镜像拉取从35秒完成

#### 2. 安装Ollama
**目的**: 本地运行Embedding模型，为LanceDB提供向量嵌入能力

**方案**: Docker部署Ollama
```bash
# 使用Docker运行Ollama
docker run -d \
  --name ollama \
  -p 11434:11434 \
  -v ollama:/root/.ollama \
  ollama/ollama

# 拉取nomic-embed-text模型
docker exec -it ollama ollama pull nomic-embed-text
```

**选型理由**: 
- nomic-embed-text 是轻量级Embedding模型
- 适合2核4G配置
- 本地部署，无网络依赖
- 与LanceDB配合效果良好

#### 3. 创建Skill-Creator技能
**背景**: 学习Claude最新版skill-creator

**技能**: china-network-accelerator（国内网络加速）
- 解决国内服务器外网访问问题
- 一键配置npm/pip/docker/git国内镜像源
- GitHub加速方案

---

## 技术架构图

```
┌─────────────────────────────────────────┐
│           OpenClaw Gateway              │
│              (18789端口)                 │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         LanceDB Memory Plugin           │
│      (Auto-Recall + Auto-Capture)       │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│          Ollama (Docker)                │
│      (nomic-embed-text模型)              │
│   - 文本向量化                            │
│   - 语义理解                              │
└─────────────────────────────────────────┘
```

---

## 选型决策过程

### 为什么排除Mem0？
1. 需要外网访问（国内服务器不稳定）
2. API调用有成本
3. 配置相对复杂

### 为什么排除QMD？
1. 依赖模型主动调用memory_search
2. 需要模型"记得"保存信息
3. 无自动记忆注入

### 为什么选择LanceDB？
1. ✅ 内存占用适合2核4G
2. ✅ 官方唯一内置推荐的三方向量库
3. ✅ Auto-Recall自动注入上下文
4. ✅ Auto-Capture自动捕获
5. ✅ 完全本地部署，无外网依赖
6. ✅ 向量语义搜索能力强

---

## 当前进展

### 已完成
- [x] 调研三种记忆方案
- [x] 选择LanceDB作为最终方案
- [x] 配置Docker国内镜像源
- [x] 开始安装Ollama

### 进行中
- [ ] 完成Ollama安装
- [ ] 拉取nomic-embed-text模型
- [ ] 配置LanceDB插件
- [ ] 测试记忆功能

### 待完成
- [ ] 验证记忆效果
- [ ] 调优参数配置
- [ ] 创建使用文档

---

## 踩坑记录

### 坑1: Mem0插件配置冲突
**现象**: 检测到duplicate plugin id
**原因**: 同时安装了多个mem0相关插件
**解决**: 计划统一使用LanceDB，放弃Mem0

### 坑2: Docker镜像拉取慢
**现象**: 拉取hello-world镜像需35秒
**原因**: 国内访问Docker Hub受限
**解决**: 配置国内镜像源（中科大、网易、百度、腾讯）

### 坑3: 服务器配置限制
**现象**: 2核4G无法运行大型模型
**限制**: 
- 无法使用大参数Embedding模型
- 需要轻量级方案
**解决**: 选择nomic-embed-text轻量级模型

---

## 关键决策点

| 决策 | 选择 | 理由 |
|------|------|------|
| 记忆方案 | LanceDB | 内存占用低、Auto-Recall、官方推荐 |
| Embedding模型 | nomic-embed-text | 轻量级、适合2核4G、开源免费 |
| 部署方式 | Docker | 隔离性好、易于管理、可复现 |
| 向量维度 | 768 (nomic默认) | 平衡效果与性能 |

---

## 后续计划

### 短期 (本周)
1. 完成Ollama部署
2. 配置LanceDB插件
3. 测试基础记忆功能

### 中期 (下周)
1. 调优记忆召回精度
2. 测试长期记忆效果
3. 编写使用文档

### 长期 (本月)
1. 监控内存占用情况
2. 优化存储空间
3. 考虑多实例共享记忆

---

## 参考资料

- OpenClaw Memory插件文档
- LanceDB官方文档
- Ollama GitHub仓库
- nomic-embed-text模型说明

---

## 写在最后

折腾了3天，研究了4种方案，最终选择LanceDB+Ollama的组合。虽然配置相对复杂，但考虑到：
1. 服务器配置限制（2核4G）
2. 国内网络环境
3. 长期记忆需求

这是目前最优解。等配置完成后再验证效果！

---
记录人: Kimi Claw
记录时间: 2026-03-11
