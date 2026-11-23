#!/usr/bin/env python3
"""Static site generator for endurance-rea.com.

Writes plain HTML into ../site. Edit content in this file, articles.py or
faqs.py, then run:  python3 tools/build.py
"""
import json, os, re
from datetime import date

from common import SITE, DOMAIN, BIZ, OG_DEFAULT, ICON, esc, ph, img
from articles import ARTICLES
from faqs import TENANT_FAQ, LANDLORD_FAQ, FAQ

BUILD_DATE = date.today().isoformat()
V = '3'  # asset version for cache busting
FONTS = 'https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:ital,wght@0,400;0,500;0,600;1,400&display=swap'
PAGES = []
ARROW = ICON['arrow']

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
            subs = ''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if path == h else ""}>{l}</a></li>' for l, h in sub)
            items.append(f'<li class="has-sub"><a href="{href}"{cur}>{label}</a><ul class="sub">{subs}</ul></li>')
        else:
            items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    cur = ' aria-current="page"' if path == '/contact/' else ''
    items.append(f'<li class="nav-contact-m"><a href="/contact/"{cur}>Contact</a></li>')
    return f'''<a class="skip" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="wrap hdr">
    <a class="logo" href="/" aria-label="{BIZ['name']} home"><img src="/images/brand/endurance-real-estate-advisors-logo.svg" width="196" height="37" alt="{BIZ['name']} logo"></a>
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
        <a href="/" aria-label="{BIZ['name']} home"><img src="/images/brand/endurance-real-estate-advisors-logo.svg" width="196" height="37" alt="{BIZ['name']} logo" loading="lazy"></a>
        <p style="margin-top:20px;max-width:36ch">A full-service commercial real estate brokerage and advisory firm in New York City, representing tenants and landlords.</p>
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
          <li><a href="/about/">About and Team</a></li>
          <li><a href="/insights/">Insights</a></li>
          <li><a href="/faq/">FAQ</a></li>
          <li><a href="/about/#careers">Careers</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </div>
      <div>
        <h2>Office</h2>
        <address>
          {BIZ['street']}<br>{BIZ['city']}, {BIZ['region']} {BIZ['zip']}<br>
          <a href="tel:{BIZ['tel']}">{BIZ['phone']}</a><br>
          <a href="mailto:{BIZ['email']}">{BIZ['email']}</a>
        </address>
      </div>
    </div>
    <div class="fbottom">
      <span>&copy; {date.today().year} {BIZ['name']}</span>
      <span>Commercial real estate brokerage, New York City</span>
    </div>
  </div>
</footer>
<div class="mbar" aria-label="Quick contact">
  <a class="btn btn-light" href="tel:{BIZ['tel']}">{ICON['phone']} Call</a>
  <a class="btn btn-primary" href="/contact/">Contact Us</a>
</div>
<script src="/js/main.js?v={V}" defer></script>'''


def crumbs_html(trail):
    lis = []
    for i, (name, href) in enumerate(trail):
        lis.append(f'<li aria-current="page">{esc(name)}</li>' if i == len(trail) - 1 else f'<li><a href="{href}">{esc(name)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>{"".join(lis)}</ol></div></nav>'


def crumbs_schema(trail):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': DOMAIN + h}
                                for i, (n, h) in enumerate(trail)]}


def hero(image, alt, h1, sub, cta=('Schedule a Consultation', '/contact/'), second=None, home=False,
         focal=('50% 50%', '50% 50%'), extra=''):
    btns = f'<a class="btn btn-primary" href="{cta[1]}">{cta[0]} {ARROW}</a>' if cta else ''
    if second:
        btns += f'<a class="btn btn-light" href="{second[1]}">{second[0]}</a>'
    return f'''<section class="hero {'hero-home' if home else 'hero-inner'}">
  <div class="hero-media">{img(image, alt, eager=True, focal=focal)}</div>
  <div class="wrap hero-body">
    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
    {extra}
    <div class="hero-actions">{btns}</div>
  </div>
</section>'''


def cta_band(title='Negotiate your next lease from a position of strength',
             text='Advice, attention and service you would expect from a friend, with the expertise of an industry veteran.',
             primary=('Schedule a Consultation', '/contact/')):
    return f'''<section class="cta" aria-label="Contact Endurance Real Estate Advisors">
  <div class="wrap">
    <div><h2>{title}</h2><p>{text}</p></div>
    <div class="btns">
      <a class="btn btn-primary" href="{primary[1]}">{primary[0]} {ARROW}</a>
      <a class="btn btn-dark" href="tel:{BIZ['tel']}">{ICON['phone']} {BIZ['phone']}</a>
    </div>
  </div>
</section>'''


def page(path, title, desc, body, schemas=(), trail=None, og_image=None, og_type='website', robots='index,follow'):
    assert len(title) <= 60, (path, len(title), title)
    assert 140 <= len(desc) <= 160, (path, len(desc), desc)
    assert '—' not in body and '–' not in body, path
    canonical = DOMAIN + path
    schema_tags = '\n'.join(
        f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False, separators=(",", ":"))}</script>'
        for s in list(schemas) + ([crumbs_schema(trail)] if trail else []))
    og = DOMAIN + (og_image or OG_DEFAULT)
    if trail:
        body = body.replace('<!--CRUMBS-->', crumbs_html(trail), 1)
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#17191c">
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{FONTS}"></noscript>
<link rel="stylesheet" href="/css/style.css?v={V}">
<script>document.documentElement.classList.add('js');setTimeout(function(){{if(!window.__reveal)document.documentElement.classList.add('reveal-off')}},3000)</script>
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


