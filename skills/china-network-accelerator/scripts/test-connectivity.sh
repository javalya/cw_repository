#!/bin/bash
# 网络连通性诊断

echo "🌐 网络连通性诊断"
echo "=================="
echo ""

# 要测试的站点
SITES=(
    "github.com"
    "google.com"
    "npmjs.com"
    "docker.com"
    "pypi.org"
    "anthropic.com"
    "openai.com"
)

echo "测试外网连通性:"
echo ""

for site in "${SITES[@]}"; do
    if ping -c 1 -W 3 "$site" > /dev/null 2>&1; then
        echo "  ✅ $site - 可访问"
    else
        echo "  ❌ $site - 不可访问"
    fi
done

echo ""
echo "代理环境变量:"
echo "  HTTP_PROXY:  ${HTTP_PROXY:-未设置}"
echo "  HTTPS_PROXY: ${HTTPS_PROXY:-未设置}"
echo "  ALL_PROXY:   ${ALL_PROXY:-未设置}"

echo ""
echo "当前镜像源配置:"

# NPM
if command -v npm &> /dev/null; then
    NPM_REGISTRY=$(npm config get registry)
    echo "  NPM: $NPM_REGISTRY"
fi

# PIP
if [ -f ~/.pip/pip.conf ]; then
    PIP_INDEX=$(grep "index-url" ~/.pip/pip.conf | cut -d= -f2 | tr -d ' ')
    echo "  PIP: $PIP_INDEX"
fi

# GitHub代理
if git config --global --get url."https://ghproxy.com/https://github.com/".insteadOf &> /dev/null; then
    echo "  GitHub: 已配置ghproxy"
fi

echo ""
