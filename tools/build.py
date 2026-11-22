#!/usr/bin/env python3
"""Static site generator for endurance-rea.com.

Writes plain HTML into ../site. No runtime dependencies; the output is a
static folder ready for Cloudflare Pages. Re-run after editing content:

    python3 tools/build.py
"""
import json, os, html
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, '..', 'site')
DOMAIN = 'https://endurance-rea.com'
IMG = json.load(open(os.path.join(ROOT, 'imginfo.json')))
BUILD_DATE = date.today().isoformat()
V = '1'  # asset version for cache busting

BIZ = {
    'name': 'Endurance Real Estate Advisors',
    'phone': '(646) 662-3546',
    'tel': '+16466623546',
    'email': 'greg.gang@endurance-rea.com',
    'street': '136 Madison Ave, 5th Floor',
    'city': 'New York', 'region': 'NY', 'zip': '10016',
    'instagram': 'https://www.instagram.com/endurance_rea/',
    'linkedin': 'https://www.linkedin.com/company/1560494/',
    'maps': 'https://www.google.com/maps/search/?api=1&query=136+Madison+Ave+5th+Floor+New+York+NY+10016',
}
OG_DEFAULT = '/images/og-endurance-real-estate-advisors-nyc.jpg'

esc = html.escape

# ---------------------------------------------------------------- icons
ICON = {
 'phone': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
 'menu': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>',
 'arrow': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 5l7 7-7 7"/></svg>',
 'mail': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/></svg>',
 'chart': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/></svg>',
 'shield': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
 'target': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
 'search': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>',
 'building': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="2" width="16" height="20" rx="1"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/></svg>',
 'handshake': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 17l2 2a1 1 0 0 0 1.4 0l4.6-4.6a2 2 0 0 0 0-2.8L15 7.6a2 2 0 0 0-2.8 0L11 8.8"/><path d="M13 7L9.6 3.6a2 2 0 0 0-2.8 0L2.6 7.8a2 2 0 0 0 0 2.8L9 17"/><path d="M8 12l3 3"/></svg>',
 'lock': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>',
 'megaphone': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11v3a1 1 0 0 0 1 1h3l5 4V6L7 10H4a1 1 0 0 0-1 1z"/><path d="M16 9a4 4 0 0 1 0 6M19 6a8 8 0 0 1 0 12"/></svg>',
 'instagram': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1.1.4 2.2.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1.1.4-2.2.4-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1.1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1.1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 1.8c-3.1 0-3.5 0-4.7.1-1.1.1-1.7.2-2.1.4-.5.2-.9.4-1.3.8-.4.4-.6.8-.8 1.3-.2.4-.3 1-.4 2.1C2.6 9.9 2.6 10.3 2.6 12s0 2.1.1 3.3c.1 1.1.2 1.7.4 2.1.2.5.4.9.8 1.3.4.4.8.6 1.3.8.4.2 1 .3 2.1.4 1.2.1 1.6.1 4.7.1s3.5 0 4.7-.1c1.1-.1 1.7-.2 2.1-.4.5-.2.9-.4 1.3-.8.4-.4.6-.8.8-1.3.2-.4.3-1 .4-2.1.1-1.2.1-1.6.1-4.7s0-3.5-.1-4.7c-.1-1.1-.2-1.7-.4-2.1-.2-.5-.4-.9-.8-1.3-.4-.4-.8-.6-1.3-.8-.4-.2-1-.3-2.1-.4C15.5 4 15.1 4 12 4zm0 3.1a4.9 4.9 0 1 1 0 9.8 4.9 4.9 0 0 1 0-9.8zm0 8a3.1 3.1 0 1 0 0-6.2 3.1 3.1 0 0 0 0 6.2zm6.2-8.2a1.1 1.1 0 1 1-2.3 0 1.1 1.1 0 0 1 2.3 0z"/></svg>',
 'linkedin': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.4 20.5h-3.6v-5.6c0-1.3 0-3-1.8-3s-2.1 1.4-2.1 2.9v5.7H9.4V9h3.4v1.6h.1c.5-.9 1.6-1.8 3.4-1.8 3.6 0 4.3 2.4 4.3 5.5v6.2zM5.3 7.4a2.1 2.1 0 1 1 0-4.2 2.1 2.1 0 0 1 0 4.2zM7.1 20.5H3.6V9h3.5v11.5zM22.2 0H1.8C.8 0 0 .8 0 1.7v20.6c0 .9.8 1.7 1.8 1.7h20.4c1 0 1.8-.8 1.8-1.7V1.7C24 .8 23.2 0 22.2 0z"/></svg>',
}

def ph(text):
    """Visible, clearly marked placeholder."""
    return f'<mark class="ph">[{esc(text)}]</mark>'

# ---------------------------------------------------------------- images
def img(name, alt, sizes='100vw', eager=False, cls='', ratio=None):
    info = IMG[name]
    ws = info['sizes']
    srcset = ', '.join(f'/images/{name}-{w}.webp {w}w' for w, h in ws)
    w, h = ws[-1]
    mid = ws[1] if len(ws) > 1 else ws[0]
    attrs = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ''
    return (f'<img src="/images/{name}-{mid[0]}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{esc(alt)}" {attrs}{c}>')

def og_url(name):
    return f'/images/{name}.jpg' if name else OG_DEFAULT

# ---------------------------------------------------------------- layout
NAV = [
    ('Services', '/services/', [
        ('Tenant Representation', '/services/tenant-representation/'),
        ('Landlord Representation', '/services/landlord-representation/'),
    ]),
    ('About', '/about/', None),
    ('Insights', '/insights/', None),
    ('FAQ', '/faq/', None),
]

def header(path):
    items = []
    for label, href, sub in NAV:
        cur = ' aria-current="page"' if path == href else ''
        if sub:
            subs = ''.join(
                f'<li><a href="{h}"{" aria-current=\"page\"" if path == h else ""}>{l}</a></li>' for l, h in sub)
            items.append(f'<li class="has-sub"><a href="{href}"{cur}>{label}</a><ul class="sub">{subs}</ul></li>')
        else:
            items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    cur = ' aria-current="page"' if path == '/contact/' else ''
    items.append(f'<li class="nav-contact-m"><a href="/contact/"{cur}>Contact</a></li>')
    return f'''<a class="skip" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="wrap hdr">
    <a class="logo" href="/" aria-label="{BIZ['name']} home"><img src="/images/brand/endurance-real-estate-advisors-logo.svg" width="200" height="37" alt="{BIZ['name']} logo"></a>
    <nav class="nav" id="site-nav" aria-label="Main"><ul>{''.join(items)}</ul></nav>
    <a class="hdr-phone" href="tel:{BIZ['tel']}">{ICON['phone']}{BIZ['phone']}</a>
    <a class="btn btn-primary hdr-cta" href="/contact/">Contact Us</a>
    <a class="hdr-call" href="tel:{BIZ['tel']}" aria-label="Call {BIZ['phone']}">{ICON['phone']}</a>
    <button class="menu-btn" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu">{ICON['menu']}</button>
  </div>
</header>'''

def footer():
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="fgrid">
      <div>
        <a href="/" aria-label="{BIZ['name']} home"><img src="/images/brand/endurance-real-estate-advisors-logo.svg" width="200" height="37" alt="{BIZ['name']} logo" loading="lazy"></a>
        <p style="margin-top:16px">A full-service commercial real estate brokerage and advisory firm in New York City, representing tenants and landlords with attention to detail and a commitment to exceeding expectations.</p>
        <div class="social">
          <a href="{BIZ['instagram']}" rel="noopener" target="_blank" aria-label="Endurance Real Estate Advisors on Instagram">{ICON['instagram']}</a>
          <a href="{BIZ['linkedin']}" rel="noopener" target="_blank" aria-label="Endurance Real Estate Advisors on LinkedIn">{ICON['linkedin']}</a>
        </div>
      </div>
      <div>
        <h2>Services</h2>
        <ul>
          <li><a href="/services/tenant-representation/">Tenant Representation</a></li>
          <li><a href="/services/landlord-representation/">Landlord Representation</a></li>
          <li><a href="/services/">All Services</a></li>
        </ul>
      </div>
      <div>
        <h2>Company</h2>
        <ul>
          <li><a href="/about/">About &amp; Team</a></li>
          <li><a href="/insights/">Insights</a></li>
          <li><a href="/faq/">FAQ</a></li>
          <li><a href="/about/#careers">Careers</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </div>
      <div>
        <h2>Visit or Call</h2>
        <address>
          {BIZ['street']}<br>{BIZ['city']}, {BIZ['region']} {BIZ['zip']}<br>
          <a href="tel:{BIZ['tel']}">{BIZ['phone']}</a><br>
          <a href="mailto:{BIZ['email']}">{BIZ['email']}</a>
        </address>
      </div>
    </div>
    <div class="fbottom">
      <span>&copy; {date.today().year} {BIZ['name']}. All rights reserved.</span>
      <span>Commercial real estate brokerage serving New York City.</span>
    </div>
  </div>
</footer>
<div class="mbar" aria-label="Quick contact">
  <a class="btn btn-ghost" href="tel:{BIZ['tel']}">{ICON['phone']} Call Now</a>
  <a class="btn btn-primary" href="/contact/">Get in Touch</a>
</div>
<script src="/js/main.js?v={V}" defer></script>'''

def crumbs_html(trail):
    if not trail:
        return ''
    lis = []
    for i, (name, href) in enumerate(trail):
        if i == len(trail) - 1:
            lis.append(f'<li aria-current="page">{esc(name)}</li>')
        else:
            lis.append(f'<li><a href="{href}">{esc(name)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>{"".join(lis)}</ol></div></nav>'

def crumbs_schema(trail):
    return {
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': DOMAIN + h}
            for i, (n, h) in enumerate(trail)
        ]}

def hero(image, alt, h1, sub, cta=('Schedule a Consultation', '/contact/'), second=None, small=True, eyebrow=None, extra=''):
    eb = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ''
    btns = f'<a class="btn btn-primary" href="{cta[1]}">{cta[0]} {ICON["arrow"]}</a>' if cta else ''
    if second:
        btns += f'<a class="btn btn-ghost" href="{second[1]}">{second[0]}</a>'
    return f'''<section class="hero{' hero-sm' if small else ''}">
  <div class="hero-img">{img(image, alt, eager=True)}</div>
  <div class="wrap">
    {eb}
    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
    {extra}
    <div class="hero-actions">{btns}</div>
  </div>
