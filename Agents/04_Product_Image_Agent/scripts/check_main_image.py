#!/usr/bin/env python3
"""像素级商品主图合规校验。

  python check_main_image.py 图.png --platform amazon_us
  python check_main_image.py 图.png --platform ebay_us
  python check_main_image.py 图.png --platform shopee_sea
  python check_main_image.py 图.png --platform tiktok
  python check_main_image.py 图.png --platform shopee --fix 修复后.png

`shopee` / `amazon` / `mercadolivre` 三个旧键保留，供既有夹具对照。
一等站点用 amazon_us、ebay_us、shopee_sea、tiktok。
只依赖 Pillow。未核到的硬阈值不判 FAIL。

检查项
  size_min        : 短边像素（低于平台最小值 = 直接 fail）
  square          : 宽高比 1:1（±1%，非正方形会被平台自动裁切）
  coverage        : 主体包围盒最长边 ÷ 图边（三平台要求不同，ML 最严 ~95%）
  white_bg        : 边缘 2% 带内近白像素占比（Amazon 必须 / Shopee 优先 / ML 不适用）
  bg_uniformity   : 边缘带主色占比（ML 的"背景干净"，informational）
  file_size       : 平台单图上限（Shopee 2MB 最严）

--fix 自动修复：近白像素拉到纯白、补成正方形、按目标占比重排画布。
  （ML 实景背景的"清理"需要抠图，脚本不做，会明确提示。）
"""
import argparse
import json
import os
import sys

try:
    from PIL import Image, ImageChops
except ImportError:
    sys.exit("需要 Pillow：pip install pillow")

# 平台阈值（来源：references/platform-*.md 规则卡）
PLATFORMS = {
    "shopee": dict(
        min_px=500, rec_px=1024, cover_min=0.60, cover_lo=0.70, cover_hi=0.92,
        white_fail=0.90, white_warn=0.98, uniform_info=0.90, max_mb=2, fix_target=0.80,
    ),
    "mercadolivre": dict(
        min_px=500, rec_px=1200, cover_min=0.80, cover_lo=0.85, cover_hi=0.97,
        white_fail=None, white_warn=None, uniform_info=0.90, max_mb=10, fix_target=0.88,
    ),
    "amazon": dict(
        min_px=1000, rec_px=2000, cover_min=0.85, cover_lo=0.85, cover_hi=0.97,
        white_fail=0.98, white_warn=0.99, uniform_info=0.90, max_mb=10, fix_target=0.87,
        square="warn", size_axis="long",
        white_note="Amazon 主图要纯白。本键把短边/长边 ≥1000 当作缩放档，正方形只警告：官方样式指南写的是最长边，不强制全类目 1:1。文件 10MB 是旧工具箱阈值，本次未在样式指南里复核。",
    ),
    "amazon_us": dict(
        min_px=1000, rec_px=1000, cover_min=0.85, cover_lo=0.85, cover_hi=0.97,
        white_fail=0.98, white_warn=0.99, uniform_info=0.90, max_mb=None, fix_target=0.87,
        square="warn", size_axis="long",
        white_note="主图纯白 RGB(255,255,255)，主体约 85%（Amazon 类目样式指南）。最长边 ≥1000px 来自 Industrial & Scientific 指南的缩放档；服饰指南写 1500px，以该类目指南为准。",
    ),
    "ebay_us": dict(
        min_px=500, rec_px=500, cover_min=None, cover_warn=None,
        white_fail=None, white_warn=None, uniform_info=0.90, max_mb=12, fix_target=0.85,
        square="skip", size_axis="long",
        white_note="eBay 未要求主图纯白。帮助页：至少 1 张、最多 24 张，单张 ≤12MB；高级刊登工具写最长边至少 500px。主体占比没有官方百分比。",
    ),
    "shopee_sea": dict(
        min_px=500, rec_px=500, cover_min=None, cover_warn=0.60,
        white_fail=None, white_warn=0.90, uniform_info=0.90, max_mb=2, fix_target=0.80,
        square="fail", size_axis="short",
        white_note="SG：1:1 仍必传；Media Space 单图 ≤2MB，JPG/JPEG/PNG。Mall 封面建议白/纯色、商品至少 60%、最低 500×500，且封面不叠促销字。非 Mall 不要把 60% 当成全站硬 FAIL。",
    ),
    "tiktok": dict(
        min_px=600, rec_px=600, cover_min=None, cover_warn=0.60,
        white_fail=None, white_warn=0.90, uniform_info=0.90, max_mb=None, fix_target=0.80,
        square="fail", size_axis="short",
        white_note="PH 卖家大学：最多 9 张正方形、至少 600×600、主图纯色（建议白）、商品至少占画面 60%、须完整正面。SG 上传说明要求纯白且无文字/水印。单图文件大小未核到（视频上限 5MB 不在本脚本）。",
    ),
}


