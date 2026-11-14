# platform-title-rules.md · 标题规则卡

> 一等站点在前。巴西站与 Mercado Livre 收在文末，只供旧案例对照。
> 字符数用 `len()`（字符，不是字节）。发布前到卖家中心复核。

校验：

```bash
python scripts/title_lint.py "标题" --platform amazon_us
python scripts/title_lint.py "标题" --platform ebay_us
python scripts/title_lint.py "标题" --platform shopee_sg
python scripts/title_lint.py "标题" --platform tiktok_us
python scripts/title_lint.py "标题" --platform shopee_th
```

`--platform shopee` 会拒绝执行，必须带站点。`--platform amazon` 映射到 `amazon_us`。

---

## Amazon US（非媒体类上限 75）

| 规则 | 内容 | 级别 |
|---|---|---|
| 字符上限 | 75，含空格。2026-07-27 起 Seller Central 公告，媒体类除外 | 硬 |
| Item Highlights | 另 125 字符。与标题合计 200。两边都进搜索 | 硬（字段分开写） |
| 媒体类 | 精确上限本次未核到。`--media` 时不套 75，只警告 | 未知 |
| 重复词 | 2025-01-21 公告：同一词不超过两次。介词、冠词、连词除外 | 硬 |
| 字符 | `! $ ? _ { } ^ ¬ ¦` 不允许，除非属于品牌名 | 硬 |
| 促销语 | 不写 free shipping、best seller、折扣 | 硬 |
| 语言 | 英语。中文直接失败 | 硬 |

## eBay US（上限 80）

| 规则 | 内容 | 级别 |
|---|---|---|
| 字符上限 | 80。Seller Center 建议把品牌、型号、颜色、规格写进去，并尽量用满，但不要灌无关词 | 硬 |
| 副标题 | 付费升级，不是标题的溢出位 | 信息 |
| Item specifics | 必填项必须填。不知道就留空，不编 | 硬 |
| 语言 | 英语。视频也必须是站点语言 | 硬 |
| 促销/无关词 | 帮助页要求避免特殊字符和无关词 | 软 |

## TikTok Shop US 与 SEA

| 规则 | 内容 | 级别 |
|---|---|---|
| 字符上限 | **未知**。脚本只报告字数 | 未知 |
| 标题内容 | 品类、材质、关键特征、数量。品牌仅在已授权时写 | 硬 |
| 禁止 | 促销（如 x% off）、卖家 URL 或店名、未授权 TikTok 字样、与商品无关的符号 | 硬 |
| 语言 | US / SG / PH 英语；MY 英语或马来语；TH 泰语；ID 印尼语；VN 越南语 | 硬 |
| 描述 | PH 指南：不少于 30 个词。其他站未核到 | PH 硬 / 其余未知 |

## Shopee SEA

| 站点 | 字符上限 | 语言 |
|---|---|---|
| SG / MY / TH / ID / VN / PH | **按店铺 `v2.product.get_item_limit`**，本卡不写死 | SG、PH 英语；MY 英语或马来语；TH 泰语；ID 印尼语；VN 越南语 |

SG Mall 已核对的命名禁则（[article/34](https://seller.shopee.sg/edu/article/34)）：

| 规则 | 级别 |
|---|---|
| 结构：Brand + specifications and type + model | 硬（Mall） |
| 不全大写，品牌名除外 | 硬（Mall） |
| 不写 Hot Item / Best Seller / Sale / Free Shipping，不堆无关词 | 硬（Mall） |
| 不用表情，不用 `} ~ $ ^ { < ! * # ; % >` | 硬（Mall） |

非 Mall 是否逐条相同，以该站卖家中心为准。脚本对上述符号和促销词按失败处理，是把 Mall 指南当作保守下限。

---

## 参考：Shopee 巴西（上限 120）与 Mercado Livre（上限 60）

不再作为 `--platform shopee` 的默认。需要对照旧案例时用 `shopee_br_ref` 或 `mercadolivre`。

| 规则 | Shopee BR 参考 | Mercado Livre 参考 |
|---|---|---|
| 字符上限 | 120；前 30 字符单独提示 | 60 |
| 语言 | PT-BR | PT-BR |
| 促销词 | 警告 | 警告 |

---

## 脚本说明

- 未知上限 = `WARN`，不是 `FAIL`。
- 禁用词仍由 `--forbidden` 传入。平台没有公开完整违禁词表。
- 泰语站点若标题里没有泰文字符，给出警告。确认该类目允许英语时再 `--locale en`。
