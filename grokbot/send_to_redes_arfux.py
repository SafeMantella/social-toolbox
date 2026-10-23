#!/usr/bin/env python3
"""Envia uma mensagem para o Redes Arfux (Grok Bot) via webhook."""
import argparse, json, os, pathlib, sys, urllib.request

# credenciais: variáveis de ambiente ou .env ao lado deste script (gitignored)
ENV = pathlib.Path(__file__).resolve().parent / ".env"
if ENV.is_file():
    for linha in ENV.read_text().splitlines():
        if "=" in linha and not linha.lstrip().startswith("#"):
            k, v = linha.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"'))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("message", nargs="?", help="texto; se omitido, lê do stdin")
    p.add_argument("-s", "--subject", default="Mensagem do Claude")
    p.add_argument("--no-reply", action="store_true")
    a = p.parse_args()
    url = os.environ.get("ARFUX_WEBHOOK_URL")
    auth = os.environ.get("ARFUX_WEBHOOK_AUTH")
    if not url or not auth:
        sys.exit("Defina ARFUX_WEBHOOK_URL e ARFUX_WEBHOOK_AUTH")
    if not auth.startswith("Bearer "):  # aceita só a chave no .env
        auth = f"Bearer {auth}"
    msg = a.message or sys.stdin.read()
    if not msg.strip():
        sys.exit("Mensagem vazia")
    body = json.dumps({"from": "claude-redes", "subject": a.subject,
                       "message": msg, "reply_needed": not a.no_reply}).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": auth, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print(f"Enviado ({r.status})")
    except urllib.error.HTTPError as e:
        sys.exit(f"Falhou: HTTP {e.code} {e.read().decode()[:300]}")

if __name__ == "__main__":
    main()
