#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全站统一头部/页脚：替换 MIP masthead/colophon 为干净响应式 sp-hdr/sp-ftr。"""
import glob, re

SP_CSS = '''
<style>
.sp-hdr{background:#111;position:sticky;top:0;z-index:60}
.sp-hdr-in{max-width:1080px;margin:0 auto;padding:0 18px;display:flex;align-items:center;justify-content:space-between;min-height:56px;gap:12px}
.sp-hdr-logo{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font-weight:600;font-size:15px;min-width:0}
.sp-hdr-logo img{height:34px;width:auto;flex:none}
.sp-hdr-logo span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sp-nav-sw{display:none}
.sp-hamb{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:6px 4px}
.sp-hamb span{display:block;width:24px;height:2px;background:#fff;transition:.28s}
.sp-nav-list{list-style:none;display:flex;gap:18px;margin:0;padding:0}
.sp-nav-list a{color:#cfd3da;text-decoration:none;font-size:14px;white-space:nowrap;transition:color .2s}
.sp-nav-list a:hover{color:#fff}
.sp-ftr{background:#111;color:#9aa0a6;text-align:center;font-size:13px;padding:24px 16px;line-height:2.1}
.sp-ftr a{color:#cfd3da;text-decoration:none}
.sp-ftr a:hover{color:#fff}
@media(max-width:760px){
  .sp-hdr{position:relative}
  .sp-hamb{display:flex}
  .sp-nav{position:absolute;left:0;right:0;top:56px;background:#111;display:none;box-shadow:0 10px 18px rgba(0,0,0,.3)}
  .sp-nav-list{flex-direction:column;gap:0;padding:6px 18px 14px}
  .sp-nav-list li{border-bottom:1px solid rgba(255,255,255,.08)}
  .sp-nav-list li:last-child{border-bottom:0}
  .sp-nav-list a{display:block;padding:13px 0}
  .sp-nav-sw:checked~.sp-nav{display:block}
  .sp-nav-sw:checked~.sp-hamb span:nth-child(1){transform:translateY(7px) rotate(45deg)}
  .sp-nav-sw:checked~.sp-hamb span:nth-child(2){opacity:0}
  .sp-nav-sw:checked~.sp-hamb span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
}
</style>
'''

HDR = '<header class="sp-hdr"><div class="sp-hdr-in"><a class="sp-hdr-logo" href="https://www.geiar.com/index.html"><img src="https://www.geiar.com/public2/assets/002/img/logo.jpg" alt="金刚石选型机选形机专业厂家"> <span>金刚石选型机选形机专业厂家</span></a><input type="checkbox" id="sp-nav-sw" class="sp-nav-sw"><label class="sp-hamb" for="sp-nav-sw" aria-label="展开菜单"><span></span><span></span><span></span></label><nav class="sp-nav" aria-label="主导航"><ul class="sp-nav-list"><li><a href="https://www.geiar.com">首页</a></li><li><a href="https://www.geiar.com/xuanxingji.html">金刚石选形机</a></li><li><a href="https://www.geiar.com/article/701.html">金刚石选型机</a></li><li><a href="https://www.geiar.com/article/701.html">氧化锆珠分选机</a></li><li><a href="https://www.geiar.com/weiqiufenji.html">微球分选机</a></li><li><a href="https://www.geiar.com/about.html">关于厂家</a></li></ul></nav></div></header>'

FTR = '<footer class="sp-ftr"><div>© 2023 武进区横林兴顺金刚石设备厂 · 金刚石选型机／金刚石选形机／氧化锆珠分选机／微球分选机厂家 · <a href="https://www.geiar.com/sitemap.xml">网站地图</a></div><div>联系电话：<a href="tel:13506122530">13506122530</a>（邓经理）· 欢迎来样试机与实地考察</div></footer>'

files = [f for f in glob.glob('article/*.html') if not f.endswith('.bak')] \
      + [f'article/page/{n}.html' for n in range(2, 8)] \
      + ['index.html']

stat = {}
for fn in files:
    c = open(fn, encoding='utf-8', errors='ignore').read()
    o = c
    # 替换 header
    c, nh = re.subn(r'<header id="masthead".*?</header>', HDR, c, count=1, flags=re.S)
    # 替换 footer
    c, nf = re.subn(r'<footer id="colophon".*?</footer>', FTR, c, count=1, flags=re.S)
    # 头部CSS(仅当尚无 sp-hdr 样式块时)
    if '.sp-hdr{' not in c:
        ne = 0
        if '</head>' in c:
            c = c.replace('</head>', SP_CSS.rstrip() + '\n</head>', 1)
            ne = 1
    else:
        ne = 0
    if c != o:
        open(fn, 'w', encoding='utf-8').write(c)
    stat[fn] = (nh, nf, '.sp-hdr{' in c)
    print(f"[{fn}] header={nh} footer={nf} css={'Y' if '.sp-hdr{' in c else 'N'}")

bad = [ (f,v) for f,v in stat.items() if v[0]!=1 or v[1]!=1 or not v[2] ]
print("\n异常项(应为空):", bad if bad else "无")