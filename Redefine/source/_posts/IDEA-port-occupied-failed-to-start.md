---
title: IDEA 端口占用，启动失败，提示 Web server failed to start. Port 9090 was already in use.
date: 2025-04-28 23:14:56
tags: 
  - IDEA
  - Port occupied
  - 端口占用
---

# 1、**问题描述：**

使用IDEA开发Spring Boot项目，启动提示端口被占用，导致启动失败！（上午就用的这个端口，可以正常启动，下午就启动失败了）

```cmd
***************************
APPLICATION FAILED TO START
***************************

Description:

Web server failed to start. Port 8800 was already in use.

Action:

Identify and stop the process that's listening on port 8800 or configure this application to listen on another port.
```

# 2、**解决思路：**

## 方法一：更换端口

修改配置文件`application.yml`文件中的端口配置：

```yaml
server:
  port: 19090
```

修改完后可以正常启动。

## 方法二：杀掉占用端口的进程

使用`win+r`打开**运行**，输入`cmd`打开命令提示符，运行命令：

```cmd
netstat -ano | findstr "9090"
```

==**但是发现并没有进程占用！！！？？？**==

如果查找到了占用端口，可以通过PID暴力地直接杀了这个进程（如果你非用这个端口不可的话）！

```cmd
:: 查找占用端口进程的 PID
netstat -ano | findstr "19090"
  TCP    0.0.0.0:19090          0.0.0.0:0              LISTENING       4180
  TCP    127.0.0.1:11459        127.0.0.1:19090        ESTABLISHED     4180
  TCP    127.0.0.1:19090        127.0.0.1:11459        ESTABLISHED     4180
  TCP    192.168.1.16:11464     192.168.1.16:19090     ESTABLISHED     4180
  TCP    192.168.1.16:11468     192.168.1.16:19090     ESTABLISHED     4180
  TCP    192.168.1.16:19090     192.168.1.16:11464     ESTABLISHED     4180
  TCP    192.168.1.16:19090     192.168.1.16:11468     ESTABLISHED     4180
  TCP    [::]:19090             [::]:0                 LISTENING       4180
  
:: 杀掉该进程 taskkill /PID <PID> /F
taskkill /PID 4180 /F
```

## 方法三：检查并释放 Windows 保留端口

**如果 `netstat` 查不到占用，但 Spring Boot 仍报错，可能是==Windows 保留端口==导致，尝试下面的方法**：

### 1、检查 Windows 保留端口

在`cmd`中输入下面命令：

```cmd
netsh interface ipv4 show excludedportrange protocol=tcp

协议 tcp 端口排除范围

开始端口    结束端口
----------    --------
      1058        1157
      1158        1257
      1258        1357
      1458        1557
      1558        1657
      1658        1757
      2166        2265
      2266        2365
      2566        2665
      8562        8661
      8662        8761
      8762        8861
      8949        9048
      9049        9148
      9192        9291
     10652       10751
     10752       10851
     10852       10951
     12853       12952
     12953       13052
     13053       13152
     50000       50059     *

* - 管理的端口排除。
```

可以看到`9090`端口在**端口排除范围**中： 9049        9148。

### 2、释放端口（**需谨慎**）

在`cmd`中输入下面命令（**需要管理员权限**）：

```cmd
netsh int ipv4 delete excludedportrange protocol=tcp startport=9049 number=100
```

