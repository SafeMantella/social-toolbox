#!/usr/bin/env python3
import sys
from pathlib import Path

import pymupdf4llm


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 pdf_to_md.py <caminho.pdf> [--pages 1,2,3]")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        print(f"Arquivo não encontrado: {pdf_path}")
        sys.exit(1)

    pages = None
    if "--pages" in sys.argv:
        raw = sys.argv[sys.argv.index("--pages") + 1]
        pages = [int(p) - 1 for p in raw.split(",")]  # pymupdf4llm é 0-indexed

    md_text = pymupdf4llm.to_markdown(str(pdf_path), pages=pages)

    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"{pdf_path.stem}.md"
    out_path.write_text(md_text, encoding="utf-8")

    print(f"Markdown salvo em: {out_path}")
    print(f"{len(md_text)} caracteres, {md_text.count(chr(10))} linhas")


if __name__ == "__main__":
    main()
