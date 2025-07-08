---
title: 搭建订阅转换网站的教程
date: 2022-10-05 23:46:50
password: subconvertor
abstract: 有东西被加密了, 请输入密码查看.
message: 您好, 这里需要密码.
wrong_pass_message: 抱歉, 这个密码看着不太对, 请再试试.
wrong_hash_message: 抱歉, 这个文章不能被校验, 不过您还是能看看解密后的内容.
tags: 
  - Ubuntu
  - sub-web 
  - SubConverter 
  - 订阅转换
---

## 本文是搭建Sub-Web的教程！自行搭建Clash订阅转换平台，自建Sub-Web前端和SubConverter后端！

###  一、准备工作

#### 1. 准备服务器

可以使用国内的阿里云等的服务器。使用的系统是 **Ubuntu20.04** 。

#### 2. 准备前端项目和后端项目

{% btn regular::前端项目地址::https://github.com/CareyWang/sub-web::fa-brands fa-github %}
{% btn regular::后端项目地址::https://github.com/tindy2013/subconverter::fa-brands fa-github %}

#### 3. 解析两个域名

**前端** 使用 `subc.xxx.xxx` 进行解析。

**后端** 使用 `subs.xxx.xxx` 进行解析。

### 二、安装BT面板并设置网站

如何安装宝塔面板请自行百度搜索。

新建两个站点 `sub.xxx.xxx` 和 `suc.xxx.xxx`，并为这两个站点添加ssl证书且开启强制HTTPS。

### 三、搭建Sub-Web前端

#### 1. 更新系统并安装 Node 与 Yarn

```bash
sudo apt update -y
sudo apt install -y curl wget sudo nodejs npm git
npm install -g yarn
```

{% notel info 命令执行完毕以后，记得验证是否安装成功 %}

运行下面的代码查询 Node 与 Yarn 是否安装成功，若是成功会返回版本号。

```bash
node -v
yarn --version
```

{% endnotel %}

#### 2. 下载并安装 sub-web

拉取 sub-web 程序，并进入 sub-web 文件夹。

```bash
git clone https://github.com/CareyWang/sub-web.git
cd sub-web
```

在项目目录中安装构建依赖项，构建的过程稍微有点长。

```bash
yarn install
```

使用 webpack 运行 Web 客户端以进行本地开发。

```bash
yarn serve
```

到目前为止，浏览器访问 [http://服务器ip:8080/](http://服务器ip:8080/) 应该可以进行前端 sub-web 的预览了，记得放行端口。

#### 3. 修改默认后端地址

找到 `sub-web/src/views/Subconverter.vue` 文件；

找到 `backendOptions:`，替换后面的 `http://127.0.0.1:25500/sub?` 为 `https://suc.xxx.xxx/sub?`。

如果要将自己的域名设为默认地址，找到 `defaultBackend`，将 `=` 后的内容替换为上面的地址即可。

{% note tip  %}

**tips: 域名为你刚才准备的后端域名，是 https 而非 http！**

{% endnote %}

#### 4. 更换远程规则

因为这个版本更新以后，规则方面很少，经常用到的一些经典的 ACL4SSR 的规则并没有集成，大家可以看看，若是有，就不需要这样操作。找到 `sub-web/src/views/Subconverter.vue` 文件，找到 `remoteConfig: [`，敲下回车，插入下面内容。

{% folding blue::太长了，影响阅读，折叠起来了。点击可查看全部！ %} 

```json
{
            label: "ACL4SSR",
            options: [
              {
                label: "ACL4SSR_Online 默认版 分组比较全 (与Github同步)",
                value:
                  "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online.ini"
              },
              {
                label: "ACL4SSR_Online_AdblockPlus 更多去广告 (与Github同步)",
                value:
                  "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_AdblockPlus.ini"
              },
              {
                label: "ACL4SSR_Online_NoAuto 无自动测速 (与Github同步)",
                value:
                  "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_NoAuto.ini"
              },
              {
                label: "ACL4SSR_Online_NoReject 无广告拦截规则 (与Github同步)",
                value:
                  "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_NoReject.ini"
              },
              {
                label: "ACL4SSR_Online_Mini 精简版 (与Github同步)",
                value:
                  "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Mini.ini"
              },
              {
                label: "ACL4SSR_Online_Mini_AdblockPlus.ini 精简版 更多去广告 (与Github同步)",
                value:
                  "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Mini_AdblockPlus.ini"
              },
              {
                label: "ACL4SSR_Online_Mini_NoAuto.ini 精简版 不带自动测速 (与Github同步)",
                value:
                  "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Mini_NoAuto.ini"
              },
              {
                label: "ACL4SSR_Online_Mini_Fallback.ini 精简版 带故障转移 (与Github同步)",
                value:
                  "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Mini_Fallback.ini"
              },
              {
                label: "ACL4SSR_Online_Mini_MultiMode.ini 精简版 自动测速、故障转移、负载均衡 (与Github同步)",
                value:
                  "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Mini_MultiMode.ini"
              },
              {
                label: "ACL4SSR_Online_Full 全分组 重度用户使用 (与Github同步)",
                value:
                  "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Full.ini"
              },
              {
                label: "ACL4SSR_Online_Full_NoAuto.ini 全分组 无自动测速 重度用户使用 (与Github同步)",
                value:
                  "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Full_NoAuto.ini"
              },
              {
                label: "ACL4SSR_Online_Full_AdblockPlus 全分组 重度用户使用 更多去广告 (与Github同步)",
                value:
                  "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Full_AdblockPlus.ini"
              },
              {
                label: "ACL4SSR_Online_Full_Netflix 全分组 重度用户使用 奈飞全量 (与Github同步)",
                value:
                  "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Full_Netflix.ini"
              },
              {
                label: "ACL4SSR 本地 默认版 分组比较全",
                value: "config/ACL4SSR.ini"
              },
              {
                label: "ACL4SSR_Mini 本地 精简版",
                value: "config/ACL4SSR_Mini.ini"
              },
              {
                label: "ACL4SSR_Mini_NoAuto.ini 本地 精简版+无自动测速",
                value: "config/ACL4SSR_Mini_NoAuto.ini"
              },
              {
                label: "ACL4SSR_Mini_Fallback.ini 本地 精简版+fallback",
                value: "config/ACL4SSR_Mini_Fallback.ini"
              },
              {
                label: "ACL4SSR_BackCN 本地 回国",
                value: "config/ACL4SSR_BackCN.ini"
              },
              {
                label: "ACL4SSR_NoApple 本地 无苹果分流",
                value: "config/ACL4SSR_NoApple.ini"
              },
              {
                label: "ACL4SSR_NoAuto 本地 无自动测速 ",
                value: "config/ACL4SSR_NoAuto.ini"
              },
              {
                label: "ACL4SSR_NoAuto_NoApple 本地 无自动测速&无苹果分流",
                value: "config/ACL4SSR_NoAuto_NoApple.ini"
              },
              {
                label: "ACL4SSR_NoMicrosoft 本地 无微软分流",
                value: "config/ACL4SSR_NoMicrosoft.ini"
              },
              {
                label: "ACL4SSR_WithGFW 本地 GFW列表",
                value: "config/ACL4SSR_WithGFW.ini"
              }
            ]
          },
```

{% endfolding %}

##### 5. 配置完毕刷新前端网页

配置完毕以后，程序会自动更新，再次刷新前端网页，会出现刚才添加的相关规则。

至此，我们的前端搭建完毕，我们现在需要打包，生成一个发布目录。

首先停止调试程序，CTRL+C ，退出当前调试，然后执行下面的命令进行打包：

```bash
yarn build
```

执行以下打包命令，在 `sub-web` 目录下面会生成一个 `dist` 目录，这个目录即为网页的发布目录。

#### 6. 发布订阅转换网站

将 `sub-web/dist` 下的文件拷贝至 `subc.xxx.xxx` 站点的目录下。

### 四、SubConverter后台搭建

#### 1. 下载并解压后端程序

```bash
cd /root
wget https://github.com/tindy2013/subconverter/releases/download/v0.6.3/subconverter_linux64.tar.gz
tar -zxvf subconverter_linux64.tar.gz
```

完成以后，在 `/root` 文件夹下会多出一个 `subconverter` 的文件夹，这个就是我们的后端程序。

#### 2. 修改配置文件参数

现在需要修改后端配置文件中的一些参数。

找到文件 `/root/subconverter/pref.ini` ，找到如下参数进行修改：

```bash
api_access_token=123123dfsdsdfsdfsdf            #随意设置自己知道就行
managed_config_prefix=https://subs.xxx.xxx  	#设置成我们刚刚解析的后端域名
listen=127.0.0.1                                #这里改成 127.0.0.1 进行反代
```

#### 3. 创建服务进程并启动

进入目录 `/etc/systemd/system`，创建一个名为 `subs.service` 的文件；

打开文件，贴入以下内容，保存。

```shell
[Unit]
Description=A API For Subscription Convert
After=network.target
 
[Service]
Type=simple
ExecStart=/root/subconverter/subconverter
WorkingDirectory=/root/subconverter
Restart=always
RestartSec=10
 
[Install]
WantedBy=multi-user.target
```

检查运行状态以及设置开机自启

```bash
systemctl daemon-reload
systemctl start subs
systemctl enable subs
systemctl status subs
```

至此，后端也就搭建完毕了，我们现在可以在浏览器里面访问我们的后端了，正常的话会显示 `subconverter v0.6.3 backend`。





