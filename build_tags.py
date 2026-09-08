#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 9 个选型机标签页：全站统一模板（文章页同款头部/侧边栏/底部 + content-list 列表）。"""
import re, glob, os
from datetime import date
BASE = "https://www.geiar.com"

# 读取 81 篇文章的 H1 标题 / 描述 / 发布日期
articles = {}
for f in glob.glob('article/*.html'):
    n = os.path.basename(f).replace('.html', '')
    if not n.isdigit():
        continue
    with open(f, encoding='utf-8', errors='ignore') as r:
        html = r.read()
    m = re.search(r'<h1 class="entry-title">(.*?)</h1>', html, re.S)
    t = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ''
    md = re.search(r'<meta name="description" content="([^"]*)"', html)
    d = md.group(1).strip() if md else ''
    dt = re.search(r'og:release_date" content="(\d{4}-\d{2}-\d{2})"', html)
    articles[int(n)] = (t, d, dt.group(1) if dt else '')

# 标签定义: slug -> (展示名, description, intro段落, [文章id], 相关产品块)
TAGS = [
    ("jingangshixuanxingji", "金刚石选型机",
     "金刚石选型机、金刚石选形机相关文章合集",
     "金刚石选型机（又称金刚石选形机）是用于金刚石微粉、CBN 等超硬磨料基于圆度与粒径进行高效分选的专用设备，以物理分选替代人工挑选，显著提升超硬材料精制与分级环节的成品率与批次一致性。本标签汇总金刚石选型机的工作原理、技术参数、价格、选型指南、维护保养等文章，帮助快速建立选型与采购认知。",
     [1, 3, 6, 13, 17, 22, 26, 38, 43, 47, 52, 56, 65, 81, 85, 111, 119, 151, 173, 700, 701],
     "金刚石选型机 · 金刚石选形机"),
    ("yanghuagaozhushaifenji", "氧化锆珠筛分机",
     "氧化锆珠筛分机、氧化锆珠分选机相关文章合集",
     "氧化锆珠筛分机用于对氧化锆珠、陶瓷磨介按粒径与圆度进行高精度分选，广泛应用于砂磨介质、研磨珠的精制分级。本标签汇总氧化锆珠筛分机的工作原理、分选精度、技术参数、价格、选型指南与维护保养等文章，便于比对选型。",
     [2, 5, 9, 10, 12, 16, 29, 30, 33, 37, 42, 46, 51, 55, 60, 64, 68, 71, 103, 163],
     "氧化锆珠筛分机 · 微球分选机"),
    ("bolizhuxuanqiuji", "玻璃珠选球机",
     "玻璃珠选球机相关文章合集",
     "玻璃珠选球机专用于玻璃珠、小玻璃丸等球状颗粒的高效自动分选，通过旋转盘面实现按圆度与粒径自动分级。本标签汇总玻璃珠选球机的工作原理、技术参数、价格、常见型号、选型指南、如何维护保养与设备优势等文章。",
     [4, 7, 8, 15, 19, 20, 24, 28, 32, 36, 45, 50, 54, 58, 63, 67, 113, 153, 157, 171],
     "玻璃珠选球机 · 选球机"),
    ("gangzhuxuanqiuji", "钢珠选球机",
     "钢珠选球机相关文章合集",
     "钢珠选球机用于钢珠、钢丸、轴承用球等高耐磨球状颗粒的自动分选，保证批次圆度一致性与生产效率。本标签汇总钢珠选球机的工作原理、技术参数、价格、常见型号、选型指南、维护保养与生产线配置等文章。",
     [14, 18, 23, 27, 35, 39, 40, 44, 48, 53, 57, 62, 66, 70, 77, 91, 95, 161, 165, 176],
     "钢珠选球机 · 选球机"),
    ("changjiazhixiao", "厂家直销",
     "厂家直销类文章合集（本地原厂，支持来样试机）",
     "选型机和分选机厂家直销，意味着一手价格、直接技术对接与来样试机支持，减少中间环节、降低成本与沟通损耗。本标签汇总 金刚石选型机、氧化锆珠筛分机、玻璃珠选球机、钢珠选球机 的厂家直销相关文章。",
     [8, 13, 35, 42],
     "厂家直销"),
    ("xuanxingzhinan", "选型指南",
     "选型指南类文章合集（怎么选、选型要点）",
     "设备选型不是只看价格，还要看粒径范围、处理量、分选精度与场地条件。本标签汇总金刚石选型机、氧化锆珠筛分机、玻璃珠选球机、钢珠选球机的选型指南与「怎么选」文章，帮你在采购前理清需求、减少踩坑。",
     [700, 7, 12, 70, 119],
     "选型指南"),
    ("weihubaoyang", "维护保养",
     "维护保养类文章合集（如何维护保养、操作规程）",
     "适度维护能显著延长选型机、分选机与选球机的使用寿命，保持分选精度稳定。本标签汇总金刚石选型机、氧化锆珠筛分机、玻璃珠选球机、钢珠选球机的维护保养与操作规程相关文章。",
     [17, 38, 39, 46, 67, 163, 165, 171],
     "维护保养"),
    ("jiage", "价格",
     "价格类文章合集（多少钱一台、价格构成）",
     "分选设备价格受机型规格、分选精度、接触件材质与是否非标定制等因素影响。本标签汇总金刚石选型机、氧化锆珠筛分机、玻璃珠选球机、钢珠选球机 的价格与「多少钱一台」相关文章，供参考比价。",
     [19, 26, 33, 48, 55, 62, 111, 113],
     "价格"),
    ("tuijianchangjia", "推荐厂家",
     "推荐厂家、哪家好类文章合集",
     "选购选型机、分选机与选球机时，厂家是否支持来样试机、是否可非标定制、售后是否及时都是关键。本标签汇总金刚石选型机、氧化锆珠筛分机、玻璃珠选球机、钢珠选球机 的推荐厂家与「哪家好」相关文章。",
     [2, 20, 32, 56, 68, 77, 173, 176],
     "推荐厂家"),
    ("gongzuoyuanli", "工作原理",
     "工作原理类文章合集（怎么分选、怎么工作）",
     "想用好分选设备，先弄懂原理：金刚石选型机、氧化锆珠筛分机、玻璃珠选球机、钢珠选球机通过圆盘旋转与离心力实现按圆度、粒径自动分级。本标签汇总四类设备的工作原理详解文章，帮你判断分选精度与处理量是否满足需求。",
     [1, 10, 18, 54],
     "金刚石选型机 · 氧化锆珠筛分机 · 微球分选机"),
]

