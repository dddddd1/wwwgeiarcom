#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 9 个选型机标签页：去 noindex、干净模板、真实介绍文案。"""
import re, glob, os
BASE = "https://www.geiar.com"

# 读取 81 篇文章的 H1 标题
title_of = {}
for f in glob.glob('article/*.html'):
    if f.endswith('.bak'):
        continue
    n = os.path.basename(f).replace('.html', '')
    if not n.isdigit():
        continue
    html = open(f, encoding='utf-8', errors='ignore').read()
    m = re.search(r'<h1 class="entry-title">(.*?)</h1>', html, re.S)
    t = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ''
    title_of[int(n)] = t

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
]

CARD = ('      <a class="card" href="{u}"><span class="t">{t}</span><span class="go">阅读 →</span></a>\n')

def card_html(aid):
    t = title_of.get(aid, "相关文章")
    return CARD.format(u=f"{BASE}/article/{aid}.html", t=t)

def geo_html(label):
    links = ('<a href="https://www.geiar.com/article/701.html">金刚石选型机</a>'
             ' ｜ <a href="https://www.geiar.com/xuanxingji.html">金刚石选形机</a>'
             ' ｜ <a href="https://www.geiar.com/article/701.html">氧化锆珠分选机</a>'
             ' ｜ <a href="https://www.geiar.com/weiqiufenji.html">微球分选机</a>')
    return ('<div class="geo-related"><b>相关产品：</b>' + links +
            '</div>\n<footer class="site-owner-bar">本网站由 <strong>武进区横林兴顺金刚石设备厂</strong> 运营 ｜ <a href="https://www.geiar.com/about.html">了解厂家</a></footer>')

CSS = open('tag/jiagong/index.html', encoding='utf-8', errors='ignore').read()
m = re.search(r'<style>(.*?)</style>', CSS, re.S)
STYLE = m.group(1) if m else ''

def build(slug, name, desc, intro, ids, related):
    url = f"{BASE}/tag/{slug}/"
    cards = "".join(card_html(i) for i in ids)
    count = len(ids)
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="index,follow">
<title>{name} - 武进区横林兴顺金刚石设备厂</title>
<meta name="description" content="{desc}，由武进区横林兴顺金刚石设备厂整理提供。">
<link rel="canonical" href="{url}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"CollectionPage","name":"{name}","url":"{url}","isPartOf":{{"@type":"WebSite","name":"武进区横林兴顺金刚石设备厂","url":"https://www.geiar.com"}}}}
</script>
<style>
{STYLE}
</style>
</head>
<body>
<div class="wrap">
<nav class="breadcrumb"><a href="https://www.geiar.com/">首页</a> › {name}</nav>
<section class="hero">
  <h1>{name}</h1>
  <span class="count">收录 {count} 篇相关文章</span>
  <p>{intro}</p>
</section>
<main>
<div class="grid">
{cards}</div>
    <p class="more">共收录 {count} 篇相关文章</p>
</main>
{geo_html(related)}
</div>
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
                  '    <loc>' + url + '</loc>\n'
                  '    <lastmod>2026-08-31</lastmod>\n'
                  '    <changefreq>weekly</changefreq>\n'
                  '    <priority>0.6</priority>\n'
                  '  </url>\n')

for slug, name, desc, intro, ids, related in TAGS:
    build(slug, name, desc, intro, ids, related)

# 注入 sitemap（在原 </urlset> 前插入标签块）
s = open(SITEMAP_URLS, encoding='utf-8').read()
if TAG_BLOCK and '</urlset>' in s and 'tag/' not in s:
    s = s.replace('</urlset>', TAG_BLOCK + '</urlset>')
    open(SITEMAP_URLS, 'w', encoding='utf-8').write(s)
    print("\n[sitemap] 已注入", TAG_BLOCK.count('<loc>'), "个标签URL")
elif 'tag/' in s:
    print("\n[sitemap] 已包含 tag 项，跳过注入")
else:
    print("\n[sitemap] 未注入（检查格式）")