</section>'''

def cta_band(title='Ready to negotiate from a position of strength?',
             text='Advice, attention and service you would expect from a friend, with the expertise of an industry veteran.',
             primary=('Schedule a Consultation', '/contact/')):
    return f'''<section class="cta-band" aria-label="Contact Endurance Real Estate Advisors">
  <div class="wrap">
    <div><h2>{title}</h2><p>{text}</p></div>
    <div class="btns">
      <a class="btn btn-white" href="{primary[1]}">{primary[0]}</a>
      <a class="btn btn-ghost" href="tel:{BIZ['tel']}">{ICON['phone']} {BIZ['phone']}</a>
    </div>
  </div>
</section>'''

def page(path, title, desc, body, schemas=(), trail=None, og_image=None, og_type='website', robots='index,follow'):
    assert len(title) <= 60, (path, len(title), title)
    assert 140 <= len(desc) <= 160, (path, len(desc), desc)
    canonical = DOMAIN + path
    schema_tags = '\n'.join(
        f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False, separators=(",", ":"))}</script>'
        for s in list(schemas) + ([crumbs_schema(trail)] if trail else []))
    og = DOMAIN + (og_image or OG_DEFAULT)
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#15171a">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{BIZ['name']}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og}">
<link rel="stylesheet" href="/css/style.css?v={V}">
{schema_tags}
</head>
<body>
{header(path)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
'''
    out = os.path.join(SITE, path.lstrip('/'))
    if path.endswith('/'):
        out = os.path.join(out, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(doc)
    PAGES.append((path, robots))

PAGES = []

# ---------------------------------------------------------------- shared content
T = {  # testimonials, verbatim facts from the existing site (em dashes removed)
 'shemesh': ('Our building was acquired, and the new landlord wanted to take back our space. Endurance negotiated a lease buyout and successfully relocated us to a new building, expanding our footprint from 11,000 SF to over 38,000 SF. Greg is incredibly hands-on, attentive to every detail, and stayed actively involved throughout the entire process.', 'Yaron Shemesh', 'President, Creative Home Ideas'),
 'berdzeni': ('We toured over 75 spaces across 9 months. Endurance was relentless. Ultimately, we realized that expanding into a new space within our current building made the most financial sense. Endurance negotiated the new lease successfully and remained true professionals throughout. I wouldn’t hesitate to recommend them.', 'Natalya Berdzeni', 'President, Chase Cost Management'),
 'jenna': ('Endurance delivered a state-of-the-art studio with creativity and a clear understanding of our vision.', 'Jenna', 'Owner, Lemon Poppy Studio'),
 'ibragimov': ('Endurance’s market knowledge and hands-on approach made the entire process seamless and successful.', 'Bakhtiyor Ibragimov', 'Republic of Uzbekistan to the UN'),
 'jerome': ('Endurance stepped in with targeted marketing and delivered with exceptional follow-through.', 'Ginny Jerome', 'Owner, 110 Chambers Street'),
 'gofshteyn': ('Endurance found the perfect space and negotiated a deal that positioned us for success.', 'Maria Gofshteyn', 'NY Regional Director, RSM'),
 'gulati': ('Endurance is honest, knowledgeable, and consistently delivers as a trusted real estate partner.', 'Shyam Gulati', 'President, InfoPeople Corporation'),
 'levine': ('Endurance led our office search with expertise and found the perfect space.', 'Adam Levine', 'President, Regal USA/Fuen USA'),
 'classi': ('Endurance guided the process, positioned the space, and secured the right tenant, meeting our financial goals.', 'Matt Classi', 'Real Estate Investor'),
}

def tcard(key, feature=False):
    q, n, r = T[key]
    return f'<figure class="tcard{" feature" if feature else ""}"><blockquote><p>{esc(q)}</p></blockquote><figcaption><b>{esc(n)}</b>{esc(r)}</figcaption></figure>'

def stats_bar():
    return '''<section class="stats" aria-label="Track record">
  <div class="wrap">
    <div class="stat"><b>1,850<span>+</span></b><small>Successful leasing transactions</small></div>
    <div class="stat"><b>30<span>+</span> Years</b><small>Representing landlords and tenants across NYC</small></div>
    <div class="stat"><b>$3B</b><small>In aggregate leasing transaction volume</small></div>
  </div>
</section>'''

def faq_block(items, heading_tag='h3'):
    out = []
    for q, a in items:
        out.append(f'<details class="faq"><summary><{heading_tag}>{esc(q)}</{heading_tag}></summary><div class="a">{a}</div></details>')
    return '\n'.join(out)

import re
def strip_tags(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()

def faq_schema(items):
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q,
                            'acceptedAnswer': {'@type': 'Answer', 'text': strip_tags(a)}} for q, a in items]}

ORG_REF = {'@type': 'RealEstateAgent', '@id': DOMAIN + '/#business', 'name': BIZ['name'], 'url': DOMAIN + '/'}
AREA = [{'@type': 'City', 'name': 'New York City'}, {'@type': 'Place', 'name': 'Manhattan, New York'}]

def service_schema(name, desc, path, stype):
    return {'@context': 'https://schema.org', '@type': 'Service', 'name': name, 'serviceType': stype,
            'description': desc, 'url': DOMAIN + path, 'provider': ORG_REF, 'areaServed': AREA}

