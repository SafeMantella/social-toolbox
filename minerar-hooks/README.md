# minerar-hooks

**Descobre quais tipos de abertura (hook) performam num conjunto de vídeos.** Você junta um CSV de hooks reais com as views de cada um; o script ranqueia, classifica cada hook numa família (resultado primeiro, lista, contrarian, pergunta direta, erro/aviso, POV…) e conta as palavras de carga emocional. É a metade *mecânica* da mineração; o remix (adaptar a estrutura pro seu tema, trocando só as power words) fica com você ou com o agente.

```bash
python3 minerar.py hooks.csv --top 40 --out resultado/
python3 minerar.py --selftest
```

## Entrada

CSV com uma coluna de hook, uma de views e, opcionalmente, fonte e autor. Os nomes das colunas são detectados automaticamente (PT e EN; fonte pode se chamar source, fonte, autor, canal, plataforma…).

```csv
hook,views,source
Cortei meu gasto de tokens pela metade,182000,reel-fala
Pare de usar o ChatGPT assim,95000,reel-fala
5 configs que ninguém te conta do Claude Code,310000,yt-titulo
```

## Saída

- `<nome-do-csv>.mined.json` (ex.: `hooks.mined.json`) com o ranking, a família de cada hook e as power words, mais um resumo no terminal.
- Ranking por **percentil dentro da fonte**, e resultados **separados por fonte**: `yt-titulo` (embalagem do vídeo) e `reel-fala` (gancho falado) nunca se misturam, porque um título e uma fala de 3 segundos não competem na mesma régua.

## Famílias de abertura

`results-first` · `list-tease` · `contrarian` · `mistake-warning` · `confession` · `identity-call` · `pov` · `open-loop` · `direct-question` · `newsjack`. A ordem é a prioridade do match; o primeiro padrão que bater define a família. Os padrões (regex em PT e EN) ficam no topo de `minerar.py` e são fáceis de editar.

## Limites

- Regex não entende contexto: leia o ranking como pista, não como verdade. Hook que não bate com nenhum padrão fica sem família.
- Percentil com poucos hooks por fonte engana; use algumas dezenas de linhas no mínimo.

## Origem

Adaptado de [Ootto-AI/claude-content-skills](https://github.com/Ootto-AI/claude-content-skills) (licença MIT) para PT-BR.
