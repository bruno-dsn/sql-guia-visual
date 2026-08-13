from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path


SEED = 42
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

FIRST_NAMES = [
    "Ana", "Beatriz", "Bruno", "Caio", "Camila", "Carlos", "Clara", "Daniel",
    "Eduarda", "Felipe", "Fernanda", "Gabriel", "Helena", "Igor", "Isabela",
    "João", "Juliana", "Larissa", "Leonardo", "Lucas", "Mariana", "Marcos",
    "Nathalia", "Paulo", "Rafael", "Renata", "Roberto", "Sofia", "Thiago", "Vitória",
]

LAST_NAMES = [
    "Almeida", "Barbosa", "Cardoso", "Costa", "Dias", "Ferreira", "Gomes",
    "Lima", "Martins", "Mendes", "Moreira", "Nascimento", "Oliveira", "Pereira",
    "Ramos", "Rocha", "Rodrigues", "Santos", "Silva", "Souza",
]

CITIES = [
    ("São Paulo", "SP"), ("Campinas", "SP"), ("Santos", "SP"),
    ("Rio de Janeiro", "RJ"), ("Niterói", "RJ"),
    ("Belo Horizonte", "MG"), ("Uberlândia", "MG"),
    ("Curitiba", "PR"), ("Londrina", "PR"),
    ("Porto Alegre", "RS"), ("Florianópolis", "SC"),
    ("Salvador", "BA"), ("Recife", "PE"), ("Brasília", "DF"),
]

ASSETS = [
    (1, "LABA3", "Laboratórios Aurora", "Ação", "Saúde", 27.40),
    (2, "SOLR3", "Energia Solar Sul", "Ação", "Energia", 18.75),
    (3, "HORA4", "Banco Horizonte", "Ação", "Financeiro", 31.20),
    (4, "VIVA3", "Viva Varejo", "Ação", "Consumo", 12.85),
    (5, "TECA3", "Tecnologia Atlântico", "Ação", "Tecnologia", 44.10),
    (6, "MOBI3", "Mobilidade Brasil", "Ação", "Transportes", 21.35),
    (7, "FLOG11", "Fundo Logística Central", "FII", "Logística", 96.30),
    (8, "FCOM11", "Fundo Comercial Urbano", "FII", "Imobiliário", 82.60),
    (9, "FCRI11", "Fundo Recebíveis Brasil", "FII", "Recebíveis", 101.20),
    (10, "RFIX1", "Renda Fixa Curta", "Renda fixa", "Pós-fixado", 100.00),
    (11, "IPCA1", "Tesouro Inflação", "Renda fixa", "Inflação", 128.50),
    (12, "DOLA1", "Fundo Cambial", "Fundo", "Câmbio", 54.80),
]


def write_csv(file_name: str, fieldnames: list[str], rows: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with (DATA_DIR / file_name).open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_clients(rng: random.Random) -> list[dict]:
    rows = []
    used_names: set[str] = set()
    start = date(2022, 1, 10)

    for client_id in range(1, 61):
        while True:
            name = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
            if name not in used_names:
                used_names.add(name)
                break
        city, state = rng.choice(CITIES)
        rows.append(
            {
                "cliente_id": client_id,
                "nome": name,
                "cidade": city,
                "uf": state,
                "perfil_investidor": rng.choices(
                    ["Conservador", "Moderado", "Arrojado"], weights=[38, 42, 20]
                )[0],
                "data_cadastro": (start + timedelta(days=rng.randint(0, 1500))).isoformat(),
            }
        )
    return rows


def generate_accounts(rng: random.Random, clients: list[dict]) -> list[dict]:
    rows = []
    account_id = 1001
    for client in clients:
        number_of_accounts = 2 if rng.random() < 0.25 else 1
        for position in range(number_of_accounts):
            account_type = "Investimentos" if position == 0 else rng.choice(["Digital", "Previdência"])
            rows.append(
                {
                    "conta_id": account_id,
                    "cliente_id": client["cliente_id"],
                    "tipo_conta": account_type,
                    "saldo": round(rng.triangular(800, 120000, 18000), 2),
                    "status": rng.choices(["Ativa", "Inativa"], weights=[91, 9])[0],
                }
            )
            account_id += 1
    return rows


def generate_assets() -> list[dict]:
    return [
        {
            "ativo_id": asset_id,
            "ticker": ticker,
            "nome_ativo": name,
            "tipo_ativo": asset_type,
            "setor": sector,
        }
        for asset_id, ticker, name, asset_type, sector, _ in ASSETS
    ]


def generate_orders(rng: random.Random, accounts: list[dict]) -> list[dict]:
    rows = []
    start = date(2025, 1, 2)
    active_accounts = [row for row in accounts if row["status"] == "Ativa"]

    for order_id in range(1, 521):
        account = rng.choice(active_accounts)
        asset_id, _, _, asset_type, _, base_price = rng.choice(ASSETS)
        quantity = rng.randint(1, 40) if asset_type in {"Ação", "FII"} else rng.randint(1, 12)
        rows.append(
            {
                "ordem_id": order_id,
                "conta_id": account["conta_id"],
                "ativo_id": asset_id,
                "lado": rng.choice(["Compra", "Venda"]),
                "quantidade": quantity,
                "preco": round(base_price * rng.uniform(0.86, 1.14), 2),
                "data_ordem": (start + timedelta(days=rng.randint(0, 570))).isoformat(),
                "status": rng.choices(
                    ["Executada", "Cancelada", "Pendente"], weights=[84, 10, 6]
                )[0],
            }
        )
    return rows


def main() -> None:
    rng = random.Random(SEED)
    clients = generate_clients(rng)
    accounts = generate_accounts(rng, clients)
    assets = generate_assets()
    orders = generate_orders(rng, accounts)

    write_csv(
        "clientes.csv",
        ["cliente_id", "nome", "cidade", "uf", "perfil_investidor", "data_cadastro"],
        clients,
    )
    write_csv(
        "contas.csv",
        ["conta_id", "cliente_id", "tipo_conta", "saldo", "status"],
        accounts,
    )
    write_csv(
        "ativos.csv",
        ["ativo_id", "ticker", "nome_ativo", "tipo_ativo", "setor"],
        assets,
    )
    write_csv(
        "ordens.csv",
        ["ordem_id", "conta_id", "ativo_id", "lado", "quantidade", "preco", "data_ordem", "status"],
        orders,
    )

    print(
        f"Dados gerados: {len(clients)} clientes, {len(accounts)} contas, "
        f"{len(assets)} ativos e {len(orders)} ordens."
    )


if __name__ == "__main__":
    main()

