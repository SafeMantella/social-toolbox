# keyword-mining — termos de busca reais (= dores de cliente)

`suggest.py` — minera o que as pessoas de fato digitam em torno de uma semente, via **autocomplete do Google e do YouTube** (endpoint público `suggestqueries.google.com`, sem chave, sem custo).

Termo de busca É dor de cliente: "claude code limite de tokens", "claude code muito lento", "claude code não abre", "why claude code is so slow" — é o que a pessoa digita quando está com o problema. O script agrupa por tipo pra separar **dor** de **comparação** de **intenção de compra** de **pergunta**.

## Uso

```bash
python3 ferramentas/keyword-mining/suggest.py "<semente>" ["<semente2>" ...] \
  [--lang pt-BR] [--no-alpha] [--sleep 0.3] [--out termos.md]
```

- `--no-alpha` — pula a varredura a-z. Mais rápido (~30-40 termos vs ~700), menos ruído, foca em dores/perguntas/comparações. **Usar por padrão**; rodar completo só quando quiser o mapa exaustivo.
- `--lang` — `pt-BR` (default), `en`, etc. Rodar nos dois se o nicho é bilíngue.
- `--sleep` — pausa entre requests (default 0.4s). Baixar se estiver com pressa, subir se o Google começar a devolver vazio.
- Sem `--out` → markdown no stdout.

## Como expande

Pra cada semente: a semente pura + modificadores de pergunta (`como`, `o que é`, `por que`, `how to`, `why`...), comparação (`vs`, `ou`, `alternativa`...), dor (`erro`, `não funciona`, `lento`, `caro`, `limite`...), intenção (`preço`, `grátis`, `tutorial`, `vale a pena`...), prefixos (`como <semente>`, `why <semente>`), e opcionalmente a-z. Cada expansão consulta Google **e** YouTube autocomplete. Dedupe + categoriza.

## Saída

Markdown com 5 seções: **Dores** · **Perguntas** · **Comparações** · **Intenção** · **Relacionados**. Termo marcado `_(YT)_` só apareceu no YouTube, `_(G+YT)_` nos dois (sinal mais forte).

Pra pesquisa de conteúdo, as seções **Dores** e **Perguntas** são a matéria-prima de hook e de roteiro. **Comparações** = ideias de post "X vs Y". **Intenção** = onde há disposição de pagar.

## Gotchas

- Endpoint não-oficial do Google — pode mudar sem aviso. Se voltar vazio de repente, testar `curl -s "https://suggestqueries.google.com/complete/search?client=firefox&q=teste"`.
- Rate limit: rodar muitas sementes seguidas com `--sleep` baixo pode fazer o Google devolver 429/vazio por alguns minutos.
- É autocomplete, não volume de busca. Diz *o que* as pessoas procuram e a ordem relativa de relevância do Google, não *quantas*.

## Smoke test (02/09/2026)

`suggest.py "claude code"` → 713 termos; bucket "Dores" trouxe "limite de tokens", "muito lento", "muito caro", "não abre", "error query closed before response received", "why claude code is so slow". `--no-alpha "notion ia"` → 41 termos em ~20s.