# ---------------------------------------------------------------- articles
ARTICLES = [
 {
  'slug': 'tribeca-prep-leases-116-nassau-street',
  'title': 'Tribeca Prep Leases 12,900+ SF at 116 Nassau Street',
  'seo_title': 'Tribeca Prep Leases 12,900+ SF at 116 Nassau Street',
  'desc': 'Tribeca Prep leased the entire 2nd floor, 12,900+ SF, at 116 Nassau Street in the Financial District. Space from 5,231 to 11,365 SF remains. Inquire today.',
  'tag': 'Deal News', 'img': 'manhattan-skyline-brooklyn-bridge-nyc',
  'img_alt': 'Lower Manhattan skyline and the Brooklyn Bridge at night, home of the Financial District',
  'card_img': 'tribeca-prep-lease-116-nassau-street-financial-district',
  'excerpt': 'Tribeca Prep has leased the entire second floor, more than 12,900 SF, at 116 Nassau Street in the Financial District. Availabilities from 5,231 to 11,365 SF remain.',
  'cta': ('Inquire About 116 Nassau', '/contact/?topic=landlord'),
  'body': lambda: f'''
<p><strong>Tribeca Prep has leased the entire second floor, more than 12,900 square feet, at 116 Nassau Street in the Financial District.</strong> Availabilities from 5,231 to 11,365 SF remain in multiple configurations.</p>
{img('tribeca-prep-lease-116-nassau-street-financial-district', '116 Nassau Street, Financial District: 12,900+ SF leased to Tribeca Prep, entire second floor', sizes='(min-width: 900px) 720px, 100vw')}
<p>Tribeca Prep didn’t choose a newer building. They chose the right building.</p>
<ul>
  <li><strong>Tenant:</strong> Tribeca Prep</li>
  <li><strong>Space:</strong> 12,900+ SF, entire second floor</li>
  <li><strong>Location:</strong> 116 Nassau Street, between Ann and Beekman Streets, Financial District</li>
</ul>
<h2>Committed ownership in Lower Manhattan</h2>
<p>For over three decades, the ownership of 116 Nassau Street has stood resilient, weathering shifting markets, economic recessions, and the constant evolution of Lower Manhattan. That kind of commitment to a building and its tenants is rare, and tenants notice.</p>
<p>Now, 116 Nassau is the proud new home of Tribeca Prep, which has signed for the entire second floor: more than 12,900 square feet of space in the heart of the Financial District, between Ann and Beekman Streets.</p>
<p>Real estate trends come and go, but well-located buildings with committed ownership always endure. More importantly, ownership that understands when to move decisively and capitalize on the right opportunity creates long-term value for both the building and its tenants.</p>
<p>That is the definition of Endurance.</p>
<h2>Space still available at 116 Nassau Street</h2>
<p>Availabilities remaining at 116 Nassau Street range from <strong>5,231 to 11,365 SF</strong>, in multiple configurations. To inquire, contact Greg Gang at <a href="mailto:{BIZ['email']}">{BIZ['email']}</a> or <a href="tel:{BIZ['tel']}">646-662-3546</a>.</p>
<p>Own a building and want results like this? See how our <a href="/services/landlord-representation/">landlord representation services</a> position properties to attract quality tenants.</p>
'''},
 {
  'slug': 'self-help-clause-commercial-lease-nyc',
  'title': 'Self-Help in Today’s Leasing Market',
  'seo_title': 'Self-Help Clause in a Commercial Lease | NYC Guide',
  'desc': 'What a self-help clause is, why NYC office tenants need one now, and the 5 elements every strong clause should include. Talk to a tenant advocate today.',
  'tag': 'Tenant Guide', 'img': 'nyc-commercial-tenant-self-help-clause',
  'img_alt': 'Business professional in a suit preparing for an office lease negotiation in New York',
  'excerpt': 'When landlords fall behind on their obligations, a well-crafted self-help clause lets tenants fix critical issues and recoup the cost. Here are the five elements to push for.',
  'cta': ('Talk to a Tenant Advocate', '/contact/?topic=tenant'),
  'body': lambda: f'''
<p><strong>A self-help clause gives a commercial tenant the right to fix certain problems the landlord fails to address, then recover the cost, often through a rent offset.</strong> In today’s New York City office market, it is one of the most important protections a tenant can negotiate.</p>
<p>As a commercial real estate broker, I’ve seen how quickly things can unravel when landlords fall behind on their financial obligations and tenants don’t have the right protections in place.</p>
<p>Buildings once considered financially stable are now under distress. Imagine arriving at your office to find one of the elevators out of service for days, your space not cleaned the night before, or the air conditioning not working properly. If a property falls into receivership, the situation can deteriorate even further.</p>
<p>That’s why I strongly advise clients: whether negotiating a new office lease or a renewal, don’t overlook the importance of a well-crafted self-help clause.</p>
<h2>What is a self-help clause?</h2>
<p>A self-help clause gives tenants the right to step in and address a landlord’s failure to perform certain obligations, typically related to maintaining the leased premises, and recoup the cost, often through a rent offset.</p>
<p>It’s a safeguard for critical services tied directly to your space: HVAC servicing, plumbing repairs, lighting, janitorial services, and other operational necessities that go unaddressed despite repeated notices.</p>
<h2>Why it matters right now in NYC</h2>
<p>In New York City, many office landlords are under financial pressure, cutting operating budgets or reducing building services to stay afloat. Without a self-help clause, tenants have little recourse if garbage piles up, restrooms go uncleaned, or heating and cooling systems stop working.</p>
<p>In buildings where ownership is distracted by debt service or loan workouts, tenants often find themselves waiting or, worse, paying out of pocket with no reimbursement.</p>
<p>This isn’t theoretical. In today’s NYC market, I’ve seen firsthand how delays in basic services can hurt productivity, disrupt operations, and even lead to lost business.</p>
<h2>What should a strong self-help clause include?</h2>
<p>Based on years of experience structuring leases in New York’s office market, here are five elements every tenant should push for:</p>
<ol>
  <li><strong>Clear scope.</strong> The lease should specifically define which repairs or services tenants can address. Focus on non-structural issues affecting your premises.</li>
  <li><strong>Defined notice and cure periods.</strong> Require written notice and a clear window for the landlord to respond, typically 10 to 30 days. Some leases require a second notice; make sure the timing is realistic.</li>
  <li><strong>Reimbursement or offset mechanism.</strong> If you’re fixing something the landlord failed to handle, the lease should outline how and when you’re reimbursed, ideally via rent offset, without arbitrary dollar limits.</li>
  <li><strong>Avoid rent withholding confusion.</strong> A self-help clause isn’t a free pass to stop paying rent. It should allow cost recovery, not blanket rent withholding, which could put you in default.</li>
  <li><strong>Legal review.</strong> Work with a qualified real estate attorney familiar with NYC office leases. Language matters; these clauses must be tailored and enforceable.</li>
</ol>
<h2>What happens without it?</h2>
<p>I’ve seen too many tenants trapped in underperforming buildings with no ability to act. In some cases, a lack of basic cleaning services or an HVAC or plumbing issue disrupted operations for weeks because the lease lacked a basic self-help right.</p>
<p>In today’s market, with more buildings being sold at distressed prices, services can slip. Without self-help protection, tenants are forced to wait or escalate disputes, often at high cost.</p>
<h2>Bottom line: it’s a strategic must-have</h2>
<p>In this market, with high vacancies, minimal rent growth, increased operating expenses and financially stressed landlords, the self-help clause isn’t just legal fine print. It’s a strategic safeguard.</p>
<p>Tenants need the ability to protect their operations. In a tenant-favorable environment like NYC’s, this clause is negotiable, and it should be part of every serious lease conversation. Don’t wait for something to go wrong to realize you don’t have the tools to fix it.</p>
<p>Related reading: <a href="/insights/why-sndas-matter-to-tenants/">why SNDAs matter to tenants</a> and <a href="/insights/lessons-from-a-landlords-troubles/">how to gain leverage with a distressed landlord</a>. Learn how our <a href="/services/tenant-representation/">tenant representation services</a> build these protections into every lease.</p>
<p class="note">Disclaimer: I am not an attorney, and this article is not intended as legal advice. It is based on my professional experience working with landlords and tenants in NYC commercial real estate for over 30 years. For legal advice, consult a qualified attorney. For brokerage advice, please do not hesitate to reach out.</p>
'''},
 {
  'slug': 'why-sndas-matter-to-tenants',
  'title': 'Why SNDAs Matter to Tenants',
  'seo_title': 'Why SNDAs Matter to Commercial Tenants | NYC',
  'desc': 'An SNDA protects your lease if your landlord’s lender forecloses. Learn how subordination, non-disturbance and attornment work, and how to negotiate one.',
  'tag': 'Tenant Guide', 'img': 'conference-room-lease-negotiation-nyc',
  'img_alt': 'Empty conference room table and chairs ready for a commercial lease negotiation',
  'excerpt': 'A Subordination, Non-Disturbance, and Attornment Agreement keeps your lease rights intact if your landlord’s lender forecloses. Here is how it works and how to secure one.',
  'cta': ('Talk to a Tenant Advocate', '/contact/?topic=tenant'),
  'body': lambda: '''
<p><strong>An SNDA (Subordination, Non-Disturbance, and Attornment Agreement) protects a tenant’s right to stay in its space under its existing lease if the landlord’s lender forecloses.</strong> In times of economic uncertainty, it is one of the most valuable documents a commercial tenant can secure.</p>
<p>When landlords face mortgage defaults, lenders may initiate foreclosures, putting tenants at risk of eviction even if they have a valid lease. SNDAs play a pivotal role as a safeguard, ensuring that tenants retain their lease rights even after a foreclosure.</p>
<h2>Understanding SNDAs: a shield for tenants</h2>
<p>An SNDA is a legally binding contract between three parties: a tenant, a landlord, and the landlord’s lender. Its primary purpose is to protect the tenant’s interest in the leased premises should the landlord’s mortgage lead to foreclosure.</p>
<h3>1. Subordination</h3>
<p>The subordination provision establishes that the tenant’s lease is subordinate to the lender’s mortgage. In simpler terms, if the landlord defaults on its loan, the lender takes precedence over the leased premises, and the tenant cannot prevent the lender from foreclosing and taking possession of the property.</p>
<h3>2. Non-disturbance</h3>
<p>The non-disturbance provision ensures that the lender will not disturb the tenant’s lease as long as the tenant complies with the lease terms. The tenant can continue to occupy the premises after a foreclosure sale, even if the lender sells the property to a new owner.</p>
<h3>3. Attornment</h3>
<p>The attornment provision requires the tenant to recognize the lender as the new landlord following a foreclosure sale. This means paying rent to the lender and abiding by the lease terms.</p>
<h2>Why SNDAs are essential for tenants</h2>
<p>SNDAs provide assurance and stability in the face of foreclosure. Without one, tenants risk eviction if the lender forecloses on the landlord’s mortgage, which could disrupt business operations and result in significant financial losses.</p>
<p>SNDAs can also help tenants negotiate more favorable lease terms. Landlords are more inclined to offer advantageous conditions to tenants willing to sign an SNDA, because SNDAs make the leased premises more appealing to lenders.</p>
<h2>How to secure an SNDA</h2>
<p>Not every tenant can secure an SNDA. Eligibility often depends on the amount of space being leased, the lease term, and the tenant’s financial commitment, especially in markets like New York City.</p>
<p>The most effective way to obtain an SNDA is to negotiate it as part of the lease agreement. If the landlord is initially unwilling, tenants may explore other negotiation avenues, such as seeking a lower rent or an extended lease term.</p>
<p>Obtaining an SNDA after lease signing is more challenging, because both the landlord and the lender must be convinced to sign.</p>
<h2>Tenant tip</h2>
<p>Start negotiating the SNDA early in the leasing process to maximize your leverage.</p>
<h2>In conclusion</h2>
<p>An SNDA is a vital document that shields tenants from the upheaval and financial repercussions of a foreclosure. Tenants should proactively negotiate an SNDA as part of the lease. If that is not possible during initial negotiations, securing one after signing may present additional hurdles, but its importance in safeguarding tenant rights cannot be overstated.</p>
<p>Related reading: <a href="/insights/self-help-clause-commercial-lease-nyc/">the self-help clause every NYC tenant needs</a>. See how our <a href="/services/tenant-representation/">tenant representation team</a> negotiates these protections.</p>
<p class="note">Full disclosure: I am not an attorney. Always seek legal advice regarding these agreements.</p>
'''},
 {
  'slug': 'lessons-from-a-landlords-troubles',
  'title': 'Lessons From a Landlord’s Troubles',
  'seo_title': 'Distressed Landlords: Tenant Leverage in NYC',
  'desc': 'High-profile NYC landlord defaults create leverage for tenants. Learn what to negotiate, the due diligence to run, and lease protections to demand. Call us.',
  'tag': 'Market Insight', 'img': 'manhattan-office-tower-distressed-landlord',
  'img_alt': 'Pre-war Manhattan office tower viewed from street level',
  'excerpt': 'Reported defaults across a major NYC landlord’s portfolio show how ownership distress can shift leverage to tenants, and what due diligence to run before you sign.',
  'cta': ('Assess Your Landlord’s Position', '/contact/?topic=tenant'),
  'body': lambda: f'''
<p><strong>When a landlord is in financial distress, tenants often gain negotiating leverage, but they also take on new risks that require careful due diligence and stronger lease protections.</strong> Recent headlines surrounding Joe Moinian’s real estate portfolio are more than industry gossip; they’re a window into today’s market and an opportunity for tenants to take control.</p>
<p>In the past few weeks alone:</p>
<ul>
  <li>LNR Partners filed suit to seize 535-545 Fifth Avenue, alleging default on a $310M loan.</li>
  <li>AIG moved to foreclose on 500-512 Seventh Avenue, where $285M remains outstanding.</li>
  <li>Moinian lost the Hilton Garden Inn in Midtown via UCC foreclosure after failing to pay off a $175M loan.</li>
</ul>
<p>With interest rates still elevated and lenders growing less flexible, even long-established owners are finding it hard to refinance or restructure. This matters to you as a tenant because distress at the ownership level can change the equation when it comes to your lease.</p>
<h2>Tenant advantage in a distressed market</h2>
<p>Reports of high-profile defaults, including lawsuits, foreclosure filings, and ownership turnover, may seem like distant headlines. But if you’re a tenant in New York City, this kind of distress can directly affect your lease, your rent, and your future occupancy. Here’s how to think strategically, and how we help clients use this moment to their advantage.</p>
<h3>Negotiating leverage</h3>
<p>When landlords are under financial pressure, they’re far more likely to work with tenants to stabilize their income and avoid vacancies.</p>
<p><strong>If you’re a current tenant,</strong> this could mean:</p>
<ul>
  <li>Opportunities to renegotiate lease terms</li>
  <li>Lower rent or rent abatements</li>
  <li>Early renewal options with better terms</li>
  <li>Relief from escalations or pass-through charges</li>
</ul>
<p><strong>If you’re a prospective tenant looking for new space,</strong> distressed landlords may offer larger concession packages, including:</p>
<ul>
  <li><strong>Generous free rent periods:</strong> often several months, significantly reducing initial occupancy costs.</li>
  <li><strong>Higher tenant improvement (TI) allowances:</strong> negotiate for substantial funds to customize the space. If capital is an issue, landlord and tenant will need to be creative to find a solution.</li>
  <li><strong>More flexible lease structures:</strong> explore shorter terms (for example, 3 to 5 years) if your business outlook is uncertain, or build in options for expansion or contraction.</li>
</ul>
<h3>Due diligence and risk awareness</h3>
<p>When a property is at risk of foreclosure or is in special servicing, it’s more than a financial event; it can affect your business operations. Potential risks include:</p>
<ul>
  <li>Deferred maintenance or delayed improvements</li>
  <li>Reduced services (like cleaning, HVAC, or security)</li>
  <li>Uncertainty during ownership transition, including possible lease renegotiation</li>
</ul>
<p>If you’re already in a building facing distress, it’s critical to review your lease protections, such as SNDA clauses and remedies if landlord obligations are not met.</p>
<p><strong>For tenants looking for new space, due diligence is paramount:</strong></p>
<ul>
  <li><strong>Financial health of the landlord.</strong> Go beyond surface-level checks. Investigate the landlord’s overall financial stability, including debt service coverage ratio (DSCR), equity position in the property, and the status of the mortgage (is it current, in special servicing, or nearing maturity?). Look for public filings of lawsuits or foreclosures against the portfolio. A strong cash position indicates a landlord less likely to defer maintenance or services.</li>
  <li><strong>Property condition.</strong> Beyond a walk-through, consider commissioning a third-party Property Condition Assessment (PCA). It can uncover hidden issues with structural integrity, HVAC, plumbing, and electrical systems, especially if the lease shifts repair responsibilities to the tenant. Check for signs of deferred maintenance.</li>
  <li><strong>Environmental and compliance.</strong> Verify compliance with building codes, zoning regulations, and accessibility laws (like the ADA).</li>
</ul>
<p><strong>Lease protections in a new lease.</strong> Make sure your new lease includes critical clauses:</p>
<ul>
  <li><strong>A strong SNDA</strong> (Subordination, Non-Disturbance, and Attornment) protects your lease in the event of foreclosure, allowing you to remain in the space under the same terms if a new owner takes over. <a href="/insights/why-sndas-matter-to-tenants/">Read our SNDA guide.</a></li>
  <li><strong>Security protections:</strong> negotiate specific language around security or rent abatements in the event of an ownership change or significant disruption.</li>
</ul>
<h2>Why strategic insight matters</h2>
<p>At Endurance Real Estate Advisors, we go far beyond standard site tours and rent comps. Before we negotiate, we:</p>
<ul>
  <li>Research the ownership’s financial position</li>
  <li>Evaluate loan performance and debt maturity risk</li>
  <li>Flag potential foreclosure or UCC sales</li>
  <li>Help tenants protect themselves before problems arise</li>
</ul>
<p>This insight gives our clients real leverage at the table: not just market knowledge, but strategic foresight. It is the foundation of our <a href="/services/tenant-representation/">Tenant Advantage Analysis</a>.</p>
<p>Below is a sample 7-year income and expense chart for a typical office building. Though hypothetical, it shows how a once-healthy asset can become financially strained due to broader economic shifts. Understanding these patterns gives tenants insight and leverage.</p>
{img('office-building-income-expense-chart', 'Sample bar chart of an office building’s estimated total expenses versus gross income from 2017 to 2025, with income falling below expenses', sizes='(min-width: 900px) 720px, 100vw')}
<h2>What to keep in mind</h2>
<p>If your space is in a building owned by a distressed landlord (like 535 Fifth Avenue or 500 Seventh Avenue), now is the time to:</p>
<ul>
  <li>Scrutinize your lease, especially around services and landlord default</li>
  <li>Monitor servicing or foreclosure activity</li>
  <li>Consider asking for security protections in the event of an ownership change</li>
  <li>If you’re looking for new space, begin your search early: 6 to 18 months before your current lease expires. This allows ample time for due diligence, market research, and negotiation without pressure.</li>
  <li>Always have a qualified commercial real estate attorney review all lease documents before signing.</li>
</ul>
<h2>Want to understand your landlord’s position?</h2>
<p>Let’s talk. We’ll help you assess risk, explore your options, and negotiate from a position of strength. <a href="/contact/?topic=tenant">Contact our tenant advocates</a> or call <a href="tel:{BIZ['tel']}">{BIZ['phone']}</a>.</p>
'''},
 {
  'slug': 'renewals-shrinking-ti-allowances',
  'title': 'Renewals and Shrinking TI Allowances',
  'seo_title': 'Lease Renewals and Shrinking TI Allowances | NYC',
  'desc': 'Smaller tenant improvement allowances can work in a tenant’s favor at renewal. Learn how net deals and new landlord limits create leverage. Talk to us.',
  'tag': 'Tenant Guide', 'img': 'lease-renewal-tenant-improvement-allowance',
  'img_alt': 'Tenant signing a commercial lease renewal document',
  'excerpt': 'Declining tenant improvement allowances do not have to be bad news. For tenants renewing their leases, the shift opens the door to net deals and better terms.',
  'cta': ('Plan Your Renewal Strategy', '/contact/?topic=tenant'),
  'body': lambda: '''
<p><strong>Shrinking tenant improvement (TI) allowances can actually benefit tenants at renewal, because landlords who cannot fund build-outs are often more flexible on rent, term and renewal options.</strong> While it’s easy to assume declining TIs are a bad omen, the reality is far more nuanced.</p>
<h2>The unforeseen impact of coworking on office design</h2>
<p>The rise of coworking spaces has subtly shifted the perception of corporate office design. The traditional demand for highly customized spaces has waned, making room for more standardized, cost-effective designs. Many corporations have embraced this evolution, leading landlords to develop larger, pre-built spaces versatile enough to meet a wide range of tenant needs.</p>
<h2>Why landlords might prefer lower TIs</h2>
<p>Landlords are feeling the pinch of high construction costs and extended build-out timelines. Liquidity issues make it less appealing to offer extensive TIs. That reluctance opens the door for tenants to negotiate on other fronts, such as base rent, lease length, or renewal options. With less focus on TIs, landlords may be more open to discussing these alternative terms.</p>
<h2>The power shift: from “No” to “I can’t”</h2>
<p>Until recently, leverage in tenant-landlord negotiations often rested with the landlord. Today’s market constraints are prompting more landlords to say “I can’t” when it comes to TIs. Lending restrictions mean some landlords simply cannot fund extensive improvements. This creates an opening for tenants, particularly those willing to fund their own TIs.</p>
<h2>The advantages of net deals</h2>
<p>For tenants renewing their leases, this is an opportunity to negotiate net deals. In these arrangements, rents are adjusted according to the TIs funded by the tenant. Because tenants often have a lower cost of capital than landlords, net deals can yield substantial savings over the lease term.</p>
<h2>Seizing the opportunity</h2>
<p>Landlords adapting to these conditions may be more willing to negotiate, offering terms that favor long-term tenants. Whether it’s a net deal or the chance to occupy a space with high salvage value, tenants have more options than ever.</p>
<p>Declining TIs don’t necessarily mean a loss for tenants. With the right strategy and negotiation skills, tenants can turn these market shifts to their advantage.</p>
<p>This is where partnering with Endurance becomes invaluable. As your <a href="/services/tenant-representation/">tenant advocate</a>, we guide you through the shifting dynamics so you are in the best position to negotiate favorable lease terms, whether that’s lower base rent, a more flexible lease length, or advantageous renewal options.</p>
'''},
]

