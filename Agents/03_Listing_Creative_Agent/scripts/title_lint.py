#!/usr/bin/env python3
"""标题合规校验 —— 字符数是实测值，不是估算。

一等平台：
  python title_lint.py "65W GaN USB-C Charger, 2-Port" --platform amazon_us
  python title_lint.py "65W GaN USB-C Wall Charger 2 Port" --platform ebay_us
  python title_lint.py "65W GaN USB-C Charger 2 Port" --platform shopee_sg
  python title_lint.py "65W GaN USB-C Charger 2 Port" --platform tiktok_us

参考（不再是默认）：
  python title_lint.py "标题" --platform shopee_br_ref
  python title_lint.py "标题" --platform mercadolivre

未核到官方字符上限的站点只报告字数，不判超限 FAIL。
"""
import argparse
import json
import re
import sys

# limit=None：官方字符上限未核到，或必须按店铺/类目查。
# promo: fail = 官方明确禁止标题里的促销语；warn = 建议移出标题。
PLATFORMS = {
    "amazon_us": dict(
        limit=75, limit_note="非媒体类。2026-07-27 起 Seller Central 公告：除媒体类外标题 ≤75 字符（含空格）。媒体类用 --media。",
        first_n=None, promo="fail", emoji="fail",
        locale="en", repeat_gt=2,
        special="amazon",
    ),
    "ebay_us": dict(
        limit=80, limit_note="eBay Seller Center：标题 80 字符。",
        first_n=None, promo="warn", emoji="warn",
        locale="en", repeat_gt=None,
        special=None,
    ),
    "tiktok_us": dict(
        limit=None, limit_note="本次未在卖家大学正文核到 US 标题字符上限。内容禁则来自商品上架指南：不写促销、卖家 URL、未授权 TikTok 品牌。",
        first_n=None, promo="fail", emoji="fail",
        locale="en", repeat_gt=None,
        special=None,
    ),
    "tiktok_sg": dict(limit=None, limit_note="字符上限未核到。内容禁则同 TikTok Shop 上架指南。", first_n=None, promo="fail", emoji="fail", locale="en", repeat_gt=None, special=None),
    "tiktok_ph": dict(limit=None, limit_note="字符上限未核到。PH 卖家大学要求描述不少于 30 个词，标题禁促销与卖家 URL。", first_n=None, promo="fail", emoji="fail", locale="en", repeat_gt=None, special=None),
    "tiktok_my": dict(limit=None, limit_note="字符上限未核到。买家可见文本用英文或马来文，以类目/站点要求为准。", first_n=None, promo="fail", emoji="fail", locale="en", repeat_gt=None, special=None),
    "tiktok_th": dict(limit=None, limit_note="字符上限未核到。买家可见文本用泰语。", first_n=None, promo="fail", emoji="fail", locale="th", repeat_gt=None, special=None),
    "tiktok_id": dict(limit=None, limit_note="字符上限未核到。买家可见文本用印尼语。", first_n=None, promo="fail", emoji="fail", locale="id", repeat_gt=None, special=None),
    "tiktok_vn": dict(limit=None, limit_note="字符上限未核到。买家可见文本用越南语。", first_n=None, promo="fail", emoji="fail", locale="vi", repeat_gt=None, special=None),
    "shopee_sg": dict(limit=None, limit_note="字符上限按店铺调用 v2.product.get_item_limit。SG Mall 命名：Brand + specifications and type + model；禁促销词、全大写、表情与指定符号。", first_n=None, promo="fail", emoji="fail", locale="en", repeat_gt=None, special="shopee_mall_symbols"),
    "shopee_ph": dict(limit=None, limit_note="字符上限未核到，按店铺 get_item_limit。买家可见文本用英语。", first_n=None, promo="fail", emoji="fail", locale="en", repeat_gt=None, special="shopee_mall_symbols"),
    "shopee_my": dict(limit=None, limit_note="字符上限未核到，按店铺 get_item_limit。英语或马来语，以站点要求为准。", first_n=None, promo="fail", emoji="fail", locale="en", repeat_gt=None, special="shopee_mall_symbols"),
    "shopee_th": dict(limit=None, limit_note="字符上限未核到，按店铺 get_item_limit。买家可见文本用泰语。", first_n=None, promo="fail", emoji="fail", locale="th", repeat_gt=None, special="shopee_mall_symbols"),
    "shopee_id": dict(limit=None, limit_note="字符上限未核到，按店铺 get_item_limit。买家可见文本用印尼语。", first_n=None, promo="fail", emoji="fail", locale="id", repeat_gt=None, special="shopee_mall_symbols"),
    "shopee_vn": dict(limit=None, limit_note="字符上限未核到，按店铺 get_item_limit。买家可见文本用越南语。", first_n=None, promo="fail", emoji="fail", locale="vi", repeat_gt=None, special="shopee_mall_symbols"),
    "shopee_br_ref": dict(
        limit=120, limit_note="参考：历史巴西站规则卡 120 字符。不是东南亚默认。",
        first_n=30, promo="warn", emoji="fail",
        locale="pt", repeat_gt=None, special=None,
    ),
    "mercadolivre": dict(
        limit=60, limit_note="参考：Mercado Livre 60 字符。不再是默认平台。",
        first_n=None, promo="warn", emoji="warn",
        locale="pt", repeat_gt=None, special=None,
    ),
}

