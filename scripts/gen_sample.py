import csv, random, datetime

random.seed(42)

produtos = [
    ("Notebook Gamer X15", "Eletrônicos", 4899.90),
    ("Mouse Sem Fio Pro", "Eletrônicos", 129.90),
    ("Teclado Mecânico RGB", "Eletrônicos", 349.90),
    ("Monitor 27\" 4K", "Eletrônicos", 1899.00),
    ("Fone Bluetooth ANC", "Eletrônicos", 599.00),
    ("Cadeira Ergonômica", "Móveis", 1299.00),
    ("Mesa Escritório Compacta", "Móveis", 799.00),
    ("Luminária LED Articulada", "Móveis", 149.90),
    ("Câmera Web Full HD", "Eletrônicos", 259.90),
    ("SSD NVMe 1TB", "Eletrônicos", 449.90),
    ("Power Bank 20000mAh", "Acessórios", 179.90),
    ("Mochila para Notebook", "Acessórios", 219.90),
    ("Suporte para Monitor", "Acessórios", 129.00),
    ("Hub USB-C 7 em 1", "Acessórios", 189.90),
    ("Impressora Multifuncional", "Eletrônicos", 899.00),
]

clientes = [
    "Ana Beatriz Souza", "Carlos Eduardo Lima", "Fernanda Alves", "João Pedro Costa",
    "Mariana Rocha", "Rafael Menezes", "Juliana Ferreira", "Lucas Andrade",
    "Patrícia Gomes", "Bruno Cardoso", "Camila Nogueira", "Diego Santos",
    "Larissa Martins", "Thiago Barbosa", "Gabriela Pereira", "Rodrigo Teixeira",
    "Beatriz Ramos", "Felipe Araújo", "Vanessa Correia", "Eduardo Machado",
]

cidades = [
    ("Recife", "PE"), ("São Paulo", "SP"), ("Rio de Janeiro", "RJ"),
    ("Salvador", "BA"), ("Fortaleza", "CE"), ("Belo Horizonte", "MG"),
    ("Curitiba", "PR"), ("Porto Alegre", "RS"), ("Olinda", "PE"),
    ("Natal", "RN"), ("João Pessoa", "PB"), ("Brasília", "DF"),
]

canais = ["Site", "App", "Marketplace", "Loja Física"]

start = datetime.date(2026, 5, 1)
rows = []
sale_id = 1000
for i in range(320):
    dia = start + datetime.timedelta(days=random.randint(0, 99))
    produto, categoria, preco = random.choice(produtos)
    qtd = random.choices([1, 2, 3, 4], weights=[60, 25, 10, 5])[0]
    cliente = random.choice(clientes)
    cidade, uf = random.choice(cidades)
    canal = random.choice(canais)
    desconto = random.choices([0, 0.05, 0.10], weights=[70, 20, 10])[0]
    valor_unit = round(preco * (1 - desconto), 2)
    valor_total = round(valor_unit * qtd, 2)
    sale_id += 1
    rows.append([
        f"V{sale_id}", dia.isoformat(), cliente, cidade, uf, produto, categoria,
        qtd, valor_unit, valor_total, canal
    ])

rows.sort(key=lambda r: r[1])

with open("sample-data/vendas_exemplo.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id_venda", "data", "cliente", "cidade", "uf", "produto", "categoria",
                "quantidade", "valor_unitario", "valor_total", "canal"])
    w.writerows(rows)

print(f"Gerado {len(rows)} registros")
