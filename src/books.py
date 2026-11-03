"""Storybooks: the Learn shelf and one page per book, made from src/books.json.

build.py calls this, so adding a book is: python3 src/add_book.py ... then python3 src/build.py.
Each book's images live in assets/books/<slug>/ (cover.webp/.jpg, page-02.webp/.jpg, ...; page 1 is the cover).
Optional narration: drop assets/books/<slug>/audio/page-02.mp3, page-03.mp3, ... and rebuild;
the Listen button then plays those recordings instead of the device voice.
"""
import json
import pathlib
import re
from html import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOKS_FILE = ROOT / 'src' / 'books.json'


def load():
    return json.loads(BOOKS_FILE.read_text(encoding='utf-8'))


def describe(b):
    """A search-result description: the story's opening question, then what the book is."""
    first = re.split(r'(?<=[.!?”])\s+', b.get('summary', ''))[0] if b.get('summary') else ''
    short = f'A free {b["topic"].lower()} storybook for ages {b["ages"]}.'
    text = f'{first} {short}'.strip()
    if first and len(text) <= 220:
        return text
    return f'A free illustrated {b["topic"].lower()} storybook for children aged {b["ages"]}. Read it online or listen along.'


def shelf_ld(books, site):
    return {
        '@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Free climate storybooks for children',
        'itemListElement': [{'@type': 'ListItem', 'position': i, 'url': f'{site}story-{b["slug"]}.html', 'name': b['title']}
                            for i, b in enumerate(books, start=1)],
    }


def book_ld(b, site):
    url = f'{site}story-{b["slug"]}.html'
    org = {'@type': 'Organization', 'name': 'Dunia Endelevu', 'url': site}
    lo, hi = (int(n) for n in re.findall(r'\d+', b['ages'])[:2])
    book = {
        '@context': 'https://schema.org', '@type': 'Book', 'name': b['title'], 'url': url,
        'image': f'{site}assets/books/{b["slug"]}/cover.jpg', 'description': b.get('summary', ''),
        'author': org, 'publisher': org, 'inLanguage': 'en', 'isAccessibleForFree': True,
        'bookFormat': 'https://schema.org/EBook', 'numberOfPages': len(b['pages']) - 1,
        'genre': 'Children’s picture book', 'about': b['topic'],
        'audience': {'@type': 'PeopleAudience', 'suggestedMinAge': lo, 'suggestedMaxAge': hi},
    }
    crumbs = {
        '@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': site},
            {'@type': 'ListItem', 'position': 2, 'name': 'Storybooks', 'item': f'{site}learn.html'},
            {'@type': 'ListItem', 'position': 3, 'name': b['title'], 'item': url},
        ]}
    return [book, crumbs]


def page_entries(books):
    """PAGES rows for build.py: (name, title, description, nav key, sitemap priority)."""
    rows = []
    for b in books:
        rows.append((f'story-{b["slug"]}', f'{b["title"]} · Free children’s storybook · Dunia Endelevu', describe(b), 'learn', '0.7'))
    return rows


def cover_size(b):
    return b.get('cover_size', [800, 1236])


def og_for(b):
    w, h = cover_size(b)
    return {'image': f'assets/books/{b["slug"]}/cover.jpg', 'w': w, 'h': h, 'alt': escape(b['cover_alt'])}


def _pic(src, alt, w, h, lazy=True, cls=''):
    c = f' class="{cls}"' if cls else ''
    load = ' loading="lazy"' if lazy else ''
    return (f'<picture{c}><source type="image/webp" srcset="{src}.webp">'
            f'<img src="{src}.jpg" alt="{escape(alt)}" width="{w}" height="{h}"{load}></picture>')


def card(b, i=0):
    d = f' reveal-d{i % 3}' if i % 3 else ''
    return (f'      <li class="reveal{d}"><a class="book-card" href="story-{b["slug"]}.html">'
            f'<span class="book-card__cover">{_pic(f"assets/books/{b["slug"]}/cover", b["cover_alt"], *cover_size(b), lazy=i > 3)}</span>'
            f'<span class="book-card__title">{escape(b["title"])}</span></a></li>')


