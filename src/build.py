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

import books as booklib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'

# Change these two lines when the site moves to its own domain,
# e.g. SITE_URL = 'https://duniaendelevu.org/' and BASE_PATH = '/'.
SITE_URL = 'https://dunia-endelevu.vercel.app/'
BASE_PATH = '/'

EMAIL = 'hello@duniaendelevu.org'
SPOTIFY_SHOW = 'https://open.spotify.com/show/2kU7BcWISSFWf1rI8klQaq'
ALANA_SITE = 'https://alanachelangat.com/'
SLOGAN = 'Young voices for a sustainable world.'

# Search engine verification: paste the code Google Search Console or Bing Webmaster Tools gives you
# (only the content="..." part), rebuild and push.
GOOGLE_SITE_VERIFICATION = ''
BING_SITE_VERIFICATION = ''

# Words and phrases people search for. Google mostly reads titles, headings and text; Bing and some
# AI tools also read this list.
KEYWORDS = ('Dunia Endelevu, Dunia Endelevu Kenya, youth-led climate incubator Kenya, climate change education for children, '
            'climate education Kenya, children climate programmes Nairobi, free climate storybooks for children, '
            'climate change storybooks for kids, children’s books about climate change, Kenyan children’s books environment, '
            'Climate Gumzo podcast, climate podcast for kids, young climate advocates Kenya, child climate activists Kenya, '
            'Alana Chelangat, climate justice for children, environmental rights for children, Article 42 Kenya, '
            'biodiversity for kids, climate action for kids, early warning for schools Kenya, air quality alerts schools, '
            'sponsor a child’s book Kenya, donate climate education Kenya, volunteer Nairobi children climate, '
            'dunia endelevu meaning sustainable world')
UPDATED = '2026-11-03'

