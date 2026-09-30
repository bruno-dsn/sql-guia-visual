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


_SQL_PARTS = re.compile(
    r"'(?:''|[^'])*'|\"(?:\"\"|[^\"])*\"|`(?:``|[^`])*`|\[[^\]]*\]|--[^\r\n]*|/\*.*?\*/",
    flags=re.DOTALL,
)


def _without_comments(query: str) -> str:
    # Literais e identificadores citados são preservados integralmente.
    return _SQL_PARTS.sub(
        lambda match: " " if match.group().startswith(("--", "/*")) else match.group(),
        query,
    ).strip()


def validate_read_only_query(query: str) -> str:
    """Aceita uma única consulta SELECT ou WITH e bloqueia alterações no banco."""
    if not isinstance(query, str) or len(query) > 10_000:
        raise QueryValidationError("A consulta deve ter no máximo 10000 caracteres.")
    cleaned = _without_comments(query)
    if not cleaned:
        raise QueryValidationError("Escreva uma consulta antes de executar.")

    masked = _SQL_PARTS.sub(" ", cleaned).strip()
    if masked.endswith(";"):
        cleaned = cleaned.rstrip()[:-1].rstrip()
        masked = masked[:-1].rstrip()
    if ";" in masked:
        raise QueryValidationError("Execute apenas uma consulta por vez.")

    statement = cleaned
    first_word = re.match(r"^[A-Za-z]+", masked)
    if not first_word or first_word.group(0).lower() not in {"select", "with"}:
        raise QueryValidationError("O laboratório aceita apenas consultas SELECT ou WITH.")

    words = set(re.findall(r"\b[A-Za-z_]+\b", masked.lower()))
    blocked = sorted(words.intersection(FORBIDDEN_WORDS))
    if blocked:
        raise QueryValidationError(
            "Comando bloqueado no modo de aprendizagem: " + ", ".join(blocked)
        )

    return statement


def execute_query(
    connection: sqlite3.Connection, query: str, max_rows: int = 500,
    max_operations: int = 1_000_000,
) -> pd.DataFrame:
    statement = validate_read_only_query(query)
    if not isinstance(max_rows, int) or isinstance(max_rows, bool) or not 1 <= max_rows <= 10_000:
        raise QueryValidationError("O limite de linhas deve ficar entre 1 e 10000.")
    if not isinstance(max_operations, int) or isinstance(max_operations, bool) or max_operations < 1:
        raise QueryValidationError("O limite de operações deve ser positivo.")
    # Limitar a execução e a leitura evita materializar toda a consulta em memória.
    calls = 0
    def progress():
        nonlocal calls
        calls += 100
        return int(calls >= max_operations)
    allowed = {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION,
               sqlite3.SQLITE_RECURSIVE}
    def authorize(action, arg1, arg2, database, trigger):
        if action not in allowed:
            return sqlite3.SQLITE_DENY
        if action == sqlite3.SQLITE_FUNCTION and str(arg2 or arg1).lower() in {
            'load_extension', 'readfile', 'writefile'
        }:
            return sqlite3.SQLITE_DENY
        return sqlite3.SQLITE_OK
    cursor = None
    previous_length = connection.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 1_000_000)
    connection.set_progress_handler(progress, 100)
    connection.set_authorizer(authorize)
    try:
        cursor = connection.execute(statement)
        columns = [column[0] for column in cursor.description]
        return pd.DataFrame.from_records(cursor.fetchmany(max_rows), columns=columns)
    except sqlite3.DatabaseError as error:
        if 'interrupted' in str(error).lower():
            raise QueryValidationError("A consulta excedeu o limite de operações.") from error
        raise QueryValidationError(f"Consulta não executada: {error}") from error
    finally:
        if cursor is not None:
            cursor.close()
        connection.set_progress_handler(None, 0)
        connection.set_authorizer(None)
        connection.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, previous_length)


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
