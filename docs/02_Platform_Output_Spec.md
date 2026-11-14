# 02 · 平台输出字段规范

> ⚠️ **硬指标以各站点卖家中心当时的原文为准。** 下表只收录本次能对着公开页面核对的规则，以及明确标成「未知」的空位。空位不是 0，也不是沿用巴西站的旧数字。
>
> 核对日期：2026-11-14。卖家发布前再复核一次。

---

## 站点地位

| 地位 | 站点 |
|---|---|
| **一等** | Shopee SG / MY / TH / ID / VN / PH；Amazon US；TikTok Shop US；TikTok Shop SG / MY / TH / ID / VN / PH；eBay，主站点 eBay US |
| **参考** | Shopee 巴西、Mercado Livre 巴西、Amazon 巴西、TikTok Shop 巴西。历史案例仍留在仓库里，**不再是默认语言、默认费率或默认规则卡** |

Shopify、速卖通不在本轮一等名单里。没有核到的字段不要补一个「行业常用值」。

---

## 买家可见语言

内部备注、自检、脚本输出用中文。买家能看见的标题、描述、Item specifics 取值、图内字、字幕、配音，用**目标站点语言**：

| 站点 | 买家可见语言 |
|---|---|
| Amazon US、eBay US、TikTok Shop US | 英语 |
| Shopee SG、Shopee PH、TikTok Shop SG、TikTok Shop PH | 英语 |
| Shopee MY、TikTok Shop MY | 英语或马来语，以该类目/站点实际要求为准 |
| Shopee TH、TikTok Shop TH | 泰语 |
| Shopee ID、TikTok Shop ID | 印尼语 |
| Shopee VN、TikTok Shop VN | 越南语 |
| Shopee BR、Mercado Livre（仅参考） | 巴西葡萄牙语 |

未指定站点时停止，输出 `[INPUT_MISSING]`。不要默认写成葡语，也不要把英语硬套到泰语/印尼语/越南语站点。

---

## 一、标题