def post_card(a, heading='h3'):
    im = a.get('card_img', a['img'])
    alt = a['img_alt'] if 'card_img' not in a else '116 Nassau Street lease announcement banner'
    return f'''<a class="post" href="/insights/{a['slug']}/">
  {img(im, alt, sizes='(min-width: 1080px) 360px, (min-width: 760px) 50vw, 100vw', cls='contain' if 'card_img' in a else '')}
  <div class="body"><span class="tag">{a['tag']}</span><{heading}>{esc(a['title'])}</{heading}><p>{esc(a['excerpt'])}</p><span class="more">Read article →</span></div>
</a>'''

# ================================================================ PAGES
def build_home():
    biz_schema = {
        '@context': 'https://schema.org', '@type': 'RealEstateAgent', '@id': DOMAIN + '/#business',
        'name': BIZ['name'], 'url': DOMAIN + '/',
        'description': 'Full-service commercial real estate brokerage and advisory firm in New York City providing tenant representation and landlord representation for office and retail space.',
        'telephone': BIZ['tel'], 'email': BIZ['email'],
        'image': DOMAIN + OG_DEFAULT,
        'logo': DOMAIN + '/apple-touch-icon.png',
        'address': {'@type': 'PostalAddress', 'streetAddress': BIZ['street'], 'addressLocality': BIZ['city'],
                    'addressRegion': BIZ['region'], 'postalCode': BIZ['zip'], 'addressCountry': 'US'},
        'areaServed': AREA,
        'sameAs': [BIZ['instagram'], BIZ['linkedin']],
        'founder': {'@type': 'Person', 'name': 'Gregory Gang', 'jobTitle': 'Founder & Principal'},
        'knowsAbout': ['Tenant representation', 'Landlord representation', 'Commercial office leasing', 'Retail leasing', 'Lease negotiation', 'SNDA agreements', 'Lease renewals'],
        'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Commercial real estate services', 'itemListElement': [
            {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'Tenant Representation', 'url': DOMAIN + '/services/tenant-representation/'}},
            {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'Landlord Representation', 'url': DOMAIN + '/services/landlord-representation/'}},
        ]},
        # 'openingHoursSpecification': add once office hours are confirmed
    }
    site_schema = {'@context': 'https://schema.org', '@type': 'WebSite', '@id': DOMAIN + '/#website', 'name': BIZ['name'], 'url': DOMAIN + '/', 'publisher': {'@id': DOMAIN + '/#business'}}
    body = hero('manhattan-skyline-brooklyn-bridge-nyc', 'Manhattan skyline and the Brooklyn Bridge at night, New York City',
        'NYC Commercial Real Estate Brokers Who Put Your Interests First',
        'Tenant and landlord representation in New York City, backed by 30+ years of experience and data that lets you negotiate from strength.',
        cta=('Schedule a Consultation', '/contact/'), second=('Explore Our Services', '/services/'), small=False,
        eyebrow='Endurance Real Estate Advisors')
    body += stats_bar()
    body += f'''
<section class="section">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">How can we help?</span>
      <h2>Commercial real estate advisors for both sides of the lease</h2>
      <p class="lead">Endurance Real Estate Advisors is a full-service commercial real estate brokerage and advisory firm in New York City. We are results-driven, focused on attention to detail and on exceeding our clients’ expectations. Choose your path:</p>
    </div>
    <div class="grid-2">
      <a class="path" href="/services/tenant-representation/">
        {img('nyc-office-space-tenant-representation', 'Professionals working in a bright Manhattan loft office', sizes='(min-width: 760px) 50vw, 100vw')}
        <div class="body"><span class="who">I’m a tenant</span><h3>Tenant Representation</h3>
        <p>Leasing, renewing, expanding or relocating? We develop and implement solution-based transactions using intimate knowledge of your needs and every corner of the NYC market, starting with our proprietary Tenant Advantage Analysis.</p>
        <span class="more">See tenant services →</span></div>
      </a>
      <a class="path" href="/services/landlord-representation/">
        {img('nyc-retail-storefront-landlord-leasing', 'Ground-floor retail storefront on a New York City street', sizes='(min-width: 760px) 50vw, 100vw')}
        <div class="body"><span class="who">I’m a landlord or owner</span><h3>Landlord Representation</h3>
        <p>We deliver a customized, efficient leasing strategy that protects your interests and helps your office, retail, condo or coop asset realize its full potential with quality tenants.</p>
        <span class="more">See landlord services →</span></div>
      </a>
    </div>
  </div>
</section>

<section class="section section-dark">
  <div class="wrap split">
    <div>
      <span class="eyebrow">Our promise</span>
      <p class="quote-big">“Our sole fiduciary duty is to protect the interests of our clients, and we strive to do it better than anyone else in the business.”</p>
      <div class="quote-by">
        {img('gregory-gang-founder-endurance-real-estate-advisors', 'Gregory Gang, Founder and Principal of Endurance Real Estate Advisors', sizes='72px')}
        <div><b>Gregory Gang</b><span>Founder &amp; Principal, Endurance Real Estate Advisors</span></div>
      </div>
      <p style="margin-top:28px"><a class="btn btn-ghost" href="/about/#team">Meet Our Team</a></p>
    </div>
    <div>
      <h2>Why NYC businesses and owners choose Endurance</h2>
      <ul class="checks">
        <li><strong>Our name is symbolic of who we are.</strong> We see every deal through, from the first tour to the signed lease.</li>
        <li><strong>Insight that creates leverage.</strong> We research ownership finances, loan performance and market comps before we negotiate.</li>
        <li><strong>Both sides of the table.</strong> A clear understanding of landlord and tenant priorities helps us structure deals that close.</li>
        <li><strong>Hands-on senior attention.</strong> Advice and service you would expect from a friend, with the expertise of an industry veteran.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section section-mist">
  <div class="wrap">
    <div class="head center">
      <span class="eyebrow">Client results</span>
      <h2>What our clients say</h2>
      <p class="lead center">From a relocation that more than tripled a footprint to renewals that made the most financial sense, here is what working with Endurance looks like.</p>
    </div>
    <div class="tgrid">
      {tcard('shemesh', feature=True)}
      {tcard('berdzeni', feature=True)}
    </div>
    <div class="tgrid three" style="margin-top:20px">
      {tcard('gofshteyn')}{tcard('classi')}{tcard('ibragimov')}
    </div>
    <p class="center" style="margin-top:28px"><a href="/about/#testimonials">Read more client testimonials</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">How we work</span>
      <h2>A clear process from first call to signed lease</h2>
    </div>
    <ol class="steps">
      <li><h3>Understand your goals</h3><p>We work closely with you to establish short and long-term goals and objectives, whether you are leasing space or leasing up a building.</p></li>
      <li><h3>Arm you with data</h3><p>Market rates, concessions, comparable properties and ownership intel, delivered in a confidential analysis tailored to your situation.</p></li>
      <li><h3>Negotiate and close</h3><p>We lead negotiations with a customized strategy and stay hands-on through lease signing to secure terms aligned with your goals.</p></li>
    </ol>
  </div>
</section>

<section class="section section-mist">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">Pulse &amp; Perspective</span>
      <h2>NYC commercial leasing insights</h2>
      <p class="lead">Practical guidance on lease protections, renewals and today’s market from our team. <a href="/insights/">View all insights</a>.</p>
    </div>
    <div class="posts three">
      {post_card(ARTICLES[0])}{post_card(ARTICLES[1])}{post_card(ARTICLES[2])}
    </div>
  </div>
</section>
'''
    body += cta_band()
    page('/', 'NYC Commercial Real Estate Broker | Endurance REA',
         'Endurance Real Estate Advisors: NYC commercial real estate brokers for tenants and landlords. 1,850+ leases, $3B volume. Schedule a consultation today.',
         body, schemas=[biz_schema, site_schema])

