---
title: 农历数据变量说明
date: 2024-3-25 10:16:05
tags:
  - Lunar
  - 农历数据
---

{% tabs First unique name %}
<!-- tab 一 -->

## 1. StartYear

数据起始年份(公历)

## 2. EndYear

数据终止年份(不包含该年)

## 3. PreLeapIndex

**`(StartYear - 1)`**年农历十月及以后的闰月索引，对应**`PreMonth`**中的序号，当前为-1，表示1799年农历十月以后无闰月。

## 4. PreMonth

**`(StartYear - 1)`** 年农历十月及以后的月份，每月初一在 **StartYear** 年的年内序数。**`PreMonth`**中分别对应农历的十月、十一月、十二月、正月。

## 5. MonthInfo

农历月份信息，一年用4个字节表示。数据长度为 **`(EndYear - StartYear)`**

| 第31位 |  第30-27位   |  第26-23位   |       第22-17位        | 第16-13位 |         第12-0位         |
| :----: | :----------: | :----------: | :--------------------: | :-------: | :----------------------: |
|  保留  | 元旦天干序数 | 元旦地支序数 | 农历正月初一的年内序数 |   闰月    | 一个比特对应一个月份大小 |

月份大小数据是月份小的在低位, 月份大的在高，即正月在最低位。
以1900年为例，4个字节的数据展开成二进制位：

|  0   | 0000  |  1010  |    011110    |  1000  |                  1 0 1 1 0 1 1 0 1 0 0 1 0                  |
| :--: | :---: | :----: | :----------: | :----: | :---------------------------------------------------------: |
| 保留 | 0(甲) | 10(戌) | 30 (1月31日) | 闰八月 | 从左往右依次为腊月, 冬月...闰八月, 八月, ... , 正月的天数。 |

**P.S. 农历月份对应的位为0, 表示这个月为29天(小月), 为1表示有30天(大月).** 

## 6. SolarTermsSource & SolarTermsIndex

二十四节气信息， 节气数据将由 **`SolarTermsSource`** 和 **`SolarTermsIndex`** 中的数据生成。

一年用6个字节表示，每个节气使用两比特数据。

| 第一字节最高两位  | 第一字节其余6位至第六字节共46个位  |
| :---------------: | :--------------------------------: |
| 小寒的年内序数减3 | 每个节气距离上一节气的天数, 共23组 |

小寒的年内序数已给出，剩下的23个节气分别对应这23组数据, 有以下含义：

| 二进制位 | 意义 |               描述               |
| :------: | :--: | :------------------------------: |
|    00    | 14天 | 当前对应的节气距离上一节气为14天 |
|    01    | 15天 | 当前对应的节气距离上一节气为15天 |
|    10    | 16天 | 当前对应的节气距离上一节气为16天 |
|    11    | 17天 | 当前对应的节气距离上一节气为17天 |

由上表可以看出，除小寒以外的其余23个节气的两比特数据加上14就是距离上一节气的天数。
节气顺序：

| 节气 | 中气 | 节气 | 中气 | 节气 | 中气 | 节气 | 中气 | 节气 | 中气 | 节气 | 中气 |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| 小寒 | 大寒 | 立春 | 雨水 | 惊蛰 | 春分 | 清明 | 谷雨 | 立夏 | 小满 | 芒种 | 夏至 |
| 小暑 | 大暑 | 立秋 | 处暑 | 白露 | 秋分 | 寒露 | 霜降 | 立冬 | 小雪 | 大雪 | 冬至 |

## 7. PreDongzhiOrder

**`(StartYear - 1)`** 年冬至日在**`StartYear`**年的年内序数, 这个数据将被用在 **`StartYear`** 年`数九`的计算上.

## 8. ExtremeSeason

每年数九、入梅、出梅及三伏的信息，一年用两个字节表示。

| 第15-11位 | 第10-6位 | 第5-1位 | 最末位 |
| :-------: | :------: | :-----: | :----: |
|   入梅    |   出梅   |  初伏   |  末伏  |

