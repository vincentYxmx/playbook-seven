# 案例 · 65W GaN 双口充电器（一等站点默认路径）

> 这条链路覆盖 **Amazon US、eBay US、TikTok Shop US、Shopee SEA**。
> 买家可见文本用站点语言。内部说明用中文。
> 数字只来自本页的 `spec_table`，或来自已经核对过的公开规则。没有核对到的字段写成未知。

巴西电动滑板车案例仍在 [`../01_Patinete_Eletrico_500W/`](../01_Patinete_Eletrico_500W/)，只作参考。

---

## 1. 产品背景

| 项 | 内容 |
|---|---|
| 产品 | 无品牌 GaN 充电器。不是任何已注册商标的仿款 |
| 在售内容 | 充电器本体。**不含数据线** |
| 主站点 | Amazon US、eBay US、TikTok Shop US、Shopee SG |
| 同一套参数还要改写的站点 | Shopee MY / TH / ID / VN / PH，TikTok 对应 SEA 站 |

### spec_table（唯一数字来源）

| 字段 | 值 |
|---|---|
| output_power | 65W |
| ports | 1× USB-C, 1× USB-A |
| input_voltage | 100-240V |
| cable_included | no |

重量、输出电流、认证号、产地都不在表里。下文不写。

---

## 2. 定价（02）

到岸成本按 **8**（平台货币），试售价 **24.99**。`return_pct=2` 和 `ad_pct=5` 是工具箱预留，不是平台费。`tax_pct=0` 表示没算税。

```bash
python Agents/02_Product_Strategy_Agent/scripts/sku_pricing.py calc \
  --platform ebay_us --cost 8 --price 24.99

python Agents/02_Product_Strategy_Agent/scripts/sku_pricing.py calc \
  --platform tiktok_us --cost 8 --price 24.99
```

| 平台 | 脚本结果 | 怎么读 |
|---|---|---|
| eBay US | 佣金 13.6% + 固定费 0.40；净利率 45.8%；盈亏价 9.83；广告前盈亏 ROAS 1.97 | 13.6% 只是多数类目、$7,500 以内的起步。基数含运费和 **sales tax**。这里的 24.99 只是商品价，费用会被低估 |
| TikTok Shop US | 佣金 6%；净利率 55.0%；盈亏价 8.70 | 多数类目的起步。珠宝和 Pre-Owned 不是 6%。公式含买家运费、不含税 |

Amazon US 与 Shopee SG **不能**用上面两个百分比：

```text
python sku_pricing.py calc --platform amazon_us --cost 8 --price 24.99
→ [INPUT_MISSING] … 起点：https://sell.amazon.com/pricing

python sku_pricing.py calc --platform shopee_sg --cost 8 --price 24.99
→ [INPUT_MISSING] … 起点：https://seller.shopee.sg/edu/article/13107/seller-fees
```

卖家在类目表上确认费率之后，再传 `--commission`。不要把 Everything Else 的 15% 或巴西站的 14% 填进来充数。MY/TH/ID/VN/PH 与 TikTok SEA 同样没有单一预设。

---

## 3. 标题（03）

各站标题故意不一样，避免同一字符串铺四个站点。

| 站点 | 买家可见标题 | 校验 |
|---|---|---|
| Amazon US | `65W GaN USB-C Charger, 2-Port, 100-240V` | 39/75，通过。非媒体类 |
| eBay US | `GaN USB-C Wall Charger 65W, 2 Ports, 100-240V` | ≤80。英语 |
| TikTok Shop US | `65W GaN USB-C Charger, Two Ports, 100-240V Input` | 字符上限**未知**，脚本只警告 |
| Shopee SG | `65W GaN USB-C Charger 2 Port Universal Voltage` | 上限按 `get_item_limit`，**不是 120** |
| Shopee PH | `65W GaN USB-C Travel Charger, 2-Port, 100-240V` | 英语。上限未知 |
| Shopee MY | `65W GaN USB-C Charger Dual Port 100-240V` | 英语。若类目要求马来语，整句重写，不要中英混贴 |
| Shopee TH | `ที่ชาร์จ GaN 65W พอร์ต USB-C และ USB-A ไฟเข้า 100-240V` | 泰语 |
| Shopee ID | `Charger GaN 65W 2 Port USB-C dan USB-A 100-240V` | 印尼语 |
| Shopee VN | `Củ sạc GaN 65W 2 cổng USB-C và USB-A 100-240V` | 越南语 |

Amazon Item Highlights（另计，不占那 75 字符）示例：

`USB-C and USB-A. Input 100-240V. Output 65W. Cable not included.`

eBay Item specifics：只填表单允许、且上表有的值（输出 65W、输入 100-240V、两个口）。Brand、产地、认证留空，直到有授权和证书。Condition 选 New 只在商品确实是全新时。

没有写 Best Seller、Free Shipping、100%、Original。

---

## 4. 图（04）

| 站点 | 主图 |
|---|---|
| Amazon US | 纯白 RGB(255,255,255)，主体约 85%，**无文字**。`--platform amazon_us` |
| eBay US | 完整正面。不要求白底，不要求 1:1。最长边至少 500px，单张 ≤12MB。`--platform ebay_us` |
| Shopee SG | 1:1，单图 ≤2MB。Mall 封面不叠促销字。`--platform shopee_sea` |
| TikTok | 至少 600×600 的正方形，最多 9 张。视频另计，≤5MB。`--platform tiktok` |

第 8 张是包装清单，英语站写 **Cable not included**。泰语、印尼语、越南语站点换成对应句子，不留英文。

不要画 FCC、CE 或其他标志。本表没有认证号。

---

## 5. 视频（05）

| 站点 | 按已核对的规则裁 |
|---|---|
| Shopee SG | **10–60 秒**，MP4，≤30MB，分辨率不超过 1280×1280。口播英语 |
| eBay US | ≤150MB，建议约 1 分钟，英语。变体刊登不能加视频 |
| TikTok | 1 条，**≤5MB**。时长未知，所以 15 秒只是内容选择，不是平台上限 |
| Amazon US | 已核对的是 shoppable video：1–12 分钟、≤5GB。主图视频位是否更短，发布前再看 Seller Central |

口播只说 65W、两个口、100-240V、不含线。2.5 词/秒只用来估英语时长。

---

## 6. 上架之后的回流（06 / 07）

闭环顺序不变：上架 → 广告与评论 → 只改出问题的那一环。

- **06**：用本节第 2 步的盈亏 ROAS 当尺子。eBay 这组假设下，广告前盈亏 ROAS 是 **1.97**。真实报表低于它，就先停加预算，不要先改标题。巴西站的「北京 11:00 休眠」节律不套用到美国或东南亚。
- **07**：若评论反复写 “thought a cable was included”，修补文案用英语加进描述和第 8 张图：`Cable not included.` 不要私信诱导删评。

---

## 7. 这条案例故意没做的事

| 没做 | 原因 |
|---|---|
| 给 Shopee SEA 一个佣金百分比 | 公开页是类目表或尚未核到 |
| 给 TikTok / Shopee 标题一个字符上限 | 卖家大学正文和 SG 教育页没有这个数字 |
| 承诺净利率 | 2% 退货和 5% 广告是预留，税也没算 |
| 把巴西滑板车的 PT-BR 文案翻译过来当英语站 | 英语站直接用英语写 |
