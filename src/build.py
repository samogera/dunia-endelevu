#!/usr/bin/env python3
"""Build the Dunia Endelevu website.

Each page's main content lives in src/pages/<name>.html. This script wraps it
with the shared <head>, header, mobile menu and footer, and writes the finished
page to the site root (index.html, about.html, ...). It also writes sitemap.xml.

Run from anywhere:  python3 src/build.py
"""
import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'

# Change these two lines when the site moves to its own domain,
# e.g. SITE_URL = 'https://duniaendelevu.org/' and BASE_PATH = '/'.
SITE_URL = 'https://samogera.github.io/dunia-endelevu/'
BASE_PATH = '/dunia-endelevu/'

EMAIL = 'hello@duniaendelevu.org'
SPOTIFY_SHOW = 'https://open.spotify.com/show/2kU7BcWISSFWf1rI8klQaq'
UPDATED = '2026-11-01'

PAGES = [
    # name, title, description, nav key, sitemap priority
    ('index', 'Dunia Endelevu · Youth-led climate incubator in Kenya',
     'Dunia Endelevu helps children in Kenya publish their own climate books, speak on our podcast Climate Gumzo and take the stage at environmental events. Free for every family.',
     'index', '1.0'),
    ('about', 'About us · Dunia Endelevu',
     'Dunia Endelevu is a youth-led climate incubator in Kenya, founded by Alana Chelangat. Our story, our safeguarding promise and how to volunteer.',
     'about', '0.8'),
    ('programs', 'The Youth Advocate Journey · Dunia Endelevu',
     'Three free tracks for children under 18: Storyteller (publish a book), Voice (speak on our podcast) and Diplomat (take the stage at real events).',
     'programs', '0.9'),
    ('donate', 'Donate · Dunia Endelevu',
     'Sponsor a child’s book, a podcast episode or a seat at a climate event. Every gift keeps Dunia Endelevu free for children in Kenya.',
     'donate', '0.9'),
    ('contact', 'Contact and apply · Dunia Endelevu',
     'Parents and guardians can apply for a child under 18. Schools, partners and press can send an enquiry. We reply within three working days.',
     'contact', '0.8'),
    ('privacy', 'Privacy Policy · Dunia Endelevu',
     'How Dunia Endelevu collects, uses and protects personal information, especially information about children, under Kenya’s Data Protection Act, 2019.',
     None, '0.3'),
    ('terms', 'Terms of Service · Dunia Endelevu',
     'The rules for using the Dunia Endelevu website and taking part in, or supporting, our programmes.',
     None, '0.3'),
    ('cookies', 'Cookie Policy · Dunia Endelevu',
     'Dunia Endelevu does not use advertising or tracking cookies. Here is exactly what the website does and does not store.',
     None, '0.3'),
    ('404', 'Page not found · Dunia Endelevu',
     'This page could not be found.',
     None, None),
]


# The Speaking D: a D-shaped speech bubble; its spine, top, bottom and horizon form an E; a sun rises inside.
MARK_D = ('M12 8 H31 A22 22 0 0 1 31 52 H24 L12 60 Z M20 16 H31 A14 14 0 0 1 31 44 H20 Z')
MARK_SUN = 'M22 33 A10 10 0 0 1 42 33 Z'
MARK_BAR = 'M19.25 33 H39.75 A3.25 3.25 0 0 1 39.75 39.5 H19.25 Z'
WORDMARK_RATIO = 9.075  # width / height of assets/img/wordmark.svg


def mark(fg='#12372F', w=29, h=36, cls=None):
    c = f' class="{cls}"' if cls else ''
    return (f'<svg{c} width="{w}" height="{h}" viewBox="10.5 6.5 44 55" aria-hidden="true" focusable="false">'
            f'<path d="{MARK_D}" fill="{fg}" fill-rule="evenodd"/>'
            f'<path d="{MARK_SUN}" fill="#F2B233"/><path d="{MARK_BAR}" fill="{fg}"/></svg>')


def wordmark(h):
    return (f'<img class="brand__word" src="assets/img/wordmark.svg" alt="" width="{round(h * WORDMARK_RATIO)}" height="{h}">')


def asset_version():
    h = hashlib.sha1()
    for p in ('assets/css/site.css', 'assets/js/site.js'):
        h.update((ROOT / p).read_bytes())
    return h.hexdigest()[:8]


NAV = [
    ('about', 'about.html', 'About'),
    ('programs', 'programs.html', 'Programmes'),
    ('donate', 'donate.html', 'Donate'),
]

