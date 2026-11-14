# eBay US · 商品图 / 视频 / 刊登字段规则卡

> 主站点是 eBay US。其他 eBay 站点不在本卡展开。
> 来源均为 ebay.com 帮助中心或 Seller Center，核对日期 2026-11-14。

## 照片

来源：[Adding pictures](https://www.ebay.com/help/selling/listings/adding-pictures-listings?id=4148)、[高级刊登工具](https://www.ebay.com/help/selling/listings/using-advanced-listing-tool?id=5196)。

| 项 | 要求 |
|---|---|
| 张数 | 至少 1 张，最多 **24** 张。带缩放的 24 张在费用页标注为免费 |
| 单张大小 | 最大 **12 MB** |
| 格式 | jpeg、png、gif、tiff、heic、bmp |
| 尺寸 | 最长边至少 **500 px** |
| 主图 | 搜索结果用第一张。应完整、正面展示**这一件**在售商品 |
| 附图 | 多角度；有瑕疵就拍近景；尺寸不明显时可用参照物；单件和套装要能区分 |
| 白底 / 1:1 / 主体占比 | **官方页没有这些百分比。** 不要为了「像 Amazon」而当成 eBay 硬性失败 |

```bash
python scripts/check_main_image.py 图.png --platform ebay_us
```

脚本只硬性检查最长边 ≥ 500 px 和 12 MB。不要求白底，不要求正方形。

## 视频

见 [`../../05_Product_Video_Agent/references/video-specs.md`](../../05_Product_Video_Agent/references/video-specs.md) 的 eBay US 段。变体刊登不能加视频。

## 标题、描述、Item specifics

| 字段 | 规则 |
|---|---|
| 标题 | **80** 字符。写品牌（仅限真实且允许使用的）、型号、颜色、规格。不堆无关词 |
| 副标题 | 可选、付费。拍卖约 $1.50 / $3.00，一口价约 $2.00 / $6.00，视价格档。不是标题的第 81 个字符 |
| Item specifics | 必填项全部填写。建议项在知道的时候填写。买家用它们筛选，漏填就进不了对应筛选 |
| Condition | 按表单选项如实选。不把 Used 写成 New |
| 描述 | 高级刊登工具建议单一字体、黑色、约 14 pt。**字符上限本次未核到** |
| 语言 | 英语，含视频 |

不知道的 specifics 留空，并在内部备注写 `[INPUT_MISSING]`。不要为了「完整度」编产地、认证或品牌。

## 费用起步（多数类目）

详见 `platform_fees.json` 的 `ebay_us`。公开帮助页：多数类目最终成交费 **13.6%**（成交额 $7,500 以内的部分）+ 每单 **$0.30 / $0.40**。基数含商品价、运费（有例外）和 **sales tax**。店铺订阅、Motors、类目例外都不在这条起步数字里。

## 合规

- 图片、视频和文字不得引导买家离开 eBay（联系方式、外链、去其他网站的号召）。见 [Images, videos and text policy](https://www.ebay.com/help/policies/listing-policies/images-videos-text-policy?id=4240)。站外成交另有最终成交费，即使没卖出。
- 描述、图片和视频使用刊登站点的主要语言。eBay US 用英语。见 [Item description policy](https://www.ebay.com/help/policies/listing-policies/item-description-policy?id=4372)。
- 商标：没有授权就不要把别人的品牌写成自己的品牌。准确描述兼容关系前，先看该类目是否允许。
- 禁售清单不在本卡抄录：[Prohibited and restricted items](https://www.ebay.com/help/policies/prohibited-restricted-items/prohibited-restricted-items?id=4207)。
