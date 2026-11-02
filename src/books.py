"""Storybooks: the Learn shelf and one page per book, made from src/books.json.

build.py calls this, so adding a book is: python3 src/add_book.py ... then python3 src/build.py.
Each book's images live in assets/books/<slug>/ (cover.webp/.jpg, page-01.webp/.jpg, ...).
Optional narration: drop assets/books/<slug>/audio/page-01.mp3, page-02.mp3, ... and rebuild;
the Listen button then plays those recordings instead of the device voice.
"""
import json
import pathlib
from html import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOKS_FILE = ROOT / 'src' / 'books.json'


def load():
    return json.loads(BOOKS_FILE.read_text(encoding='utf-8'))


def page_entries(books):
    """PAGES rows for build.py: (name, title, description, nav key, sitemap priority)."""
    rows = []
    for b in books:
        desc = (f'A free illustrated storybook about {b["topic"].lower()} for children aged {b["ages"]}. '
                f'Read it online, listen along or download the PDF.')
        rows.append((f'story-{b["slug"]}', f'{b["title"]} · Storybook · Dunia Endelevu', desc, 'learn', '0.7'))
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


def shelf(books):
    cards = []
    for i, b in enumerate(books):
        d = f' reveal-d{i % 3}' if i % 3 else ''
        cards.append(
            f'      <li class="reveal{d}"><a class="book-card" href="story-{b["slug"]}.html">'
            f'<span class="book-card__cover">{_pic(f"assets/books/{b["slug"]}/cover", b["cover_alt"], *cover_size(b), lazy=i > 3)}</span>'
            f'<span class="book-card__title">{escape(b["title"])}</span>'
            f'<span class="book-card__meta">{escape(b["topic"])} · Ages {escape(b["ages"])}</span></a></li>')
    cards.append('      <li class="reveal"><div class="book-card book-card--soon"><span class="book-card__cover">'
                 '<span>More stories<br>are on the way</span></span></div></li>')
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


def book_page(b):
    slug, title = b['slug'], b['title']
    w, h = b.get('page_size', [1600, 1236])
    n = len(b['pages'])
    base = f'assets/books/{slug}'
    figs = []
    for i, text in enumerate(b['pages'], start=1):
        alt = f'Cover: {title}.' if i == 1 else text
        audio = ROOT / base / 'audio' / f'page-{i:02d}.mp3'
        a = f' data-audio="{base}/audio/page-{i:02d}.mp3"' if audio.exists() else ''
        if i == 1:  # the export puts the cover on the right half of a blank spread: show it centred instead
            img = _pic(f'{base}/cover', alt, *cover_size(b), lazy=False)
            figs.append(f'        <figure class="reader__page reader__page--cover" data-say="{escape(text)}"{a}>{img}</figure>')
            continue
        figs.append(f'        <figure class="reader__page" data-say="{escape(text)}"{a}>'
                    f'{_pic(f"{base}/page-{i:02d}", alt, w, h, lazy=i > 2)}</figure>')
    learn = ''
    if b.get('learn'):
        items = ''.join(f'<li>{escape(x)}</li>' for x in b['learn'])
        learn = f'''
        <div class="book-learn">
          <h2 class="book-learn__title">What children will learn</h2>
          <ul class="ticks">{items}</ul>
        </div>'''
    summary = f'\n        <p class="lead">{escape(b["summary"])}</p>' if b.get('summary') else ''
    text_items = ''.join(f'<li>{escape(t)}</li>' for t in b['pages'][1:])
    pdf = ''
    if b.get('pdf'):
        size = f' ({b["pdf_size"]})' if b.get('pdf_size') else ''
        pdf = f'<a class="more" href="{base}/{b["pdf"]}" download>Download the PDF{size} <span class="arrow">{{{{icon:download}}}}</span></a>'
    listen_btn = ('<button class="btn btn--ghost listen-btn" type="button" data-listen aria-pressed="false" hidden>'
                  '<span class="listen-ico" aria-hidden="true">{{icon:volume}}{{icon:pause}}</span>'
                  '<span data-listen-label>Listen</span></button>')
    return f'''<main id="main">

  <section class="wrap book-top" aria-labelledby="book-title">
    <figure class="book-top__cover">{_pic(f"{base}/cover", b["cover_alt"], *cover_size(b), lazy=False)}</figure>
    <div class="book-top__copy">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="learn.html">Storybooks</a><span aria-hidden="true">›</span><span aria-current="page">{escape(title)}</span></nav>
      <h1 id="book-title" class="h2">{escape(title)}</h1>
      <ul class="book-meta" aria-label="About this book"><li class="chip">{escape(b["topic"])}</li><li class="chip">Ages {escape(b["ages"])}</li><li class="chip">{n} pages</li></ul>{summary}{learn}
      <div class="btn-row">
        <a class="btn btn--sun" href="#read">Read the book {{{{arrow}}}}</a>
        {listen_btn}
      </div>
    </div>
  </section>

  <section class="wrap reader-wrap" id="read" aria-label="Read {escape(title)}">
    <div class="reader" data-reader>
      <div class="reader__pages">
{chr(10).join(figs)}
      </div>
      <div class="reader__bar">
        <button class="reader__btn" type="button" data-prev aria-label="Previous page">{{{{arrow}}}}</button>
        <span class="reader__count" aria-live="polite"><span data-count>1</span> of {n}</span>
        <button class="reader__btn reader__btn--next" type="button" data-next aria-label="Next page">{{{{arrow}}}}</button>
        <button class="reader__listen" type="button" data-listen aria-pressed="false" hidden><span class="listen-ico" aria-hidden="true">{{{{icon:volume}}}}{{{{icon:pause}}}}</span><span data-listen-label>Listen</span></button>
      </div>
    </div>
    <div class="book-foot">
      {pdf}
      <p class="fine">{escape(b.get("credit", "Story by Dunia Endelevu."))} Free to read, print and share for learning.</p>
    </div>
    <details class="book-text">
      <summary>Read the story as text</summary>
      <ol>{text_items}</ol>
    </details>
    <p class="book-back"><a class="more" href="learn.html"><span class="arrow arrow--back">{{{{arrow}}}}</span> All storybooks</a></p>
  </section>

</main>
'''
