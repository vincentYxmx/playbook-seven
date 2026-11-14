# 视频规范卡

> 核对日期 2026-11-14。只写公开页面上的数字。时长「建议」和「硬上限」分开。
> 买家可见字幕和口播用目标站点语言。内部备注用中文。

## Shopee SG（商品视频 / Media Space）

来源：[Uploading to Media Space](https://seller.shopee.sg/edu/article/2473)、[Creating good product videos](https://seller.shopee.sg/edu/article/6084)。

| 项 | 要求 |
|---|---|
| 时长 | **10–60 秒** |
| 格式 | MP4。VP9 不支持 |
| 大小 | **≤ 30 MB** |
| 分辨率 | 不超过 **1280×1280** |
| 语言 | 教育页要求音轨和文字用主要本地语言。SG 用英语 |
| 其他五站 | **未逐站核到同一组数字**。上传前看该站 Media Space 说明 |

MY / TH / ID / VN / PH 的口播分别用该站语言（MY 英语或马来语，以站点要求为准）。

## TikTok Shop（PH 与 SG 上传说明）

| 项 | 要求 |
|---|---|
| 条数 | 每个商品 **1** 条 |
| 大小 | **≤ 5 MB** |
| 时长 / 画幅 / 分辨率 | **未知**。不要把短视频信息流的 9:16 习惯写成商品视频位的硬限制 |
| 内容 | 必须是在售商品。不导流到站外（电话、二维码、第三方链接、Link in bio） |
| 语言 | 与站点一致。US 英语 |

## Amazon US

来源：[sell.amazon.com shoppable video](https://sell.amazon.com/blog/amazon-product-video)。这是 shoppable video，不一定等于主图视频位。

| 项 | 要求 |
|---|---|
| 格式 | `.mov` 或 `.mp4` |
| 分辨率 | 最高 1080p |
| 大小 | 最大 **5 GB** |
| 时长 | **1–12 分钟** |
| 展示条件 | 该页写：要出现在详情页主媒体区，商品图片需少于 6 张 |
| 主图视频位更短的限制 | **未知**，到 Seller Central 再确认 |
| 语言 | 英语 |

## eBay US

来源：[Add a video to your listing](https://www.ebay.com/help/selling/listings/creating-managing-listings/add-video-to-listing?id=5272)、[高级刊登工具](https://www.ebay.com/help/selling/listings/using-advanced-listing-tool?id=5196)。

| 项 | 要求 |
|---|---|
| 条数 | **1** 条。同一文件可复用到多条刊登 |
| 格式 | `.mp4`（MPEG-4 AVC）或 `.mov` |
| 大小 | **≤ 150 MB** |
| 分辨率 | 上传最高 1080p；输出 240p / 360p / 480p / 720p |
| 时长 | 帮助页写 ideally about one minute or less。这是建议，不是另一套已公布的硬秒数 |
| 语言 | 必须与刊登站点一致。eBay US 用英语 |
| 不支持 | 变体刊登；YouTube 或其他外链 |
| 审核 | 通常 48 小时内，高峰最长 7 个工作日 |

视频和图片一样，不能演示商品没有的功能，不能仿官方标识。

## 参考：Shopee 巴西 / Mercado Livre

旧卡里的「≤30 秒、PT-BR、9:16」只属于历史案例。不要用它覆盖上面的 SG 10–60 秒或 eBay 150 MB。

## 口播预算

`video_timing.py` 的默认 **2.5 词/秒** 是规划值，方便英语脚本先估时长。它不是平台规则。泰语、越南语、印尼语以实际配音为准，用 `--wps` 改。超时就删词，不要把语速调到听不清。

静音可读：字幕用站点语言，画面本身仍要能看出在售商品。字幕里的数字必须能在 `spec_table` 找到。
