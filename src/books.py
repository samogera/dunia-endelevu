"""Storybooks: the Learn shelf and one page per book, made from src/books.json.

build.py calls this, so adding a book is: python3 src/add_book.py ... then python3 src/build.py.
Each book's images live in assets/books/<slug>/ (cover.webp/.jpg, page-02.webp/.jpg, ...; page 1 is the cover).
Optional narration: drop assets/books/<slug>/audio/page-02.mp3, page-03.mp3, ... and rebuild;
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
                f'Read it online or listen along.')
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
    base = f'assets/books/{slug}'
    # page 1 of the export is the cover, already shown above the book, so the reader starts at the story;
    # Listen says the title first
    story = b['pages'][1:]
    figs = []
    for i, text in enumerate(story, start=2):
        say = f'{b["pages"][0]} {text}' if i == 2 else text
        audio = ROOT / base / 'audio' / f'page-{i:02d}.mp3'
        a = f' data-audio="{base}/audio/page-{i:02d}.mp3"' if audio.exists() else ''
        figs.append(f'        <figure class="reader__page" data-say="{escape(say)}"{a}>'
                    f'{_pic(f"{base}/page-{i:02d}", text, w, h, lazy=i > 3)}</figure>')
    summary = f'\n    <p class="lead">{escape(b["summary"])}</p>' if b.get('summary') else ''
    return f'''<main id="main">

  <section class="wrap book-intro" aria-labelledby="book-title">
    <h1 id="book-title" class="sr-only">{escape(title)}</h1>
    <figure class="book-intro__cover">{_pic(f"{base}/cover", b["cover_alt"], *cover_size(b), lazy=False)}</figure>{summary}
  </section>

  <section class="wrap reader-wrap" id="read" aria-label="Read {escape(title)}">
    <div class="reader" data-reader>
      <div class="reader__pages">
{chr(10).join(figs)}
      </div>
      <div class="reader__bar">
        <button class="reader__btn" type="button" data-prev aria-label="Previous page">{{{{arrow}}}}</button>
        <span class="reader__count" aria-live="polite"><span data-count>1</span> of {len(story)}</span>
        <button class="reader__btn reader__btn--next" type="button" data-next aria-label="Next page">{{{{arrow}}}}</button>
        <button class="reader__listen" type="button" data-listen aria-pressed="false" hidden><span class="listen-ico" aria-hidden="true">{{{{icon:volume}}}}{{{{icon:pause}}}}</span><span data-listen-label>Listen</span></button>
      </div>
    </div>
    <p class="book-back"><a class="more" href="learn.html"><span class="arrow arrow--back">{{{{arrow}}}}</span> All storybooks</a></p>
  </section>

</main>
'''
