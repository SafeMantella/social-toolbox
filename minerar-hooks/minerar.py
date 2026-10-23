#!/usr/bin/env python3
"""Minera um CSV de hooks reais (EN + PT-BR): ranqueia, classifica nas famílias do swipe-openers e conta power words.

Metade MECÂNICA do hook-mining (adaptado de Ootto-AI/claude-content-skills, MIT). O remix (trocar só
as power words, manter a estrutura) é trabalho do Claude, em PT-BR — ver README.md.

  python minerar.py hooks.csv [--top 40] [--out dir]
  python minerar.py --selftest
"""
import csv, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

# famílias = tabela "Padrões que ranqueiam" de referencia/swipe-openers.md (ordem = prioridade do match)
PATTERNS = [
    ("results-first",  r"^\bi\b.*\b(made|built|got|cut|grew|went from|turned)\b|\b\d[\d,.]*\s?((k|m|gb|ram|x|views|followers)\b|%|\$)|\b(cortei|fiz|construí|ganhei|reduzi|passei de)\b|\bR\$\s?\d"),
    ("list-tease",     r"^\d+\s+\w+|\b(these|top|exactly|only)\s+\d+\b|^(\d+|tr[eê]s|cinco|quatro|dois)\s+(coisas|configs|erros|formas|jeitos)|\b\d+\s+(coisas|configs|erros|formas|jeitos)\b"),
    ("contrarian",     r"\b(wrong|lie|dead|dying|overrated)\b|\bstop\s+\w+ing\b|\bnobody\b|\b(errado|mentira|morreu|morrendo|superestimado)\b|\bpare de\b|\bninguém\b|\bn[aã]o (deixa|faz|precisa)\b.*\b(mais|nem)\b"),
    ("mistake-warning", r"\b(mistake|don'?t|never|avoid|warning|before you|dumber|wasting)\b|\b(erro|não faça|nunca|cuidado|antes de|jogando fora|burra)\b"),
    ("confession",     r"^\bi\b.*\b(wrong|mistake|wasted|failed|lied)\b|\b(usei|errei|perdi|gastei|descobri que eu)\b"),
    ("identity-call",  r"\bif you\b.*\b(use|are|want|have)\b|\bthis is for you\b|^\bse (você|vc)\b|\bé pra você\b|\bpra quem\b"),
    ("pov",            r"^\bpov\b|^\bpov:"),
    ("open-loop",      r"\b(secret|hidden|quietly|ridiculous|here'?s why)\b|\bwait\b|\buntil\b|\b(segredo|escondido|descobri|ridícul[ao]|o motivo)\b"),
    ("direct-question", r"\?\s*$|^\b(what|why|how|who|can|do|did|is|are|should)\b|^\b(o que|por que|como|quem|será)\b"),
    ("newsjack",       r"\bjust\s+(shipped|dropped|launched|released|built)\b|\b(acabou de|acaba de|lançou|saiu)\b"),
]

# carga emocional — só isto pode ser trocado num remix
POWER = {
    "free","secret","hidden","actually","literally","nobody","crazy","insane","hack","brutal","exact","stop","never",
    "worst","best","broken","dead","dying","killing","ruining","lie","mistake","only","quietly","dumber","wild","truth","real",
    "grátis","gratis","segredo","escondido","ninguém","absurdo","insano","brutal","exato","pare","nunca","pior","melhor",
    "quebrado","morreu","morrendo","mentira","erro","só","apenas","burra","verdade","real","ridículo","ridiculo",
}

def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip())

def pick_col(fields, wants, avoid=()):
    best, score = None, 0
    for f in fields or []:
        low = (f or "").lower()
        if any(a in low for a in avoid):
            continue
        s = sum(2 if w == low else 1 for w in wants if w in low)
        if s > score:
            best, score = f, s
    return best

def to_num(v):
    v = re.sub(r"[^\d.kmKM]", "", str(v or "").replace(",", "."))
    if not v:
        return 0.0
    mult = 1_000_000 if v[-1] in "mM" else 1_000 if v[-1] in "kK" else 1
    try:
        return float(re.sub(r"[kmKM]", "", v)) * mult
    except ValueError:
        return 0.0

def pattern_of(hook):
    h = (hook or "").lower()
    for name, rx in PATTERNS:
        if re.search(rx, h):
            return name
    return "outro"

def power_words(hook):
    return sorted({w for w in re.findall(r"[\wáàâãéêíóôõúç']+", (hook or "").lower()) if w in POWER})