# ---------------------------------------------------------------- shared content
# Testimonials, verbatim from the existing site (em dashes replaced with punctuation).
T = {
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


def pull(key=None, quote=None, name=None, role=None, photo=None, large=False):
    if key:  # client testimonial: featured message card
        q, n, r = T[key]
        return (f'<figure class="q q-feature"><blockquote><p>“{esc(q)}”</p></blockquote>'
                f'<figcaption><b>{esc(n)}</b><span>{esc(r)}</span></figcaption></figure>')
    pic = img(photo, f'{name}, {role}', sizes='160px' if large else '76px') if photo else ''
    cls = 'pull long' if len(quote) > 160 else 'pull'
    if large:
        cls += ' lg'
    return f'<figure class="{cls}"><blockquote><p>“{esc(quote)}”</p></blockquote><figcaption>{pic}<span><b>{esc(name)}</b>{esc(role)}</span></figcaption></figure>'


def quotes(*keys):
    items = ''.join(f'<figure class="q"><blockquote><p>“{esc(T[k][0])}”</p></blockquote><figcaption><b>{esc(T[k][1])}</b><span>{esc(T[k][2])}</span></figcaption></figure>' for k in keys)
    return f'<div class="quotes">{items}</div>'


def stats():
    return '''<section class="stats" aria-label="Track record">
  <div class="wrap">
    <div class="stat"><b>1,850+</b><span>Successful leasing transactions</span></div>
    <div class="stat"><b>30+ years</b><span>Representing landlords and tenants across NYC</span></div>
    <div class="stat"><b>$3B</b><span>In aggregate leasing transaction volume</span></div>
  </div>
</section>'''


def split(media, text, rev=False, cls=''):
    return f'<div class="split{" rev" if rev else ""}{(" " + cls) if cls else ""}"><div class="media">{media}</div><div>{text}</div></div>'


def faq_block(items):
    out = ''.join(f'<details class="faq" name="faq"><summary><h3>{esc(q)}</h3></summary><div class="a">{a}</div></details>' for q, a in items)
    return f'<div class="faqs">{out}</div>'


def strip_tags(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()


def faq_schema(items):
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': strip_tags(a)}} for q, a in items]}


ORG_REF = {'@type': 'RealEstateAgent', '@id': DOMAIN + '/#business', 'name': BIZ['name'], 'url': DOMAIN + '/'}
AREA = [{'@type': 'City', 'name': 'New York City'}, {'@type': 'Place', 'name': 'Manhattan, New York'}]


def service_schema(name, desc, path, stype):
    return {'@context': 'https://schema.org', '@type': 'Service', 'name': name, 'serviceType': stype,
            'description': desc, 'url': DOMAIN + path, 'provider': ORG_REF, 'areaServed': AREA}


def post_card(a):
    im, alt = a['img'], a['img_alt']
    return f'''<a class="post" href="/insights/{a['slug']}/">
  {img(im, alt, sizes='(min-width: 760px) 33vw, 100vw')}
  <h3>{esc(a['title'])}</h3><p>{esc(a['excerpt'])}</p><span class="more">Read the article {ARROW}</span>
</a>'''


def post_row(a):
    im, alt = a['img'], a['img_alt']
    return f'''<a class="postrow" href="/insights/{a['slug']}/">
  {img(im, alt, sizes='(min-width: 800px) 360px, 100vw')}
  <div><time datetime="2026-11-20">November 20, 2026</time><h2>{esc(a['title'])}</h2><p>{esc(a['excerpt'])}</p><span class="more">Read the article {ARROW}</span></div>
</a>'''


TEAM = [
 ('Gregory Gang', 'Founder & Principal', 'greg.gang@endurance-rea.com', '646-662-3546', 'gregory-gang-founder-endurance-real-estate-advisors', 'https://www.linkedin.com/in/gregory-gang-276263a/'),
 ('Sergio Turaev', 'Director', 'sergio.turaev@endurance-rea.com', '917-981-0404', 'sergio-turaev-director-endurance-real-estate-advisors', 'https://www.linkedin.com/in/sergioturaev/'),
 ('Mark Levy', 'Research and Analyst', 'mark.levy@endurance-rea.com', '347-882-1663', 'mark-levy-research-analyst-endurance-real-estate-advisors', 'https://www.linkedin.com/in/marklevy10/'),
 ('Jim Torre', 'Special Project Analyst', 'jim.torre@endurance-rea.com', '973-452-8445', 'jim-torre-special-project-analyst-endurance-real-estate-advisors', 'https://www.linkedin.com/in/jim-torre-a67467178/'),
 ('Steven Andersen', 'Design and Workplace Strategy', 'steven.andersen@endurance-rea.com', '917-509-9099', 'steven-andersen-design-workplace-strategy-endurance-real-estate-advisors', None),
]

# ================================================================ PAGES
def build_home():
    biz_schema = {
        '@context': 'https://schema.org', '@type': 'RealEstateAgent', '@id': DOMAIN + '/#business',
        'name': BIZ['name'], 'url': DOMAIN + '/',
        'description': 'Full-service commercial real estate brokerage and advisory firm in New York City providing tenant representation and landlord representation for office and retail space.',
        'telephone': BIZ['tel'], 'email': BIZ['email'],
        'image': DOMAIN + OG_DEFAULT, 'logo': DOMAIN + '/apple-touch-icon.png',
        'address': {'@type': 'PostalAddress', 'streetAddress': BIZ['street'], 'addressLocality': BIZ['city'],
                    'addressRegion': BIZ['region'], 'postalCode': BIZ['zip'], 'addressCountry': 'US'},
        'areaServed': AREA,
        'sameAs': [BIZ['instagram'], BIZ['linkedin']],
        'founder': {'@type': 'Person', 'name': 'Gregory Gang', 'jobTitle': 'Founder & Principal', 'sameAs': [TEAM[0][5]]},
        'knowsAbout': ['Tenant representation', 'Landlord representation', 'Commercial office leasing', 'Retail leasing', 'Lease negotiation', 'SNDA agreements', 'Lease renewals'],
        'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Commercial real estate services', 'itemListElement': [
            {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'Tenant Representation', 'url': DOMAIN + '/services/tenant-representation/'}},
            {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'Landlord Representation', 'url': DOMAIN + '/services/landlord-representation/'}},
        ]},
        # 'openingHoursSpecification': add once office hours are confirmed
    }
    site_schema = {'@context': 'https://schema.org', '@type': 'WebSite', '@id': DOMAIN + '/#website', 'name': BIZ['name'], 'url': DOMAIN + '/', 'publisher': {'@id': DOMAIN + '/#business'}}
    body = hero('manhattan-skyline-brooklyn-bridge-nyc', 'Lower Manhattan skyline and the Brooklyn Bridge at night, New York City',
        'NYC Commercial Real Estate Brokers Who Put Your Interests First',
        'Tenant and landlord representation in New York City, backed by 30+ years of experience and the data to negotiate from strength.',
        second=('Explore Our Services', '/services/'), home=True, focal=('68% 55%', '77% 50%'))
    body += stats()
    body += f'''
<section class="section">
  <div class="wrap">
    <div class="intro">
      <h2>Commercial real estate advisors for both sides of the lease</h2>
      <p class="lead">Endurance Real Estate Advisors is a full-service commercial real estate brokerage and advisory firm in New York City. We are results-driven, focused on attention to detail, and committed to exceeding our clients’ expectations.</p>
    </div>
    {split(img('nyc-office-space-tenant-representation', 'Professionals in a bright Manhattan loft office with tall windows', sizes='(min-width: 900px) 50vw, 100vw'),
      f"""<h3>For tenants: representation that gives you leverage</h3>
      <p>Leasing, renewing, expanding or relocating, we develop and implement solution-based transactions using an intimate knowledge of your needs and every part of the NYC market. It starts with our proprietary Tenant Advantage Analysis, a confidential look at rents, concessions and your landlord’s position.</p>
      <a class="more" href="/services/tenant-representation/">Tenant representation in NYC {ARROW}</a>""")}
    {split(img('nyc-retail-storefront-landlord-leasing', 'Ground-floor retail storefront on a New York City street', sizes='(min-width: 900px) 50vw, 100vw'),
      f"""<h3>For owners: a leasing strategy built around your asset</h3>
      <p>We work with owners, investors, and condo and coop boards to deliver a customized, efficient leasing strategy that protects their interests and helps each office, retail, condo or coop asset realize its full potential with quality tenants.</p>
      <a class="more" href="/services/landlord-representation/">Landlord representation in NYC {ARROW}</a>""", rev=True)}
  </div>
</section>

<section class="section dark">
  <div class="wrap cols">
    <div>
      {pull(quote='Our sole fiduciary duty is to protect the interests of our clients, and we strive to do it better than anyone else in the business.', name='Gregory Gang', role='Founder & Principal', photo='gregory-gang-founder-endurance-real-estate-advisors', large=True)}
      <p style="margin-top:36px"><a class="btn btn-light" href="/about/#team">Meet the Team</a></p>
    </div>
    <div>
      <h2>Why NYC businesses and owners choose Endurance</h2>
      <ul class="rows">
        <li><strong class="t">Our name is symbolic of who we are</strong><p>We see every deal through, from the first tour to the signed lease.</p></li>
        <li><strong class="t">Insight that creates leverage</strong><p>We research ownership finances, loan performance and market comps before we negotiate.</p></li>
        <li><strong class="t">Both sides of the table</strong><p>A clear understanding of landlord and tenant priorities helps us structure deals that close.</p></li>
        <li><strong class="t">Senior attention on every assignment</strong><p>Advice and service you would expect from a friend, with the expertise of an industry veteran.</p></li>
      </ul>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="intro"><h2>What our clients say</h2></div>
    {pull('shemesh')}
    {quotes('berdzeni', 'gofshteyn', 'classi', 'ibragimov')}
    <p style="margin-top:40px"><a class="more" href="/about/#testimonials">Read more client testimonials {ARROW}</a></p>
  </div>
</section>

<section class="section warm">
  <div class="wrap">
    {split(img('client-strategy-meeting-nyc-office', 'Endurance advisors meeting with clients around a conference table in a New York office', sizes='(min-width: 900px) 50vw, 100vw'),
      """<h2>Every assignment starts with your goals</h2>
      <p>We begin by listening. Working closely with you, we establish your short and long-term goals and objectives, whether you need room for a growing company or the right tenants for a building.</p>
      <p>Then we do the research. For tenants, that means a confidential Tenant Advantage Analysis covering current rents, concessions, comparable properties and your landlord’s motivations. For owners, it means a leasing strategy built on comprehensive market analysis and a clear story about what makes the property worth leasing.</p>
      <p>From there we negotiate, and we stay involved through lease signing. One client toured more than 75 spaces with us over nine months before choosing the option that made the most financial sense. In her words, Endurance was relentless.</p>""", rev=True)}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="intro">
      <h2>NYC commercial leasing insights</h2>
      <p class="lead">Practical guidance on lease protections, renewals and today’s market from our team, published as Pulse &amp; Perspective. <a href="/insights/">View all insights</a>.</p>
    </div>
    <div class="posts">{post_card(ARTICLES[0])}{post_card(ARTICLES[1])}{post_card(ARTICLES[2])}</div>
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
        'Representation for tenants and landlords, with one goal: protecting your interests at every step of the lease.',
        focal=('60% 45%', '62% 50%'))
    body += '<!--CRUMBS-->'
    body += f'''
