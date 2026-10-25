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
UPDATED = '2026-10-25'

NAV = [
    ('index', 'index.html', 'Home'),
    ('about', 'about.html', 'About'),
    ('programs', 'programs.html', 'Programs'),
    ('stories', 'stories.html', 'Stories'),
    ('partner', 'partner.html', 'Partner'),
    ('contact', 'contact.html', 'Contact'),
]

PAGES = [
    # name, title, description, nav key, sitemap priority
    ('index', 'Dunia Endelevu · Youth-led climate incubator in Kenya',
     'Dunia Endelevu helps children in Kenya publish their own climate books, speak on our podcast Climate Gumzo and take the stage at environmental events. Free for every family.',
     'index', '1.0'),
    ('about', 'About us · Dunia Endelevu',
     'A youth-led social enterprise and incubator in Kenya. Our mission, our team and our safeguarding promise to every child under 18.',
     'about', '0.8'),
    ('programs', 'The Youth Advocate Journey · Dunia Endelevu',
     'Three free tracks for children under 18: Storyteller (publish a book), Voice (speak on our podcast) and Diplomat (take the stage at real events).',
     'programs', '0.9'),
    ('stories', 'Stories, episodes and stages · Dunia Endelevu',
     'The Dunia Endelevu Climate Anthology, our podcast Climate Gumzo and the young advocates speaking at events in Nairobi.',
     'stories', '0.7'),
    ('partner', 'Partner with us · Dunia Endelevu',
     'Sponsor a podcast series, book youth speakers, order the Climate Anthology or fund a young author. Every partnership keeps our programme free for children.',
     'partner', '0.9'),
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


def nav_links(active, cls=''):
    out = []
    for key, href, label in NAV:
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
<link rel="preload" href="assets/fonts/fraunces-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css?v={ver}">
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
<script src="assets/js/site.js?v={ver}" defer></script>{jsonld}
</head>'''


def header(active):
    return f'''<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="index.html" aria-label="Dunia Endelevu, home">
      {mark()}
      {wordmark(19)}
    </a>
    <nav class="nav" aria-label="Main">
        {nav_links(active)}
    </nav>
    <a class="btn btn--primary btn--sm header-cta" href="partner.html">Support a child</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu">
      <span class="menu-toggle__label">Menu</span><span class="menu-toggle__icon" aria-hidden="true"></span>
    </button>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu" hidden>
  <nav aria-label="Main menu">
        {nav_links(active)}
  </nav>
  <div class="mobile-menu__foot">
    <a class="btn btn--primary" href="partner.html">Support a child</a>
    <a class="btn btn--ghost" href="contact.html#apply">Apply for a child</a>
    <a class="fine" href="mailto:{EMAIL}">{EMAIL}</a>
  </div>
</div>'''


def footer(name):
    def legal(href, label, key):
        cur = ' aria-current="page"' if name == key else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<footer class="site-footer">
  <div class="wrap site-footer__inner">
    <div class="newsletter">
      <div class="newsletter__text">
        <h2>Subscribe to our newsletter</h2>
        <p>One short update each school term: new books, new episodes and where young advocates are speaking next.</p>
      </div>
      <form data-form data-subject="Newsletter sign-up" data-ok-title="You’re on the list." data-ok=" Look out for our next update at the start of term.">
        <label class="label" for="newsletter-email-{name}">Stay up to date</label>
        <div class="inline field">
          <input class="input" id="newsletter-email-{name}" type="email" name="email" autocomplete="email" placeholder="Enter your email" required>
          <button class="btn btn--sun btn--md" type="submit">Subscribe</button>
        </div>
        <input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
        <input type="hidden" name="form" value="Newsletter">
        <span class="fine">For adults only. By subscribing you agree to our <a href="privacy.html">Privacy Policy</a>.</span>
      </form>
    </div>
    <div class="footer-cols">
      <div class="footer-brand">
        <a class="brand" href="index.html" aria-label="Dunia Endelevu, home">{mark(w=24, h=30)}{wordmark(16)}</a>
        <p>A youth-led climate incubator giving children the platform to lead the conversation.</p>
        <a class="email" href="mailto:{EMAIL}">{EMAIL}</a>
      </div>
      <nav class="footer-nav" aria-labelledby="f-org-{name}">
        <h2 id="f-org-{name}">Organisation</h2>
        <a href="about.html">About us</a>
        <a href="programs.html">Programs</a>
        <a href="stories.html">Stories</a>
        <a href="about.html#team">Our team</a>
        <a href="assets/brand/dunia-endelevu-logo-pack.zip" download>Logo pack</a>
      </nav>
      <nav class="footer-nav" aria-labelledby="f-inv-{name}">
        <h2 id="f-inv-{name}">Get involved</h2>
        <a href="contact.html#apply">Join the programme</a>
        <a href="partner.html">Partner with us</a>
        <a href="partner.html#ways">Fund a young author</a>
        <a href="contact.html#enquiry">Contact</a>
      </nav>
      <nav class="footer-nav" aria-labelledby="f-legal-{name}">
        <h2 id="f-legal-{name}">Legal</h2>
        {legal('privacy.html', 'Privacy Policy', 'privacy')}
        {legal('terms.html', 'Terms of Service', 'terms')}
        {legal('cookies.html', 'Cookie Policy', 'cookies')}
        <a href="about.html#safeguarding">Safeguarding</a>
      </nav>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Dunia Endelevu. All rights reserved.</span>
      <span>Nairobi, Kenya</span>
    </div>
  </div>
</footer>
</body>
</html>
'''


def expand(body):
    body = body.replace('{{mark_white}}', mark(fg='#FFFFFF', w=26, h=32))
    body = body.replace('{{mark}}', mark())
    body = body.replace('{{email}}', EMAIL)
    body = body.replace('{{spotify}}', SPOTIFY_SHOW)
    body = body.replace('{{updated}}', '25 October 2026')

    def art(m):
        return (SRC / 'art' / f'{m.group(1)}.svg').read_text().strip()
    body = re.sub(r'\{\{art:([a-z0-9-]+)\}\}', art, body)
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