ARROW = ('<svg class="arrow-i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg>')
DOODLES = {
    'sparkle': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0C12.9 7.4 16.6 11.1 24 12 16.6 12.9 12.9 16.6 12 24 11.1 16.6 7.4 12.9 0 12 7.4 11.1 11.1 7.4 12 0Z" fill="currentColor"/></svg>',
    'squiggle': '<svg viewBox="0 0 80 24" aria-hidden="true"><path d="M3 14C11 3 19 23 27 12S43 3 51 12 67 23 77 10" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></svg>',
    'arrow': '<svg viewBox="0 0 70 52" aria-hidden="true"><path d="M4 6C24 4 46 14 58 40" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/><path d="M47 36L58 42L62 29" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'burst': '<svg class="marquee__burst" viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="7" fill="currentColor"/><g stroke="currentColor" stroke-width="3.2" stroke-linecap="round"><path d="M20 2v6M20 32v6M2 20h6M32 20h6M7.3 7.3l4.2 4.2M28.5 28.5l4.2 4.2M7.3 32.7l4.2-4.2M28.5 11.5l4.2-4.2"/></g></svg>',
    'sun': '<svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="26" fill="#F2B233"/><g stroke="#F2B233" stroke-width="7" stroke-linecap="round"><path d="M60 8v14M60 98v14M8 60h14M98 60h14M23 23l10 10M87 87l10 10M23 97l10-10M87 33l10-10"/></g></svg>',
}
SHAPES = ('<svg class="shape-defs" aria-hidden="true" focusable="false"><defs>'
          '<clipPath id="bubble" clipPathUnits="objectBoundingBox">'
          '<path d="M0.06 0H0.4634A0.5366 0.4231 0 0 1 0.4634 0.8462H0.2927L0 1V0.045Q0 0 0.06 0Z"/></clipPath>'
          '</defs></svg>')
_sticker_n = [0]


def sticker(text, core, variant='ink', cls=''):
    _sticker_n[0] += 1
    pid = f'ring{_sticker_n[0]}'
    return (f'<div class="sticker sticker--{variant} {cls}" aria-hidden="true">'
            f'<svg class="sticker__ring" viewBox="0 0 136 136"><defs><path id="{pid}" d="M68 68m-50 0a50 50 0 1 1 100 0a50 50 0 1 1-100 0"/></defs>'
            f'<text><textPath href="#{pid}" textLength="312" lengthAdjust="spacing">{text}</textPath></text></svg>'
            f'<span class="sticker__core">{core}</span></div>')


def nav_links(active, home=False):
    items = ([('index', 'index.html', 'Home')] if home else []) + NAV
    out = []
    for key, href, label in items:
        cur = ' aria-current="page"' if key == active else ''
        out.append(f'<a href="{href}"{cur}>{label}</a>')
    return '\n        '.join(out)


def head(name, title, desc, ver):
    url = SITE_URL if name == 'index' else f'{SITE_URL}{name}.html'
    base = f'\n<base href="{BASE_PATH}">' if name == '404' else ''
    robots = '\n<meta name="robots" content="noindex">' if name == '404' else ''
    canonical = '' if name == '404' else f'\n<link rel="canonical" href="{url}">'
    jsonld = ''
    if name == 'index':
        data = {
            '@context': 'https://schema.org',
            '@type': 'Organization',
            'name': 'Dunia Endelevu',
            'url': SITE_URL,
            'logo': f'{SITE_URL}assets/img/icon-512.png',
            'email': EMAIL,
            'description': 'A youth-led climate incubator in Kenya that helps children publish books, speak on a podcast and take the stage at environmental events.',
            'address': {'@type': 'PostalAddress', 'addressLocality': 'Nairobi', 'addressCountry': 'KE'},
            'sameAs': [SPOTIFY_SHOW],
        }
        jsonld = '\n<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'
    og_title = title.split(' · ')[0] if name != 'index' else 'Dunia Endelevu'
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">{base}
<title>{title}</title>
<meta name="description" content="{desc}">{robots}{canonical}
<meta name="theme-color" content="#FFFFFF">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Dunia Endelevu">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Dunia Endelevu. Children aren’t just in the room. They’re on the stage.">
<meta property="og:locale" content="en_KE">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="assets/fonts/inter-tight-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css?v={ver}">
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
<script src="assets/js/site.js?v={ver}" defer></script>{jsonld}
</head>'''


def header(active):
    return f'''<body>
{SHAPES}
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <div class="site-header__inner">
      <a class="brand" href="index.html" aria-label="Dunia Endelevu, home">
        {mark(w=31, h=38)}
        {wordmark(19)}
      </a>
      <nav class="nav" aria-label="Main">
        {nav_links(active)}
      </nav>
      <a class="btn btn--sun btn--sm header-cta" href="contact.html#apply">Join us {ARROW}</a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu">
        <span class="menu-toggle__label">Menu</span><span class="menu-toggle__icon" aria-hidden="true"></span>
      </button>
    </div>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu" hidden>
  <nav aria-label="Main menu">
        {nav_links(active, home=True)}
  </nav>
  <div class="mobile-menu__foot">
    <a class="btn btn--sun" href="contact.html#apply">Apply for a child {ARROW}</a>
    <a class="btn btn--light" href="donate.html">Donate</a>
    <a class="fine" href="mailto:{EMAIL}">{EMAIL}</a>
  </div>