<section class="section">
  <div class="wrap">
    <div class="intro">
      <h2>Two specialties, one standard of service</h2>
      <p class="lead">Endurance Real Estate Advisors provides commercial real estate brokerage and advisory services across New York City. Because we understand both landlord and tenant priorities, we deliver the insight and data that let every client negotiate from a position of strength.</p>
    </div>
    {split(img('tenant-advantage-analysis-lease-research', 'Team researching market data on laptops for a tenant lease analysis', sizes='(min-width: 900px) 50vw, 100vw'),
      f"""<h3>Tenant representation</h3>
      <p>We act as your tenant advocate for new leases, renewals, expansions and relocations of office space in NYC.</p>
      <ul class="plain">
        <li>Proprietary Tenant Advantage Analysis</li>
        <li>Market rents, concessions and comparable properties</li>
        <li>Landlord motivations and negotiation history</li>
        <li>A customized negotiation strategy</li>
      </ul>
      <a class="more" href="/services/tenant-representation/">Explore tenant representation {ARROW}</a>""")}
    {split(img('landlord-leasing-market-analysis', 'Advisors reviewing leasing market charts and financial reports for a property owner', sizes='(min-width: 900px) 50vw, 100vw'),
      f"""<h3>Landlord representation</h3>
      <p>We serve as exclusive leasing partner for building owners, investors, and condo and coop boards with office and retail space.</p>
      <ul class="plain">
        <li>Property positioning and narrative</li>
        <li>A leasing strategy built on market analysis</li>
        <li>Targeted marketing to quality tenants</li>
        <li>Hands-on support from marketing to lease signing</li>
      </ul>
      <a class="more" href="/services/landlord-representation/">Explore landlord representation {ARROW}</a>""", rev=True)}
  </div>
