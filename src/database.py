from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


TABLE_FILES = {
    "clientes": "clientes.csv",
    "contas": "contas.csv",
    "ativos": "ativos.csv",
    "ordens": "ordens.csv",
}


def create_database(data_dir: str | Path) -> sqlite3.Connection:
    """Cria um banco SQLite em memória a partir dos CSVs do projeto."""
    data_path = Path(data_dir)
    connection = sqlite3.connect(":memory:", check_same_thread=False)

    for table_name, file_name in TABLE_FILES.items():
        frame = pd.read_csv(data_path / file_name)
        frame.to_sql(table_name, connection, index=False, if_exists="replace")

    return connection


def list_tables(connection: sqlite3.Connection) -> list[str]:
    query = "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
    rows = connection.execute(query).fetchall()
    return [row[0] for row in rows]


def table_columns(connection: sqlite3.Connection, table_name: str) -> list[str]:
    if table_name not in list_tables(connection):
        raise ValueError(f"Tabela desconhecida: {table_name}")
    rows = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    return [row[1] for row in rows]


def table_preview(
    connection: sqlite3.Connection, table_name: str, limit: int = 8
) -> pd.DataFrame:
    if table_name not in list_tables(connection):
        raise ValueError(f"Tabela desconhecida: {table_name}")
    safe_limit = max(1, min(int(limit), 100))
    return pd.read_sql_query(
        f"SELECT * FROM {table_name} LIMIT {safe_limit}", connection
    )

