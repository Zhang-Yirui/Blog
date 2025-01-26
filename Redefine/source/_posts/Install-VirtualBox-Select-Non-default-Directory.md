---
title: 安装 VirtualBox-7.1.4 选择非默认目录踩坑
date: 2024-11-09 14:11:26
tags: 
  - VirtualBox
---

安装 **`VirtualBox-7.1.4`** 选择非默认目录或非C盘目录时，出现 `Invalid installation directory` 的提示。

![](https://files.bd3qif.com/2025/01/27/20250127021248_066645c15df7a688cce9f217ba8c0774_20241114224712_066645c15df7a688cce9f217ba8c0774_6730a283078cb.png)


解决方法如下：

运行下面代码，注意需要将 `<安装目录>` 自己的路径

```cmd
icacls <安装目录> /reset /t /c
icacls <安装目录> /inheritance:d /t /c
icacls <安装目录> /grant *S-1-5-32-545:(OI)(CI)(RX)
icacls <安装目录> /deny *S-1-5-32-545:(DE,WD,AD,WEA,WA)
icacls <安装目录> /grant *S-1-5-11:(OI)(CI)(RX)
icacls <安装目录> /deny *S-1-5-11:(DE,WD,AD,WEA,WA)
```



例如：

如果想要的安装的目录为 `D:\VirtualBox\`，用管理员身份打开CMD，运行下面的命令

```cmd
icacls D:\VirtualBox\ /reset /t /c
icacls D:\VirtualBox\ /inheritance:d /t /c
icacls D:\VirtualBox\ /grant *S-1-5-32-545:(OI)(CI)(RX)
icacls D:\VirtualBox\ /deny *S-1-5-32-545:(DE,WD,AD,WEA,WA)
icacls D:\VirtualBox\ /grant *S-1-5-11:(OI)(CI)(RX)
icacls D:\VirtualBox\ /deny *S-1-5-11:(DE,WD,AD,WEA,WA)
```

如果安装目录为 `D:\Oracle\VirtualBox\`，则需要在每一层目录运行上面的代码

```cmd
icacls D:\Oracle\ /reset /t /c
icacls D:\Oracle\ /inheritance:d /t /c
icacls D:\Oracle\ /grant *S-1-5-32-545:(OI)(CI)(RX)
icacls D:\Oracle\ /deny *S-1-5-32-545:(DE,WD,AD,WEA,WA)
icacls D:\Oracle\ /grant *S-1-5-11:(OI)(CI)(RX)
icacls D:\Oracle\ /deny *S-1-5-11:(DE,WD,AD,WEA,WA)

icacls D:\Oracle\VirtualBox\ /reset /t /c
icacls D:\Oracle\VirtualBox\ /inheritance:d /t /c
icacls D:\Oracle\VirtualBox\ /grant *S-1-5-32-545:(OI)(CI)(RX)
icacls D:\Oracle\VirtualBox\ /deny *S-1-5-32-545:(DE,WD,AD,WEA,WA)
icacls D:\Oracle\VirtualBox\ /grant *S-1-5-11:(OI)(CI)(RX)
icacls D:\Oracle\VirtualBox\ /deny *S-1-5-11:(DE,WD,AD,WEA,WA)
```



参考连接：[https://www.virtualbox.org/manual/ch02.html#install-win-installdir-req](https://www.virtualbox.org/manual/ch02.html#install-win-installdir-req)
