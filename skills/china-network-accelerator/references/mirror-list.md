# 国内镜像源参考

## NPM/Yarn镜像

| 镜像 | 地址 |
|------|------|
| 淘宝npm | https://registry.npmmirror.com |
| 腾讯云 | https://mirrors.cloud.tencent.com/npm |
| 华为云 | https://mirrors.huaweicloud.com/repository/npm |

## Python pip镜像

| 镜像 | 地址 |
|------|------|
| 清华 | https://pypi.tuna.tsinghua.edu.cn/simple |
| 阿里云 | https://mirrors.aliyun.com/pypi/simple |
| 中科大 | https://pypi.mirrors.ustc.edu.cn/simple |

## Docker镜像

| 镜像 | 地址 |
|------|------|
| 中科大 | https://docker.mirrors.ustc.edu.cn |
| 网易云 | https://hub-mirror.c.163.com |
| 上海交大 | https://docker.mirrors.sjtug.sjtu.edu.cn |

## GitHub加速

- ghproxy: https://ghproxy.com/
- fastgit: https://hub.fastgit.xyz/

## Linux系统镜像

### Ubuntu/Debian
```bash
sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list
```

### CentOS/RHEL
```bash
# 使用阿里云镜像
wget -O /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo
```
