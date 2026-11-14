# Shopee SEA · 商品图规则卡

> 一等站点：新加坡、马来西亚、泰国、印尼、越南、菲律宾。
> 能核对的公开页主要来自 Shopee SG Seller Education（2026-11-14）。其他五站未逐条核到的，不抄新加坡数字。

## 一、SG 已核对

| 项 | 要求 | 来源 |
|---|---|---|
| 张数 | 封面必填，最多再加 8 张 | [Listing your first product](https://seller.shopee.sg/edu/article/6933/list-first-product) |
| 比例 | **1:1 必传**。3:4 只能在已有 1:1 之后附加 | [3:4 说明](https://seller.shopee.sg/edu/article/17318/product-images-3-4-ratio) |
| 格式 / 大小 | JPG、JPEG、PNG；单图 **≤ 2 MB** | [Media Space](https://seller.shopee.sg/edu/article/2473) |
| Mall 封面 | 纯色背景，白优先；商品至少 **60%**；最低 **500×500**；不叠促销字、水印、装饰边框；Logo 若有，左上且 ≤ 画面 10% | [Mall Listings Guidelines](https://seller.shopee.sg/edu/article/34) |
| 非 Mall 的 60% | **不要当成全站硬阈值** | 上架教程没有写这个百分比 |

```bash
python scripts/check_main_image.py 图.png --platform shopee_sea
```

`shopee_sea` 硬性检查 1:1、短边 ≥ 500、文件 ≤ 2 MB。60% 和白底是警告。旧键 `--platform shopee` 仍是历史夹具（白底失败线 90%），不是东南亚默认。

## 二、其他五站

MY / TH / ID / VN / PH 的张数、像素、文件大小：**未逐站核完**。用该站 Seller Education，或接口 `v2.product.get_item_limit`。

图内文字用站点语言：SG / PH 英语；MY 英语或马来语；TH 泰语；ID 印尼语；VN 越南语。

## 三、9 图内容顺序（方法，不是平台硬性槽位）

平台只限制张数和封面，不规定第 5 张必须是尺寸图。下面是本工具箱的内容顺序，方便和 07 的差评回流对齐：

| 图位 | 内容 |
|---|---|
| 1 | 封面：在售商品完整正面 |
| 2 | 其他角度 |
| 3 | 接口 / 材质特写 |
| 4 | 真实使用场景（不超出 `usage_scope`） |
| 5 | 尺寸，数字来自 `spec_table` |
| 6 | 2–3 个可验证卖点 |
| 7 | 变体（用平台变体功能，不靠拼图冒充多色） |
| 8 | 包装清单，标出**不含**什么 |
| 9 | 已持有的认证或保修。没有的标志不要画 |

## 四、参考：Shopee 巴西

巴西站旧卡的差异只供旧案例对照，**不能**拿来做东南亚封面：

| 项 | 巴西参考案例里的做法 | 东南亚现在怎么做 |
|---|---|---|
| 语言 | PT-BR 大字 | 站点语言。SG Mall 封面不叠促销字 |
| 审美 | 高饱和、暖色、折扣角标 | 不把折扣角标当成默认 |
| 字符与费率 | 120 字符、巴西阶梯费 | 字符走 `get_item_limit`；费率走 `shopee_sg` 等键，多数需要 `--commission` |

保修图在巴西消费法语境下是强建议。SEA / US 是否必须，看该类目和当地法规，不默认加一张葡语保修图。