def entry_html(aid, tag_name):
    t, d, dt = articles.get(aid, ("相关文章", "", ""))
    meta = f'<span class="entry-category">{tag_name}</span>'
    if dt:
        meta += f'<span class="entry-date">{dt}</span>'
    return (f'<div class="clear post type-post status-publish hentry">'
            f'<h2 class="entry-title"><a href="{BASE}/article/{aid}.html">{t}</a></h2>'
            f'<div class="entry-overview">'
            f'<div class="entry-summary">{d[:100]}</div>'
            f'<div class="entry-meta">{meta}</div>'
            f'</div></div>\n')

# 产品名 -> 落地页/聚合页链接（同一页面内不出现重复 URL）
PRODUCT_LINKS = {
    "金刚石选型机": "/xuanxingji.html",
    "金刚石选形机": "/article/701.html",
    "氧化锆珠筛分机": "/article/701.html",
    "微球分选机": "/weiqiufenji.html",
    "玻璃珠选球机": "/article/701.html",
    "钢珠选球机": "/article/701.html",
}
DEFAULT_PRODUCTS = ["金刚石选型机", "氧化锆珠筛分机", "微球分选机"]

def geo_html(related):
    names = [n.strip() for n in related.split('·') if n.strip() in PRODUCT_LINKS]
    if not names:
        names = DEFAULT_PRODUCTS
    links = ' ｜ '.join(f'<a href="{BASE}{PRODUCT_LINKS[n]}">{n}</a>' for n in names)
    return (f'<div class="geo-related" data-geo-related="1" style="margin:18px 0;padding:12px 16px;'
            f'border:1px solid #e5e5e5;border-radius:8px;background:#fafafa;font-size:14px">'
            f'<b>相关产品：</b>{links}</div>')

# 从文章页提取全站统一的头部/侧边栏/底部/样式组件，保证与其他页面一致
_src = next(f for f in sorted(glob.glob('article/*.html'))
            if os.path.basename(f)[:-5].isdigit())
with open(_src, encoding='utf-8', errors='ignore') as r:
    _h = r.read()
_b = re.search(r'<body.*?>(.*)</body>', _h, re.S).group(1)
HEADER = re.search(r'<header class="sp-hdr">.*?</header>', _b, re.S).group(0)
SIDEBAR = re.search(r'<aside id="secondary".*?</aside>', _b, re.S).group(0)
FOOTER = re.search(r'<footer class="sp-ftr">.*?</footer>', _b, re.S).group(0)
SP_STYLE = next(s for s in re.findall(r'<style>.*?</style>', _h, re.S) if 'sp-hdr' in s)
TAG_INTRO_STYLE = ('<style>.tag-intro{margin:0 0 25px;padding:14px 16px;background:#fafafa;'
                   'border:1px solid #e5e5e5;border-radius:8px;font-size:14px;line-height:1.8;color:#444}'
                   '.tag-intro p{margin:0}</style>')