def build_services():
    trail = [('Home', '/'), ('Services', '/services/')]
    body = hero('landlord-representation-leasing-strategy-meeting', 'Commercial real estate advisor presenting a leasing strategy in a glass-walled Manhattan conference room',
        'Commercial Real Estate Services in NYC',
        'Expert representation for tenants and landlords, with one goal: protecting your interests at every step of the lease.',
        eyebrow='Our Services')
    body += crumbs_html(trail)
    body += f'''
<section class="section">
  <div class="wrap">
    <div class="head">
      <h2>Two specialties, one standard of service</h2>
      <p class="lead">Endurance Real Estate Advisors provides commercial real estate brokerage and advisory services across New York City. Because we understand both landlord and tenant priorities, we deliver insights and data that empower every client to negotiate from a position of strength.</p>
    </div>
    <div class="grid-2">
      <a class="path" href="/services/tenant-representation/">
        {img('tenant-advantage-analysis-lease-research', 'Team researching market data on laptops for a tenant lease analysis', sizes='(min-width: 760px) 50vw, 100vw')}
        <div class="body"><span class="who">For tenants</span><h3>Tenant Representation</h3>
        <p>We act as your tenant advocate for new leases, renewals, expansions and relocations of office space in NYC.</p>
        <ul class="checks">
          <li>Proprietary Tenant Advantage Analysis (TAA)</li>
          <li>Market rents, concessions and comparable properties</li>
          <li>Landlord motivation and negotiation history</li>
          <li>Customized negotiation strategy</li>
        </ul>
        <span class="more">Explore tenant representation →</span></div>
      </a>
      <a class="path" href="/services/landlord-representation/">
        {img('landlord-leasing-market-analysis', 'Advisors reviewing leasing market charts and financial reports for a property owner', sizes='(min-width: 760px) 50vw, 100vw')}
        <div class="body"><span class="who">For landlords</span><h3>Landlord Representation</h3>
        <p>We serve as an exclusive leasing partner for building owners, investors, and condo and coop boards with office and retail space.</p>
        <ul class="checks">
          <li>Property positioning and narrative</li>
          <li>Customized leasing strategy from market analysis</li>
          <li>Targeted marketing to quality tenants</li>
          <li>Hands-on support from marketing to lease signing</li>
        </ul>
        <span class="more">Explore landlord representation →</span></div>
      </a>
    </div>
  </div>
</section>
'''
    body += stats_bar()
    body += f'''
<section class="section section-mist">
  <div class="wrap">
    <div class="head center"><h2>Trusted by tenants and owners across NYC</h2></div>
    <div class="tgrid three">{tcard('levine')}{tcard('jerome')}{tcard('gulati')}</div>
    <p class="center" style="margin-top:28px">Have questions first? Visit our <a href="/faq/">commercial real estate FAQ</a>.</p>
  </div>
</section>
'''
    body += cta_band()
    schema = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Commercial real estate services in NYC', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'url': DOMAIN + '/services/tenant-representation/', 'name': 'Tenant Representation'},
        {'@type': 'ListItem', 'position': 2, 'url': DOMAIN + '/services/landlord-representation/', 'name': 'Landlord Representation'}]}
    page('/services/', 'Commercial Real Estate Services NYC | Endurance REA',
         'Tenant representation and landlord representation for NYC office and retail space. Data-driven strategy and hands-on negotiation. Book a consultation.',
         body, schemas=[schema], trail=trail, og_image=og_url('landlord-representation-leasing-strategy-meeting'))

TENANT_FAQ = [
 ('What does a tenant representation broker do?',
  '<p>A tenant representation broker negotiates on behalf of the tenant, not the landlord, to secure the best possible lease terms. At Endurance, our sole fiduciary duty is to protect our clients’ interests. We provide the market data, landlord intel and negotiation strategy you need to make informed decisions throughout the process.</p>'),
 ('What is the Tenant Advantage Analysis?',
  '<p>The Tenant Advantage Analysis (TAA) is Endurance’s proprietary, confidential report on your specific leasing situation. It covers market insights such as rental rates, concessions and comparable properties, intel on your landlord’s motivations and negotiation history, and a customized strategy to secure the best possible lease terms.</p>'),
 ('Can you help me renew my current lease instead of moving?',
  '<p>Yes. Endurance negotiates renewals and expansions as well as relocations. One client toured over 75 spaces across 9 months before realizing that expanding within their current building made the most financial sense, and Endurance negotiated that new lease. In today’s market, renewing tenants may also benefit from <a href="/insights/renewals-shrinking-ti-allowances/">net deals as TI allowances shrink</a>.</p>'),
 ('When should I start looking for new office space?',
  '<p>Start your search 6 to 18 months before your current lease expires. That window allows time for thorough due diligence, market research and negotiation without pressure, and it gives you leverage if a renewal is also on the table.</p>'),
 ('What lease protections should NYC tenants ask for?',
  '<p>Key protections include a <a href="/insights/self-help-clause-commercial-lease-nyc/">self-help clause</a>, an <a href="/insights/why-sndas-matter-to-tenants/">SNDA</a>, and security protections in case of an ownership change. These matter more than ever with many NYC landlords under financial pressure. Always have a qualified real estate attorney review your lease.</p>'),
]