ALIASES = {
    "amazon": "amazon_us",
    "ebay": "ebay_us",
    "shopee_br": "shopee_br_ref",
}

PROMO_WORDS = [
    "free shipping", "best seller", "hot item", "sale", "discount", "% off",
    "limited time", "frete grátis", "frete gratis", "promoção", "promocao",
    "oferta", "imperdível", "imperdivel", "brinde", "desconto", "promo",
    "gratis ongkir", "diskon", "miễn phí vận chuyển", "giảm giá",
    "penghantaran percuma", "diskaun", "ส่งฟรี", "ลดราคา",
    "免费", "促销", "特价", "免运费",
]

AMAZON_SPECIAL = set("!$?_{}^¬¦")
# SG Mall 指南点名的符号：} ~ $ ^ { < ! * # ; % >
SHOPEE_MALL_CHARS = set("}~$^{<!*#;%>")

STOPWORDS = {
    "a", "an", "the", "and", "or", "for", "of", "to", "in", "on", "with",
    "by", "at", "from", "de", "da", "do", "das", "dos",
}

EMOJI_RE = re.compile("[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F900-\U0001F9FF]")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
THAI_RE = re.compile(r"[\u0e00-\u0e7f]")


def analyse(title, platform, args):
    p = PLATFORMS[platform]
    if args.media and platform == "amazon_us":
        p = dict(p)
        p["limit"] = None
        p["limit_note"] = "已加 --media。媒体类不在 75 字符规则内，精确上限本次未核到，请看 Seller Central 的 Product title requirements。"
    res = []
    t = title.strip()
    n = len(t)

    limit = p["limit"]
    if limit is None:
        res.append(("WARN", "length", f"{n} 字符。{p['limit_note']}"))
    elif n > limit:
        res.append(("FAIL", "length", f"{n} 字符 > 上限 {limit}。{p['limit_note']}"))
    else:
        res.append(("PASS", "length", f"{n}/{limit} 字符。{p['limit_note']}"))

    if p["first_n"]:
        res.append(("INFO", "first30", f"「{t[:p['first_n']]}」← 前 {p['first_n']} 字符（参考站规则卡）"))

    forbidden = list(args.forbidden or [])
    if isinstance(forbidden, str):
        forbidden = [w.strip() for w in forbidden.split(",") if w.strip()]
    if args.forbidden_file:
        try:
            with open(args.forbidden_file, encoding="utf-8") as f:
                forbidden += [ln.strip() for ln in f if ln.strip()]
        except OSError as e:
            res.append(("WARN", "forbidden", f"禁用词文件读不了：{e}"))
    hits = [w for w in forbidden if w and w.lower() in t.lower()]
    if hits:
        res.append(("FAIL", "forbidden", f"命中禁用词：{'、'.join(hits)}"))
    elif forbidden:
        res.append(("PASS", "forbidden", f"0 命中（查了 {len(forbidden)} 个词）"))

    if args.keywords:
        kws = [k.strip() for k in args.keywords.split(",") if k.strip()]
        missing = [k for k in kws if k.lower() not in t.lower()]
        if missing:
            res.append(("WARN", "keywords", f"核心词未覆盖：{'、'.join(missing)}"))
        else:
            res.append(("PASS", "keywords", f"{len(kws)} 个核心词全覆盖"))

    if EMOJI_RE.search(t):
        lv = "FAIL" if p["emoji"] == "fail" else "WARN"
        res.append((lv, "emoji", f"发现表情/符号：{EMOJI_RE.findall(t)[:5]}"))

    caps = [w for w in re.findall(r"[A-Za-z]{4,}", t) if w.isupper()]
    if caps:
        res.append(("WARN", "all_caps", f"全大写词：{'、'.join(caps[:6])}（品牌缩写需人工确认是否允许）"))

    promos = [w for w in PROMO_WORDS if w in t.lower()]
    if promos:
        lv = "FAIL" if p["promo"] == "fail" else "WARN"
        res.append((lv, "promo_words", f"促销词：{'、'.join(promos)}"))

    words = re.findall(r"[A-Za-zÀ-ÿ0-9]+", t.lower())
    dup3 = [w for w in set(words) if words.count(w) >= 3 and len(w) > 2]
    if dup3:
        res.append(("FAIL", "duplicates", f"重复 ≥3 次：{'、'.join(dup3)}"))
    if p["repeat_gt"] == 2:
        dup2 = [w for w in set(words) if words.count(w) > 2 and w not in STOPWORDS and len(w) > 1]
        if dup2:
            res.append(("FAIL", "word_repeat",
                        f"同一词超过 2 次：{'、'.join(dup2)}（Amazon 2025-01-21 标题规则；介词/冠词/连词除外，本清单只是辅助）"))

    if p["special"] == "amazon":
        bad = sorted({ch for ch in t if ch in AMAZON_SPECIAL})
        if bad:
            res.append(("FAIL", "special_chars",
                        f"Amazon 标题禁用字符：{''.join(bad)}（品牌名自带时需人工豁免）"))
    if p["special"] == "shopee_mall_symbols":
        bad = sorted({ch for ch in t if ch in SHOPEE_MALL_CHARS})
        if bad:
            res.append(("FAIL", "special_chars",
                        f"Shopee Mall 命名指南点名的符号：{''.join(bad)}"))

    locale = args.locale or p["locale"]
    if CJK_RE.search(t):
        res.append(("FAIL", "locale", "标题含中文。中文只用于内部备注；买家可见文本用目标站点语言。"))
    if locale == "th" and not THAI_RE.search(t):
        res.append(("WARN", "locale", "泰语站点标题里没有泰文字符。请改成泰语，或在确认可用英语时显式 --locale en。"))
    if locale == "en" and THAI_RE.search(t):
        res.append(("WARN", "locale", "当前 locale=en，标题里有泰文。确认站点后再改 --locale。"))

    ok = not any(lv == "FAIL" for lv, _, _ in res)
    return dict(platform=platform, locale=locale, chars=n, limit=limit, ok=ok,
                checks=res, first_30=t[:30])


