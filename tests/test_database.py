from pathlib import Path

from src.database import create_database, list_tables, table_columns, table_preview


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def test_database_contains_expected_tables():
    connection = create_database(DATA_DIR)
    assert list_tables(connection) == ["ativos", "clientes", "contas", "ordens"]


def test_table_preview_respects_limit():
    connection = create_database(DATA_DIR)
    preview = table_preview(connection, "clientes", 5)
    assert len(preview) == 5
    assert "cliente_id" in preview.columns


def test_orders_have_relationship_columns():
    connection = create_database(DATA_DIR)
    columns = table_columns(connection, "ordens")
    assert "conta_id" in columns
    assert "ativo_id" in columns

