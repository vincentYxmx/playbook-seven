# Amazon US · 商品图规则卡

> 一等站点是 Amazon.com（美国）。Amazon 巴西预设只在费率文件里作参考，不在这张卡里。

## 主图（类目样式指南里的共同项）

Amazon 托管的类目样式指南（Industrial & Scientific、Clothing）写明：

| 项 | 要求 |
|---|---|
| 背景 | 纯白，RGB **255,255,255** |
| 主体 | 约占画面 **85%**，商品完整，不要裁切 |
| 内容 | 只放在售商品和随货配件。不放文字、Logo、水印、价格、评分、未包含的配件 |
| 角度 | 主图一个正面。不要在主图里并排前后视图 |
| 缩放尺寸 | Industrial & Scientific：最长边至少 **1000** px（该指南写到最多 2000 px）。Clothing：最长边至少 **1500** px |
| 格式 | 这两份指南写 JPEG（优先）和 TIFF。PNG / GIF 是否仍被主图接受，**本次未在同一份指南里核对** |
| 1:1 | **不是这两份指南的全类目硬性要求。** 脚本对非正方形只警告 |

```bash
python scripts/check_main_image.py 图.png --platform amazon_us
```

旧键 `--platform amazon` 仍把文件大小 10 MB 当作失败线。那是旧工具箱阈值，**不是**这次从样式指南核对到的数字。`amazon_us` 不因文件大小失败。

## 标题（与图一起发布时）

非媒体类标题 **≤ 75** 字符（2026-07-27 公告，含空格）。Item Highlights **125** 字符。细节在 `03` 的 `platform-title-rules.md`。

## 视频

Shoppable video 的 1–12 分钟、5 GB、1080p 见 `05` 的 `video-specs.md`。不要把这个时长当成主图视频位已经核对过。

## 费用

`amazon_us` **没有**单一佣金。Referral fee 按类目，见 [sell.amazon.com/pricing](https://sell.amazon.com/pricing)。Professional 月费该页为 **$39.99**，Individual 为 **$0.99/件**。FBA 另计。脚本不传 `--commission` 会拒绝计算。