def _min_channel(img):
    """每像素取 RGB 最小通道：dist = 255 - 该值，0 = 纯白。纯 Pillow 实现。"""
    r, g, b = img.convert("RGB").split()
    return ImageChops.darker(ImageChops.darker(r, g), b)


def _near_white_ratio(mc_img, tol):
    """近白像素占比（min channel >= 255-tol）。histogram 是 C 级实现，快。"""
    h = mc_img.histogram()
    total = sum(h)
    if not total:
        return 0.0
    return sum(h[256 - tol:]) / total


def analyse(img, plt_name, tol=3, product_thr=12, band_pct=0.02):
    p = PLATFORMS[plt_name]
    w, h = img.size
    mc = _min_channel(img)
    hist = mc.histogram()
    total = w * h

    # 主体包围盒：min channel < 255-thr 的像素 = 明显非白
    lut = [255 if v < 255 - product_thr else 0 for v in range(256)]
    bbox = mc.point(lut).getbbox()
    if bbox is None:
        return dict(width=w, height=h, coverage=0.0, bbox=None,
                    white_background=1.0, exact_ffffff=1.0, bg_uniformity=1.0)

    x0, y0, x1, y1 = bbox
    bw, bh = x1 - x0 + 1, y1 - y0 + 1
    coverage = max(bw / w, bh / h)

    # 边缘 2% 带（四条），分别算近白占比与主色占比
    band = max(2, round(min(w, h) * band_pct))
    strips = [img.crop((0, 0, w, band)), img.crop((0, h - band, w, h)),
              img.crop((0, 0, band, h)), img.crop((w - band, 0, w, h))]
    mc_strips = [_min_channel(s) for s in strips]
    white_bg = sum(_near_white_ratio(m, tol) for m in mc_strips) / len(mc_strips)

    uni = []
    for s in strips:
        q = s.convert("RGB").quantize(colors=8)
        cols = q.getcolors(maxcolors=256) or []
        tot = sum(c for c, _ in cols)
        uni.append((max(c for c, _ in cols) / tot) if tot else 0.0)
    bg_uniformity = sum(uni) / len(uni)

    # 纯白占背景像素比（informational）
    product_px = sum(hist[:256 - product_thr])
    bg_px = total - product_px
    exact = (hist[255] / bg_px) if bg_px else 0.0

    return dict(width=w, height=h, coverage=round(coverage, 4), bbox=list(bbox),
                white_background=round(white_bg, 4), exact_ffffff=round(exact, 4),
                bg_uniformity=round(bg_uniformity, 4))