PAGES = [
    # name, title, description, nav key, sitemap priority
    ('index', 'Dunia Endelevu · Youth-led climate action for children in Kenya',
     'Dunia Endelevu helps children in Kenya publish climate books, speak on our podcast Climate Gumzo and take the stage at events. Free for every family.',
     'index', '1.0'),
    ('about', 'About us · Founded by Alana Chelangat · Dunia Endelevu',
     'Dunia Endelevu is a youth-led climate incubator in Kenya, founded by Alana Chelangat. Our story, our safeguarding promise and how to volunteer.',
     'about', '0.8'),
    ('programs', 'Free climate programmes for children in Kenya · Dunia Endelevu',
     'Three free tracks for children under 18: publish a climate book, speak on our podcast or take the stage at real events. Plus early warning alerts for schools, now in pilot.',
     'programs', '0.9'),
    ('learn', 'Climate storybooks for children · Learn · Dunia Endelevu',
     'Illustrated storybooks that help children aged 6 to 10 learn about climate change, biodiversity, climate justice, climate action and environmental rights.',
     'learn', '0.9'),
    ('donate', 'Donate · Sponsor a child’s climate book · Dunia Endelevu',
     'Sponsor a child’s book, a podcast episode or a seat at a climate event. Every gift keeps Dunia Endelevu free for children in Kenya.',
     'donate', '0.9'),
    ('contact', 'Apply for your child or contact us · Dunia Endelevu',
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

BOOKS = booklib.load()
_at = [p[0] for p in PAGES].index('learn') + 1
PAGES[_at:_at] = booklib.page_entries(BOOKS)


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
    ('about', '/about', 'About'),
    ('programs', '/programs', 'Programmes'),
    ('learn', '/learn', 'Learn'),
    ('donate', '/donate', 'Donate'),
    ('contact', '/contact', 'Contact'),
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
    items = ([('index', '/', 'Home')] if home else []) + NAV
    out = []
    for key, href, label in items:
        cur = ' aria-current="page"' if key == active else ''
        out.append(f'<a href="{href}"{cur}>{label}</a>')
    return '\n        '.join(out)


def head(name, title, desc, ver, og=None, ld=None):
    url = SITE_URL if name == 'index' else f'{SITE_URL}{name}'
    base = f'\n<base href="{BASE_PATH}">' if name == '404' else ''
    robots = ('\n<meta name="robots" content="noindex">' if name == '404' else
              '\n<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">')
    verify = ''
    if GOOGLE_SITE_VERIFICATION:
        verify += f'\n<meta name="google-site-verification" content="{GOOGLE_SITE_VERIFICATION}">'
    if BING_SITE_VERIFICATION:
        verify += f'\n<meta name="msvalidate.01" content="{BING_SITE_VERIFICATION}">'
    canonical = '' if name == '404' else f'\n<link rel="canonical" href="{url}">'
    jsonld = ''
    blocks = list(ld or [])
    if name == 'index':
        data = {
            '@context': 'https://schema.org',
            '@type': 'NGO',
            '@id': f'{SITE_URL}#organization',
            'name': 'Dunia Endelevu',
            'alternateName': ['Dunia Endelevu Kenya', 'Dunia Endelevu youth climate incubator'],
            'slogan': SLOGAN,
            'url': SITE_URL,
            'image': f'{SITE_URL}assets/img/og-image.png',
            'logo': f'{SITE_URL}assets/img/icon-512.png',
            'email': EMAIL,
            'description': 'A youth-led climate incubator in Kenya that helps children publish books, speak on a podcast and take the stage at environmental events.',
            'address': {'@type': 'PostalAddress', 'addressLocality': 'Nairobi', 'addressCountry': 'KE'},
            'areaServed': {'@type': 'Country', 'name': 'Kenya'},
            'knowsAbout': ['Climate change education for children', 'Children’s climate storybooks', 'Youth climate advocacy',
                           'Biodiversity', 'Climate justice', 'Environmental rights'],
            'founder': {'@type': 'Person', 'name': 'Alana Chelangat', 'url': ALANA_SITE,
                        'description': 'Kenyan climate advocate, author and podcaster; Little Miss Environment Kenya 2025.'},
            'foundingLocation': {'@type': 'Place', 'name': 'Nairobi, Kenya'},
            'nonprofitStatus': 'Nonprofit',
            'sameAs': [SPOTIFY_SHOW, ALANA_SITE],
        }
        site = {'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'Dunia Endelevu', 'url': SITE_URL, 'inLanguage': 'en-KE'}
        blocks = [data, site] + blocks
    for data in blocks:
        jsonld += '\n<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'
    og_title = title.split(' · ')[0] if name != 'index' else 'Dunia Endelevu'
    og = og or {'image': 'assets/img/og-image.png', 'w': 1200, 'h': 630,
                'alt': 'Dunia Endelevu. Young voices for a sustainable world.'}
    card = 'summary_large_image' if og['w'] > og['h'] else 'summary'
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">{base}
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{KEYWORDS}">
<meta name="author" content="Dunia Endelevu">{robots}{canonical}{verify}
<meta name="theme-color" content="#FFFFFF">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Dunia Endelevu">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}{og['image']}">
<meta property="og:image:width" content="{og['w']}">
<meta property="og:image:height" content="{og['h']}">
<meta property="og:image:alt" content="{og['alt']}">
<meta property="og:locale" content="en_KE">
<meta name="twitter:card" content="{card}">
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="alternate" type="text/plain" href="llms.txt" title="Plain-text summary for AI assistants">
<link rel="preload" href="assets/fonts/bricolage-grotesque-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css?v={ver}">
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>
<script src="assets/js/site.js?v={ver}" defer></script>
<script>window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};</script>
<script defer src="/_vercel/insights/script.js"></script>{jsonld}
</head>'''


def header(active):
    return f'''<body>
{SHAPES}
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <div class="site-header__inner">
      <a class="brand" href="/" aria-label="Dunia Endelevu, home">
        {mark(w=31, h=38)}
        {wordmark(19)}
      </a>
      <nav class="nav" aria-label="Main">
        {nav_links(active)}
      </nav>
      <a class="btn btn--sun btn--sm header-cta" href="/contact#apply">Join us {ARROW}</a>
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
    <a class="btn btn--sun" href="/contact#apply">Apply for a child {ARROW}</a>
    <a class="btn btn--light" href="/donate">Donate</a>
    <a class="fine" href="mailto:{EMAIL}">{EMAIL}</a>
  </div>
</div>'''


# Line icons from Tabler Icons (MIT licence, tabler.io/icons)
_ICON_PATHS = {
    'instagram': ['M4 8a4 4 0 0 1 4 -4h8a4 4 0 0 1 4 4v8a4 4 0 0 1 -4 4h-8a4 4 0 0 1 -4 -4z', 'M9 12a3 3 0 1 0 6 0a3 3 0 0 0 -6 0', 'M16.5 7.5v.01'],
    'tiktok': ['M21 7.917v4.034a9.948 9.948 0 0 1 -5 -1.951v4.5a6.5 6.5 0 1 1 -8 -6.326v4.326a2.5 2.5 0 1 0 4 2v-11.5h4.083a6.005 6.005 0 0 0 4.917 4.917z'],
    'x': ['M4 4l11.733 16h4.267l-11.733 -16z', 'M4 20l6.768 -6.768m2.46 -2.46l6.772 -6.772'],
    'facebook': ['M7 10v4h3v7h4v-7h3l1 -4h-4v-2a1 1 0 0 1 1 -1h3v-4h-3a5 5 0 0 0 -5 5v2h-3'],
    'linkedin': ['M8 11v5', 'M8 8v.01', 'M12 16v-5', 'M16 16v-3a2 2 0 1 0 -4 0', 'M3 7a4 4 0 0 1 4 -4h10a4 4 0 0 1 4 4v10a4 4 0 0 1 -4 4h-10a4 4 0 0 1 -4 -4z'],
    'youtube': ['M2 8a4 4 0 0 1 4 -4h12a4 4 0 0 1 4 4v8a4 4 0 0 1 -4 4h-12a4 4 0 0 1 -4 -4v-8z', 'M10 9l5 3l-5 3z'],
    'spotify': ['M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0', 'M8 11.973c2.5 -1.473 5.5 -.973 7.5 .527', 'M9 15c1.5 -1 4 -1 5 .5', 'M7 9c2 -1 6 -2 10 .5'],
    'mail': ['M3 7a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v10a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-10z', 'M3 7l9 6l9 -6'],
    'heart': ['M19.5 12.572l-7.5 7.428l-7.5 -7.428a5 5 0 1 1 7.5 -6.566a5 5 0 1 1 7.5 6.572'],
    'lock': ['M5 13a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v6a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2v-6z', 'M11 16a1 1 0 1 0 2 0a1 1 0 0 0 -2 0', 'M8 11v-4a4 4 0 1 1 8 0v4'],
    'phone': ['M6 5a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v14a2 2 0 0 1 -2 2h-8a2 2 0 0 1 -2 -2v-14z', 'M11 4h2', 'M12 17v.01'],
    'bank': ['M3 21l18 0', 'M3 10l18 0', 'M5 6l7 -3l7 3', 'M4 10l0 11', 'M20 10l0 11', 'M8 14l0 3', 'M12 14l0 3', 'M16 14l0 3'],
    'card': ['M3 8a3 3 0 0 1 3 -3h12a3 3 0 0 1 3 3v8a3 3 0 0 1 -3 3h-12a3 3 0 0 1 -3 -3z', 'M3 10l18 0', 'M7 15l.01 0', 'M11 15l2 0'],
    'user': ['M8 7a4 4 0 1 0 8 0a4 4 0 0 0 -8 0', 'M6 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2'],
    'eye-off': ['M10.585 10.587a2 2 0 0 0 2.829 2.828', 'M16.681 16.673a8.717 8.717 0 0 1 -4.681 1.327c-3.6 0 -6.6 -2 -9 -6c1.272 -2.12 2.712 -3.678 4.32 -4.674m2.86 -1.146a9.055 9.055 0 0 1 1.82 -.18c3.6 0 6.6 2 9 6c-.666 1.11 -1.379 2.067 -2.138 2.87', 'M3 3l18 18'],
    'volume': ['M15 8a5 5 0 0 1 0 8', 'M17.7 5a9 9 0 0 1 0 14', 'M6 15h-2a1 1 0 0 1 -1 -1v-4a1 1 0 0 1 1 -1h2l3.5 -4.5a.8 .8 0 0 1 1.5 .5v14a.8 .8 0 0 1 -1.5 .5l-3.5 -4.5'],
    'pause': ['M6 6a1 1 0 0 1 1 -1h2a1 1 0 0 1 1 1v12a1 1 0 0 1 -1 1h-2a1 1 0 0 1 -1 -1z', 'M14 6a1 1 0 0 1 1 -1h2a1 1 0 0 1 1 1v12a1 1 0 0 1 -1 1h-2a1 1 0 0 1 -1 -1z'],
    'download': ['M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2', 'M7 11l5 5l5 -5', 'M12 4l0 12'],
    'eye': ['M10 12a2 2 0 1 0 4 0a2 2 0 0 0 -4 0', 'M21 12c-2.4 4 -5.4 6 -9 6c-3.6 0 -6.6 -2 -9 -6c2.4 -4 5.4 -6 9 -6c3.6 0 6.6 2 9 6'],
    'bell': ['M10 5a2 2 0 1 1 4 0a7 7 0 0 1 4 6v3a4 4 0 0 0 2 3h-16a4 4 0 0 0 2 -3v-3a7 7 0 0 1 4 -6', 'M9 17v1a3 3 0 0 0 6 0v-1'],
    'circle-check': ['M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0', 'M9 12l2 2l4 -4'],
    'users': ['M9 7m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0', 'M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2', 'M16 3.13a4 4 0 0 1 0 7.75', 'M21 21v-2a4 4 0 0 0 -3 -3.85'],
    'wind': ['M5 8h8.5a2.5 2.5 0 1 0 -2.34 -3.24', 'M3 12h15.5a2.5 2.5 0 1 1 -2.34 3.24', 'M4 16h5.5a2.5 2.5 0 1 1 -2.34 3.24'],
    'temperature': ['M10 13.5a4 4 0 1 0 4 0v-8.5a2 2 0 0 0 -4 0v8.5', 'M10 9l4 0'],
    'cloud-rain': ['M7 18a4.6 4.4 0 0 1 0 -9a5 4.5 0 0 1 11 2h1a3.5 3.5 0 0 1 0 7', 'M11 13v2m0 3v2m4 -5v2m0 3v2'],
    'check': ['M5 12l5 5l10 -10'],
    'pin': ['M9 11a3 3 0 1 0 6 0a3 3 0 0 0 -6 0', 'M17.657 16.657l-4.243 4.243a2 2 0 0 1 -2.827 0l-4.244 -4.243a8 8 0 1 1 11.314 0z'],
}


def icon(name):
    paths = ''.join(f'<path d="{d}"/>' for d in _ICON_PATHS[name])
    return (f'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>')


# Duotone gift icons (48 x 48), drawn for Dunia Endelevu in the brand colours.
_DE, _DS, _DSOFT, _DMINT, _DCLAY = '#12372F', '#F2B233', '#FCEBC0', '#CFE3D6', '#F3C3AE'
_DST = f'stroke="{_DE}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"'
_DUO = {
    'book': f'''<path d="M4 15.5V40h15.5c2 0 3.6.8 4.5 2 .9-1.2 2.5-2 4.5-2H44V15.5" fill="none" {_DST}/><path d="M24 41.5C20 38 14.5 36.6 8 37V11.6c6.3-.5 11.8 1 16 4.4z" fill="#FFFFFF" {_DST}/><path d="M24 41.5c4-3.5 9.5-4.9 16-4.5V11.6c-6.3-.5-11.8 1-16 4.4z" fill="#FFFFFF" {_DST}/><path d="M24 16C23 9.6 25.6 5 31 2.5c2.8 6.5 2.2 14-1.6 20-1.6 2.4-3.4 4.3-5.4 5.8z" fill="{_DS}" {_DST}/><path d="M24 16v25.5" fill="none" {_DST}/><path d="M31.5 27c2-.5 4-.7 5.6-.6M31.5 31.6c2-.5 4-.7 5.6-.6M11 20.5c2.4-.1 5 .4 7 1.3M11 25.5c2.4-.1 5 .4 7 1.3" fill="none" stroke="{_DE}" stroke-width="1.8" stroke-linecap="round" opacity=".45"/>''',
    'mic': f'''<rect x="17" y="4" width="14" height="23" rx="7" fill="{_DS}" {_DST}/><path d="M17 12.5h4.5M17 17h4.5M17 21.5h4.5" fill="none" {_DST}/><path d="M11 21a13 13 0 0 0 26 0" fill="none" {_DST}/><path d="M24 34v8M16 43h16" fill="none" {_DST}/>''',
    'ticket': f'''<path d="M5 14.5a3.5 3.5 0 0 0 3.5-3.5h31a3.5 3.5 0 0 0 3.5 3.5v5a4.5 4.5 0 0 0 0 9v5a3.5 3.5 0 0 0-3.5 3.5h-31A3.5 3.5 0 0 0 5 33.5v-5a4.5 4.5 0 0 0 0-9z" fill="{_DSOFT}" {_DST}/><path d="M32 13v4M32 22v4M32 31v4" fill="none" {_DST}/><path d="M19 15.8l2.5 5.1 5.6.8-4 4 .9 5.6-5-2.6-5 2.6.9-5.6-4-4 5.6-.8z" fill="{_DS}" {_DST}/>''',
    'school': f'''<rect x="6" y="35" width="35" height="8" rx="2.5" fill="{_DS}" {_DST}/><path d="M35.5 35v8" fill="none" {_DST}/><rect x="9" y="27" width="32" height="8" rx="2.5" fill="{_DMINT}" {_DST}/><path d="M14.5 27v8" fill="none" {_DST}/><rect x="7" y="19" width="33" height="8" rx="2.5" fill="{_DCLAY}" {_DST}/><path d="M34.5 19v8" fill="none" {_DST}/><path d="M15 10.5v4.8c0 1.6 4 2.7 9 2.7s9-1.1 9-2.7v-4.8" fill="{_DE}" {_DST}/><path d="M24 3.5l17 6.3-17 6.3-17-6.3z" fill="{_DE}" {_DST}/><path d="M40.5 10v6.5" fill="none" {_DST}/><circle cx="40.5" cy="18.3" r="2" fill="{_DS}" {_DST}/>''',
    # payment methods: solid shapes in evergreen with a sun accent
    'paycard': f'''<g transform="rotate(-16 22 20)"><rect x="5" y="9" width="31" height="20" rx="3.5" fill="{_DE}"/><rect x="25" y="13" width="7" height="5.5" rx="1.4" fill="{_DS}"/></g><rect x="12" y="20" width="31" height="20" rx="3.5" fill="#FFFFFF" stroke="{_DE}" stroke-width="2.6"/><rect x="12" y="24.5" width="31" height="4.6" fill="{_DE}"/><rect x="16" y="32.6" width="10" height="2.6" rx="1.3" fill="{_DE}"/><rect x="28.5" y="32.6" width="7" height="2.6" rx="1.3" fill="{_DE}"/>''',
    'paybank': f'''<path d="M24 4.5 43 14.6V18H5v-3.4z" fill="{_DE}"/><circle cx="24" cy="12.6" r="3.2" fill="{_DS}"/><rect x="8" y="20" width="32" height="2.8" rx="1" fill="{_DE}"/><rect x="10.5" y="24" width="5.5" height="12" fill="{_DE}"/><rect x="21.25" y="24" width="5.5" height="12" fill="{_DE}"/><rect x="32" y="24" width="5.5" height="12" fill="{_DE}"/><rect x="8" y="37.2" width="32" height="2.8" rx="1" fill="{_DE}"/><rect x="5" y="41.2" width="38" height="3.8" rx="1.2" fill="{_DE}"/>''',
    'payphone': f'''<rect x="11" y="4" width="21" height="40" rx="4.6" fill="{_DE}"/><rect x="14" y="9" width="15" height="25.5" rx="1.6" fill="#FFFFFF"/><circle cx="21.5" cy="39.2" r="1.8" fill="#FFFFFF"/><circle cx="33.5" cy="16" r="9" fill="{_DS}" stroke="{_DE}" stroke-width="2.4"/><path d="M29.4 16h7.6M34.2 12.4 37.8 16l-3.6 3.6" fill="none" stroke="{_DE}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>''',
    'heart': f'''<path d="M24 41.5S6.5 31.7 6.5 18.8C6.5 13 10.9 8.5 16.4 8.5c3.3 0 6 1.6 7.6 4.2 1.6-2.6 4.3-4.2 7.6-4.2 5.5 0 9.9 4.5 9.9 10.3C41.5 31.7 24 41.5 24 41.5z" fill="{_DS}" {_DST}/><path d="M13.5 17.5c.3-2.3 2-4 4.2-4.3" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"/>''',
}


def duo(name):
    return f'<svg class="duo" viewBox="0 0 48 48" aria-hidden="true">{_DUO[name]}</svg>'


# Social profiles for the footer. Paste a full link (https://...) to switch an icon on.
# Icons without a link are shown, but are not clickable until a link is added.
SOCIAL = [
    ('Instagram', 'instagram', ''),
    ('TikTok', 'tiktok', ''),
    ('X', 'x', ''),
    ('Facebook', 'facebook', ''),
    ('LinkedIn', 'linkedin', ''),
    ('YouTube', 'youtube', ''),
    ('Spotify', 'spotify', SPOTIFY_SHOW),
]


def social_links():
    out = []
    for label, key, url in SOCIAL:
        if url:
            name = 'Climate Gumzo on Spotify' if key == 'spotify' else f'Dunia Endelevu on {label}'
            out.append(f'<a href="{url}" target="_blank" rel="noopener" aria-label="{name}" title="{label}">{icon(key)}</a>')
        else:
            out.append(f'<span class="is-soon" title="{label}, link coming soon" aria-hidden="true">{icon(key)}</span>')
    out.append(f'<a href="mailto:{EMAIL}" aria-label="Email us" title="Email">{icon("mail")}</a>')
    return '\n          '.join(out)


def footer(name):
    def legal(href, label, key):
        cur = ' aria-current="page"' if name == key else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <nav class="footer-nav" aria-labelledby="f-menu-{name}">
        <h2 id="f-menu-{name}">Menu</h2>
        <a href="/about">About us</a>
        <a href="/programs">Programmes</a>
        <a href="/learn">Learn</a>
        <a href="/donate">Donate</a>
      </nav>
      <nav class="footer-nav" aria-labelledby="f-help-{name}">
        <h2 id="f-help-{name}">Get involved</h2>
        <a href="/contact#apply">Apply for a child</a>
        <a href="/about#volunteer">Volunteer</a>
        <a href="/donate?for=book">Sponsor a book</a>
      </nav>
      <div class="footer-nav">
        <h2>Contact</h2>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <a href="/contact">Send a message</a>
        <span>Nairobi, Kenya</span>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Dunia Endelevu</span>
      <div class="footer-bottom__end">
        <nav class="footer-legal" aria-label="Legal">
          {legal('/privacy', 'Privacy Policy', 'privacy')}
          {legal('/terms', 'Terms', 'terms')}
          {legal('/cookies', 'Cookies', 'cookies')}
        </nav>
        <div class="footer-social" aria-label="Social media">
          {social_links()}
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
    body = body.replace('{{alana}}', ALANA_SITE)
    body = body.replace('{{updated}}', '1 November 2026')
    body = body.replace('{{arrow}}', ARROW)
    body = re.sub(r'\{\{icon:([a-z-]+)\}\}', lambda m: icon(m.group(1)), body)
    body = re.sub(r'\{\{duo:([a-z]+)\}\}', lambda m: duo(m.group(1)), body)
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



def _text(fragment):
    from html import unescape
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', expand(fragment)))).strip()


def faq_ld(body):
    """Question-and-answer data from a page's <details><summary> blocks, so Google and AI tools can quote them."""
    pairs = re.findall(r'<details[^>]*>\s*<summary>(.*?)</summary>(.*?)</details>', body, re.S)
    if not pairs:
        return None
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': _text(q), 'acceptedAnswer': {'@type': 'Answer', 'text': _text(a)}} for q, a in pairs]}


PROGRAMMES = [
    ('Storyteller', 'programs#storyteller', 'Children write, illustrate and publish their own climate book, with workshops, editing and a launch.'),
    ('Voice', 'programs#voice', 'Children research, script and co-host episodes of Climate Gumzo, our climate podcast for young listeners.'),
    ('Diplomat', 'programs#diplomat', 'Children train to speak at real conferences, climate summits and panels.'),
    ('Early warning for schools (pilot)', 'programs#early-warning',
     'Alerts that warn schools about unhealthy air, heat and heavy rain, with a suggested step for each school. Now in pilot.'),
]


def programmes_ld():
    return {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Dunia Endelevu programmes', 'itemListElement': [
        {'@type': 'ListItem', 'position': i, 'item': {
            '@type': 'Service', 'name': n, 'url': f'{SITE_URL}{u}', 'description': d, 'areaServed': 'Kenya',
            'provider': {'@id': f'{SITE_URL}#organization'}, 'isAccessibleForFree': True}}
        for i, (n, u, d) in enumerate(PROGRAMMES, start=1)]}


