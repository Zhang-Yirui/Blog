---
title: Win10系统怎么删除网络和修改网络名称
date: 2025-06-03 08:44:32
tags:
  - win10
  - network
---

**Win10修改网络名称或删除网络方法：**

1.  按`Win+R`打开运行，输入`regedit`回车打开注册表编辑器；
2.  展开这个位置：`HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles\`

​	在该项下你会看到一个或多个子项，每一项就代表一个网络。选中其中一项后，在右侧会出现一系列注册表键值。其中的`ProfileName`即代表网络名称，将其修改为你希望看到的名字即可。在删除不需要的网络时，同样依据`ProfileName`键值来确定。
