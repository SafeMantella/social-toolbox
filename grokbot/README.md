# Redes Arfux (Grok Bot) via webhook

Estrategista de redes do Pedro no Grok Bot. Recebe pautas, pedidos de roteiro/legenda/análise e contexto; manda prompts pro Pedro colar no Claude Code. Só faz rascunho, não publica nada. Webhook exclusivo deste projeto de redes (não é ferramenta global).

**A resposta chega pro Pedro no chat do Grok Bot, não volta pelo webhook.** Toda mensagem tem que ser autocontida.

## Enviar

    python3 ferramentas/grokbot/send_to_redes_arfux.py -s "assunto curto" "texto"
    python3 ferramentas/grokbot/send_to_redes_arfux.py -s "assunto" < arquivo.md
    # --no-reply quando for só aviso

Só dizer "enviado" com a saída `Enviado (<status>)`.

Corpo: `{"from": "claude-redes", "subject", "message", "reply_needed"}`, header `Authorization`.

## Credenciais

`ARFUX_WEBHOOK_URL` e `ARFUX_WEBHOOK_AUTH` (`Bearer <chave>` ou só a chave: o script põe o `Bearer ` se faltar), no ambiente ou em `.env` nesta pasta (gitignored, modelo em `.env.example`). Nunca imprimir, nunca versionar, nunca colocar no corpo.

## Regras

1. Uma mensagem por assunto.
2. Erro 401/403: não tentar de novo, avisar o Pedro.
3. Erro de rede: tentar de novo uma vez só.
4. Ao terminar tarefa que veio de um prompt dele: resumo curto (o que foi feito, caminhos, pendências). Nada de DM de terceiros nem segredo.

## Handoff

`handoff.md` tem o contexto completo (papel, Notion, repos, comandos, regras, formato dos prompts). Atualizar quando pendências, links ou comandos mudarem e reenviar:

    python3 ferramentas/grokbot/send_to_redes_arfux.py -s "Handoff: gerente de conteúdo" < ferramentas/grokbot/handoff.md
