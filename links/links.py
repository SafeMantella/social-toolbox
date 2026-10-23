#!/usr/bin/env python3
"""Consulta rápida do ferramentas.csv. Ex: links.py --uso thumbnail --custo sub | links.py -q upscale --status all"""
import argparse
from pathlib import Path
import pandas as pd

df = pd.read_csv(Path(__file__).with_name("ferramentas.csv"), dtype=str).fillna("")
ap = argparse.ArgumentParser(description=__doc__)
for f in ("categoria", "custo", "uso"):
    ap.add_argument(f"--{f}", help=f"filtra por {f} (valores: ver --valores)")
ap.add_argument("--status", default="agora", help="agora (padrão), depois, recusado ou all")
ap.add_argument("--tag", help="tag exata (coluna tags separada por ;)")
ap.add_argument("-q", help="busca livre em nome/nota/url")
ap.add_argument("--valores", action="store_true", help="lista valores possíveis dos filtros")
ap.add_argument("--csv", action="store_true", help="saída em CSV (pra pipe)")
a = ap.parse_args()

if a.valores:
    for c in ("categoria", "custo", "uso_pipeline", "status"):
        print(f"{c}: {', '.join(sorted(df[c].unique()))}")
    print("tags:", ", ".join(sorted({t for s in df.tags for t in s.split(';') if t})))
    raise SystemExit

m = pd.Series(True, index=df.index)
if a.status != "all": m &= df.status == a.status
if a.categoria: m &= df.categoria == a.categoria
if a.custo: m &= df.custo == a.custo
if a.uso: m &= df.uso_pipeline == a.uso
if a.tag: m &= df.tags.apply(lambda s: a.tag in s.split(";"))
if a.q: m &= df.apply(lambda r: a.q.lower() in " ".join(r[["nome", "nota", "url", "tags"]]).lower(), axis=1)
out = df[m]
if a.csv: print(out.to_csv(index=False), end="")
elif out.empty: print("nada encontrado (tente --status all)")
else:
    for _, r in out.iterrows():
        print(f"{r.nome}  [{r.categoria} | {r.custo} | {r.uso_pipeline} | {r.status}]\n  {r.url}\n  {r.nota}")
