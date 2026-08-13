from pathlib import Path

import pytest

from src.database import create_database
from src.validation import QueryValidationError, execute_query, validate_read_only_query


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


@pytest.mark.parametrize(
    "query",
    [
        "DELETE FROM clientes",
        "UPDATE contas SET saldo = 0",
        "DROP TABLE ordens",
        "CREATE TABLE teste (id INTEGER)",
    ],
)
def test_write_commands_are_blocked(query):
    with pytest.raises(QueryValidationError):
        validate_read_only_query(query)


def test_multiple_statements_are_blocked():
    with pytest.raises(QueryValidationError):
        validate_read_only_query("SELECT * FROM clientes; SELECT * FROM contas;")


def test_select_query_is_executed():
    connection = create_database(DATA_DIR)
    result = execute_query(
        connection,
        "SELECT uf, COUNT(*) AS total FROM clientes GROUP BY uf ORDER BY uf",
    )
    assert list(result.columns) == ["uf", "total"]
    assert result["total"].sum() == 60


def test_comments_do_not_prevent_safe_select():
    query = "-- consulta inicial\nSELECT nome FROM clientes LIMIT 3;"
    assert validate_read_only_query(query).startswith("SELECT")