</section>
'''
    body += stats()
    body += f'''
<section class="section">
  <div class="wrap">
    <div class="intro"><h2>Trusted by tenants and owners across NYC</h2></div>
    {pull('levine')}
    {quotes('jerome', 'gulati')}
    <p style="margin-top:40px">Have questions first? Read our <a href="/faq/">commercial real estate FAQ</a>.</p>
  </div>
</section>
'''
    body += cta_band()
    schema = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Commercial real estate services in NYC', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'url': DOMAIN + '/services/tenant-representation/', 'name': 'Tenant Representation'},
        {'@type': 'ListItem', 'position': 2, 'url': DOMAIN + '/services/landlord-representation/', 'name': 'Landlord Representation'}]}
    page('/services/', 'Commercial Real Estate Services NYC | Endurance REA',
         'Tenant representation and landlord representation for NYC office and retail space. Data-driven strategy and hands-on negotiation. Book a consultation.',
         body, schemas=[schema], trail=trail, og_image='/images/landlord-representation-leasing-strategy-meeting.jpg')


def build_tenant():
    path = '/services/tenant-representation/'
    trail = [('Home', '/'), ('Services', '/services/'), ('Tenant Representation', path)]
    body = hero('nyc-office-space-tenant-representation', 'Professionals talking in a Manhattan loft office with tall factory windows',
        'Tenant Representation in NYC: Negotiate Your Lease With Leverage',
        'A tenant-advocate approach that gives you confidential market and landlord data, so you secure better lease terms.',
        cta=('Request a Consultation', '/contact/?topic=tenant'), focal=('62% 55%', '58% 55%'))
    body += '<!--CRUMBS-->'
    body += f'''
<section class="section">
  <div class="wrap">
    {split(img('lease-review-notes-tenant-representation', 'Tenant advisor taking notes while reviewing lease terms', sizes='(min-width: 900px) 50vw, 100vw'),
      """<h2>Landlords negotiate leases every day. Most tenants don’t.</h2>
      <p>As a commercial tenant broker in New York City, we understand the complexities of lease negotiations. Landlords know the market, the comps and their own motivations. Most tenants walk in without that information.</p>
      <p>Our mission is to empower tenants. We give you the critical information and insights you need to make informed decisions throughout the process, so you sit across from your landlord as an equal.</p>
      <p>We represent office tenants on new leases, renewals, expansions and relocations across Manhattan and NYC.</p>""")}
  </div>
</section>

