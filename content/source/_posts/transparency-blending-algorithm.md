---
title: RGBA alpha 透明度混合算法实现和测试
date: 2023-12-05 02:03:27
tags: 透明度混合算法
---

## 1、算法叙述

算法参考自：[【RGBA alpha 透明度混合算法】](https://blog.csdn.net/xhhjin/article/details/6445460) 。

### 1.1、透明度混合算法1

`R1`、`G1`、`B1`、`Alpha1` 为前景颜色值，`R2`、`G2`、`B2`、`Alpha2`  为背景颜色值，则：

```
Alpha = 1 - (1 - Alpha1) * ( 1 - Alpha2)
R = (R1 * Alpha1 + R2 * Alpha2 * (1-Alpha1))/Alpha
G = (G1 * Alpha1 + G2 * Alpha2 * (1-Alpha1))/Alpha
B = (B1 * Alpha1 + B2 * Alpha2 * (1-Alpha1))/Alpha
```

这里的`Alpha`取值范围是`[0,1]`，需要使用到浮点计算（实数计算）。对于我们常见的8位图像，我们可以将其值域改为`[0,255]`进行计算，具体的见下面测试代码。

### 1.2、AlphaBlend算法介绍

混合算法目前在常用到的算法是 **`AlphaBlend`**。
计算公式如下:假设一幅图像是`A`，另一幅透明的图像是`B`，那么**透过B去看A**，看上去的图像`C`就是`B`和`A`的混合图像，
设B图像的透明度为`alpha`(取值为`0-1`，`1`为完全透明，`0`为完全不透明).
`Alpha` 混合公式如下：

```
R(C)=(1-alpha)*R(B) + alpha*R(A)
G(C)=(1-alpha)*G(B) + alpha*G(A)
B(C)=(1-alpha)*B(B) + alpha*B(A)
```

`R(x)`、`G(x)`、`B(x)`分别指颜色`x`的`RGB`分量原色值。从上面的公式可以知道，**`Alpha`其实是一个决定混合透明度的数值**。

这里只对`B`图的`Alpha`进行了处理，但`A`图本身如果也有透明通道的，也需要进行一样的处理，即

```
A(C)=(1-alpha)*A(B) + alpha*A(A)
```

### 1.3、简易Alpha混合算法

首先，要能取得上层与下层颜色的 RGB三基色，然后用r,g,b 为最后取得的颜色值；**r1、g1、b1**是上层的颜色值；**r2、g2、b2**是下层颜色值，若Alpha=上层透明度，则：

- 当`Alpha=50%`时

  ```
  r = r1/2 + r2/2;
  g = g1/2 + g2/2;
  b = b1/2 + b2/2;
  ```

- 当`Alpha<50%`时

  ```
  r = r1 - r1/Alpha + r2/Alpha;
  g = g1 - g1/Alpha + g2/Alpha;
  b = b1 - b1/Alpha + b2/Alpha;
  ```

- 当`Alpha>50%`时

  ```
  r = r1/Alpha + r2 - r2/Alpha;
  g = g1/Alpha + g2 - g2/Alpha;
  b = b1/Alpha + b2 - b2/Alpha;
  ```

这个算法比较简单，我也没有去做实现。简单来说这里就是看透明度高是否超过50%，来决定是上下层图像谁占主导地位。

## 2、算法实现代码和测试

实现其实是很简单的，只是注意下面没有实数的计算，都是使用的整数计算，要注意移位与抹零的操作别出错。

下面的`rgba1`表示前景图（我的代码里是水印图）的一个像素值，是RGBA8888格式的。`rgba2`表示背景图的一个像素值。`a1`表示`rgba1`中的`Alpha`分量值，`a2`表示`rgba2`中的`Alpha`分量值。

### 2.1、透明度混合算法1实现代码

```c
// 如果alpha的值域是[0,1]，这里相当于将其拉伸为[0,255]
// 所以相当于是 Alpha = 1 - (1 - Alpha1) * ( 1 - Alpha2)乘以了两次255
// 当a1和a2都接近于0的时候，会导致计算得到的A值不为0，导致叠加不正常
uint32_t A = (0xffff - (0xff - a1) * (0xff - a2));
// 下面左边部分少左移8位，相当于乘以了255
uint32_t R = (((rgba1 << 8 & 0xff00U) * a1 + (rgba2 >> 0  & 0xffU) * a2 *(0xff - a1)) / A) & 0xffU;
uint32_t G = (((rgba1 >> 0 & 0xff00U) * a1 + (rgba2 >> 8  & 0xffU) * a2 *(0xff - a1)) / A) & 0xffU;
uint32_t B = (((rgba1 >> 8 & 0xff00U) * a1 + (rgba2 >> 16 & 0xffU) * a2 *(0xff - a1)) / A) & 0xffU;
```

### 2.1、AlphaBlend算法实现代码

```c
uint32_t A = a1;
uint32_t R = (((rgba1 >> 0  & 0xffU) * A + (rgba2 >> 0  & 0xffU) *(0xff - A)) >> 8) & 0xffU;
uint32_t G = (((rgba1 >> 8  & 0xffU) * A + (rgba2 >> 8  & 0xffU) *(0xff - A)) >> 8) & 0xffU;
uint32_t B = (((rgba1 >> 16 & 0xffU) * A + (rgba2 >> 16 & 0xffU) *(0xff - A)) >> 8) & 0xffU;
A = ((a1 * A + a2 * (0xff - A)) >> 8) & 0xffU; // 必须对Alpha波段也处理
```