# social-toolbox

**Sete scripts pequenos de pesquisa e produção de conteúdo pra redes sociais**, escritos pra serem chamados por um agente de código (Claude Code, Codex, Gemini…) ou direto no terminal. Cada um faz uma coisa, tem uma entrada e uma saída claras e quase nenhuma dependência.

Pesquisar o que o público procura, minerar hooks que funcionaram, ler PDF sem gastar token, gerar imagem, tirar o áudio de um vídeo: o trabalho repetitivo antes de gravar ou escrever.

| pasta | o que faz | linguagem | depende de |
|---|---|---|---|
| [`keyword-mining`](keyword-mining) | minera o que as pessoas digitam no Google e no YouTube em volta de um tema e separa em dores, perguntas, comparações e intenção de compra | Python | só stdlib, sem chave |
| [`minerar-hooks`](minerar-hooks) | CSV de hooks + views → ranking por percentil e famílias de abertura (resultado, lista, contrarian…) | Python | só stdlib |
| [`pdf-to-markdown`](pdf-to-markdown) | PDF e EPUB → Markdown local, com OCR nas páginas sem texto | Python | `pymupdf4llm`, `ebooklib`, `html2text` |
| [`extrair-audio`](extrair-audio) | extrai o áudio do vídeo **sem reencodar** (cópia da faixa) | bash | `ffmpeg` |
| [`grok-imagem`](grok-imagem) | gera 1 imagem pelo [Grok CLI](https://x.ai) e copia pro destino | bash | `grok`, `jq` |
| [`links`](links) | catálogo consultável de ferramentas (`ferramentas.csv`) com filtro por categoria, custo e uso | Python | `pandas` |
| [`grokbot`](grokbot) | manda mensagem pra um bot estrategista por webhook (exemplo de integração) | Python | só stdlib |

## Exemplos rápidos

```bash
# 1. o que as pessoas procuram sobre um tema (Google + YouTube autocomplete, grátis)
python3 keyword-mining/suggest.py "claude code" --no-alpha --lang pt-BR

# 2. quais aberturas performam num CSV de hooks (colunas hook e views auto-detectadas)
python3 minerar-hooks/minerar.py hooks.csv --top 40

# 3. PDF grande vira texto barato pro agente ler
python3 pdf-to-markdown/pdf_to_md.py "playbook.pdf"          # -> output/playbook.md
python3 pdf-to-markdown/pdf_to_md.py "playbook.pdf" --pages 2,3

# 4. áudio do vídeo, sem perda
extrair-audio/extrair-audio -o audio/ "pasta-com-videos/"

# 5. ferramentas grátis pra thumbnail
python3 links/links.py --uso thumbnail --custo free
```

Cada pasta tem seu README com flags, saída e gotchas.

## Instalação

Não há pacote nem instalador: clone e rode o script.

```bash
git clone https://github.com/SafeMantella/social-toolbox.git
cd social-toolbox
pip install pandas pymupdf4llm ebooklib html2text   # só se for usar links e pdf-to-markdown
```

`keyword-mining`, `minerar-hooks` e `grokbot` rodam só com o Python 3 padrão.

## Antes de usar

- Criado pro projeto de redes sociais do autor, no macOS. A maioria dos scripts é independente do layout, mas **alguns têm caminho absoluto** (`/Volumes/1TB Mac/...`) e `ferramentas/...` nos exemplos e docstrings. Ajuste esses caminhos antes de usar em outra máquina.
- `keyword-mining` usa o endpoint de autocomplete **não oficial** do Google: pode mudar ou limitar sem aviso. Detalhes no README da pasta.
- `grokbot` precisa de um webhook seu em `.env` (modelo em `grokbot/.env.example`). O `.env` está no `.gitignore`: nunca o commite. O `handoff.md` da pasta é o contexto de uma instância privada do autor e serve só como exemplo de formato.
- `grok-imagem` gasta crédito do Grok a cada chamada (o script imprime o custo) e a moderação pode recusar um prompt inofensivo e cobrar mesmo assim.

## Repos relacionados

Mesmo kit do [@SafeMantella](https://github.com/SafeMantella): [video-cut-pipeline](https://github.com/SafeMantella/video-cut-pipeline), [transcrever-ptbr](https://github.com/SafeMantella/transcrever-ptbr), [video-tools](https://github.com/SafeMantella/video-tools), [sau-tools](https://github.com/SafeMantella/sau-tools), [token-kit](https://github.com/SafeMantella/token-kit). O áudio extraído aqui alimenta o [Adobe Podcast](https://github.com/SafeMantella/Adobe-Podcast-for-Claude-Code).
