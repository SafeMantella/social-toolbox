# minerar-hooks

Entrada: CSV com colunas de hook, views e (opcional) fonte/autor. Nomes são auto-detectados.
`python3 minerar.py hooks.csv [--top 40] [--out dir]` → `hooks.mined.json` + resumo no terminal.
Ranking por percentil dentro da fonte; saída separada por fonte (`yt-titulo` = embalagem, `reel-fala` = gancho, nunca misturar). Famílias = tabela de `referencia/swipe-openers.md`.
`--selftest` valida. O remix (trocar só power words) é do Claude; ver `memory/pipeline_pesquisa.md`.
Origem: github.com/Ootto-AI/claude-content-skills (MIT), adaptado.
