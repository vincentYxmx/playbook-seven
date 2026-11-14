# pricing-rules.md · 定价公式与口径

> 所有数字由 `scripts/sku_pricing.py` 计算。怀疑数字 → `[METRIC_SUSPECT]`。

---

## 公式

```text
广告前毛利 = 售价 − 到岸成本 − 售价×佣金% − 售价×退货损耗% − 售价×税率%
净利率     = (广告前毛利 − 售价×广告%) ÷ 售价
盈亏平衡价 = 到岸成本 ÷ (1 − 佣金% − 退货% − 税率%)
目标价     = 到岸成本 ÷ (1 − 佣金% − 退货% − 广告% − 目标毛利%)
优惠券余量 = 售价 × (实际净利率 − 目标毛利%)
```

**到岸成本** = 产品成本 + 头程 + 尾程 + 仓储（全塞进 `--cost` 一个参数，别拆开重复计）。

---

## 参数默认值与出处

费率表是 **2026-11-14** 的公开起步口径，来源在 `../scripts/platform_fees.json`。卖家必须按自己的类目复核。`return_pct=2` 和 `ad_pct=5` 是定价预留，不是平台费。`tax_pct` 默认 0，**不代算税**。

### 一等平台（默认路径）

| key | 佣金 | 能不能直接算 |
|---|---|---|
| `ebay_us` | 多数类目 **13.6%**（成交额 $7,500 以内）+ 每单 $0.30 / $0.40 | 可以，当作起步。类目例外、店铺费、sales tax 进基数，见 JSON notes |
| `tiktok_us` | 多数类目 **6%**。指定珠宝与 Pre-Owned 为 5% | 多数类目可以起步。例外用 `--commission`。公式不含税、含买家运费 |
| `amazon_us` | 按类目。公开页没有安全的单一百分比 | **拒绝计算**，直到传入 `--commission`。月费 $39.99 只提示 |
| `shopee_sg` / `shopee_my` / `shopee_th` / `shopee_id` / `shopee_vn` / `shopee_ph` | SG 有类目表；其余五站本次未核到单一费率 | **全部拒绝**，直到 `--commission` |
| `tiktok_sg` / `tiktok_my` / `tiktok_id` | 类目表。SG 交易费页面另写 3.27% | **拒绝**。交易费确认后用 `--extra-pct`，不要并进佣金 |
| `tiktok_th` / `tiktok_vn` / `tiktok_ph` | 未知 | **拒绝** |

```bash
python scripts/sku_pricing.py calc --platform ebay_us --cost 8 --price 24.99
python scripts/sku_pricing.py calc --platform tiktok_us --cost 8 --price 24.99
python scripts/sku_pricing.py calc --platform amazon_us --cost 8 --price 24.99 --commission 15
python scripts/sku_pricing.py --list-platforms
```

`--commission 15` 只是「卖家已经核对过自己的类目」之后的传参示例，**不是** Amazon 全类目费率。

### 参考平台（巴西 / Mercado Livre，非默认）

| key | 佣金 | 说明 |
|---|---|---|
| `shopee_br` | <R$80 → 20%；≥R$80 → 14%，外加阶梯固定费 | 只服务旧案例 |
| `mercadolivre_br` / `_premium` | 11% / 16% 口径 | 只服务旧案例 |
| `amazon_br` | 15% 多数类目口径 | 不是 `amazon_us` |
| `tiktok_br` | <R$50 → 10%；≥R$50 → 6%，另有 6% 免运计划 | 不是 `tiktok_us` |

### 未指定 `--platform` 时

脚本仍用历史 14% 佣金，并在 stderr 警告。这个 14% **不是** 任何一个一等站点的费率。

| 参数 | 默认 | 说明 |
|---|---|---|
| 退货损耗 | 2% | 工具箱预留，不是平台费 |
| 广告 | 5% | 定价预留。真实投放用 06 的盈亏线再核对 |
| 税 | 0% | 不代算。eBay 基数含 sales tax；TikTok US referral 不含税；其余看各页 |
| 目标毛利 | 32% | 公司自己的目标，不是平台规则 |

---

## 三个经典误判（脚本输出会提醒）

**① 引流款净利率低于目标 = 战略亏损？**
不一定。对照 `break_even_price`：只要售价在盈亏价之上就是赚钱的，
低于目标毛利只是「没赚到目标那么多」。引流款 27.5% vs 目标 32% 属正常策略。

**② 高配款净利率被主推款反超 = 定错了？**
常见现象：成本涨 34.8% 售价只涨 22.7%（配置涨价非线性）。
高配款的存在价值往往是**价格锚**，不一定是利润款 —— 但脚本会提醒你复核。

**③ 优惠券想发多少发多少？**
`coupon_headroom` 就是额度：净利率超目标的部分 × 售价。
主推款净利率 36.5%、目标 32% → 余量 R$ 98.52 → 发 R$100 券刚好贴着目标线。

---

## 价格阶梯判读

| 相邻价差 | 含义 |
|---|---|
| < 10% | 互相蚕食 —— 买家全买便宜的 |
| 10–35% | 健康阶梯（引流 → 主推常见 30%+） |
| > 50% | 中间留了空位给竞品 |