</div>'''


SPOTIFY_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">'
                '<circle cx="12" cy="12" r="9.5"/><path d="M7.2 9.4c3.3-1 6.9-.7 9.8.9"/><path d="M7.8 12.4c2.7-.8 5.6-.5 8 .8"/><path d="M8.4 15.2c2.1-.6 4.3-.4 6.2.6"/></svg>')
MAIL_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M4 7.5l8 5.5 8-5.5"/></svg>')


def footer(name):
    def legal(href, label, key):
        cur = ' aria-current="page"' if name == key else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <nav class="footer-nav" aria-labelledby="f-menu-{name}">
        <h2 id="f-menu-{name}">Menu</h2>
        <a href="about.html">About us</a>
        <a href="programs.html">Programmes</a>
        <a href="donate.html">Donate</a>
      </nav>
      <nav class="footer-nav" aria-labelledby="f-help-{name}">
        <h2 id="f-help-{name}">Get involved</h2>
        <a href="contact.html#apply">Apply for a child</a>
        <a href="about.html#volunteer">Volunteer</a>
        <a href="donate.html?for=book">Sponsor a book</a>
      </nav>
      <div class="footer-nav">
        <h2>Contact</h2>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <a href="contact.html">Send a message</a>
        <span>Nairobi, Kenya</span>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Dunia Endelevu</span>
      <div class="footer-bottom__end">
        <nav class="footer-legal" aria-label="Legal">
          {legal('privacy.html', 'Privacy Policy', 'privacy')}
          {legal('terms.html', 'Terms', 'terms')}
          {legal('cookies.html', 'Cookies', 'cookies')}
        </nav>
        <div class="footer-social">
          <a href="{SPOTIFY_SHOW}" target="_blank" rel="noopener" aria-label="Climate Gumzo on Spotify">{SPOTIFY_ICON}</a>
          <a href="mailto:{EMAIL}" aria-label="Email us">{MAIL_ICON}</a>
        </div>
      </div>
    </div>
    <div class="footer-giant" aria-hidden="true"><img src="assets/img/footer-word.svg" alt="" width="1397" height="126" loading="lazy"></div>
  </div>
</footer>
</body>
</html>
'''


def expand(body):
    body = body.replace('{{mark_white}}', mark(fg='#FFFFFF', w=28, h=35))
    body = body.replace('{{mark}}', mark())
    body = body.replace('{{email}}', EMAIL)
    body = body.replace('{{spotify}}', SPOTIFY_SHOW)
    body = body.replace('{{updated}}', '1 November 2026')
    body = body.replace('{{arrow}}', ARROW)
    body = re.sub(r'\{\{doodle:([a-z]+)\}\}', lambda m: DOODLES[m.group(1)], body)
    body = re.sub(r'\{\{sticker:([^|}]+)\|([^|}]+)\|([a-z]+)\}\}', lambda m: sticker(m.group(1), m.group(2), m.group(3)), body)

    def art(m):
        svg = (SRC / 'art' / f'{m.group(1)}.svg').read_text().strip()
        if m.group(2):
            svg = svg.replace('<rect width="500" height="400" fill="#F7F8F5"/>', '', 1)
        return svg
    body = re.sub(r'\{\{art:([a-z0-9-]+)(:clear)?\}\}', art, body)
    left = re.findall(r'\{\{[^}]+\}\}', body)
    assert not left, f'unexpanded tokens: {left}'
    return body



def build():
    ver = asset_version()
    for name, title, desc, nav, _ in PAGES:
        body = expand((SRC / 'pages' / f'{name}.html').read_text())
        html = '\n'.join([head(name, title, desc, ver), header(nav), body.strip(), footer(name)])
        (ROOT / f'{name}.html').write_text(html)
    urls = []
    for name, _, _, _, prio in PAGES:
        if prio is None:
            continue
        loc = SITE_URL if name == 'index' else f'{SITE_URL}{name}.html'
        urls.append(f'  <url><loc>{loc}</loc><lastmod>{UPDATED}</lastmod><priority>{prio}</priority></url>')
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + '\n'.join(urls) + '\n</urlset>\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: {BASE_PATH}src/\n\nSitemap: {SITE_URL}sitemap.xml\n')
    print(f'Built {len(PAGES)} pages (assets v{ver}).')


if __name__ == '__main__':
    build()
