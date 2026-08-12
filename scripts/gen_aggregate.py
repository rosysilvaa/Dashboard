import csv, json
from collections import defaultdict

with open("sample-data/vendas_exemplo.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

total_vendas = len(rows)
faturamento = round(sum(float(r["valor_total"]) for r in rows), 2)
ticket_medio = round(faturamento / total_vendas, 2)

por_produto = defaultdict(lambda: {"quantidade": 0, "receita": 0.0})
por_cidade = defaultdict(lambda: {"vendas": 0, "receita": 0.0})
por_cliente = defaultdict(lambda: {"compras": 0, "receita": 0.0})
por_categoria = defaultdict(lambda: {"receita": 0.0})
por_canal = defaultdict(lambda: {"vendas": 0, "receita": 0.0})
por_dia = defaultdict(lambda: {"vendas": 0, "receita": 0.0})

for r in rows:
    v = float(r["valor_total"])
    por_produto[r["produto"]]["quantidade"] += int(r["quantidade"])
    por_produto[r["produto"]]["receita"] += v
    cidade_key = f'{r["cidade"]}/{r["uf"]}'
    por_cidade[cidade_key]["vendas"] += 1
    por_cidade[cidade_key]["receita"] += v
    por_cliente[r["cliente"]]["compras"] += 1
    por_cliente[r["cliente"]]["receita"] += v
    por_categoria[r["categoria"]]["receita"] += v
    por_canal[r["canal"]]["vendas"] += 1
    por_canal[r["canal"]]["receita"] += v
    por_dia[r["data"]]["vendas"] += 1
    por_dia[r["data"]]["receita"] += v

def top(d, key="receita", n=None):
    items = sorted(d.items(), key=lambda kv: kv[1][key], reverse=True)
    return items[:n] if n else items

produtos_top = [
    {"produto": k, "quantidade": v["quantidade"], "receita": round(v["receita"], 2)}
    for k, v in top(por_produto, "receita", 6)
]
cidades_top = [
    {"cidade": k, "vendas": v["vendas"], "receita": round(v["receita"], 2)}
    for k, v in top(por_cidade, "receita", 8)
]
clientes_top = [
    {"cliente": k, "compras": v["compras"], "receita": round(v["receita"], 2)}
    for k, v in top(por_cliente, "receita", 6)
]
categorias = [
    {"categoria": k, "receita": round(v["receita"], 2)}
    for k, v in top(por_categoria, "receita")
]
canais = [
    {"canal": k, "vendas": v["vendas"], "receita": round(v["receita"], 2)}
    for k, v in top(por_canal, "receita")
]
serie_diaria = [
    {"data": k, "vendas": v["vendas"], "receita": round(v["receita"], 2)}
    for k, v in sorted(por_dia.items())
]

output = {
    "resumo": {
        "totalVendas": total_vendas,
        "faturamento": faturamento,
        "ticketMedio": ticket_medio,
        "totalClientes": len(por_cliente),
        "totalCidades": len(por_cidade),
    },
    "produtosMaisVendidos": produtos_top,
    "vendasPorCidade": cidades_top,
    "topClientes": clientes_top,
    "vendasPorCategoria": categorias,
    "vendasPorCanal": canais,
    "serieDiaria": serie_diaria,
}

with open("dashboard/dados_demo.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(json.dumps(output["resumo"], ensure_ascii=False, indent=2))
