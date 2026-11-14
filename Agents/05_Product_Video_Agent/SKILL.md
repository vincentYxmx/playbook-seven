---
name: shopee-br-product-video
description: 跨境电商产品视频创作 Skill。默认站点为 Shopee SEA、TikTok Shop US/SEA、Amazon US、eBay US。覆盖脚本、分镜、AI 视频 Prompt、配音与字幕，并用脚本校验时长。硬时长以 video-specs.md 已核对的数字为准。当用户要"做产品视频 / 短视频带货 / 出分镜 / 配音稿字幕"时使用。
---

# 产品视频 Skill（05 Product Video Agent）

## 什么时候用

- 要为一等站点做商品视频。Shopee SG 的硬时长是 10–60 秒；eBay 建议约 1 分钟；TikTok 商品视频只核到 ≤5MB，时长未知
- 已有脚本/配音稿，要**校验时长是否达标、字幕是否超行**
- 要把脚本变成分镜表 + AI 视频 Prompt + 配音字幕包

## 三条底线（不可协商）

1. **不虚构参数** —— 台词里出现的每个数字必须来自 `spec_table`；
   溯源用 [`../03_Listing_Creative_Agent/scripts/spec_consistency.py`](../03_Listing_Creative_Agent/scripts/spec_consistency.py) 校验。
2. **时长与字幕交给脚本** —— 词数→时长的换算、字幕行长检查**不许自己心算**，
   一律跑 `scripts/video_timing.py`。超时**删词，不许提速语速**。
3. **买家可见文本必须是目标站点语言** —— 英语站直接用英语写，不要默认 PT-BR。

## 工作流

```text
[Step 1] 读 references/video-specs.md（平台视频规范）
[Step 2] 写脚本（15s / 30s 双版本，每句台词 = 一个分镜）
[Step 3] 跑 scripts/video_timing.py --target 15 / 30 校验
         → ❌ 超时/偏短：删词或加卖点句，改完重跑，直到 ✅
[Step 4] 跑 03 的 spec_consistency.py 校验台词数字
[Step 5] 出分镜表 + AI 视频 Prompt + 字幕文件（SRT）
```

## 命令速查

```bash
# 时长 + 字幕校验（最常用）
python scripts/video_timing.py --script 配音稿.txt --target 30

# 指定语速与字幕行宽
python scripts/video_timing.py --script 配音稿.txt --target 15 --wps 2.4 --subtitle-max 40
```

输出：逐句时间轴（起止秒）、总时长 vs 目标（±15% 容差）、字幕超行告警、
钩子检查（第一句 > 8 词 = 超出 3 秒黄金开场，告警）。

## 语速基准

**2.5 词/秒** 只是英语脚本的规划值，不是平台规定：
- 30s 版台词预算 ≈ **65 词**（留 4s 给留白与镜头切换）
- 15s 版台词预算 ≈ **30 词**（留 3s 留白）

> 语速因配音工具/主播而异，正式交付前按实际配音回听微调 `--wps`。

## 平台速记（详见 references/video-specs.md）

| 平台 | 已核对的时长 / 大小 | 语言 |
|---|---|---|
| Shopee SG | **10–60 秒**，MP4，≤30MB，≤1280×1280 | 英语 |
| TikTok Shop | 1 条，**≤5MB**。时长未知 | 站点语言 |
| Amazon US shoppable video | **1–12 分钟**，≤5GB。主图视频位是否更短：未知 | 英语 |
| eBay US | ≤150MB；建议约 1 分钟。变体刊登不支持视频 | 英语 |

平台数值为编写时公开规则，**发布前复核卖家中心原文**。

## 边界

- 本 Skill **不负责渲染**（交给 AI 视频工具/剪辑软件）与 BGM 版权采购
- 只产出：脚本、分镜表、Prompt、配音稿、字幕