def build_tenant():
    path = '/services/tenant-representation/'
    trail = [('Home', '/'), ('Services', '/services/'), ('Tenant Representation', path)]
    body = hero('nyc-office-space-tenant-representation', 'Silhouettes of professionals in a Manhattan loft office with tall windows',
        'Tenant Representation in NYC: Negotiate Your Lease With Leverage',
        'A tenant-advocate approach that arms you with confidential market and landlord data to secure better lease terms.',
        cta=('Request a Consultation', '/contact/?topic=tenant'), eyebrow='Tenant Advocate')
    body += crumbs_html(trail)
    body += f'''
<section class="section">
  <div class="wrap split">
    <div>
      <span class="eyebrow">The problem</span>
      <h2>Landlords negotiate leases every day. You don’t.</h2>
      <p>As a commercial tenant broker in New York City, we understand the complexities of lease negotiations. Landlords know the market, the comps and their own motivations. Most tenants walk in without that information.</p>
      <p>Our mission is to empower tenants. We give you the critical information and insights you need to make informed decisions throughout the process, so you negotiate with your landlord as an equal.</p>
      <p>We represent office tenants on <strong>new leases, renewals, expansions and relocations</strong> across Manhattan and NYC.</p>
    </div>
    {img('tenant-advantage-analysis-lease-research', 'Endurance advisors researching lease comps and market data on laptops', sizes='(min-width: 900px) 520px, 100vw', cls='rounded')}
  </div>
</section>

<section class="section section-dark">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">Our edge</span>
      <h2>The Tenant Advantage Analysis (TAA)</h2>
      <p class="lead">Our proprietary report goes beyond what most brokers offer. It is a confidential, comprehensive analysis of your specific leasing situation.</p>
    </div>
    <div class="grid-3">
      <div class="card"><div class="icon">{ICON['chart']}</div><h3>Market insights</h3><p>Understand current rental rates, concessions and comparable properties in your desired area.</p></div>
      <div class="card"><div class="icon">{ICON['search']}</div><h3>Landlord leverage</h3><p>Gain valuable intel on your landlord’s motivations and negotiation history, including ownership finances and loan performance.</p></div>
      <div class="card"><div class="icon">{ICON['target']}</div><h3>Strategic recommendations</h3><p>Armed with data, we develop a customized negotiation strategy to secure the best possible lease terms.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split rev">
    <div>
      <span class="eyebrow">Results driven</span>
      <h2>What the TAA delivers for tenants</h2>
      <ul class="checks">
        <li><strong>Stronger negotiating position.</strong> Negotiate with confidence and leverage.</li>
        <li><strong>Cost savings potential.</strong> Our insights can lead to significant savings on rent, concessions and other lease terms.</li>
        <li><strong>Favorable lease terms.</strong> Secure a lease that aligns with your business needs and budget.</li>
        <li><strong>Confidentiality throughout.</strong> Your information is always protected, for a smooth and stress-free negotiation.</li>
      </ul>
      <p><a class="btn btn-primary" href="/contact/?topic=tenant">Start Your Tenant Advantage Analysis {ICON['arrow']}</a></p>
    </div>
    {img('conference-room-lease-negotiation-nyc', 'Conference room table set for a commercial lease negotiation in New York', sizes='(min-width: 900px) 520px, 100vw', cls='rounded')}
  </div>
</section>

<section class="section section-mist">
  <div class="wrap">
    <div class="head center"><span class="eyebrow">Tenant results</span><h2>Tenants we’ve represented</h2></div>
    <div class="tgrid">{tcard('shemesh', True)}{tcard('berdzeni', True)}</div>
    <div class="tgrid three" style="margin-top:20px">{tcard('gofshteyn')}{tcard('levine')}{tcard('gulati')}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Tenant guides</span><h2>Know your lease protections</h2></div>
    <div class="posts three">{post_card(ARTICLES[1])}{post_card(ARTICLES[2])}{post_card(ARTICLES[3])}</div>
  </div>
</section>

<section class="section section-mist">
  <div class="wrap prose" style="margin:0 auto">
    <h2>Tenant representation FAQs</h2>
    {faq_block(TENANT_FAQ)}
    <p style="margin-top:20px">More answers on our <a href="/faq/">commercial real estate FAQ page</a>. Own a building? See <a href="/services/landlord-representation/">landlord representation</a>.</p>
  </div>
</section>
'''
    body += cta_band('Find out what your lease should really cost',
                     'Get a confidential Tenant Advantage Analysis and negotiate your next lease or renewal from a position of strength.',
                     ('Request a Consultation', '/contact/?topic=tenant'))
    page(path, 'Tenant Representation NYC | Endurance Real Estate',
         'NYC tenant representation from a true tenant advocate. Our Tenant Advantage Analysis gives you data and leverage to cut lease costs. Request a consult.',
         body, trail=trail, og_image=og_url('nyc-office-space-tenant-representation'),
         schemas=[service_schema('Tenant Representation', 'Commercial tenant representation in New York City for new leases, renewals, expansions and relocations, powered by the proprietary Tenant Advantage Analysis.', path, 'Commercial tenant representation'),
                  faq_schema(TENANT_FAQ)])

LANDLORD_FAQ = [
 ('What types of properties does Endurance lease for landlords?',
  '<p>Endurance leases buildings, office spaces, retail properties, and condo and coop commercial assets in New York City. We work with property owners, condo and coop boards, and investors in office or retail space.</p>'),
 ('How do you attract tenants to a property?',
  '<p>We attract tenants by crafting a narrative that showcases your property’s best features and competitive edge, then reaching the right prospects with focused, targeted marketing. Our leasing strategy is built on comprehensive market analysis to achieve optimal pricing and quality tenants.</p>'),
 ('How involved are you once a prospect is interested?',
  '<p>Very involved. From initial marketing to lease signing, we work closely with ownership to ensure a seamless transition from prospect to tenant, and our skilled negotiation delivers lease terms tailored to your objectives.</p>'),
 ('How are landlord leasing fees structured?',
  f'<p>{ph("CONFIRM: landlord fee and commission structure")} Endurance reviews compensation with ownership before an exclusive leasing engagement begins. Call {BIZ["phone"]} to discuss your property.</p>'),
]

def build_landlord():
    path = '/services/landlord-representation/'
    trail = [('Home', '/'), ('Services', '/services/'), ('Landlord Representation', path)]
    body = hero('nyc-retail-storefront-landlord-leasing', 'Ground-floor retail storefront for lease on a New York City street',
        'Landlord Representation in NYC That Leases Space Faster',
        'Strategic positioning, targeted marketing and skilled negotiation to attract quality tenants and boost profitability.',
        cta=('Discuss Your Property', '/contact/?topic=landlord'), eyebrow='Landlord Representation')
    body += crumbs_html(trail)
    body += f'''
<section class="section">
  <div class="wrap split">
    <div>
      <span class="eyebrow">Results-driven approach</span>
      <h2>Every property has a story. We make tenants want to hear it.</h2>
      <p>Every property has a unique blend of strengths and qualities that resonate with the right tenants. Our landlord representation team unlocks that potential by crafting a narrative that showcases your property’s best features and competitive edge.</p>
      <p>We strategically position <strong>buildings, office spaces, retail properties, and condo and coop assets</strong> across New York City to attract quality tenants, enhancing both occupancy and profitability.</p>
    </div>
    {img('landlord-leasing-market-analysis', 'Advisors reviewing leasing market analysis charts for a NYC property owner', sizes='(min-width: 900px) 520px, 100vw', cls='rounded')}
  </div>
</section>

<section class="section section-dark">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">Insight and strategy</span>
      <h2>How we lease your space</h2>
    </div>
    <div class="grid-3">
      <div class="card"><div class="icon">{ICON['chart']}</div><h3>Strategic recommendations</h3><p>Customized leasing strategies based on comprehensive market analysis, designed to achieve optimal pricing and lease terms tailored to your objectives.</p></div>
      <div class="card"><div class="icon">{ICON['megaphone']}</div><h3>Targeted marketing</h3><p>Focused marketing efforts that put your property in front of the right tenants, with exceptional follow-through.</p></div>
      <div class="card"><div class="icon">{ICON['handshake']}</div><h3>Transactional expertise</h3><p>From initial marketing to lease signing, we work closely with ownership to ensure a seamless transition from prospect to tenant.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split rev">
    <div>
      <span class="eyebrow">Your exclusive leasing partner</span>
      <h2>Why owners choose Endurance Real Estate Advisors</h2>
      <p>With decades of experience representing landlords, we understand how to optimize a property’s potential in a competitive market.</p>
      <ul class="checks">
        <li>Property owners, condo and coop boards, and office or retail investors</li>
        <li>Strategic insights, targeted marketing and skilled negotiation</li>
        <li>A dedicated team focused on leasing your space quickly</li>
        <li>Increased profitability and positioning for sustained success</li>
      </ul>
      <p><a class="btn btn-primary" href="/contact/?topic=landlord">Discuss Your Property {ICON['arrow']}</a></p>
    </div>
    {img('landlord-representation-leasing-strategy-meeting', 'Leasing strategy presentation to property ownership in a Manhattan conference room', sizes='(min-width: 900px) 520px, 100vw', cls='rounded')}
  </div>
</section>

<section class="section section-mist">
  <div class="wrap">
    <div class="head center"><span class="eyebrow">Landlord results</span><h2>Owners we’ve represented</h2></div>
    <div class="tgrid">{tcard('jerome', True)}{tcard('classi', True)}</div>
    <div class="grid-2" style="margin-top:40px;align-items:center">
      <div>
        <span class="eyebrow">Recent lease</span>
        <h3 style="font-size:1.5rem">Tribeca Prep leases 12,900+ SF at 116 Nassau Street</h3>
        <p>Tribeca Prep signed for the entire second floor at 116 Nassau Street in the Financial District. Availabilities from 5,231 to 11,365 SF remain.</p>
        <p><a href="/insights/tribeca-prep-leases-116-nassau-street/">Read about the 116 Nassau Street lease</a></p>
      </div>
      {img('tribeca-prep-lease-116-nassau-street-financial-district', '116 Nassau Street lease announcement: 12,900+ SF leased to Tribeca Prep', sizes='(min-width: 760px) 50vw, 100vw', cls='rounded')}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap prose" style="margin:0 auto">
    <h2>Landlord representation FAQs</h2>
    {faq_block(LANDLORD_FAQ)}
    <p style="margin-top:20px">More answers on our <a href="/faq/">FAQ page</a>. Looking for space instead? See <a href="/services/tenant-representation/">tenant representation</a>.</p>
  </div>
</section>
'''
    body += cta_band('Let’s put the right tenants in your space',
                     'Tell us about your building, office, retail, condo or coop asset and we will outline a leasing strategy.',
                     ('Discuss Your Property', '/contact/?topic=landlord'))
    page(path, 'Landlord Representation NYC | Endurance Real Estate',
         'NYC landlord representation for office, retail, condo and coop assets. Strategic positioning and targeted marketing to lease faster. Discuss your property.',
         body, trail=trail, og_image=og_url('nyc-retail-storefront-landlord-leasing'),
         schemas=[service_schema('Landlord Representation', 'Exclusive leasing and landlord representation in New York City for buildings, office space, retail properties, and condo and coop assets.', path, 'Commercial landlord representation and exclusive leasing'),
                  faq_schema(LANDLORD_FAQ)])

TEAM = [
 ('Gregory Gang', 'Founder & Principal', 'greg.gang@endurance-rea.com', '646-662-3546', 'gregory-gang-founder-endurance-real-estate-advisors'),
 ('Sergio Turaev', 'Director', 'sergio.turaev@endurance-rea.com', '917-981-0404', 'sergio-turaev-director-endurance-real-estate-advisors'),
 ('Mark Levy', 'Research and Analyst', 'mark.levy@endurance-rea.com', '347-882-1663', None),
 ('Jim Torre', 'Special Project Analyst', 'jim.torre@endurance-rea.com', '973-452-8445', None),
 ('Steven Andersen', 'Design and Workplace Strategy', 'steven.andersen@endurance-rea.com', '917-509-9099', None),
]

