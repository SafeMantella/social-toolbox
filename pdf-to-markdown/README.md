# PDF → Markdown

Converte um PDF em Markdown localmente, sem API e sem custo — usado pra ler documentos grandes (playbooks, e-books, apostilas) sem gastar tokens de imagem lendo página por página com o Read tool. O agente lê o `.md` gerado (texto puro, barato) em vez do PDF direto.

Por que isso é útil pra agentes de IA: um PDF de 13 páginas lido direto vira 13 imagens (caro em tokens); convertido pra markdown vira um único arquivo de texto que cabe numa leitura só, e ainda fica salvo pra reuso.

## Uso

```bash
python3 pdf_to_md.py "/caminho/para/arquivo.pdf"
```

- Sem flags: converte o PDF inteiro.
- `--pages 1,2,3`: converte só as páginas listadas (1-indexed), útil pra reprocessar um trecho específico sem rodar o documento todo de novo.

## Dependências (confirmadas instaladas 25/08/2026)

- `pymupdf4llm` (`pip install pymupdf4llm`) — extrai texto com ordem de leitura consciente do layout (colunas, tabelas) e cai pra OCR local (Tesseract, embutido no pacote `pymupdf_layout`) automaticamente nas páginas sem camada de texto (ex.: páginas todas em imagem/design). Sem chave de API, roda 100% local.

**Fallback se a extração sair ruim** (texto embaralhado ou faltando em várias páginas, não só nas OCR): trocar por [Marker](https://github.com/VikParuchuri/marker) (`pip install marker-pdf`) — mais pesado (baixa modelos de layout/OCR na primeira execução, ~1-2GB, suporta Apple MPS), mas mais robusto pra PDFs com layout complexo (cards lado a lado, colunas, imagens densas).

## Saída

- `output/<nome-do-pdf>.md` — markdown gerado, mesmo nome do arquivo de origem.

## Histórico de uso

- 25/08/2026: convertido "Mr Paid Social - The Claude Edit Playbook.pdf" (13 páginas, deck desenhado com cards/screenshots) — 466 linhas de markdown, texto completo e legível incluindo tabelas. OCR local ativado automaticamente em 5 páginas sem camada de texto (2, 4, 5, 9, 11). Conteúdo usado pra atualizar `memory/feedback_video_editing_motion_graphics_ad_playbook.md`.