1. **`一九`** 即是冬至, 往后到 **`九九`** 的每个 **`九`** 相差 `9` 天, 可顺利推算出来, 故 **`数九`** 信息省略。
2. **`初伏`** 信息：该天数加上 `180` 为初伏这一日的年内序数。
3. **`中伏`** 信息：**`"三伏"`** 天的 **`"中伏"`** 在 **`"初伏"`** 后 `10` 天，而 **`"末伏"`** 在 **`"中伏"`** 后 `10` 天或 `20` 天，因此 **`"中伏"`** 信息省略。
4. **`末伏`** 信息：若该位为 `1`，表示末伏距离初伏 `30` 天，为 `0` 表示末伏距离初伏 `20` 天。
5. **`入梅`** 信息：该天数加上 `150` 为入梅这一日的年内序数。
6. **`出梅`** 信息：该天数加上 `180` 为出梅这一日的年内序数。

<!-- endtab -->

<!-- tab 二 -->

## 1. StartYear

数据起始年份(公历)

## 2. EndYear

数据终止年份(不包含该年)

## 3. PreLeapIndex

**`(StartYear - 1)`**年农历十月及以后的闰月索引，对应**`PreMonth`**中的序号，当前为-1，表示1799年农历十月以后无闰月。

## 4. PreMonth

**`(StartYear - 1)`** 年农历十月及以后的月份，每月初一在 **StartYear** 年的年内序数。**`PreMonth`**中分别对应农历的十月、十一月、十二月、正月。

## 5. MonthInfo

农历月份信息，一年用4个字节表示。数据长度为 **`(EndYear - StartYear)`**

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-7btt{border-color:inherit;font-weight:bold;text-align:center;vertical-align:top}
</style>
<table class="tg"><thead>
  <tr>
    <th class="tg-7btt">第31位</th>
    <th class="tg-7btt">第30-27位</th>
    <th class="tg-7btt">第26-23位</th>
    <th class="tg-7btt">第22-17位</th>
    <th class="tg-7btt">第16-13位</th>
    <th class="tg-7btt">第12-0位</th>
  </tr></thead>
<tbody>
  <tr>
    <td class="tg-7btt">保留</td>
    <td class="tg-7btt">元旦天干序数</td>
    <td class="tg-7btt">元旦地支序数</td>
    <td class="tg-7btt">农历正月初一的年内序数</td>
    <td class="tg-7btt">闰月</td>
    <td class="tg-7btt">一个比特对应一个月份大小</td>
  </tr>
</tbody>
</table>
月份大小数据是月份小的在低位, 月份大的在高，即正月在最低位。
以1900年为例，4个字节的数据展开成二进制位：

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-7btt{border-color:inherit;font-weight:bold;text-align:center;vertical-align:top}
</style>
<table class="tg"><thead>
  <tr>
    <th class="tg-7btt">第31位</th>
    <th class="tg-7btt">第30-27位</th>
    <th class="tg-7btt">第26-23位</th>
    <th class="tg-7btt">第22-17位</th>
    <th class="tg-7btt">第16-13位</th>
    <th class="tg-7btt">第12-0位</th>
  </tr></thead>
<tbody>
  <tr>
    <td class="tg-7btt">保留</td>
    <td class="tg-7btt">元旦天干序数</td>
    <td class="tg-7btt">元旦地支序数</td>
    <td class="tg-7btt">农历正月初一的年内序数</td>
    <td class="tg-7btt">闰月</td>
    <td class="tg-7btt">一个比特对应一个月份大小</td>
  </tr>
</tbody>
</table>


## 6. SolarTermsSource & SolarTermsIndex

二十四节气信息， 节气数据将由 **`SolarTermsSource`** 和 **`SolarTermsIndex`** 中的数据生成。

一年用6个字节表示，每个节气使用两比特数据。

<table><thead>
  <tr>
    <th>第一字节最高两位</th>
    <th>第一字节其余6位至第六字节共46个位</th>
  </tr></thead>