def mine(rows, fields, top=None):
    hcol = pick_col(fields, ["hook", "opener", "gancho", "title", "caption", "text", "headline"], avoid=("url", "link", "id"))
    pcol = pick_col(fields, ["view", "play", "visualiza", "score", "like", "curtida", "engagement", "reach"])
    # views não são comparáveis entre contas/plataformas → ranqueia por percentil dentro da fonte
    scol = pick_col(fields, ["source", "fonte", "author", "autor", "user", "perfil", "platform", "plataforma", "channel", "canal"], avoid=("url", "link", "id"))
    out = []
    for r in rows:
        hook = norm(r.get(hcol) if hcol else "")
        if len(hook) < 8:
            continue
        out.append({"hook": hook, "views": to_num(r.get(pcol)) if pcol else 0.0, "fonte": norm(r.get(scol)) if scol else "",
                    "pattern": pattern_of(hook), "power_words": power_words(hook), "words": len(hook.split())})
    groups = defaultdict(list)
    for h in out:
        groups[h["fonte"]].append(h)
    for g in groups.values():
        g.sort(key=lambda d: d["views"])
        for i, h in enumerate(g):
            h["score"] = round((i + 1) / len(g), 3)  # 1.0 = melhor da fonte
    out.sort(key=lambda d: (-d["score"], -d["views"]))
    if top:
        out = out[:top]
    buckets = defaultdict(list)
    por_fonte = defaultdict(lambda: defaultdict(list))
    for h in out:
        buckets[h["pattern"]].append(h)
        por_fonte[h["fonte"]][h["pattern"]].append(h)
    return {"hook_column": hcol, "metric_column": pcol, "source_column": scol, "total": len(out),
            "avg_words": round(sum(h["words"] for h in out) / max(len(out), 1), 1),
            "buckets": dict(sorted(buckets.items(), key=lambda kv: -len(kv[1]))),
            "por_fonte": {f: dict(sorted(b.items(), key=lambda kv: -len(kv[1]))) for f, b in por_fonte.items()},
            "power_word_frequency": Counter(w for h in out for w in h["power_words"]).most_common(20)}

def selftest():
    fields = ["Video URL", "Autor", "Hook Text", "Views"]
    rows = [
        {"Hook Text": "How I got 64,000 views with one reel", "Views": "64.8k", "Autor": "a", "Video URL": "x"},
        {"Hook Text": "You're using Claude wrong", "Views": "12000", "Autor": "a", "Video URL": "x"},
        {"Hook Text": "5 skills nobody is using", "Views": "3.1M", "Autor": "b", "Video URL": "x"},
        {"Hook Text": "Cortei meu gasto de API pela metade", "Views": "900", "Autor": "b", "Video URL": "x"},
        {"Hook Text": "Prompt gigante deixa a IA mais burra", "Views": "50", "Autor": "b", "Video URL": "x"},
        {"Hook Text": "curto", "Views": "5", "Autor": "b", "Video URL": "x"},  # < 8 chars → descartado
    ]
    r = mine(rows, fields)
    assert (r["hook_column"], r["metric_column"], r["source_column"]) == ("Hook Text", "Views", "Autor"), r
    assert r["total"] == 5, r["total"]
    assert set(r["por_fonte"]) == {"a", "b"}, r["por_fonte"].keys()
    first = next(iter(r["buckets"].values()))[0]
    assert first["score"] == 1.0
    assert pattern_of("Cortei meu gasto de API pela metade") == "results-first"
    assert pattern_of("5 skills nobody is using") == "list-tease"
    assert pattern_of("You're using Claude wrong") == "contrarian"
    assert pattern_of("explained in 5min") == "outro"  # 5m(in) não é número de resultado
    assert pattern_of("POV: a IA te entrega 200 linhas") == "pov"
    assert pattern_of("Seu agente trava em tarefa longa?") == "direct-question"
    assert pattern_of("Claude just shipped a new model") == "newsjack"
    assert "nobody" in power_words("5 skills nobody is using") and "burra" in power_words("IA mais burra")
    assert to_num("3.1M") == 3_100_000 and to_num("64.8k") == 64_800
    print("selftest OK")

def main():
    if "--selftest" in sys.argv:
        return selftest()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__); sys.exit(1)
    top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else None
    src = Path(args[0])
    outdir = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else src.parent
    with src.open(newline="", encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        res = mine(list(rd), rd.fieldnames, top)
    out = outdir / (src.stem + ".mined.json")
    out.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"hook: {res['hook_column']} | métrica: {res['metric_column']} | fonte: {res['source_column']} | {res['total']} hooks, média {res['avg_words']} palavras\n")
    for fonte, bs in res["por_fonte"].items():  # fontes não se misturam: título (embalagem) ≠ fala (gancho)
        print(f"[{fonte or 'sem fonte'}]")
        for name, hooks in bs.items():
            print(f"  {name:16s} {len(hooks):3d}   ex: {hooks[0]['hook'][:70]!r}")
    print(f"\npower words: {', '.join(w for w, _ in res['power_word_frequency'][:12])}\n→ {out}")

if __name__ == "__main__":
    main()