| 平台 | 字符上限 | 本次依据 | 硬性内容禁则（已核对） |
|---|---|---|---|
| **Amazon US** | **非媒体类 75**（含空格）。Item Highlights 另有 **125**。媒体类上限 **未知** | Seller Central 公告：2026-07-27 起除媒体类外标题 ≤75；Item name + Item highlights 合计仍是 200 字符的信息位。2025-01-21 起多数类目曾以 200 为上限，并禁止 `! $ ? _ { } ^ ¬ ¦`（品牌名自带除外），同一词不得超过两次（介词、冠词、连词除外） | 不写促销语。品牌放在 Item name 里（公告的建议） |
| **eBay US** | **80** | [Seller Center：Create great listings](https://www.ebay.com/sellercenter/listings/create-listings)：「You've got 80 characters」 | 避免特殊字符和无关词。副标题是付费升级，不占这 80 字符，费用见[售卖费帮助页](https://www.ebay.com/help/selling/fees-credits-invoices/selling-fees?id=4822) |
| **TikTok Shop US / SEA** | **未知** | PH / SG 卖家大学写了标题必须准确、含品牌（须授权）、品类、材质、关键特征；禁止促销、卖家 URL/店名、未授权的 TikTok 品牌、无关符号。**没有在这些页面写字符上限** | 不要用第三方 API 文档里的 255 当作已核实上限 |
| **Shopee SEA（六站）** | **未知，按店铺查** | 官方接口 `v2.product.get_item_limit` 按店铺（可选类目）返回 `item_name_length_limit`。SG Mall 命名：[Brand + specifications and type + model](https://seller.shopee.sg/edu/article/34)，禁全大写（品牌除外）、禁 Hot Item / Best Seller / Sale / Free Shipping、禁表情和 `} ~ $ ^ { < ! * # ; % >` | 不要把巴西站规则卡上的 120，或第三方表格里的 60/80/100，写成六站默认 |
| Shopee BR / Mercado Livre | 120 / 60 | 旧规则卡，**仅参考** | 见 `platform-title-rules.md` 参考段 |

`title_lint.py` 对「未知」只报告字数并警告，不判超限失败。

---

## 二、图片

| 平台 | 本次能核对的规则 | 未知、不要脑补 |
|---|---|---|
| **Amazon US** | 主图纯白 RGB(255,255,255)；商品约占画面 **85%**；主图不要文字、Logo、水印、未包含的配件。Industrial & Scientific 样式指南：最长边至少 **1000** px 才能缩放，并写了上限 2000 px。服饰样式指南写的是最长边至少 **1500** px | 全类目是否强制 1:1；单文件 MB 上限。以该类目的 Product image requirements 为准 |
| **eBay US** | 至少 **1** 张，最多 **24** 张；单张最大 **12 MB**。高级刊登工具：jpeg / png / gif / tiff / heic / bmp，**最长边至少 500 px**。主图应完整、正面展示在售商品；瑕疵用附图标清楚 | 主体占比、是否必须白底、是否必须 1:1。这三项官方页没有给出百分比 |
| **Shopee SG** | 封面必填，最多再加 8 张（合计 9）。**1:1 必传**，3:4 是附加。Media Space：JPG/JPEG/PNG，单图 **≤ 2 MB**。商品视频见下节。Mall 封面：纯色背景（白优先）、商品至少 **60%**、最低 **500×500**、不叠促销字/水印/装饰边框；Logo 若放，在左上且不超过画面 10% | MY/TH/ID/VN/PH 的像素与张数上限本次没有逐站核完。用各站卖家教育中心，或 `get_item_limit` 的 `item_image_count_limit` |
| **TikTok Shop** | PH 指南：最多 **9** 张正方形、至少 **600×600**、彩色、主图纯色（建议白）、商品至少 **60%**、须完整正面。每张角度不同。SG 上传说明：纯白、无文字/水印、至少 600×600、最多 9 张正方形、展示正反面 | 单图文件大小。US 若与 PH/SG 正文不一致，以 US Product Listing Policy 为准，不要拿 API 文档的 300–4000 覆盖正文 |

像素脚本：

```bash
python Agents/04_Product_Image_Agent/scripts/check_main_image.py 图.png --platform amazon_us
python Agents/04_Product_Image_Agent/scripts/check_main_image.py 图.png --platform ebay_us
python Agents/04_Product_Image_Agent/scripts/check_main_image.py 图.png --platform shopee_sea
python Agents/04_Product_Image_Agent/scripts/check_main_image.py 图.png --platform tiktok
```

`shopee` / `mercadolivre` 两个旧键仍留给历史夹具，不代表东南亚默认。

---

## 三、描述与 Item specifics

| 平台 | 已核对 | 未知 |
|---|---|---|
| **eBay US** | 必填 Item specifics 必须填；建议项能填就填，买家用它们做筛选。Condition 按刊登表单里的 New / Used / Refurbished 等选项如实选。描述建议用单一字体、黑色、约 14 pt（高级刊登工具的可读性建议，不是字符上限） | 描述字符上限 |
| **Amazon US** | 标题公告没有改写五点描述的条数或字数。不要把论坛里的「5 条 / 2000 字符」写成硬上限 | 五点条数、每条字数、商品描述字数，按类目模板 |
| **TikTok Shop PH** | 描述不少于 **30 个词**，写清特征、数量、安全信息与警示 | 其他站点的最少词数；US HTML 描述上限 |
| **Shopee SEA** | 描述为必填（SG 上架教程）。属性按类目填，不确定就留空 | 描述最短/最长字符。向 `get_item_limit` 的 `item_description_length_limit` 要 |

禁止为了填满字段而编造品牌、产地、认证、功率、容量。没有授权的品牌名不写。兼容类表述只用输入里已经证实的型号，并遵守该站点对 compatibility claim 的限制。

---

## 四、视频

| 平台 | 已核对 | 未知 |
|---|---|---|
| **Shopee SG** | 商品视频 **10–60 秒**，MP4，**≤ 30 MB**，分辨率不超过 **1280×1280**。VP9 不支持。教育页另建议用站点主要本地语言 | 其他五站是否同一组数字 |
| **TikTok Shop PH / SG** | 每个商品 **1** 条视频，**≤ 5 MB** | 时长、画幅、分辨率 |
| **Amazon US** | [sell.amazon.com 的 shoppable video 说明](https://sell.amazon.com/blog/amazon-product-video)：`.mov` 或 `.mp4`，最高 1080p，最大 **5 GB**，时长 **1–12 分钟**。该页还写：要出现在详情页主媒体区，商品图片需少于 6 张 | 主图视频位是否另有更短的时长限制 |
| **eBay US** | 每条刊登 **1** 个视频；`.mp4` 或 `.mov`；**≤ 150 MB**；上传分辨率最高 1080p；输出 240p / 360p / 480p / 720p；建议约 **1 分钟**以内；语言与刊登站点一致。变体刊登不支持视频。不支持外链 YouTube | 强制画幅 |

口播词速 2.5 词/秒只是 `video_timing.py` 的规划默认值，不是平台规则。泰语、越南语、印尼语按实际配音改 `--wps`。

---

## 五、费用

费率不写在本页，避免和 `platform_fees.json` 两套数字。口径、来源和「必须卖家复核」的清单见：

- [`Agents/02_Product_Strategy_Agent/references/pricing-rules.md`](../Agents/02_Product_Strategy_Agent/references/pricing-rules.md)
- [`Agents/02_Product_Strategy_Agent/scripts/platform_fees.json`](../Agents/02_Product_Strategy_Agent/scripts/platform_fees.json)

税：所有预设的 `tax_pct` 都是 0。eBay 最终成交费基数含 sales tax；TikTok Shop US 的 referral 公式把税减掉；Amazon 公开定价页写的是商品价 + 运费 + 礼品包装，没有在该页说明销售税。进口税和各国间接税都要卖家自己加。

---

## 六、禁售与禁词

不要在本仓库维护一份自编禁售清单。发布前打开站点原文：

| 平台 | 去哪查 |
|---|---|
| eBay US | [Prohibited and restricted items](https://www.ebay.com/help/policies/prohibited-restricted-items/prohibited-restricted-items?id=4207)，以及 [Images, videos and text policy](https://www.ebay.com/help/policies/listing-policies/images-videos-text-policy?id=4240) |
| Amazon US | Seller Central 的 Restricted products 与 Product title requirements |
| Shopee | 各站 Seller Education 的 Prohibited / Restricted items |
| TikTok Shop | 各站 Seller University 的 Product Listing Guidelines 与禁售清单 |

合规拦截的写法见 [`03_Compliance_Guard.md`](./03_Compliance_Guard.md)。工具箱不做刷单、诱评、虚假宣传、商标蹭用、站外导流。

---

## 七、跨站点复用

同一商品铺多个一等站点时逐项分开做：

| 检查 | 原因 |
|---|---|
| 标题按站点重写 | 80、75 和「上限未知」不能互相粘贴；语言也不同 |
| 主图按站点重出 | Amazon 主图不能叠字；Shopee Mall 封面也不能叠促销字；eBay 不要求白底 |
| 描述与 Item specifics 按表单重填 | eBay 的必填 specifics 是类目字段，不是 Shopee 的属性树 |
| 费率按站点重算 | 巴西阶梯费不能套到新加坡或 eBay |
| 单位 | 买家可见文本跟站点习惯。美国站可以用买家看得懂的英制，但必须与 `spec_table` 一致，不得另编一套 |

---

**相关文档**：[00 架构](./00_Architecture_SOP_to_Agent.md) · [01 Prompt 规范](./01_Prompt_Design_Guide.md) · [03 合规](./03_Compliance_Guard.md) · [04 自检](./04_Result_Checklist.md)