def main():
    ap = argparse.ArgumentParser(description="标题合规校验（字符数实测，非估算）")
    ap.add_argument("title", nargs="?", help="标题文本；或用 --file 传入")
    ap.add_argument("--file", help="从文件读标题（一行一个，逐条校验）")
    ap.add_argument("--platform", required=True,
                    choices=sorted(set(PLATFORMS) | set(ALIASES) | {"shopee"}))
    ap.add_argument("--locale", help="覆盖站点默认语言：en / ms / th / id / vi / pt")
    ap.add_argument("--media", action="store_true", help="Amazon 媒体类：不套用 75 字符上限")
    ap.add_argument("--forbidden", help="禁用词，逗号分隔")
    ap.add_argument("--forbidden-file", help="禁用词文件（每行一个）")
    ap.add_argument("--keywords", help="核心关键词，逗号分隔")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.platform == "shopee":
        sys.exit("[INPUT_MISSING] Shopee 必须写站点：shopee_sg / shopee_my / shopee_th / "
                 "shopee_id / shopee_vn / shopee_ph。巴西参考用 shopee_br_ref。")
    platform = ALIASES.get(args.platform, args.platform)
    if args.platform in ALIASES and not args.json:
        print(f"ℹ️  --platform {args.platform} → {platform}", file=sys.stderr)
    titles = []
    if args.file:
        try:
            with open(args.file, encoding="utf-8") as f:
                titles = [ln.strip() for ln in f if ln.strip()]
        except OSError as e:
            sys.exit(f"[ERROR] 读不了文件：{e}")
    elif args.title:
        titles = [args.title]
    else:
        sys.exit("[ERROR] 给标题文本或 --file")

    reports = [analyse(t, platform, args) for t in titles]
    all_ok = all(r["ok"] for r in reports)

    if args.json:
        print(json.dumps(reports if len(reports) > 1 else reports[0],
                         ensure_ascii=False, indent=2))
    else:
        for r in reports:
            icon = {"PASS": "✅", "WARN": "⚠️ ", "FAIL": "❌", "INFO": "ℹ️ "}
            cap = "未知" if r["limit"] is None else str(r["limit"])
            print(f"\n「{r['first_30']}{'…' if r['chars'] > 30 else ''}」"
                  f"  [{r['platform']}  {r['chars']}/{cap} 字符  locale={r['locale']}]"
                  f"  总判定: {'✅ 通过' if r['ok'] else '❌ 未通过'}")
            for lv, name, detail in r["checks"]:
                print(f"  {icon[lv]} {name:<14} {detail}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