<section class="section dark">
  <div class="wrap cols">
    <div>
      <h2>The Tenant Advantage Analysis</h2>
      <p class="lead">Our proprietary report goes beyond what most brokers offer. It is a confidential, comprehensive analysis of your specific leasing situation.</p>
    </div>
    <dl class="rows">
      <div><dt>Market insights</dt><dd>Current rental rates, concessions and comparable properties in the area you want.</dd></div>
      <div><dt>Landlord leverage</dt><dd>Intel on your landlord’s motivations and negotiation history, including ownership finances and loan performance.</dd></div>
      <div><dt>Strategic recommendations</dt><dd>With the data in hand, we build a customized negotiation strategy to secure the best possible lease terms.</dd></div>
    </dl>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {split(img('tenant-landlord-handshake-lease-signing', 'Tenant and landlord shaking hands after agreeing on lease terms', sizes='(min-width: 900px) 50vw, 100vw'),
      f"""<h2>What the analysis delivers</h2>
      <dl class="rows">
        <div><dt>A stronger negotiating position</dt><dd>You negotiate with confidence and leverage.</dd></div>
        <div><dt>Cost savings potential</dt><dd>Our insights can lead to significant savings on rent, concessions and other lease terms.</dd></div>
        <div><dt>Favorable lease terms</dt><dd>A lease that fits your business needs and budget.</dd></div>
        <div><dt>Confidentiality throughout</dt><dd>Your information stays protected for a smooth, low-stress negotiation.</dd></div>
      </dl>
      <p style="margin-top:32px"><a class="btn btn-primary" href="/contact/?topic=tenant">Start Your Analysis {ARROW}</a></p>""", rev=True)}
  </div>
</section>

<section class="section warm">
  <div class="wrap">
    <div class="intro"><h2>Tenants we have represented</h2></div>
    {pull('shemesh')}
    {quotes('berdzeni', 'gofshteyn', 'levine', 'gulati')}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="intro"><h2>Know your lease protections</h2></div>
    <div class="posts">{post_card(ARTICLES[1])}{post_card(ARTICLES[2])}{post_card(ARTICLES[3])}</div>
  </div>
</section>

<section class="section warm">
  <div class="wrap narrow">
    <h2>Tenant representation questions</h2>
    {faq_block(TENANT_FAQ)}
    <p style="margin-top:32px">More answers on our <a href="/faq/">commercial real estate FAQ page</a>. Own a building? See <a href="/services/landlord-representation/">landlord representation</a>.</p>
  </div>
</section>
'''
    body += cta_band('Find out what your lease should cost',
                     'Request a confidential Tenant Advantage Analysis and negotiate your next lease or renewal from a position of strength.',
                     ('Request a Consultation', '/contact/?topic=tenant'))
    page(path, 'Tenant Representation NYC | Endurance Real Estate',
         'NYC tenant representation from a true tenant advocate. Our Tenant Advantage Analysis gives you data and leverage to cut lease costs. Request a consult.',
         body, trail=trail, og_image='/images/nyc-office-space-tenant-representation.jpg',
         schemas=[service_schema('Tenant Representation', 'Commercial tenant representation in New York City for new leases, renewals, expansions and relocations, powered by the proprietary Tenant Advantage Analysis.', path, 'Commercial tenant representation'),
                  faq_schema(TENANT_FAQ)])


def build_landlord():
    path = '/services/landlord-representation/'
    trail = [('Home', '/'), ('Services', '/services/'), ('Landlord Representation', path)]
    body = hero('nyc-retail-storefront-landlord-leasing', 'Ground-floor retail storefront for lease on a New York City street',
        'Landlord Representation in NYC That Leases Space Faster',
        'Strategic positioning, targeted marketing and skilled negotiation to attract quality tenants and improve profitability.',
        cta=('Discuss Your Property', '/contact/?topic=landlord'), focal=('55% 55%', '50% 55%'))
    body += '<!--CRUMBS-->'
    body += f'''
<section class="section">
  <div class="wrap">
    {split(img('landlord-leasing-market-analysis', 'Advisors reviewing leasing market analysis charts for a NYC property owner', sizes='(min-width: 900px) 50vw, 100vw'),
      """<h2>Every property has a story. We make tenants want to hear it.</h2>
      <p>Every property has its own blend of strengths that resonate with the right tenants. Our landlord representation team unlocks that potential by crafting a narrative that shows off your property’s best features and competitive edge.</p>
      <p>We position buildings, office spaces, retail properties, and condo and coop assets across New York City to attract quality tenants, improving both occupancy and profitability.</p>""")}
  </div>
</section>

<section class="section dark">
  <div class="wrap cols">
    <div>
      <h2>How we lease your space</h2>
      <p class="lead">Insight and strategy first, then marketing and negotiation that follow through to a signed lease.</p>
    </div>
    <dl class="rows">
      <div><dt>Strategic recommendations</dt><dd>Customized leasing strategies based on comprehensive market analysis, designed to achieve optimal pricing and lease terms tailored to your objectives.</dd></div>
      <div><dt>Targeted marketing</dt><dd>Focused marketing that puts your property in front of the right tenants.</dd></div>
      <div><dt>Transactional expertise</dt><dd>From initial marketing to lease signing, we work closely with ownership to ensure a seamless transition from prospect to tenant.</dd></div>
    </dl>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {split(img('landlord-representation-leasing-strategy-meeting', 'Leasing strategy presentation to property ownership in a Manhattan conference room', sizes='(min-width: 900px) 50vw, 100vw'),
      f"""<h2>Your exclusive leasing partner</h2>
      <p>With decades of experience representing landlords, we know how to get the most from a property in a competitive market. We work with:</p>
      <ul class="plain">
        <li>Property owners</li>
        <li>Condo and coop boards</li>
        <li>Investors in office and retail space</li>
      </ul>
      <p>Partnering with us means a dedicated team focused on leasing your space quickly, increasing profitability, and positioning your property for sustained success.</p>
      <p style="margin-top:28px"><a class="btn btn-primary" href="/contact/?topic=landlord">Discuss Your Property {ARROW}</a></p>""", rev=True)}
  </div>
</section>