AI_BOTS = ['Googlebot', 'Bingbot', 'DuckDuckBot', 'Applebot', 'GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot',
           'Claude-SearchBot', 'Claude-User', 'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Applebot-Extended',
           'Meta-ExternalAgent', 'CCBot']


def robots_txt():
    lines = ['# Dunia Endelevu', '# Everyone is welcome to read and index this site, including search engines and AI assistants.', '',
             'User-agent: *', 'Allow: /', f'Disallow: {BASE_PATH}src/', '']
    for bot in AI_BOTS:
        lines += [f'User-agent: {bot}', 'Allow: /', f'Disallow: {BASE_PATH}src/', '']
    lines += [f'Sitemap: {SITE_URL}sitemap.xml', '']
    return '\n'.join(lines)


def llms_txt(full=False):
    """A plain-text summary for AI assistants (the llms.txt convention); llms-full.txt adds every story."""
    out = [
        '# Dunia Endelevu', '',
        f'> Dunia Endelevu ("a sustainable world" in Kiswahili) is a youth-led climate incubator in Nairobi, Kenya, '
        f'founded by Alana Chelangat. It helps children under 18 write, speak and lead on climate, free for every family. '
        f'Slogan: "{SLOGAN}"', '',
        'Key facts:', '',
        '- Founded by: Alana Chelangat, Kenyan climate advocate, author and podcaster; Little Miss Environment Kenya 2025',
        f'- Founder’s website: {ALANA_SITE}',
        '- Based in: Nairobi, Kenya',
        '- Who it is for: children under 18, with written consent from a parent or guardian',
        '- Cost to families: free; donors and sponsors cover every cost',
        '- Three tracks: Storyteller (publish a climate book), Voice (co-host the podcast Climate Gumzo), Diplomat (speak at real events)',
        '- For schools: early warning alerts for unhealthy air, heat and heavy rain, now in pilot',
        f'- Free storybooks for children aged 6 to 10 on climate change, biodiversity, climate justice, climate action and environmental rights',
        f'- Podcast: Climate Gumzo, {SPOTIFY_SHOW}',
        f'- Contact: {EMAIL}',
        '- Safeguarding: vetted adults, at least two adults at every session, children credited by first name and age only',
        '', '## Pages', '']
    for name, title, desc, _, prio in PAGES:
        if prio is None or name.startswith('story-'):
            continue
        url = SITE_URL if name == 'index' else f'{SITE_URL}{name}'
        out.append(f'- [{title.split(" · ")[0]}]({url}): {desc}')
    out += ['', '## Storybooks', '']
    for bk in BOOKS:
        out.append(f'- [{bk["title"]}]({SITE_URL}story-{bk["slug"]}): {bk["topic"]}, ages {bk["ages"]}. {bk.get("summary", "")}')
    if full:
        for bk in BOOKS:
            out += ['', f'## {bk["title"]}', '', f'Topic: {bk["topic"]}. Ages {bk["ages"]}. By Dunia Endelevu.', '',
                    'What children learn: ' + '; '.join(bk.get('learn', [])) + '.', '']
            out += [f'Page {i}. {t}' for i, t in enumerate(bk['pages'][1:], start=1)]
    else:
        out += ['', f'- [Full text of every storybook, for AI assistants]({SITE_URL}llms-full.txt)']
    return '\n'.join(out) + '\n'