def check(img, path, plt_name, args):
    p = PLATFORMS[plt_name]
    m = analyse(img, plt_name, tol=args.tolerance)
    res = []          # (级别, 检查项, 说明)

    def add(level, name, detail):
        res.append((level, name, detail))

    # 尺寸。size_axis=long 时用最长边（eBay / Amazon 样式指南的写法）。
    axis = p.get("size_axis", "short")
    px = max(m["width"], m["height"]) if axis == "long" else min(m["width"], m["height"])
    side = "长边" if axis == "long" else "短边"
    if px < p["min_px"]:
        add("FAIL", "size_min", f"{side} {px}px < 平台最低 {p['min_px']}px")
    elif px < p["rec_px"]:
        add("WARN", "size_min", f"{side} {px}px 达最低但低于推荐 {p['rec_px']}px")
    else:
        add("PASS", "size_min", f"{side} {px}px ≥ 推荐 {p['rec_px']}px")

    # 正方形：fail = 官方要求 1:1；warn = 不强制；skip = 不检查
    ratio = abs(m["width"] - m["height"]) / max(m["width"], m["height"])
    square_mode = p.get("square", "fail")
    if square_mode == "skip":
        add("INFO", "square", f"{m['width']}×{m['height']}（本平台不要求 1:1）")
    elif ratio > 0.01:
        lv = "FAIL" if square_mode == "fail" else "WARN"
        add(lv, "square", f"{m['width']}×{m['height']} 非正方形")
    else:
        add("PASS", "square", "1:1")

    # 主体占比。cover_min 才是硬 FAIL；只有 cover_warn 时降为警告。
    c = m["coverage"]
    if p.get("cover_min") is None:
        warn_at = p.get("cover_warn")
        if warn_at and c < warn_at:
            add("WARN", "coverage", f"{c:.0%} < {warn_at:.0%}（Mall / 主图建议值，不是已核实的全站硬阈值）")
        else:
            add("INFO", "coverage", f"{c:.0%}（本预设没有全站硬性占比）")
    elif c < p["cover_min"]:
        add("FAIL", "coverage", f"{c:.0%} < 平台下限 {p['cover_min']:.0%}")
    elif c < p["cover_lo"] or c > p["cover_hi"]:
        add("WARN", "coverage", f"{c:.0%} 超出甜区 {p['cover_lo']:.0%}–{p['cover_hi']:.0%}")
    else:
        add("PASS", "coverage", f"{c:.0%}")

    # 背景纯白
    if p["white_fail"] is not None:
        wb = m["white_background"]
        if wb < p["white_fail"]:
            add("FAIL", "white_bg", f"边缘带近白 {wb:.1%} < {p['white_fail']:.0%}")
        elif wb < p["white_warn"]:
            add("WARN", "white_bg", f"边缘带近白 {wb:.1%}（接近但未达 {p['white_warn']:.0%}，常见于灰底/米底）")
        else:
            add("PASS", "white_bg", f"{wb:.1%}")
    else:
        add("INFO", "white_bg", p.get("white_note", "本预设不把纯白当作硬性 FAIL"))

    # 背景均匀度（ML 的"背景干净"）
    u = m["bg_uniformity"]
    if u < 0.60:
        add("WARN", "bg_uniformity", f"边缘带主色仅 {u:.0%} —— 背景可能杂乱（ML：avoid messy backgrounds）")
    elif u < p["uniform_info"]:
        add("WARN", "bg_uniformity", f"边缘带主色 {u:.0%}，背景略花")
    else:
        add("PASS", "bg_uniformity", f"{u:.0%} —— 背景干净")

    # 文件大小
    mb = os.path.getsize(path) / 1048576 if os.path.exists(path) else 0
    if p.get("max_mb") is None:
        add("INFO", "file_size", f"{mb:.2f} MB（官方单图上限未核到，不判 FAIL）")
    elif mb > p["max_mb"]:
        add("FAIL", "file_size", f"{mb:.2f} MB > 上限 {p['max_mb']} MB")
    else:
        add("PASS", "file_size", f"{mb:.2f} MB ≤ {p['max_mb']} MB")

    # 无法自动检测的项 → 人工确认
    if plt_name == "mercadolivre":
        add("MANUAL", "ml_cover_text", "首图禁促销文字/平台属性词/水印/边框 —— 人工确认")
    if plt_name == "shopee":
        add("MANUAL", "shopee_text_ratio", "图内文字 ≤ 画面 20% 且不大于主体 —— 人工确认（旧巴西向夹具）")
    if plt_name == "shopee_sea":
        add("MANUAL", "cover_text", "Mall 封面不叠促销字、水印、装饰边框 —— 人工确认")
    if plt_name in ("amazon", "amazon_us"):
        add("MANUAL", "main_text", "主图不得有文字、Logo、水印、不包含的配件 —— 人工确认")
    if plt_name == "ebay_us":
        add("MANUAL", "main_photo", "主图应完整正面展示在售商品；瑕疵用附图标出。不造官方未写的占比阈值。")
    if plt_name == "tiktok":
        add("MANUAL", "main_text", "主图须为实物正面，SG 规则另禁文字与水印 —— 人工确认")

    ok = not any(lv == "FAIL" for lv, _, _ in res)
    return dict(platform=plt_name, ok=ok, metrics=m, checks=res)


