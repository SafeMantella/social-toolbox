#!/usr/bin/env python3
"""Minera os termos de busca reais em torno de uma ou mais sementes, via
autocomplete do Google e do YouTube (endpoint público, sem chave).

Termo de busca = dor de cliente. "claude code como economizar tokens",
"claude code não funciona", "claude code vs cursor" — é o que a pessoa digita
quando tem o problema. Agrupa por tipo pra separar dor de comparação de intenção.

Uso:
    suggest.py "<semente>" ["<semente2>" ...] [--lang pt-BR] [--out termos.md] [--sleep 0.4]

Sem --out, imprime o markdown no stdout.
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request

ENDPOINT = "https://suggestqueries.google.com/complete/search"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# modificadores que puxam intenção/dor (PT + um pouco de EN pro nicho tech)
QUESTIONS = ["como", "o que é", "por que", "qual", "quando", "quanto custa", "onde",
             "how to", "why", "what is"]
COMPARE = ["vs", "ou", "versus", "alternativa", "melhor que"]
PAIN = ["erro", "não funciona", "problema", "lento", "não abre", "não instala",
        "travando", "limite", "caro", "error", "not working", "fix", "issue"]
INTENT = ["preço", "grátis", "download", "tutorial", "curso", "planos", "review",
          "vale a pena", "pra que serve", "free", "pricing"]
ALPHA = list("abcdefghijklmnopqrstuvwxyz")


def fetch(query: str, lang: str, yt: bool) -> list[str]:
    params = {"client": "firefox", "hl": lang, "q": query}
    if yt:
        params["ds"] = "yt"
    url = f"{ENDPOINT}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        raw = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", "replace")
        data = json.loads(raw)
        return data[1] if len(data) > 1 and isinstance(data[1], list) else []
    except Exception as e:
        print(f"  ! falha em {query!r}: {e}", file=sys.stderr)
        return []


def expansions(seed: str, alpha: bool):
    yield seed
    for m in QUESTIONS + COMPARE + PAIN + INTENT:
        yield f"{seed} {m}"
    for m in ("como", "por que", "how to", "why"):
        yield f"{m} {seed}"
    if alpha:
        for c in ALPHA:
            yield f"{seed} {c}"


def categorize(term: str, seeds: list[str]) -> str:
    t = term.lower()
    if any(w in t for w in ("erro", "não ", "nao ", "problema", "lento", "travando",
                            "limite", "caro", "not working", "fix", "issue", "error")):
        return "dores"
    if any(w in t for w in (" vs ", " versus ", " ou ", "alternativa", "melhor que", " or ")):
        return "comparações"
    if any(t.startswith(q) or f" {q} " in t or t.endswith(f" {q}")
           for q in ("como", "por que", "o que", "qual", "quando", "onde", "quanto",
                     "how", "why", "what")):
        return "perguntas"
    if any(w in t for w in ("preço", "preco", "grátis", "gratis", "download", "tutorial",
                            "curso", "planos", "review", "vale a pena", "serve",
                            "free", "pricing")):
        return "intenção"
    return "relacionados"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("seeds", nargs="+")
    ap.add_argument("--lang", default="pt-BR")
    ap.add_argument("--sleep", type=float, default=0.4, help="pausa entre requests (evita rate-limit)")
    ap.add_argument("--no-alpha", action="store_true",
                    help="pula a varredura a-z (mais rápido, menos ruído, foca em dores/perguntas/comparações)")
    ap.add_argument("--out")
    args = ap.parse_args()

    found: dict[str, str] = {}  # termo -> fonte ("google"/"youtube"/"ambos")
    for seed in args.seeds:
        print(f"[suggest] semente: {seed!r}", file=sys.stderr)
        for q in expansions(seed, alpha=not args.no_alpha):
            for yt in (False, True):
                for s in fetch(q, args.lang, yt):
                    s = s.strip()
                    if not s or s == seed:
                        continue
                    src = "youtube" if yt else "google"
                    found[s] = "ambos" if found.get(s, src) != src else src
                time.sleep(args.sleep)

    buckets: dict[str, list[str]] = {k: [] for k in
                                     ["dores", "perguntas", "comparações", "intenção", "relacionados"]}
    for term in sorted(found):
        buckets[categorize(term, args.seeds)].append(term)

    lines = [f"# Termos de busca — {', '.join(args.seeds)}",
             f"\n_{sum(len(v) for v in buckets.values())} termos únicos (Google + YouTube autocomplete, {args.lang})_\n"]
    titles = {"dores": "## Dores (erro / não funciona / limite / caro)",
              "perguntas": "## Perguntas (como / por que / o que)",
              "comparações": "## Comparações (vs / alternativa)",
              "intenção": "## Intenção (preço / grátis / tutorial / vale a pena)",
              "relacionados": "## Relacionados"}
    for k in ["dores", "perguntas", "comparações", "intenção", "relacionados"]:
        if not buckets[k]:
            continue
        lines.append(f"\n{titles[k]}\n")
        for t in buckets[k]:
            tag = {"youtube": " _(YT)_", "ambos": " _(G+YT)_"}.get(found[t], "")
            lines.append(f"- {t}{tag}")
    out = "\n".join(lines) + "\n"

    if args.out:
        with open(args.out, "w") as f:
            f.write(out)
        print(f"[suggest] {sum(len(v) for v in buckets.values())} termos → {args.out}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
