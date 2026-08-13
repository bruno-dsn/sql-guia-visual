from __future__ import annotations

import re
import sqlite3

import pandas as pd


FORBIDDEN_WORDS = {
    "alter",
    "attach",
    "create",
    "delete",
    "detach",
    "drop",
    "insert",
    "pragma",
    "reindex",
    "replace",
    "truncate",
    "update",
    "vacuum",
}


class QueryValidationError(ValueError):
    """Erro apresentado quando uma consulta não é segura para o laboratório."""


def _without_comments(query: str) -> str:
    query = re.sub(r"/\*.*?\*/", " ", query, flags=re.DOTALL)
    query = re.sub(r"--.*?$", " ", query, flags=re.MULTILINE)
    return query.strip()


def validate_read_only_query(query: str) -> str:
    """Aceita uma única consulta SELECT ou WITH e bloqueia alterações no banco."""
    cleaned = _without_comments(query)
    if not cleaned:
        raise QueryValidationError("Escreva uma consulta antes de executar.")

    statements = [part.strip() for part in cleaned.split(";") if part.strip()]
    if len(statements) != 1:
        raise QueryValidationError("Execute apenas uma consulta por vez.")

    statement = statements[0]
    first_word = re.match(r"^[A-Za-z]+", statement)
    if not first_word or first_word.group(0).lower() not in {"select", "with"}:
        raise QueryValidationError("O laboratório aceita apenas consultas SELECT ou WITH.")

    words = set(re.findall(r"\b[A-Za-z_]+\b", statement.lower()))
    blocked = sorted(words.intersection(FORBIDDEN_WORDS))
    if blocked:
        raise QueryValidationError(
            "Comando bloqueado no modo de aprendizagem: " + ", ".join(blocked)
        )

    return statement


def execute_query(
    connection: sqlite3.Connection, query: str, max_rows: int = 500
) -> pd.DataFrame:
    statement = validate_read_only_query(query)
    frame = pd.read_sql_query(statement, connection)
    return frame.head(max_rows)


def same_result(actual: pd.DataFrame, expected: pd.DataFrame) -> bool:
    """Compara resultados ignorando apenas o índice do pandas."""
    if list(actual.columns) != list(expected.columns):
        return False
    try:
        pd.testing.assert_frame_equal(
            actual.reset_index(drop=True),
            expected.reset_index(drop=True),
            check_dtype=False,
        )
    except AssertionError:
        return False
    return True