def build(slug, name, intro, ids, related):
    url = f"{BASE}/tag/{slug}/"
    entries = "".join(entry_html(i, name) for i in ids)
    count = len(ids)
    # 相关标签：链接到其余标签页（与文章页尾部的相关标签区块同款样式）
    others = "".join(f'<a style="color:#b96;text-decoration:none;margin-right:16px" '
                     f'href="{BASE}/tag/{s2}/" title="查看 全部 {n2} 相关文章">#{n2}</a>'
                     for s2, n2, *_ in TAGS if s2 != slug)
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="applicable-device" content="pc,mobile">
<meta name="MobileOptimized" content="width" />
<meta name="HandheldFriendly" content="true" />
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=0">
<meta name="robots" content="index,follow">
<title>标签：{name}_武进区横林兴顺金刚石设备厂</title>
<meta name="description" content="{intro}">
<meta property="og:type" content="website">
<meta property="og:title" content="{name}">
<meta property="og:description" content="{intro}">
<meta property="og:url" content="{url}">
<link rel="stylesheet" type="text/css" href="{BASE}/public2/assets/002/css/mipcms.css">
<link rel="stylesheet" type="text/css" href="{BASE}/public2/assets/002/css/style.css">
<link rel="stylesheet" type="text/css" href="{BASE}/public2/assets/002/css/genericons.css">
<link rel="stylesheet" type="text/css" href="{BASE}/public2/assets/002/css/responsive.css">
<link rel="canonical" href="{url}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"CollectionPage","name":"{name}","url":"{url}","isPartOf":{{"@type":"WebSite","name":"武进区横林兴顺金刚石设备厂","url":"{BASE}"}}}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"网站首页","item":"{BASE}/"}},{{"@type":"ListItem","position":2,"name":"{name}","item":"{url}"}}]}}
</script>
{SP_STYLE}
{TAG_INTRO_STYLE}
</head>
<body>
<div id="page" class="site">
{HEADER}
<div id="content" class="site-content container clear"><!--主内容 -->
<div id="primary" class="content-area clear">
<main id="main" class="site-main clear">
<div class="breadcrumbs clear"><h1>标签：{name}</h1></div>
<div class="tag-intro"><p>{intro}</p></div>
<div id="recent-content" class="content-list">
{entries}</div>
</main>
</div><!--侧边栏-->
{SIDEBAR}
</div><!--底部 -->
<div style="max-width:1080px;margin:0 auto;padding:16px 18px 4px;color:#666;font-size:14px;line-height:2"><strong>相关标签：</strong>{others}</div>
{FOOTER}
</div><!-- #page -->
{geo_html(related)}
</body>
</html>'''
    os.makedirs(f'tag/{slug}', exist_ok=True)
    with open(f'tag/{slug}/index.html', 'w', encoding='utf-8') as w:
        w.write(html)
    print(f"[生成] tag/{slug}/index.html  -> {name} ({count} 篇)")
    # 更新 sitemap
    update_sitemap(url)

SITEMAP_URLS = 'sitemap.xml'
TAG_BLOCK = ''

def update_sitemap(url):
    global TAG_BLOCK
    TAG_BLOCK += ('  <url>\n'
                  f'    <loc>{url}</loc>\n'
                  f'    <lastmod>{date.today().isoformat()}</lastmod>\n'
                  '    <changefreq>weekly</changefreq>\n'
                  '    <priority>0.6</priority>\n'
                  '  </url>\n')

for slug, name, _, intro, ids, related in TAGS:
    build(slug, name, intro, ids, related)

# 同步 sitemap：先移除旧 tag 条目再注入，可重复执行，新增标签也能进入 sitemap
if TAG_BLOCK:
    with open(SITEMAP_URLS, encoding='utf-8') as r:
        s = r.read()
    s2 = re.sub(r'  <url>\n    <loc>[^<]*/tag/[^<]*</loc>.*?</url>\n', '', s, flags=re.S)
    s2 = s2.replace('</urlset>', TAG_BLOCK + '</urlset>')
    if s2 != s:
        with open(SITEMAP_URLS, 'w', encoding='utf-8') as w:
            w.write(s2)
        print("\n[sitemap] 已同步", TAG_BLOCK.count('<loc>'), "个标签URL")
    else:
        print("\n[sitemap] 无变化")
else:
    print("\n[sitemap] 无标签需要注入")