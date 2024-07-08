---
title: Redefine 主题中使用 LaTeX 书写数学公式避坑指南
date: 2023-10-12 21:32:01
mathjax: true
tags: 
  - mathjax
  - 数学公式
---

## 操作

如果想要完整显示所有 $\LaTeX$ 公式，首先需要安装插件 `hexo-filter-mathjax`。

```bash
npm install hexo-filter-mathjax
```

然后在 **Hexo** 配置文件 `_config.yml` 最底下增加如下配置。

```yaml
mathjax:
  tags: none               # or 'ams' or 'all'
  single_dollars: true     # enable single dollar signs as in-line math delimiters
  cjk_width: 0.9           # relative CJK char width
  normal_width: 0.6        # relative normal (monospace) width
  append_css: true         # add CSS to every page
  every_page: false        # if true, every page will be rendered by mathjax regardless 
                           #   the `mathjax` setting in Front-matter of each article
```

接着必须把 **Hexo** 原先内置的 Markdown 渲染工具 `hexo-renderer-marked` 卸载，其次安装 `hexo-renderer-pandoc` 。

```bash
npm uninstall hexo-renderer-marked
npm install hexo-renderer-pandoc
```

在文章中使用时，在文章页添加 `mathjax: true` 属性，就可以在该页面中写公式了。

至此，你可以尝试启动 **Hexo** 本地服务器看看效果，如果执行到 `hexo g` 时报错，那么你需要额外安装一个开源项目 `Pandoc`，仓库地址为 [Pandoc ](https://github.com/jgm/pandoc/releases)，最后启动 **Hexo** 服务器，可以看到所有 $\LaTeX$ 数学公式都显示出来啦。

## 测试

```tex
下面这个方程是薛定谔方程（Schrodinger Equation）的一部分，描述了量子力学中的波函数($\psi$)随时间演化的情况。

$$
i\hbar\frac{\partial}{\partial t}\psi=-\frac{\hbar^2}{2m}\nabla^2\psi+V\psi
$$

这里的符号含义如下：

- $i$ 是虚数单位；
- $\hbar$ 是约化普朗克常数；
- $\frac{\partial}{\partial t}$ 表示对时间的偏导数；
- $\psi$ 是波函数；
- $\frac{\hbar^2}{2m}\nabla^2\psi$ 表示动能项，描述了波函数的动能；
- $V$ 表示势能，描述了波函数在势场中的势能。

这个方程描述了量子力学中的一个重要现象，即波函数随着时间的变化和在给定势场下的行为。
```

如果在你的页面中可以向下面一样显示，就说明你成功避开了这个个坑！！！

------

下面这个方程是薛定谔方程（Schrodinger Equation）的一部分，描述了量子力学中的波函数($\psi$)随时间演化的情况。

$$
i\hbar\frac{\partial}{\partial t}\psi=-\frac{\hbar^2}{2m}\nabla^2\psi+V\psi
$$

这里的符号含义如下：

- $i$ 是虚数单位；
- $\hbar$ 是约化普朗克常数；
- $\frac{\partial}{\partial t}$ 表示对时间的偏导数；
- $\psi$ 是波函数；
- $\frac{\hbar^2}{2m}\nabla^2\psi$ 表示动能项，描述了波函数的动能；
- $V$ 表示势能，描述了波函数在势场中的势能。

这个方程描述了量子力学中的一个重要现象，即波函数随着时间的变化和在给定势场下的行为。