def build_about():
    trail = [('Home', '/'), ('About', '/about/')]
    people = []
    for n, r, e, p, im in TEAM:
        pic = img(im, f'{n}, {r} at Endurance Real Estate Advisors', sizes='(min-width: 760px) 260px, 100vw') if im else \
            f'<div class="avatar" role="img" aria-label="Headshot coming soon for {n}">{"".join(w[0] for w in n.split())}{ph("ADD HEADSHOT")}</div>'
        tel = '+1' + p.replace('-', '')
        people.append(f'<article class="person">{pic}<div class="info"><h3>{n}</h3><p class="role">{r}</p><a href="mailto:{e}">{e}</a><a href="tel:{tel}">{p}</a></div></article>')
    body = hero('commercial-real-estate-team-meeting-manhattan', 'Overhead view of the Endurance team meeting around a long conference table in Manhattan',
        'About Endurance Real Estate Advisors',
        'A results-driven NYC commercial real estate firm built on one principle: putting our clients’ needs first.',
        cta=('Talk to Our Team', '/contact/'), eyebrow='About Us')
    body += crumbs_html(trail)
    body += f'''
<section class="section">
  <div class="wrap split">
    <div>
      <span class="eyebrow">Our name is symbolic of who we are</span>
      <h2>A client-focused NYC commercial real estate firm</h2>
      <p>Endurance Real Estate Advisors is a results-driven, client-focused firm built on the principle of putting our clients’ needs first.</p>
      <p>With deep market knowledge, strategic expertise, and a clear understanding of both landlord and tenant priorities, we deliver insights and data that empower our clients to negotiate from a position of strength.</p>
      <p>Our tailored, thoughtful approach ensures every solution aligns with our clients’ leasing goals, one relationship at a time. Learn more about our <a href="/services/tenant-representation/">tenant representation</a> and <a href="/services/landlord-representation/">landlord representation</a> services.</p>
    </div>
    {img('commercial-real-estate-professionals-nyc', 'Group of business professionals celebrating a successful outcome', sizes='(min-width: 900px) 520px, 100vw', cls='rounded')}
  </div>
</section>
'''
    body += stats_bar()
    body += f'''
<section class="section">
  <div class="wrap">
    <div class="grid-3">
      <div class="card"><div class="icon">{ICON['shield']}</div><h3>Trusted results</h3><p>More than 1,850 successful leasing transactions for tenants and landlords.</p></div>
      <div class="card"><div class="icon">{ICON['building']}</div><h3>Proven experience</h3><p>30+ years representing landlords and tenants across New York City.</p></div>
      <div class="card"><div class="icon">{ICON['chart']}</div><h3>Market knowledge</h3><p>$3B in aggregate leasing transaction volume informs every recommendation we make.</p></div>
    </div>
  </div>
</section>

<section class="section section-dark" id="team">
  <div class="wrap">
    <div class="split" style="margin-bottom:48px">
      <div>
        <span class="eyebrow">Our team</span>
        <h2>Meet the Endurance team</h2>
        <p class="quote-big">“Working closely with our clients to establish short and long-term goals and objectives is essential to our clients’ success.”</p>
        <div class="quote-by"><div><b>Sergio Turaev</b><span>Director, Endurance Real Estate Advisors</span></div></div>
      </div>
      <div>
        <p>{ph("ADD BIO: Gregory Gang, Founder & Principal, background and experience")}</p>
        <p>{ph("ADD BIO: Sergio Turaev, Director")}</p>
      </div>
    </div>
    <div class="team">{''.join(people)}</div>
  </div>
</section>

<section class="section section-mist" id="testimonials">
  <div class="wrap">
    <div class="head center"><span class="eyebrow">Testimonials</span><h2>Trusted by NYC tenants, owners and investors</h2></div>
    <div class="tgrid">{tcard('shemesh', True)}{tcard('berdzeni', True)}</div>
    <div class="tgrid three" style="margin-top:20px">
      {tcard('jenna')}{tcard('ibragimov')}{tcard('jerome')}
      {tcard('gofshteyn')}{tcard('gulati')}{tcard('levine')}
    </div>
    <div class="tgrid" style="margin-top:20px">{tcard('classi')}<figure class="tcard"><blockquote><p>{ph("ADD TESTIMONIAL HERE")}</p></blockquote><figcaption><b>{ph("Client name")}</b>{ph("Title, Company")}</figcaption></figure></div>
  </div>
</section>

<section class="section" id="careers">
  <div class="wrap split">
    <div>
      <span class="eyebrow">Careers</span>
      <h2>Join our team</h2>
      <p>As we grow our platform, we are always looking for exceptional, qualified individuals to join our team. If you share our commitment to putting clients first, we would like to hear from you.</p>
      <p><a class="btn btn-primary" href="/contact/?topic=careers">Reach Out About Careers {ICON['arrow']}</a></p>
    </div>
    {img('tenant-advantage-analysis-lease-research', 'Team members collaborating on laptops in an office', sizes='(min-width: 900px) 520px, 100vw', cls='rounded')}
  </div>
</section>
'''
    body += cta_band()
    persons = [{'@type': 'Person', 'name': n, 'jobTitle': r, 'email': e, 'telephone': '+1' + p.replace('-', ''),
                'worksFor': {'@id': DOMAIN + '/#business'}, **({'image': DOMAIN + f'/images/{im}.jpg'} if im else {})}
               for n, r, e, p, im in TEAM]
    schema = {'@context': 'https://schema.org', '@type': 'AboutPage', 'name': 'About Endurance Real Estate Advisors',
              'url': DOMAIN + '/about/', 'about': {'@id': DOMAIN + '/#business'}, 'mainEntity': persons}
    page('/about/', 'About Our NYC Commercial Real Estate Team | Endurance',
         'Meet Endurance Real Estate Advisors: 30+ years, 1,850+ leases and $3B in NYC volume for tenants and landlords. Meet the team and contact us today.',
         body, schemas=[schema], trail=trail, og_image=og_url('commercial-real-estate-team-meeting-manhattan'))

FAQ = [
 ('Services', [
  ('What does Endurance Real Estate Advisors do?',
   '<p>Endurance Real Estate Advisors is a full-service commercial real estate brokerage and advisory firm in New York City that represents tenants and landlords in commercial leasing. We help tenants lease, renew, expand or relocate office space, and we help owners lease buildings, office, retail, and condo and coop assets. Our focus is attention to detail and exceeding clients’ expectations.</p>'),
  ('What is tenant representation?',
   '<p>Tenant representation means a broker negotiates exclusively on the tenant’s behalf to secure the best lease terms. As a tenant advocate, Endurance provides the market data, landlord intel and negotiation strategy tenants need to make informed decisions. Learn more about our <a href="/services/tenant-representation/">tenant representation services</a>.</p>'),
  ('What is the Tenant Advantage Analysis (TAA)?',
   '<p>The Tenant Advantage Analysis is Endurance’s proprietary, confidential report on a tenant’s specific leasing situation. It covers current rental rates, concessions and comparable properties, intel on the landlord’s motivations and negotiation history, and a customized negotiation strategy.</p>'),
  ('What types of properties do you lease for landlords?',
   '<p>Endurance leases buildings, office spaces, retail properties, and condo and coop commercial assets for owners, boards and investors. We position each property with a tailored narrative and targeted marketing to attract quality tenants. See our <a href="/services/landlord-representation/">landlord representation services</a>.</p>'),
  ('Do you handle lease renewals as well as relocations?',
   '<p>Yes, Endurance negotiates renewals, expansions and relocations. One client toured over 75 spaces across 9 months and ultimately expanded within their current building because it made the most financial sense. Another client’s relocation grew their footprint from 11,000 SF to over 38,000 SF.</p>'),
 ]),
 ('Pricing', [
  ('How much does it cost to hire Endurance?',
   f'<p>{ph("CONFIRM: fee structure for tenant and landlord assignments, for example whether tenant-rep fees are paid by the landlord")} Endurance explains how its compensation works before any engagement begins. Call {BIZ["phone"]} to discuss your situation.</p>'),
 ]),
 ('Process and timing', [
  ('When should I start looking for new office space?',
   '<p>Start looking 6 to 18 months before your current lease expires. This allows ample time for due diligence, market research and negotiation without pressure.</p>'),
  ('How long does it take to find and lease commercial space?',
   f'<p>{ph("CONFIRM: typical timeline from first meeting to signed lease")} Timing depends on your requirements and the market. For example, one Endurance client toured over 75 spaces across 9 months before signing the lease that made the most financial sense.</p>'),
  ('What happens to my lease if my landlord is in financial trouble?',
   '<p>Landlord distress can give tenants negotiating leverage, such as lower rent, abatements or better renewal terms, but it also brings risks like reduced services and ownership uncertainty. Endurance researches ownership finances, loan performance and debt maturity before negotiating, and helps tenants secure protections such as an SNDA. Read <a href="/insights/lessons-from-a-landlords-troubles/">lessons from a landlord’s troubles</a>.</p>'),
  ('What lease protections should a commercial tenant negotiate?',
   '<p>Commercial tenants in NYC should negotiate a self-help clause, an SNDA and security protections in case of an ownership change. A self-help clause lets you fix certain landlord failures and recover the cost, while an SNDA protects your lease if the lender forecloses. Always have a qualified real estate attorney review your lease.</p>'),
  ('Is my information kept confidential?',
   '<p>Yes. Confidentiality is built into the Endurance process, and your information is always protected throughout the negotiation.</p>'),
 ]),
 ('Experience and service area', [
  ('What areas does Endurance serve?',
   f'<p>Endurance serves tenants and landlords across New York City from its office at 136 Madison Avenue in Manhattan. Recent work includes the Financial District, where Tribeca Prep leased 12,900+ SF at 116 Nassau Street. {ph("CONFIRM: other boroughs or markets served")}</p>'),
  ('How experienced is the Endurance team?',
   '<p>Endurance has 30+ years of experience representing landlords and tenants across NYC, more than 1,850 successful leasing transactions, and $3B in aggregate leasing transaction volume. The team is led by Founder and Principal Gregory Gang. <a href="/about/#team">Meet the team</a>.</p>'),
  ('Is Endurance a licensed real estate brokerage?',
   f'<p>{ph("CONFIRM: New York State real estate broker license details")}</p>'),
 ]),
 ('Getting started', [
  ('How do I get started with Endurance?',
   f'<p>Call <a href="tel:{BIZ["tel"]}">{BIZ["phone"]}</a>, email <a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a>, or send a message through our <a href="/contact/">contact form</a>. We will discuss your goals, whether you are a tenant or a landlord, and outline next steps.</p>'),
 ]),
]

def build_faq():
    trail = [('Home', '/'), ('FAQ', '/faq/')]
    allq = [qa for _, items in FAQ for qa in items]
    assert 10 <= len(allq) <= 15, len(allq)
    groups = ''.join(f'<div class="faq-group"><h2>{g}</h2>{faq_block(items)}</div>' for g, items in FAQ)
    body = hero('tenant-advantage-analysis-lease-research', 'Advisors researching commercial lease questions on laptops',
        'NYC Commercial Real Estate FAQ',
        'Straight answers about tenant and landlord representation, lease protections, timing and getting started.',
        eyebrow='Frequently Asked Questions')
    body += crumbs_html(trail)
    body += f'''
<section class="section">
  <div class="wrap prose" style="margin:0 auto">
    <p class="lead">Answers to the questions NYC tenants and property owners ask us most about commercial leasing. Don’t see yours? <a href="/contact/">Ask us directly</a>.</p>
    {groups}
  </div>
</section>
'''
    body += cta_band('Still have questions?', 'Talk to an experienced NYC commercial real estate advisor about your space or your building.')
    page('/faq/', 'Commercial Real Estate FAQ NYC | Endurance REA',
         'Answers on NYC tenant and landlord representation: fees, timing, lease protections, SNDAs and how to get started. Read the FAQ or call (646) 662-3546.',
         body, schemas=[faq_schema(allq)], trail=trail, og_image=og_url('tenant-advantage-analysis-lease-research'))