def fix(img, plt_name, out_path, args):
    p = PLATFORMS[plt_name]
    target = p["fix_target"]
    w, h = img.size
    mc = _min_channel(img)

    # 1) 近白拉纯白（仅对白底平台）
    if p["white_fail"] is not None:
        snap_tol = max(8, args.tolerance + 5)
        mask = mc.point([255 if v >= 255 - snap_tol else 0 for v in range(256)])
        white = Image.new("RGB", img.size, (255, 255, 255))
        img = Image.composite(white, img.convert("RGB"), mask)

    # 2) 按主体包围盒重排画布到目标占比
    mc2 = _min_channel(img)
    lut = [255 if v < 255 - args.tolerance else 0 for v in range(256)]
    bbox = mc2.point(lut).getbbox()
    if bbox:
        product = img.crop(bbox)
        pw, ph = product.size
        side = int(max(pw, ph) / target)
        canvas_bg = (255, 255, 255) if p["white_fail"] is not None else _dominant_bg(img, bbox)
        canvas = Image.new("RGB", (side, side), canvas_bg)
        canvas.paste(product, ((side - pw) // 2, (side - ph) // 2))
        img = canvas

    # 3) 放大到推荐尺寸
    rec = p["rec_px"]
    if img.size[0] < rec:
        img = img.resize((rec, rec), Image.LANCZOS)

    img.save(out_path, quality=92)
    return img


def _dominant_bg(img, bbox):
    """取包围盒外的主色，作为 ML 画布底色（保持原背景感）。"""
    w, h = img.size
    x0, y0, x1, y1 = bbox
    strips = [img.crop((0, 0, w, max(1, y0))), img.crop((0, y1, w, h)),
              img.crop((0, 0, max(1, x0), h)), img.crop((x1, 0, w, h))]
    strips = [s for s in strips if s.size[0] > 0 and s.size[1] > 0]
    if not strips:
        return (255, 255, 255)
    best, best_n = (255, 255, 255), -1
    for s in strips:
        q = s.convert("RGB").quantize(colors=4)
        pal = q.getpalette() or []
        for cnt, idx in (q.getcolors(maxcolors=8) or []):
            if cnt > best_n:
                best_n = cnt
                best = tuple(pal[idx * 3: idx * 3 + 3])
    return best


def main():
    ap = argparse.ArgumentParser(description="商品主图像素级合规校验")
    ap.add_argument("image")
    ap.add_argument("--platform", required=True, choices=list(PLATFORMS),
                    help="shopee / mercadolivre / amazon")
    ap.add_argument("--tolerance", type=int, default=3, help="近白判定容差（默认 3）")
    ap.add_argument("--fix", metavar="OUT", help="自动修复并保存到指定路径")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    if not os.path.exists(args.image):
        sys.exit(f"[ERROR] 文件不存在：{args.image}")
    img = Image.open(args.image)

    report = check(img, args.image, args.platform, args)

    if args.fix:
        fixed = fix(img, args.platform, args.fix, args)
        re_report = check(fixed, args.fix, args.platform, args)
        report["fixed_to"] = args.fix
        report["after_fix_ok"] = re_report["ok"]
        report["after_fix_checks"] = re_report["checks"]

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        icon = {"PASS": "✅", "WARN": "⚠️ ", "FAIL": "❌", "INFO": "ℹ️ ", "MANUAL": "👤"}
        print(f"\n平台: {args.platform}   尺寸: {report['metrics']['width']}×"
              f"{report['metrics']['height']}   总判定: {'✅ 通过' if report['ok'] else '❌ 未通过'}\n")
        for lv, name, detail in report["checks"]:
            print(f"  {icon[lv]} {name:<16} {detail}")
        if args.fix:
            print(f"\n已修复 → {args.fix}   修复后判定: "
                  f"{'✅ 通过' if report.get('after_fix_ok') else '❌ 仍有 FAIL 项'}")
    sys.exit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
