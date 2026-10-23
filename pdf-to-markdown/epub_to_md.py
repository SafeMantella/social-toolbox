#!/usr/bin/env python3
"""EPUB -> Markdown, local, no API. Companion to pdf_to_md.py.

Usage: python3 epub_to_md.py "<file.epub>" [more.epub ...]
Output: output/<name>.md
"""
import sys
import pathlib
import warnings

warnings.filterwarnings("ignore")
import ebooklib  # noqa: E402
from ebooklib import epub  # noqa: E402
import html2text  # noqa: E402

OUT = pathlib.Path(__file__).parent / "output"


def convert(path: pathlib.Path) -> pathlib.Path:
    book = epub.read_epub(str(path), options={"ignore_ncx": True})
    h = html2text.HTML2Text()
    h.body_width = 0
    h.ignore_images = True
    h.ignore_emphasis = False
    parts = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        parts.append(h.handle(item.get_content().decode("utf-8", "ignore")))
    md = "\n\n".join(p.strip() for p in parts if p.strip())
    OUT.mkdir(exist_ok=True)
    dest = OUT / (path.stem + ".md")
    dest.write_text(md, encoding="utf-8")
    return dest


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for arg in sys.argv[1:]:
        p = pathlib.Path(arg)
        try:
            dest = convert(p)
            print(f"OK  {dest}  ({dest.stat().st_size // 1024} KB)")
        except Exception as e:  # noqa: BLE001
            print(f"ERR {p.name}: {e}")
