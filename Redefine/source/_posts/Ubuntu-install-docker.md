---
title: 在 Ubuntu 22.04 LTS 中安装 Docker 和 Docker Compose
date: 2022-10-25 12:10:30
tags:
  - Ubuntu
  - docker
  - docker-compose
---

## 本文是在 Ubuntu 中安装 Docker 和 Docker Compose 的教程。

### 什么是 Docker ？

------

**Docker** 是一个快捷、轻便的系统级虚拟化技术，开发者和系统管理员可以使用它构建具备所有必要依赖项的应用程序，并将其作为一个包发布。

Docker 与其他如 VMWare 、 VirtualBox 等工具的虚拟化方式不同，每个虚拟机不需要单独的客户操作系统。所有的 Docker 容器有效地共享同一个主机系统内核。每个容器都在同一个操作系统中的隔离用户空间中运行。

Docker 容器可以在任何 Linux 版本上运行。比如说你使用 Fedora ，我用 Ubuntu 。我们能相互开发、共享并分发 Docker 镜像。你无需担心操作系统、软件以及自定义设置，任何事都不用担心。只要我们的主机安装了 Docker ，就能持续开发。简言之，Docker 能够在任何地方运行！

前文中你读到了两个词：**Docker 镜像** 和 **Docker 容器** ，或许你在想它们的区别。通俗地说，Docker 镜像是一个描述容器应该如何表现的文件，而 Docker 容器是 Docker 镜像的运行（或停止）状态。希望你能够理解 Docker 的基础概念。更多细节，你可以 Docker 官方的[指导手册][指导手册]。

### Docker 依赖项

------

为了安装并配置 Docker ，你的系统必须满足下列最低要求：

1. 64 位 Linux 或 Windows 系统；
2. 如果使用 Linux ，内核版本必须不低于 3.10；
3. 能够使用`sudo` 权限的用户；
4. 在你的系统 BIOS 上启用了 VT（虚拟化技术）支持；
5. 你的系统应该联网；

在 Linux ，在终端上运行以下命令验证内核以及架构详细信息：

```bash
uname -a
```

输出示例：

```shell
Linux ubuntu 5.4.0-159-generic #176-Ubuntu SMP Mon Aug 14 12:04:20 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
```

正如上面你显示的那样，我的 Ubuntu 系统内核版本是 **5.4.0-159-generic** 并且系统架构是 **x86_64（x86_64 x86_64 x86_64 GNU/Linux）**。

{% note tip  %}

我使用的 Ubuntu 物理机，显示的是  **5.15.35-3-generic**。如果你使用的是Ubuntu容器，将会显示 **5.15.35-3-pve** 。

{% endnote %}

内核版本需要不低于最低要求的版本，并且是 64 位机器。这样不会有任何问题，我们能顺利安装并使用 Docker 。请注意你使用哪一个 Ubuntu 系统不重要。并且你使用 Ubuntu 桌面或服务器版本，亦或者其他 Ubuntu 变种如 Lubuntu 、Kubuntu 、Xubuntu ，都不重要。只要你的系统内核版本不低于 3.10 ，并且是 64 位系统，Docker 都会正常运行。

### 在 Ubuntu 22.04 LTS 中安装 Docker

------

#### 1、更新 Ubuntu

打开终端，依次运行下列命令：

```bash
sudo apt update
sudo apt upgrade -y
sudo apt full-upgrade -y
```

#### 2、添加 Docker 库

首先，安装必要的证书并允许 apt 包管理器使用以下命令通过 HTTPS 使用存储库：

```bash
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release
```

然后，运行下列命令添加 Docker 的官方 GPG 密钥：

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

添加 Docker 官方库：

