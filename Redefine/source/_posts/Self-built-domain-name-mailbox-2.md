---
title: Linux搭建邮件服务器的教程
date: 2024-11-14 14:45:06
tags: 
---

# Poste.io邮箱服务器搭建教程

## 前言

### 什么是域名邮箱？

域名邮箱是指使用自己的域名作为邮箱地址的电子邮件服务。这种形式的邮箱（例如，[admin@zeruns.tech](mailto:admin@zeruns.tech)）不仅增强了个人或企业的品牌识别度，而且传递出更为专业和正式的形象。相比于常见的免费邮箱服务，域名邮箱提供了更多定制化选项和安全特性，非常适合商业环境。

### Poste.io简介

Poste.io 是一个开源的电子邮件服务器解决方案，它提供了一个简单而强大的邮件服务器环境，适用于个人用户、小型企业或组织。Poste.io 的目标是提供易于安装、配置和管理的电子邮件解决方案，并且尽可能减少复杂性。
以下是 Poste.io 的一些主要特点和功能：

- 易于安装和配置：Poste.io 提供了一个简化的安装和配置过程，使用户能够快速设置和启动邮件服务器。
- Web 用户界面：它提供了一个直观的 Web 用户界面，使用户能够轻松管理邮件服务器、创建和管理邮箱账户、设置域名等。
- 邮箱功能：Poste.io 支持标准的电子邮件功能，包括收发邮件、邮件夹管理、邮件搜索、自动转发、自动回复等。
- 安全性：Poste.io 使用各种安全措施来保护你的电子邮件和服务器，包括加密通信、防垃圾邮件过滤、反病毒扫描等。
- 邮件过滤和规则：你可以设置邮件过滤器和规则，根据自定义条件自动处理邮件，例如将特定类型的邮件自动分类到特定文件夹。
- 多域名支持：Poste.io 允许你管理多个域名和相关的邮箱账户，方便你为不同组织或团队创建和管理独立的邮箱。

## 准备

### 注册域名

