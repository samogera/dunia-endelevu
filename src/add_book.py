#!/usr/bin/env python3
"""Add a storybook (a Gemini Storybook PDF export) to the Learn shelf.

    python3 src/add_book.py path/to/Book.pdf <slug> "<Title>" [options]

    --topic "Biodiversity"     shown on the shelf and the book page (default: Climate change)
    --ages "6 to 10"           (default: 6 to 10)
    --by "Dunia Endelevu"      author line read aloud with the cover
    --summary "..."            a short paragraph about the story
    --learn "..." --learn "..."  short lines: what children will learn
    --no-build                 skip rebuilding the site

What it does:
  1. cuts the cover out of page 1 (cover.webp/.jpg),
  2. saves the picture half of every story spread as a web image in assets/books/<slug>/ (page-02.webp/.jpg, ...),
  3. reads the words half of every spread with OCR; the website sets those words as real text,
     so they stay sharp and easy to read on phones, and the Listen voice reads them,
  4. adds or updates the book in src/books.json, then rebuilds the site.

Check the OCR text in src/books.json afterwards: fix any misread words there and rebuild.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile

from PIL import Image, ImageChops, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOKS_FILE = ROOT / 'src' / 'books.json'
PAGE_W = 1000  # one page (half a spread), wide enough for sharp pictures on big screens


def render(pdf, tmp):
    print('Rendering pages (a big PDF can take a few minutes)...')
    subprocess.run(['pdftoppm', '-r', '200', '-png', str(pdf), str(tmp / 'p')], check=True)
    pages = sorted(tmp.glob('p-*.png'), key=lambda p: int(p.stem.split('-')[1]))
    if not pages:
        sys.exit('No pages found in the PDF.')
    return pages


def save_web(im, base, width):
    im = im.convert('RGB')
    if im.width != width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(f'{base}.jpg', quality=82, optimize=True, progressive=True)
    im.save(f'{base}.webp', quality=78, method=6)
    return im.size


def crop_cover(im):
    rgb = im.convert('RGB')
    diff = ImageChops.difference(rgb, Image.new('RGB', rgb.size, (255, 255, 255))).convert('L')
    box = diff.point(lambda v: 255 if v > 18 else 0).getbbox()
    return rgb.crop(box) if box else rgb


def ocr_text(im):
    w, h = im.size
    # Gemini spreads: picture on the left, words on the right, a running head at the top and a page number at the bottom.
    part = im.convert('L').crop((int(w * .53), int(h * .07), int(w * .98), int(h * .91)))
    part = ImageOps.autocontrast(part)
    with tempfile.NamedTemporaryFile(suffix='.png') as f:
        part.save(f.name)
        out = subprocess.run(['tesseract', f.name, '-', '--psm', '6', '-l', 'eng'],
                             capture_output=True, text=True, check=True).stdout
    return clean(out)


FIXES = [
    (r'\s+([,.;:!?])', r'\1'), (r'(\w)- (\w)', r'\1\2'), (r'\bIna\b', 'In a'), (r'\bpufts\b', 'puffs'),
    (r'\|', 'I'), (r'\s{2,}', ' '), (r'^[^A-Za-z“"‘\']+', ''),
]


def clean(text):
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln and not re.fullmatch(r'[\d\W]{1,4}', ln)]
    t = ' '.join(lines)
    t = t.replace('“', '"').replace('”', '"')
    for a, b in FIXES:
        t = re.sub(a, b, t)
    # typographer's quotes: “ opening, ” closing, ’ apostrophes
    t = re.sub(r'(^|[\s(\[—-])"', r'\1“', t.strip()).replace('"', '”')
    t = re.sub(r"(^|[\s(\[—-])'", r'\1‘', t).replace("'", '’')
    return t


def main():
    ap = argparse.ArgumentParser(description='Add a storybook PDF to the Learn shelf.')
    ap.add_argument('pdf', type=pathlib.Path)
    ap.add_argument('slug', help='short name for the web address, e.g. "amani" makes story-amani.html')
    ap.add_argument('title')
    ap.add_argument('--topic', default='Climate change')
    ap.add_argument('--ages', default='6 to 10')
    ap.add_argument('--by', default='Dunia Endelevu')
    ap.add_argument('--summary', default='')
    ap.add_argument('--learn', action='append', default=[])
    ap.add_argument('--no-build', action='store_true')
    a = ap.parse_args()
    if not re.fullmatch(r'[a-z0-9-]+', a.slug):
        sys.exit('The slug may only use a-z, 0-9 and hyphens.')

    out = ROOT / 'assets' / 'books' / a.slug
    out.mkdir(parents=True, exist_ok=True)
    texts = []
    with tempfile.TemporaryDirectory() as t:
        tmp = pathlib.Path(t)
        pages = render(a.pdf, tmp)
        size = None
        for i, path in enumerate(pages, start=1):
            im = Image.open(path)
            if i == 1:
                save_web(crop_cover(im), out / 'cover', PAGE_W)
                texts.append(f'{a.title}. By {a.by}.')
            else:
                size = save_web(im.crop((0, 0, im.width // 2, im.height)), out / f'page-{i:02d}', PAGE_W)
                texts.append(ocr_text(im))
            print(f'  page {i}/{len(pages)} done')
    cover_size = list(Image.open(out / 'cover.jpg').size)

    books = json.loads(BOOKS_FILE.read_text(encoding='utf-8'))
    old = next((b for b in books if b['slug'] == a.slug), None)
    entry = {
        'slug': a.slug,
        'title': a.title,
        'topic': a.topic,
        'ages': a.ages,
        'summary': a.summary or (old or {}).get('summary', ''),
        'learn': a.learn or (old or {}).get('learn', []),
        'cover_alt': (old or {}).get('cover_alt', f'Cover of {a.title}.'),
        'page_size': list(size or (PAGE_W, 1545)),
        'cover_size': cover_size,
        'pages': texts,
    }
    if old:
        books[books.index(old)] = entry
    else:
        books.append(entry)
    BOOKS_FILE.write_text(json.dumps(books, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'\nAdded "{a.title}" ({len(texts)} pages). Text read from the pages:\n')
    for i, tx in enumerate(texts, start=1):
        print(f'  {i:>2}. {tx}\n')
    if not entry['summary'] or not entry['learn']:
        print('Remember to add a short summary and what children will learn in src/books.json.')
    if not a.no_build:
        subprocess.run([sys.executable, str(ROOT / 'src' / 'build.py')], check=True)


if __name__ == '__main__':
    main()
