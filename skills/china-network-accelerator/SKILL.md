---
name: china-network-accelerator
description: 解决国内服务器访问外网受限问题。自动配置npm/pip/docker/git国内镜像源，提供GitHub加速方案，诊断网络连通性。当用户遇到GitHub访问慢、npm install失败、docker pull超时、pip安装慢等问题时使用。
---

# 国内网络加速配置

解决国内服务器访问外网受限问题，一键配置国内镜像源。

## 快速开始

### 一键切换所有镜像源
```bash
bash scripts/switch-mirrors.sh
```

### 诊断当前网络状态
```bash
bash scripts/test-connectivity.sh
```

## 支持的工具

| 工具 | 加速方式 | 镜像源 |
|------|----------|--------|
| NPM | 切换registry | npmmirror(淘宝) |
| Python pip | pip.conf配置 | 清华TUNA |
| Docker | daemon.json | 中科大/网易/交大 |
| GitHub | git insteadOf | ghproxy |

## 详细配置参考

- **镜像源列表**: 见 [mirror-list.md](references/mirror-list.md)
- **代理配置**: 如需HTTP代理，设置环境变量 `export HTTP_PROXY=http://proxy:port`

## 使用场景

1. **GitHub无法访问或很慢**
   ```bash
   bash scripts/switch-mirrors.sh  # 配置ghproxy加速
   ```

2. **npm install 卡住或失败**
   ```bash
   npm config set registry https://registry.npmmirror.com
   ```

3. **pip安装慢**
   ```bash
   pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
   ```

4. **docker pull 超时**
   ```bash
   # 编辑 /etc/docker/daemon.json 添加registry-mirrors
   ```

## 验证配置

运行诊断脚本查看当前状态：
```bash
bash scripts/test-connectivity.sh
```