def build():
    ver = asset_version()
    by_page = {f'story-{b["slug"]}': b for b in BOOKS}
    for name, title, desc, nav, _ in PAGES:
        og = None
        ld = None
        if name == 'learn':
            body = booklib.shelf(BOOKS)
            ld = [booklib.shelf_ld(BOOKS, SITE_URL)]
        elif name in by_page:
            body = booklib.book_page(by_page[name], BOOKS)
            og = booklib.og_for(by_page[name])
            ld = booklib.book_ld(by_page[name], SITE_URL)
        else:
            body = (SRC / 'pages' / f'{name}.html').read_text()
            ld = [x for x in [faq_ld(body)] if x] or None
            if name == 'programs':
                ld = (ld or []) + [programmes_ld()]
        body = expand(body)
        html = '\n'.join([head(name, title, desc, ver, og, ld), header(nav), body.strip(), footer(name)])
        (ROOT / f'{name}.html').write_text(html)
    urls = []
    for name, _, _, _, prio in PAGES:
        if prio is None:
            continue
        loc = SITE_URL if name == 'index' else f'{SITE_URL}{name}'
        img = ''
        if name in by_page:
            img = f'<image:image><image:loc>{SITE_URL}assets/books/{by_page[name]["slug"]}/cover.jpg</image:loc></image:image>'
        urls.append(f'  <url><loc>{loc}</loc><lastmod>{UPDATED}</lastmod><priority>{prio}</priority>{img}</url>')
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                                      'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
                                      + '\n'.join(urls) + '\n</urlset>\n')
    (ROOT / 'robots.txt').write_text(robots_txt())
    (ROOT / 'llms.txt').write_text(llms_txt())
    (ROOT / 'llms-full.txt').write_text(llms_txt(full=True))
    print(f'Built {len(PAGES)} pages (assets v{ver}).')


if __name__ == '__main__':
    build()
