from pathlib import Path

from src.content import CHALLENGES, LESSONS
from src.database import create_database
from src.explainer import explain_query
from src.validation import execute_query, same_result


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def test_every_lesson_query_runs():
    connection = create_database(DATA_DIR)
    for lesson in LESSONS.values():
        result = execute_query(connection, lesson["query"])
        assert not result.empty


def test_every_challenge_solution_runs():
    connection = create_database(DATA_DIR)
    for challenge in CHALLENGES:
        result = execute_query(connection, challenge["solution"])
        assert not result.empty


def test_explainer_preserves_query_order():
    query = "SELECT nome FROM clientes WHERE uf = 'SP' ORDER BY nome LIMIT 5"
    clauses = [item["clause"] for item in explain_query(query)]
    assert clauses == ["SELECT", "FROM", "WHERE", "ORDER BY", "LIMIT"]


def test_result_comparison_accepts_identical_frames():
    connection = create_database(DATA_DIR)
    first = execute_query(connection, "SELECT nome FROM clientes ORDER BY nome LIMIT 3")
    second = execute_query(connection, "SELECT nome FROM clientes ORDER BY nome LIMIT 3")
    assert same_result(first, second)

