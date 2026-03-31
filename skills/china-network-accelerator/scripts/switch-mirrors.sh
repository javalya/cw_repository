#!/bin/bash
# 一键切换国内镜像源

echo "🚀 切换国内镜像源"
echo ""

# 检测系统类型
if command -v apt &> /dev/null; then
    OS="debian"
elif command -v yum &> /dev/null; then
    OS="rhel"
else
    OS="unknown"
fi

# 1. NPM镜像
echo "📦 配置NPM镜像..."
if command -v npm &> /dev/null; then
    npm config set registry https://registry.npmmirror.com
    echo "  ✅ NPM: https://registry.npmmirror.com"
else
    echo "  ⚠️  NPM未安装"
fi

# 2. Python pip镜像
echo "🐍 配置PIP镜像..."
if command -v pip &> /dev/null; then
    mkdir -p ~/.pip
    cat > ~/.pip/pip.conf << 'EOF'
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
EOF
    echo "  ✅ PIP: https://pypi.tuna.tsinghua.edu.cn/simple"
else
    echo "  ⚠️  PIP未安装"
fi

# 3. Docker镜像
echo "🐳 配置Docker镜像..."
if command -v docker &> /dev/null; then
    mkdir -p /etc/docker
    cat > /etc/docker/daemon.json << 'EOF'
{
  "registry-mirrors": [
    "https://docker.mirrors.sjtug.sjtu.edu.cn",
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}
EOF
    echo "  ✅ Docker: 已配置多镜像源"
    echo "  📝 请执行: sudo systemctl restart docker"
else
    echo "  ⚠️  Docker未安装"
fi

# 4. GitHub加速
echo "🐙 配置GitHub加速..."
git config --global url."https://ghproxy.com/https://github.com/".insteadOf "https://github.com/"
echo "  ✅ GitHub: 使用ghproxy加速"

echo ""
echo "✨ 镜像源切换完成！"