```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

使用命令更新 Ubuntu 源列表：

```bash
sudo apt update
```

#### 3、安装 Docker

运行下列命令在 Ubuntu 22.04 LTS 服务器中安装最新 Docker CE：

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

安装完成后，运行如下命令验证 Docker 服务是否在运行：

```bash
systemctl status docker
```

如果在输出中看到 `Active: active (running)`，恭喜你，Docker 完成安装且服务已启动并运行！

如果没有运行，运行以下命令运行 Docker 服务：

```bash
sudo systemctl start docker
```

使 Docker 服务在每次重启时自动启动：

```bash
sudo systemctl enable docker
```

停止运行 Docker 服务需要依次执行以下命令：

```bash
sudo systemctl stop docker.socket
sudo systemctl stop docker
```

使用以下命令可以查看已安装的 Docker 版本：

```bash
sudo docker version
```

输出示例：

```
Client: Docker Engine - Community
 Version:           24.0.7
 API version:       1.43
 Go version:        go1.20.10
 Git commit:        afdd53b
 Built:             Thu Oct 26 09:07:41 2023
 OS/Arch:           linux/amd64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          24.0.7
  API version:      1.43 (minimum version 1.12)
  Go version:       go1.20.10
  Git commit:       311b9ff
  Built:            Thu Oct 26 09:07:41 2023
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.6.26
  GitCommit:        3dd1e886e55dd695541fdcd67420c2888645a495
 runc:
  Version:          1.1.10
  GitCommit:        v1.1.10-0-g18a0cb0
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```

### 在 Ubuntu 中安装 Docker Compose

------

**Docker Compose** 是一个可用于定义和运行多容器 Docker 应用程序的工具。使用 Compose，你可以使用 Compose 文件来配置应用程序的服务。然后，使用单个命令，你可以从配置中创建和启动所有服务。

下列任何一种方式都可以安装 Docker Compose 。

{% tabs First unique name %}
<!-- tab 方式一 -->
**使用二进制文件安装 Docker Compose**
1、首先，下载最新 Docker Compose (**P.S. 我安装时最新版本是v2.23.2，但是在写这篇文章时已经更新到了v2.23.3**)。

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

如果使用其他版本，只需要将上述命令中的 **v2.23.2** 替换为最新的版本号即可。务必记得数字前的 **v** 。

2、使用下列命令赋予二进制文件可执行权限：

```bash
sudo chmod +x /usr/local/bin/docker-compose
```

运行下列命令可以获取安装的 Docker Compose 版本：

```bash
docker-compose version
```

输出示例：

```bash
Docker Compose version v2.23.2
```
<!-- endtab -->

<!-- tab 方式二 -->
**使用 pip 安装 Docker Compose**

pip 是 Python 包管理器，用来安装使用 Python 编写的应用程序。

使用以下命令安装安装pip

```bash
sudo apt update
sudo apt install python3-pip -y
```

安装 pip 后，运行以下命令安装 Docker Compose。下列命令对于所有 Linux 发行版都是相同的！

```bash
pip install docker-compose
```

<!-- endtab -->
{% endtabs %}

### 修改 Docker 镜像默认存储位置

------

我们知道在操作系统当中，默认情况下 Docker 容器的存放位置在 `/var/lib/docker` 目录下面，可以通过下面命令查看具体位置。

```bash
# 默认存放位置
sudo docker info | grep "Docker Root Dir"
```

解决默认存储容量不足的情况，最直接且最有效的方法就是挂载新的分区到该目录。但是在原有系统空间不变的情况下，所以采用软链接的方式，修改镜像和容器的存放路径达到同样的目的。

1、首先停掉 Docker 服务（上面有方法）。

2、然后移动整个 `/var/lib/docker` 目录到空间较大的目的路径。我的是存储在数据盘 `/home/docker` 上了。

```shell
# 移动原有的内容
mv /var/lib/docker /home/docker
# 进行链接
ln -sf /home/docker /var/lib/docker
```

### 修改 Docker 配置

------

以下配置会增加一段自定义内网 IPv6 地址，开启容器的 IPv6 功能，以及限制日志文件大小，防止 Docker 日志塞满硬盘 (泪的教训)：

```bash
cat > /etc/docker/daemon.json << EOF
{
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "20m",
        "max-file": "3"
    },
    "ipv6": true,
    "fixed-cidr-v6": "fd00:dead:beef:c0::/80",
    "experimental":true,
    "ip6tables":true
}
EOF
```

然后重启 Docker 服务：

```bash
systemctl restart docker
```

### 结束

------

至此，恭喜你已经成功安装了 Docker 社区版和 Docker Compose ！




[指导手册]: https://www.docker.com/