可以去[腾讯云](https://cloud.tencent.com/)、[阿里云](https://www.aliyun.com/)、[Cloudflare](https://www.cloudflare.com/)和[NameSilo](https://www.namesilo.com/)等平台注册域名。

{% note tip  %}

在**腾讯云**、**阿里云**等国内平台注册的域名需要完成域名备案。

{% endnote %}

### 准备服务器

可以在[腾讯云](https://cloud.tencent.com/)、[阿里云](https://www.aliyun.com/)等国内平台购买服务器。购买的中国大陆的服务器，需要完成域名和服务器的备案才能使用；不想备案可以购买中国香港或国外地区的服务器。

{% note primary  %}

**重要事项：要部署自己的邮箱服务器，请先确认服务器的25端口是开放的，入站出站都是OK的才行，目前国内部分服务器厂商或机房是封禁25端口的，可以提工单或找客服询问是否开放25端口或能否申请开放25端口！**

{% endnote %}

{% note info  %}

这个邮箱服务器除了要用25端口外还需要80和443这些网页服务的端口，所以不能安装网页服务器软件，如果要同时存在就要docker设置端口映射将邮箱服务器的80和443端口映射到其他端口，然后用反向代理，设置比较复杂，所以不会的还是邮箱服务器单独一个服务器吧。

{% endnote %}

## 连接服务器并验证是否开放25端口

在ssh连接工具中输入用户名和密码登入服务器，在命令行中输入并执行：`telnet smtp.qq.com 25` 。

若输出是以下内容：

```cmd
Trying 183.47.101.192...
Connected to smtp.qq.com.
Escape character is '^]'.
220 newxmesmtplogicsvrszb16-1.qq.com XMail Esmtp QQ Mail Server.
```

则证明该服务器25端口正常的，可以进行部署邮局。接着输入`quit`并回车退出。

![](https://imghub.bd3qif.com/2024/11/14/20241114224752_9385013fcbeb14160c8c0dad5e914640_67359fef9de34.jpg.jpeg)

若输出 `Trying 183.47.101.192... telnet: connect to address 183.47.101.192: Connection timed out` 之类的信息，则可以放弃部署了。

{% note warning  %}

**这个邮箱服务器需要的端口有：25、80、443、110、143、465、587、993、995**

大厂的服务器要记得都去服务器控制台的安全组/防火墙那里开放这些端口！

{% endnote %}

## 解析域名

| 主机记录 | 记录类型 |     记录值     |
| :------: | :------: | :------------: |
|   mail   |    A     | 服务器的IP地址 |
|   smtp   |  CNAME   |   自己的域名   |
|   pop    |  CNAME   |   自己的域名   |
|   imap   |  CNAME   |   自己的域名   |
|    @     |    MX    |   自己的域名   |
|    @     |   TXT    | v=spf1 mx ~all |

## **安装Docker**

**请参考[本站教程](http://localhost:4000/2022/11/10/Self-built-domain-name-mailbox/)。**

## 安装和配置Poste.io

本次部署poste.io，我们采用docker的方式。

在SSH终端里执行下面的命令：

命令中的`/home/mail`是邮箱系统的配置文件和数据存放目录路径，可以自行修改。

`-h` 后面的域名`mail.example.com`改成你自己要部署的域名

```cmd
docker run -d \
   --net=host \
   -e TZ=Asia/Shanghai \
   -v /home/mail:/data \
   --name "mailserver" \
   -h "mail.example.com" \
   -t analogic/poste.io:latest
```

![](https://imghub.bd3qif.com/2024/11/14/20241114224756_36a0687d7f8a14e9249d2dc0728c26a4_6735a89bca5b2.jpg.jpeg)

如果需要与宝塔和其他网站服务共存，docker命令可以参考下面的，将80和443端口映射到其他端口，然后用反向代理

```cmd
docker run -d \
    -p 25:25 \
    -p 81:80 \
    -p 433:443 \
    -p 110:110 \
    -p 143:143 \
    -p 465:465 \
    -p 587:587 \
    -p 993:993 \
    -p 995:995 \
    -e TZ=Asia/Shanghai \
    -v /www/wwwroot/mail:/data \
    --name "mailserver" \
    -h "mail.example.com" \
    -t hub.vpszj.top/analogic/poste.io
```

容器启动后，在浏览器地址栏输入 `https://服务器IP/admin/install/server` 或者是 `https://你的域名/admin/install/server` 进入配置页面。

![](https://imghub.bd3qif.com/2024/11/14/20241114224806_758108c0e014e3ac4f34cb6ba5ccd849_6735ae91b2069.jpg.jpeg)

在这个页面，我们输入你邮箱的域名，管理员邮箱地址，以及生成密码（也可以自己手动输入）后提交即可。切记记录一下邮箱的域名和管理员账户。

进入后台，找到 **`System settings → TLS certificate`**，点击**` issue free letsencrypt.org certificate `**进行申请SSL证书（申请SSL证书后浏览器地址栏会变小绿锁，不会显示不安全了）。

![](https://image.zhangyirui.cn/i/2024/11/14/6735afab75ab4.jpg)

![](https://imghub.bd3qif.com/2024/11/14/20241114224816_cf1f88ea70e0b4b5f366a015e098da24_6735b025c9ff0.jpg.jpeg)

申请完后，前台再次访问邮箱域名，会自动跳转到邮箱的登录页面。输入之前设置管理员账号和密码并登陆。

然后我们在**Virtual domains**点击域名，申请 `DKIM`

![](https://image.zhangyirui.cn/i/2024/11/14/6735b12c748e3.jpg)

![](https://imghub.bd3qif.com/2024/11/14/20241114224822_f866071160427708b3a89e8bd1cd6d83_6735b17c59cba.jpg.jpeg)

申请完成后，需要按照页面提示更新DNS记录，新建一个TXT记录即可。

![](https://imghub.bd3qif.com/2024/11/14/20241114224836_c38a18d00f5a6d5b85fba26880462a9f_6735b1de429bc.jpg.jpeg)

接下来我们测试发信。我们新建邮件，随便编辑一些内容我发给我的QQ邮箱，可以看到邮件该有的功能页面都有，挺齐全了。

QQ邮箱视角：收到了(如果你没找到，不妨试着看看垃圾箱~)

给这个邮局新增账号也很简单，只需要去后台的**Email accounts**这里，Create a new email即可。

测试QQ邮箱发邮件到我们搭建的域名邮箱，测试成功。

> 教程到此结束
