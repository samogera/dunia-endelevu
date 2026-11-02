#!/usr/bin/env python3
"""Add a storybook (a Gemini Storybook PDF export) to the Learn shelf.

    python3 src/add_book.py path/to/Book.pdf <slug> "<Title>" [options]

    --topic "Biodiversity"     shown on the shelf and the book page (default: Climate change)
    --ages "6 to 10"           (default: 6 to 10)
    --by "Dunia Endelevu"      author line read aloud with the cover
    --summary "..."            two sentences about the story
    --learn "..." --learn "..."  one line per thing children will learn
    --no-build                 skip rebuilding the site

What it does:
  1. renders every page to web images in assets/books/<slug>/ (page-01.webp/.jpg, ...),
  2. cuts the cover out of page 1 (cover.webp/.jpg),
  3. reads each page's text with OCR, for the alt text, the text version and the Listen voice,
  4. makes a small PDF to download (the Gemini export is often hundreds of MB),
  5. adds or updates the book in src/books.json, then rebuilds the site.

Check the OCR text in src/books.json afterwards: fix any misread words there and rebuild.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile

import img2pdf
from PIL import Image, ImageChops, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOKS_FILE = ROOT / 'src' / 'books.json'
WEB_W = 1600


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
    return t.strip()


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
        jpgs = []
        for i, path in enumerate(pages, start=1):
            im = Image.open(path)
            size = save_web(im, out / f'page-{i:02d}', WEB_W)
            jpgs.append(out / f'page-{i:02d}.jpg')
            if i == 1:
                save_web(crop_cover(im), out / 'cover', 800)
                texts.append(f'{a.title}. By {a.by}.')
            else:
                texts.append(ocr_text(im))
            print(f'  page {i}/{len(pages)} done')
    pdf_name = re.sub(r'[^a-z0-9]+', '-', a.title.lower()).strip('-') + '.pdf'
    letter = (img2pdf.in_to_pt(11), img2pdf.in_to_pt(8.5))
    (out / pdf_name).write_bytes(img2pdf.convert([str(j) for j in jpgs], layout_fun=img2pdf.get_layout_fun(letter)))
    mb = (out / pdf_name).stat().st_size / 1e6
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
        'pdf': pdf_name,
        'pdf_size': f'{max(1, round(mb))} MB',
        'page_size': list(size),
        'cover_size': cover_size,
        'credit': (old or {}).get('credit', 'Story by Dunia Endelevu. Illustrated with AI (Gemini).'),
        'pages': texts,
    }
    if old:
        books[books.index(old)] = entry
    else:
        books.append(entry)
    BOOKS_FILE.write_text(json.dumps(books, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'\nAdded "{a.title}" ({len(texts)} pages, PDF {mb:.1f} MB). Text read from the pages:\n')
    for i, tx in enumerate(texts, start=1):
        print(f'  {i:>2}. {tx}\n')
    if not entry['summary'] or not entry['learn']:
        print('Remember to add a summary and "What children will learn" in src/books.json.')
    if not a.no_build:
        subprocess.run([sys.executable, str(ROOT / 'src' / 'build.py')], check=True)


if __name__ == '__main__':
    main()