<section class="section warm">
  <div class="wrap">
    <div class="intro"><h2>Owners we have represented</h2></div>
    {pull('jerome')}
    {quotes('classi')}
    <div style="margin-top:clamp(72px,9vw,120px)">
    {split(img('tribeca-prep-lease-116-nassau-street-financial-district', '116 Nassau Street lease announcement: 12,900+ SF leased to Tribeca Prep', sizes='(min-width: 900px) 50vw, 100vw', cls='contain'),
      f"""<h3>Tribeca Prep leases 12,900+ SF at 116 Nassau Street</h3>
      <p>Tribeca Prep signed for the entire second floor at 116 Nassau Street in the Financial District. Availabilities from 5,231 to 11,365 SF remain.</p>
      <a class="more" href="/insights/tribeca-prep-leases-116-nassau-street/">Read about the 116 Nassau Street lease {ARROW}</a>""")}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <h2>Landlord representation questions</h2>
    {faq_block(LANDLORD_FAQ)}
    <p style="margin-top:32px">More answers on our <a href="/faq/">FAQ page</a>. Looking for space instead? See <a href="/services/tenant-representation/">tenant representation</a>.</p>
  </div>
</section>
'''
    body += cta_band('Put the right tenants in your space',
                     'Tell us about your building, office, retail, condo or coop asset and we will outline a leasing strategy.',
                     ('Discuss Your Property', '/contact/?topic=landlord'))
    page(path, 'Landlord Representation NYC | Endurance Real Estate',
         'NYC landlord representation for office, retail, condo and coop assets. Strategic positioning and targeted marketing to lease faster. Discuss your property.',
         body, trail=trail, og_image='/images/nyc-retail-storefront-landlord-leasing.jpg',
         schemas=[service_schema('Landlord Representation', 'Exclusive leasing and landlord representation in New York City for buildings, office space, retail properties, and condo and coop assets.', path, 'Commercial landlord representation and exclusive leasing'),
                  faq_schema(LANDLORD_FAQ)])


def build_about():
    trail = [('Home', '/'), ('About', '/about/')]
    people = []
    for n, r, e, p, im, li in TEAM:
        tel = '+1' + p.replace('-', '')
        link = f'<a class="li" href="{li}" rel="noopener" target="_blank" aria-label="{n} on LinkedIn">{ICON["linkedin"]} LinkedIn profile</a>' if li else \
               f'<a class="li" href="{BIZ["linkedin"]}" rel="noopener" target="_blank" aria-label="Endurance Real Estate Advisors on LinkedIn">{ICON["linkedin"]} Company LinkedIn</a>'
        people.append(f'<article class="person">{img(im, f"{n}, {r} at Endurance Real Estate Advisors", sizes="(min-width: 760px) 240px, 50vw")}'
                      f'<h3>{n}</h3><p class="role">{r}</p><a href="mailto:{e}">{e}</a><a href="tel:{tel}">{p}</a>{link}</article>')
    body = hero('atlas-statue-rockefeller-center-manhattan', 'Atlas statue holding the celestial heavens at Rockefeller Center in Manhattan',
        'About Endurance Real Estate Advisors',
        'A results-driven NYC commercial real estate firm built on one principle: putting our clients’ needs first.',
        cta=('Talk to Our Team', '/contact/'), focal=('50% 58%', '45% 55%'))
    body += '<!--CRUMBS-->'
    body += f'''
<section class="section">
  <div class="wrap">
    {split(img('commercial-real-estate-professionals-nyc', 'Group of smiling business professionals celebrating a successful outcome', sizes='(min-width: 900px) 50vw, 100vw'),
      """<h2>Our name is symbolic of who we are</h2>
      <p>Endurance Real Estate Advisors is a results-driven, client-focused firm built on the principle of putting our clients’ needs first.</p>
      <p>With deep market knowledge, strategic expertise, and a clear understanding of both landlord and tenant priorities, we deliver insights and data that let our clients negotiate from a position of strength.</p>
      <p>Our tailored, thoughtful approach makes sure every solution aligns with our clients’ leasing goals, one relationship at a time. Learn more about our <a href="/services/tenant-representation/">tenant representation</a> and <a href="/services/landlord-representation/">landlord representation</a> services.</p>""")}
  </div>
</section>
'''
    body += stats()
    body += f'''
<section class="section warm" id="team">
  <div class="wrap">
    <div class="cols">
      <div><h2>Meet the team</h2><p class="lead">Five people covering brokerage, research, special projects, and design and workplace strategy.</p></div>
      {pull(quote='Working closely with our clients to establish short and long-term goals and objectives is essential to our clients’ success.', name='Sergio Turaev', role='Director')}
    </div>
    <div class="team">{''.join(people)}</div>
  </div>
</section>

<section class="section" id="testimonials">
  <div class="wrap">
    <div class="intro"><h2>What our clients say</h2></div>
    {pull('shemesh')}
    {quotes('berdzeni', 'jenna', 'ibragimov', 'jerome', 'gofshteyn', 'gulati', 'levine', 'classi')}
  </div>
</section>

<section class="section warm" id="careers">
  <div class="wrap">
    {split(img('endurance-team-collaboration', 'Team members joining hands over a table as a sign of collaboration', sizes='(min-width: 900px) 50vw, 100vw'),
      f"""<h2>Join our team</h2>
      <p>As we grow our platform, we are always looking for exceptional, qualified individuals to join our team. If you share our commitment to putting clients first, we would like to hear from you.</p>
      <p style="margin-top:28px"><a class="btn btn-primary" href="/contact/?topic=careers">Reach Out About Careers {ARROW}</a></p>""", rev=True)}
  </div>