def build_insights():
    trail = [('Home', '/'), ('Insights', '/insights/')]
    cards = ''.join(post_card(a, 'h2') for a in ARTICLES)
    body = hero('conference-room-lease-negotiation-nyc', 'Conference room prepared for a commercial lease discussion',
        'NYC Commercial Leasing Insights',
        'Pulse & Perspective: practical guidance on lease protections, renewals and today’s market from Endurance.',
        cta=('Talk to an Advisor', '/contact/'), eyebrow='Pulse & Perspective')
    body += crumbs_html(trail)
    body += f'''
<section class="section">
  <div class="wrap">
    <div class="head"><p class="lead">Our team shares what we see every day negotiating leases in New York City, so tenants and owners can make better decisions. Need advice on your own situation? Explore <a href="/services/tenant-representation/">tenant representation</a> or <a href="/services/landlord-representation/">landlord representation</a>.</p></div>
    <div class="posts three">{cards}</div>
  </div>
</section>
'''
    body += cta_band()
    schema = {'@context': 'https://schema.org', '@type': 'Blog', 'name': 'Pulse & Perspective: NYC Commercial Leasing Insights',
              'url': DOMAIN + '/insights/', 'publisher': {'@id': DOMAIN + '/#business'},
              'blogPost': [{'@type': 'BlogPosting', 'headline': a['title'], 'url': f"{DOMAIN}/insights/{a['slug']}/"} for a in ARTICLES]}
    page('/insights/', 'NYC Commercial Leasing Insights | Endurance REA',
         'Guides for NYC tenants and landlords on self-help clauses, SNDAs, TI allowances, renewals and distressed landlords. Read insights from Endurance today.',
         body, schemas=[schema], trail=trail, og_image=og_url('conference-room-lease-negotiation-nyc'))

def build_articles():
    for a in ARTICLES:
        path = f"/insights/{a['slug']}/"
        trail = [('Home', '/'), ('Insights', '/insights/'), (a['title'], path)]
        others = [o for o in ARTICLES if o is not a][:3]
        body = hero(a['img'], a['img_alt'], esc(a['title']), esc(a['excerpt']),
                    cta=a['cta'], eyebrow=a['tag'],
                    extra=f'<p class="meta">By Endurance Real Estate Advisors {ph("CONFIRM: author")} · <time datetime="2026-11-20">November 20, 2026</time> {ph("CONFIRM: original publish date")}</p>')
        body += crumbs_html(trail)
        body += f'''
<article class="section">
  <div class="wrap prose" style="margin:0 auto">
    {a['body']()}
  </div>
</article>
<section class="section section-mist">
  <div class="wrap">
    <div class="head"><h2>More insights</h2></div>
    <div class="posts three">{''.join(post_card(o) for o in others)}</div>
  </div>
</section>
'''
        body += cta_band(primary=a['cta'])
        schema = {'@context': 'https://schema.org', '@type': 'Article', 'headline': a['title'], 'description': a['desc'],
                  'image': DOMAIN + f"/images/{a['img']}.jpg", 'datePublished': '2026-11-20', 'dateModified': '2026-11-20',
                  'author': {'@type': 'Organization', 'name': BIZ['name'], 'url': DOMAIN + '/'},
                  'publisher': {'@type': 'Organization', 'name': BIZ['name'], 'logo': {'@type': 'ImageObject', 'url': DOMAIN + '/apple-touch-icon.png'}},
                  'mainEntityOfPage': DOMAIN + path}
        page(path, a['seo_title'], a['desc'], body, schemas=[schema], trail=trail, og_image=og_url(a['img']), og_type='article')

def build_contact():
    trail = [('Home', '/'), ('Contact', '/contact/')]
    body = hero('manhattan-skyline-brooklyn-bridge-nyc', 'Manhattan skyline and Brooklyn Bridge at night',
        'Contact Our NYC Commercial Real Estate Brokers',
        'Attention and service you would expect from a trusted friend, with the expertise of a seasoned veteran.',
        cta=(f'Call {BIZ["phone"]}', f'tel:{BIZ["tel"]}'), eyebrow='Contact Us')
    body += crumbs_html(trail)
    body += f'''
<section class="section">
  <div class="wrap contact-grid">
    <div>
      <h2>Tell us about your space or your building</h2>
      <p>Whether you are a tenant planning a lease, renewal or relocation, or an owner looking to lease up a property, send us a note and we will be in touch.</p>
      <!-- To receive submissions without opening the visitor's email app, set data-endpoint to a form service URL (for example Formspree or a Cloudflare Pages Function). -->
      <form class="form" id="contact-form" action="mailto:{BIZ['email']}" method="post" enctype="text/plain" data-endpoint="" novalidate>
        <div class="row">
          <div><label for="first_name">First name <span class="req" aria-hidden="true">*</span></label><input id="first_name" name="first_name" autocomplete="given-name" required></div>
          <div><label for="last_name">Last name <span class="req" aria-hidden="true">*</span></label><input id="last_name" name="last_name" autocomplete="family-name" required></div>
        </div>
        <div class="row">
          <div><label for="email">Email <span class="req" aria-hidden="true">*</span></label><input id="email" name="email" type="email" autocomplete="email" required></div>
          <div><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
        </div>
        <div class="row">
          <div><label for="company">Company</label><input id="company" name="company" autocomplete="organization"></div>
          <div><label for="topic">I am interested in</label>
            <select id="topic" name="topic">
              <option value="tenant">Tenant representation (leasing or renewing space)</option>
              <option value="landlord">Landlord representation (leasing my property)</option>
              <option value="careers">Careers at Endurance</option>
              <option value="other">Something else</option>
            </select></div>
        </div>
        <div><label for="message">Message <span class="req" aria-hidden="true">*</span></label><textarea id="message" name="message" required placeholder="Square footage, location, timing, or anything else we should know"></textarea></div>
        <div class="sr-only" aria-hidden="true"><label for="company_website">Leave this field empty</label><input id="company_website" name="company_website" tabindex="-1" autocomplete="off"></div>
        <label class="check"><input type="checkbox" name="email_permission" value="yes"> By checking this box, you grant us permission to email you. You may unsubscribe at any time.</label>
        <div><button class="btn btn-primary" type="submit">Send Message {ICON['arrow']}</button></div>
        <p class="form-status" id="form-status" role="status" aria-live="polite"></p>
      </form>
    </div>
    <aside class="info-card" aria-labelledby="office-h">
      <h2 id="office-h" style="font-size:1.5rem">Our Manhattan office</h2>
      <dl>
        <dt>Phone</dt><dd><a href="tel:{BIZ['tel']}">{BIZ['phone']}</a></dd>
        <dt>Email</dt><dd><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></dd>
        <dt>Address</dt><dd>{BIZ['street']}<br>{BIZ['city']}, {BIZ['region']} {BIZ['zip']}<br><a href="{BIZ['maps']}" rel="noopener" target="_blank">Get directions</a></dd>
        <dt>Office hours</dt><dd>{ph("CONFIRM: office hours")}</dd>
        <dt>Service area</dt><dd>New York City, including Manhattan</dd>
        <dt>Follow us</dt><dd><a href="{BIZ['instagram']}" rel="noopener" target="_blank">Instagram</a> · <a href="{BIZ['linkedin']}" rel="noopener" target="_blank">LinkedIn</a></dd>
      </dl>
    </aside>
  </div>
</section>
<section class="section section-mist">
  <div class="wrap">
    <div class="head center"><h2>Before you reach out</h2><p class="lead center">Explore <a href="/services/tenant-representation/">tenant representation</a>, <a href="/services/landlord-representation/">landlord representation</a>, or read our <a href="/faq/">frequently asked questions</a>.</p></div>
    <div class="tgrid">{tcard('ibragimov')}{tcard('gulati')}</div>
  </div>
</section>
'''
    schema = {'@context': 'https://schema.org', '@type': 'ContactPage', 'name': 'Contact Endurance Real Estate Advisors',
              'url': DOMAIN + '/contact/', 'about': {'@id': DOMAIN + '/#business'}}
    page('/contact/', 'Contact a NYC Commercial Real Estate Broker | Endurance',
         'Contact Endurance Real Estate Advisors at 136 Madison Ave, New York. Call (646) 662-3546 or send a message about leasing office or retail space today.',
         body, schemas=[schema], trail=trail)

def build_404():
    body = f'''<section class="hero hero-sm nf">
  <div class="hero-img">{img('manhattan-skyline-brooklyn-bridge-nyc', 'Manhattan skyline at night', eager=True)}</div>
  <div class="wrap">
    <span class="eyebrow">Error 404</span>
    <h1>We couldn’t find that page</h1>
    <p class="sub">The page may have moved when we launched our new site. Let’s get you where you need to go.</p>
    <div class="hero-actions"><a class="btn btn-primary" href="/">Go to the Homepage {ICON['arrow']}</a><a class="btn btn-ghost" href="/contact/">Contact Us</a></div>
  </div>
</section>
<section class="section"><div class="wrap">
  <h2>Popular pages</h2>
  <ul class="checks">
    <li><a href="/services/tenant-representation/">Tenant representation in NYC</a></li>
    <li><a href="/services/landlord-representation/">Landlord representation in NYC</a></li>
    <li><a href="/about/">About Endurance Real Estate Advisors</a></li>
    <li><a href="/insights/">NYC commercial leasing insights</a></li>
    <li><a href="/faq/">Commercial real estate FAQ</a></li>
  </ul>
</div></section>'''
    page('/404.html', 'Page Not Found | Endurance Real Estate Advisors',
         'Sorry, this page could not be found. Visit the Endurance Real Estate Advisors homepage or contact our NYC commercial real estate team for help today.',
         body, robots='noindex,follow')

def build_meta_files():
    urls = [p for p, r in PAGES if r.startswith('index')]
    pri = {'/': '1.0'}
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in urls:
        xml.append(f'  <url><loc>{DOMAIN}{p}</loc><lastmod>{BUILD_DATE}</lastmod><priority>{pri.get(p, "0.8" if p.count("/") <= 3 and not p.startswith("/insights/") or p == "/insights/" else "0.6")}</priority></url>')
    xml.append('</urlset>')
    open(os.path.join(SITE, 'sitemap.xml'), 'w').write('\n'.join(xml) + '\n')
    open(os.path.join(SITE, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')

if __name__ == '__main__':
    build_home(); build_services(); build_tenant(); build_landlord(); build_about()
    build_faq(); build_insights(); build_articles(); build_contact(); build_404()
    build_meta_files()
    print('\n'.join(p for p, _ in PAGES))
