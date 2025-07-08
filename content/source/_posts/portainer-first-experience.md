---
title: Docker 之 Portainer 初体验
date: 2022-11-26 10:14:38
tags: 
  - Docker	
  - portainer
---

# 本文是在 Docker 中安装 Portainer 的教程。

最近突然想尝试一下 Docker 现有的 GUI 界面 , 找了一下发现 Portainer 的 UI 比较出众, 于是打算体验一下。

## 0x01：安装 Docker 和 Docker Compose

- 请参考[本站教程]()。

## 0x02：安装 Portainer

Portainer 有现成的 Docker 镜像, 所以就直接使用官方提供的镜像。这玩意儿关乎着所有 Docker 服务器的安危, 所以 SSL 是肯定要上的. 将证书存放在某个目录下咱就可以开始安装了(请将以下代码中的 `${DIR}` 和 `${PORT}` 更换成自己需要的值):



```bash
docker run -d -p ${PORT}:9000 --name portainer --restart always -v ${DIR}:/certs -v portainer_data:/data portainer/portainer --ssl --sslcert /certs/cert.pem --sslkey /certs/key.pem portainer/portainer-ce:linux-amd64
```

等命令执行完后打开 `https://IP:${PORT}` 就应该可以看到下面的界面了

![初始化界面](https://www.xiaolin.in/dist/ac/9a78fade479a0993.avif)

在这个界面设置好登录信息后我们就可以进入下一个环节了。

## 0x03：开启安全的 Docker Remote API

开启 Docker Remote API 的方法非常简单, 只要在 `/etc/default/docker` 中添加如下代码即可:

```ini
OPTIONS='-H=tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock'
```

但是这样就相当于直接把你的服务器毫无保留地暴露出去了, 所以我们需要一些更安全的开启方式, 我们开始吧!

## 0x04：生成服务器证书及建立 API 服务

我们将所有的证书都放置到 `/etc/docker/`目录下以便于管理

咱首先生成 CA 的公钥以及私钥:

```bash
openssl genrsa -aes256 -out ca-key.pem 4096 # 生成 CA 私钥
openssl req -new -x509 -days 3650 -key ca-key.pem -sha256 -out ca.pem # 生成 CA 公钥
```

接下来生成服务端证书、签名请求和密钥:

```bash
openssl genrsa -out server-key.pem 4096 # 生成证书私钥
openssl req -sha256 -new -key server-key.pem -out server.csr # 创建证书签名请求
# 输入一系列相关信息，可省略部分直接输入.
# 其中 Common Name 需要改成你连接服务器的地址, 比如 1.1.1.1 或 example.com
openssl x509 -req -days 3650 -sha256 -in server.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem # 生成服务器证书
```

到现在咱的服务器端证书就已经生成好了, 可以建立经过加密的 Docker Remote API 服务了

在 `/etc/default/docker` 添加如下代码:

```ini
OPTIONS='-H=tcp://0.0.0.0:2376 -H=unix:///var/run/docker.sock --tlsverify --tlscacert=/etc/docker/ca.pem --tlscert=/etc/docker/server-cert.pem --tlskey=/etc/docker/server-key.pem'
```

理论来说以上代码是可以正常运行的, 但是在小霖的服务器上貌似不起作用, 所以咱直接修改启动 Docker 的脚本参数: 打开 `/lib/systemd/system/docker.service` , 在 ExecStart 后添加以下内容:

```bash
-H=tcp://0.0.0.0:2376 --tlsverify --tlscacert=/etc/docker/ca.pem --tlscert=/etc/docker/server-cert.pem --tlskey=/etc/docker/server-key.pem
```

之后输入 `sudo systemctl daemon-reload` 重新载入 systemctl 配置文件后输入 `sudo systemctl restart docker` 重启 Docker 服务即可

## 0x05：为客户端生成证书

目前为止 API 服务已经被刚刚咱创建的证书所加密了, 接下来就要生成客户端证书以允许客户端连接上 API 服务, 代码如下

```bash
openssl genrsa -out key.pem 4096 # 生成证书私钥
openssl req -new -key key.pem -out client.csr # 创建证书签名请求
# 输入一系列相关信息, 例外同上
openssl x509 -req -days 3650 -sha256 -in client.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out cert.pem # 生成客户端证书
```

上面的代码运行完成后, 客户端的证书就生成完毕了, 我们需要将 `ca.pem` `cert.pem` 及 `key.pem` 复制到本地以便稍后在 Portainer 中添加节点

## 0x06：在 Portainer 中添加节点

完成了上面的步骤之后就可以在 Portainer 添加刚刚操作的 Docker 服务器了

在填写完账号信息后我们应该可以看到下面的界面:

![添加节点](https://www.xiaolin.in/dist/ac/9a78fade479a0993.avif)

在这个界面我们就可以添加需要的节点了

其中 `Name` 是名字, `Endpoint URL` 是服务器 IP 加上端口号, 在这里也就是上面设置的 `2376`

除了填写这些我们还要上传刚刚复制回来的三个文件, `TLS CA certificate` 对应的是 `ca.pem`, `TLS certificate` 对应的是 `cert.pem`, `TLS key` 对应的是 `key.pem`

填写完这些信息并连接成功后咱就可以进入到主页了, 如下图:

![首页](https://www.xiaolin.in/dist/2f/cbbcf95c2b2915b0.avif)

## 0x07：结束

如果步骤没有缺漏的话到这里 Portainer 就应该已经安装完成了, 体验了一下感觉还是很好用的, 不过有一些功能还是没有的, 比如增加端口或者挂载卷之类的, 希望以后会持续更新吧~