</section>
'''
    body += cta_band()
    persons = [{'@type': 'Person', 'name': n, 'jobTitle': r, 'email': e, 'telephone': '+1' + p.replace('-', ''),
                'image': DOMAIN + f'/images/{im}.jpg', 'worksFor': {'@id': DOMAIN + '/#business'},
                **({'sameAs': [li]} if li else {})} for n, r, e, p, im, li in TEAM]
    schema = {'@context': 'https://schema.org', '@type': 'AboutPage', 'name': 'About Endurance Real Estate Advisors',
              'url': DOMAIN + '/about/', 'about': {'@id': DOMAIN + '/#business'}, 'mainEntity': persons}
    page('/about/', 'About Our NYC Commercial Real Estate Team | Endurance',
         'Meet Endurance Real Estate Advisors: 30+ years, 1,850+ leases and $3B in NYC volume for tenants and landlords. Meet the team and contact us today.',
         body, schemas=[schema], trail=trail, og_image='/images/atlas-statue-rockefeller-center-manhattan.jpg')


def build_faq():
    trail = [('Home', '/'), ('FAQ', '/faq/')]
    allq = [qa for _, items in FAQ for qa in items]
    assert 10 <= len(allq) <= 15, len(allq)
    groups = ''.join(f'<div class="faq-group"><h2>{g}</h2>{faq_block(items)}</div>' for g, items in FAQ)
    body = hero('handshake-commercial-lease-agreement-nyc', 'Two professionals shaking hands outside a New York office building',
        'NYC Commercial Real Estate FAQ',
        'Straight answers about tenant and landlord representation, lease protections, timing and getting started.',
        focal=('50% 40%', '42% 40%'))
    body += '<!--CRUMBS-->'
    body += f'''
<section class="section">
  <div class="wrap narrow">
    <p class="lead" style="margin-bottom:64px">Answers to the questions NYC tenants and property owners ask us most about commercial leasing. Don’t see yours? <a href="/contact/">Ask us directly</a>.</p>
    {groups}
  </div>
</section>
'''
    body += cta_band('Still have questions?', 'Talk with an experienced NYC commercial real estate advisor about your space or your building.')
    page('/faq/', 'Commercial Real Estate FAQ NYC | Endurance REA',
         'Answers on NYC tenant and landlord representation: fees, timing, lease protections, SNDAs and how to get started. Read the FAQ or call (646) 662-3546.',
         body, schemas=[faq_schema(allq)], trail=trail, og_image='/images/handshake-commercial-lease-agreement-nyc.jpg')


def build_insights():
    trail = [('Home', '/'), ('Insights', '/insights/')]
    body = hero('conference-room-lease-negotiation-nyc', 'Conference room prepared for a commercial lease discussion',
        'NYC Commercial Leasing Insights',
        'Pulse &amp; Perspective: practical guidance on lease protections, renewals and today’s market.',
        cta=('Talk to an Advisor', '/contact/'), focal=('55% 50%', '60% 50%'))
    body += '<!--CRUMBS-->'
    body += f'''
<section class="section">
  <div class="wrap">
    <p class="lead" style="margin-bottom:56px">We share what we see every day negotiating leases in New York City, so tenants and owners can make better decisions. For advice on your own situation, see <a href="/services/tenant-representation/">tenant representation</a> or <a href="/services/landlord-representation/">landlord representation</a>.</p>
    <div class="postlist">{''.join(post_row(a) for a in ARTICLES)}</div>
  </div>
</section>
'''
    body += cta_band()
    schema = {'@context': 'https://schema.org', '@type': 'Blog', 'name': 'Pulse & Perspective: NYC Commercial Leasing Insights',
              'url': DOMAIN + '/insights/', 'publisher': {'@id': DOMAIN + '/#business'},
              'blogPost': [{'@type': 'BlogPosting', 'headline': a['title'], 'url': f"{DOMAIN}/insights/{a['slug']}/"} for a in ARTICLES]}
    page('/insights/', 'NYC Commercial Leasing Insights | Endurance REA',
         'Guides for NYC tenants and landlords on self-help clauses, SNDAs, TI allowances, renewals and distressed landlords. Read insights from Endurance today.',
         body, schemas=[schema], trail=trail, og_image='/images/conference-room-lease-negotiation-nyc.jpg')


ARTICLE_FOCAL = {
    'manhattan-skyline-brooklyn-bridge-nyc': ('68% 55%', '77% 50%'),
    'nyc-commercial-tenant-self-help-clause': ('50% 30%', '50% 30%'),
    'conference-room-lease-negotiation-nyc': ('55% 50%', '60% 50%'),
    'manhattan-office-tower-distressed-landlord': ('50% 25%', '50% 30%'),
    'lease-renewal-tenant-improvement-allowance': ('45% 45%', '45% 45%'),
}


def build_articles():
    for a in ARTICLES:
        path = f"/insights/{a['slug']}/"
        trail = [('Home', '/'), ('Insights', '/insights/'), (a['title'], path)]
        others = [o for o in ARTICLES if o is not a][:3]
        body = hero(a['img'], a['img_alt'], esc(a['title']), esc(a['excerpt']), cta=a['cta'],
                    focal=ARTICLE_FOCAL.get(a['img'], ('50% 50%', '50% 50%')),
                    extra='<p class="meta">Endurance Real Estate Advisors · <time datetime="2026-11-20">November 20, 2026</time></p>')
        body += '<!--CRUMBS-->'
        body += f'''
<article class="section">
  <div class="wrap"><div class="prose">{a['body']()}</div></div>