<tbody>
  <tr>
    <td>小寒的年内序数减3</td>
    <td>每个节气距离上一节气的天数, 共23组</td>
  </tr>
</tbody>
</table>


小寒的年内序数已给出，剩下的23个节气分别对应这23组数据, 有以下含义：

<table><thead>
  <tr>
    <th>二进制位</th>
    <th>意义</th>
    <th>描述</th>
  </tr></thead>
<tbody>
  <tr>
    <td>00</td>
    <td>14天</td>
    <td>当前对应的节气距离上一节气为14天</td>
  </tr>
  <tr>
    <td>01</td>
    <td>15天</td>
    <td>当前对应的节气距离上一节气为15天</td>
  </tr>
  <tr>
    <td>10</td>
    <td>16天</td>
    <td>当前对应的节气距离上一节气为16天</td>
  </tr>
  <tr>
    <td>11</td>
    <td>17天</td>
    <td>当前对应的节气距离上一节气为17天</td>
  </tr>
</tbody>
</table>


由上表可以看出，除小寒以外的其余23个节气的两比特数据加上14就是距离上一节气的天数。下表为节气顺序：

<table><thead>
  <tr>
    <th>节气</th>
    <th>中气</th>
    <th>节气</th>
    <th>中气</th>
    <th>节气</th>
    <th>中气</th>
    <th>节气</th>
    <th>中气</th>
    <th>节气</th>
    <th>中气</th>
    <th>节气</th>
    <th>中气</th>
  </tr></thead>
<tbody>
  <tr>
    <td>小寒</td>
    <td>大寒</td>
    <td>立春</td>
    <td>雨水</td>
    <td>惊蛰</td>
    <td>春分</td>
    <td>清明</td>
    <td>谷雨</td>
    <td>立夏</td>
    <td>小满</td>
    <td>芒种</td>
    <td>夏至</td>
  </tr>
  <tr>
    <td>小暑</td>
    <td>大暑</td>
    <td>立秋</td>
    <td>处暑</td>
    <td>白露</td>
    <td>秋分</td>
    <td>寒露</td>
    <td>霜降</td>
    <td>立冬</td>
    <td>小雪</td>
    <td>大雪</td>
    <td>冬至</td>
  </tr>
</tbody>
</table>


## 7. PreDongzhiOrder

**`(StartYear - 1)`** 年冬至日在**`StartYear`**年的年内序数, 这个数据将被用在 **`StartYear`** 年`数九`的计算上.

## 8. ExtremeSeason

每年数九、入梅、出梅及三伏的信息，一年用两个字节表示。

<table><thead>
  <tr>
    <th>第15-11位</th>
    <th>第10-6位</th>
    <th>第5-1位</th>
    <th>最末位</th>
  </tr></thead>
<tbody>
  <tr>
    <td>入梅</td>
    <td>出梅</td>
    <td>初伏</td>
    <td>末伏</td>
  </tr>
</tbody>
</table>


1. **`一九`** 即是冬至, 往后到 **`九九`** 的每个 **`九`** 相差 `9` 天, 可顺利推算出来, 故 **`数九`** 信息省略。
2. **`初伏`** 信息：该天数加上 `180` 为初伏这一日的年内序数。
3. **`中伏`** 信息：**`"三伏"`** 天的 **`"中伏"`** 在 **`"初伏"`** 后 `10` 天，而 **`"末伏"`** 在 **`"中伏"`** 后 `10` 天或 `20` 天，因此 **`"中伏"`** 信息省略。
4. **`末伏`** 信息：若该位为 `1`，表示末伏距离初伏 `30` 天，为 `0` 表示末伏距离初伏 `20` 天。
5. **`入梅`** 信息：该天数加上 `150` 为入梅这一日的年内序数。
6. **`出梅`** 信息：该天数加上 `180` 为出梅这一日的年内序数。

<!-- endtab -->
{% endtabs %}