def shelf(books):
    cards = [card(b, i) for i, b in enumerate(books)]
    return f'''<main id="main">

  <section class="wrap shelf-head" aria-labelledby="learn-title">
    <span class="tag">Storybooks</span>
    <h1 id="learn-title" class="h1 split">Stories about our planet.</h1>
    <p class="lead">Free picture books about climate and nature, for children aged 6 to 10. Tap a cover to read, or listen along.</p>
  </section>

  <section class="wrap shelf" aria-label="Our storybooks">
    <ul class="books">
{chr(10).join(cards)}
    </ul>
  </section>

</main>
'''


def book_page(b, books=()):
    """Title, what children will learn, a short summary, then the book itself.

    With JavaScript the book opens as you scroll to it and its pages turn in 3D: two pages side by side on
    big screens, one page at a time on phones. The words are real text, so they stay sharp at every size.
    Without JavaScript the pictures and words simply stack.
    """
    slug, title = b['slug'], b['title']
    pw, ph = b.get('page_size', [1000, 1545])
    ratio = pw / ph
    base = f'assets/books/{slug}'
    cover_audio = ROOT / base / 'audio' / 'page-01.mp3'
    ca = f' data-cover-audio="{base}/audio/page-01.mp3"' if cover_audio.exists() else ''
    items = []
    for i, text in enumerate(b['pages'][1:], start=2):
        audio = ROOT / base / 'audio' / f'page-{i:02d}.mp3'
        a = f' data-audio="{base}/audio/page-{i:02d}.mp3"' if audio.exists() else ''
        items.append(f'        <li class="flip__src" data-img="{base}/page-{i:02d}" data-say="{escape(text)}"{a}>'
                     f'{_pic(f"{base}/page-{i:02d}", "", pw, ph)}<p>{escape(text)}</p></li>')
    learn = ''
    if b.get('learn'):
        learn = (f'\n      <div class="book-learn"><h2 class="book-learn__title">Learn more about {escape(b["topic"].lower())}</h2><ul>'
                 + ''.join(f'<li>{escape(x)}</li>' for x in b['learn']) + '</ul></div>')
    summary = f'\n      <p class="book-summary">{escape(b["summary"])}</p>' if b.get('summary') else ''
    others = [o for o in books if o['slug'] != slug]
    more = ''
    if others:
        more = ('\n  <section class="wrap more-books" aria-labelledby="more-title">\n'
                '    <h2 id="more-title" class="h2 h2--sm">More stories to read</h2>\n'
                '    <ul class="books books--more">\n' + '\n'.join(card(o, i) for i, o in enumerate(others)) + '\n    </ul>\n  </section>\n')
    by = b['pages'][0].split('By ', 1)[-1].rstrip('.') if 'By ' in b['pages'][0] else 'Dunia Endelevu'
    return f"""<main id="main">

  <section class="wrap book-page" aria-labelledby="book-title">
    <div class="book-head">
      <h1 id="book-title" class="h2">{escape(title)}</h1>{learn}{summary}
    </div>

    <div class="flip" data-book data-cover="{base}/cover" data-cover-alt="{escape(b['cover_alt'])}" data-title-say="{escape(b['pages'][0])}" data-by="{escape(by)}"{ca} style="--page: {ratio:.4f}; --spread: {2 * ratio:.4f}">
      <div class="flip__stage" tabindex="0" role="region" aria-roledescription="book" aria-label="{escape(title)}. Swipe, tap the page or use the arrow keys to turn the pages.">
        <div class="flip__book"><div class="flip__side flip__side--l"></div><div class="flip__side flip__side--r"></div></div>
      </div>
      <ol class="flip__list">
{chr(10).join(items)}
      </ol>
      <div class="flip__bar">
        <button class="reader__btn" type="button" data-prev aria-label="Previous page">{{{{arrow}}}}</button>
        <span class="reader__count" aria-live="polite" data-count>Cover</span>
        <button class="reader__btn reader__btn--next" type="button" data-next aria-label="Next page">{{{{arrow}}}}</button>
        <button class="reader__listen" type="button" data-listen aria-pressed="false" hidden><span class="listen-ico" aria-hidden="true">{{{{icon:volume}}}}{{{{icon:pause}}}}</span><span data-listen-label>Listen</span></button>
      </div>
      <div class="flip__progress" aria-hidden="true"><span></span></div>
    </div>

  </section>
{more}
  <section class="wrap book-foot">
    <p class="book-back"><a class="more" href="learn.html"><span class="arrow arrow--back">{{{{arrow}}}}</span> All storybooks</a></p>
  </section>

</main>
"""
