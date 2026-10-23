#!/usr/bin/env bash
# Gera 1 imagem via Grok CLI (ferramenta nativa Imagine) e copia pro destino.
# Uso: gerar.sh "<prompt em inglês>" destino.jpg [16:9|9:16|1:1|4:5]
set -euo pipefail
prompt="$1"; dest="$2"; aspect="${3:-16:9}"
work="$(mktemp -d)"
grok -p "Gere UMA imagem ${aspect} com a ferramenta de imagem, usando EXATAMENTE este prompt, sem texto/logo/letras na imagem. Não crie arquivos por outros meios.

${prompt}" --cwd "$work" --output-format json --no-alt-screen --no-auto-update \
  > "$work/out.json"
jq -r '"custo US$ \(.total_cost_usd)"' "$work/out.json" >&2
# ponytail: grok grava em ~/.grok/sessions/<cwd-codificado>/<id>/images/; pega o mais recente desse cwd
img="$(ls -t ~/.grok/sessions/*"$(basename "$work")"*/*/images/*.jpg 2>/dev/null | head -1 || true)"
# moderação do Grok pode recusar prompt inofensivo (e cobrar mesmo assim): reescreva e tente de novo
[ -n "$img" ] || { echo "sem imagem. resposta do grok:" >&2; jq -r '.text' "$work/out.json" >&2; exit 1; }
mkdir -p "$(dirname "$dest")"; cp "$img" "$dest"; rm -rf "$work"; echo "$dest"