</article>
<section class="section warm">
  <div class="wrap">
    <div class="intro"><h2>More insights</h2></div>
    <div class="posts">{''.join(post_card(o) for o in others)}</div>
  </div>
</section>
'''
        body += cta_band(primary=a['cta'])
        schema = {'@context': 'https://schema.org', '@type': 'Article', 'headline': a['title'], 'description': a['desc'],
                  'articleSection': a['tag'],
                  'image': DOMAIN + f"/images/{a['img']}.jpg", 'datePublished': '2026-11-20', 'dateModified': '2026-11-20',
                  'author': {'@type': 'Organization', 'name': BIZ['name'], 'url': DOMAIN + '/'},
                  'publisher': {'@type': 'Organization', 'name': BIZ['name'], 'logo': {'@type': 'ImageObject', 'url': DOMAIN + '/apple-touch-icon.png'}},
                  'mainEntityOfPage': DOMAIN + path}
        page(path, a['seo_title'], a['desc'], body, schemas=[schema], trail=trail, og_image=f"/images/{a['img']}.jpg", og_type='article')


def build_contact():
    trail = [('Home', '/'), ('Contact', '/contact/')]
    body = hero('client-strategy-meeting-nyc-office', 'Advisors and clients meeting around a conference table in a New York office',
        'Contact Our NYC Commercial Real Estate Brokers',
        'Attention and service you would expect from a trusted friend, with the expertise of a seasoned veteran.',
        cta=(f'Call {BIZ["phone"]}', f'tel:{BIZ["tel"]}'), focal=('50% 45%', '40% 45%'))
    body += '<!--CRUMBS-->'
    body += f'''
<section class="section">
  <div class="wrap contact-grid">
    <div>
      <h2>Tell us about your space or your building</h2>
      <p class="lead">Whether you are a tenant planning a lease, renewal or relocation, or an owner leasing up a property, send a note and we will be in touch.</p>
      <!-- To receive submissions without opening the visitor's email app, set data-endpoint to a form service URL (for example Formspree or a Cloudflare Worker). -->
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
        <div><button class="btn btn-primary" type="submit">Send Message {ARROW}</button></div>
        <p class="form-status" id="form-status" role="status" aria-live="polite"></p>
      </form>
    </div>
    <aside aria-labelledby="office-h">
      <h2 id="office-h">Our Manhattan office</h2>
      <dl class="details">
        <div><dt>Phone</dt><dd><a href="tel:{BIZ['tel']}">{BIZ['phone']}</a></dd></div>
        <div><dt>Email</dt><dd><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></dd></div>
        <div><dt>Address</dt><dd>{BIZ['street']}<br>{BIZ['city']}, {BIZ['region']} {BIZ['zip']}<br><a href="{BIZ['maps']}" rel="noopener" target="_blank">Get directions</a></dd></div>
        <div><dt>Office hours</dt><dd>{ph("CONFIRM: office hours")}</dd></div>
        <div><dt>Service area</dt><dd>New York City, including Manhattan</dd></div>
        <div><dt>Follow us</dt><dd><a href="{BIZ['instagram']}" rel="noopener" target="_blank">Instagram</a> · <a href="{BIZ['linkedin']}" rel="noopener" target="_blank">LinkedIn</a></dd></div>
      </dl>
    </aside>
  </div>
</section>
<section class="section warm">
  <div class="wrap">
    {pull('ibragimov')}
    {quotes('gulati', 'levine')}
    <p style="margin-top:40px">Before you reach out, you may want to read about <a href="/services/tenant-representation/">tenant representation</a>, <a href="/services/landlord-representation/">landlord representation</a>, or our <a href="/faq/">frequently asked questions</a>.</p>
  </div>
</section>
'''
    schema = {'@context': 'https://schema.org', '@type': 'ContactPage', 'name': 'Contact Endurance Real Estate Advisors',
              'url': DOMAIN + '/contact/', 'about': {'@id': DOMAIN + '/#business'}}
    page('/contact/', 'Contact a NYC Commercial Real Estate Broker | Endurance',
         'Contact Endurance Real Estate Advisors at 136 Madison Ave, New York. Call (646) 662-3546 or send a message about leasing office or retail space today.',
         body, schemas=[schema], trail=trail, og_image='/images/client-strategy-meeting-nyc-office.jpg')


def build_404():
    body = hero('manhattan-skyline-brooklyn-bridge-nyc', 'Lower Manhattan skyline at night',
        'We couldn’t find that page',
        'The page may have moved when we launched our new site. Here is where to go next.',
        cta=('Go to the Homepage', '/'), second=('Contact Us', '/contact/'), focal=('68% 55%', '77% 50%'))
    body += '''<section class="section"><div class="wrap narrow">
  <h2>Popular pages</h2>
  <ul class="plain">
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
    def pri(p):
        if p == '/':
            return '1.0'
        return '0.6' if p.startswith('/insights/') and p != '/insights/' else '0.8'
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml += [f'  <url><loc>{DOMAIN}{p}</loc><lastmod>{BUILD_DATE}</lastmod><priority>{pri(p)}</priority></url>' for p in urls]
    xml.append('</urlset>')
    open(os.path.join(SITE, 'sitemap.xml'), 'w').write('\n'.join(xml) + '\n')
    open(os.path.join(SITE, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')


if __name__ == '__main__':
    build_home(); build_services(); build_tenant(); build_landlord(); build_about()
    build_faq(); build_insights(); build_articles(); build_contact(); build_404()
    build_meta_files()
    print('\n'.join(p for p, _ in PAGES))
