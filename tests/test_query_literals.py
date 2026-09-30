import pandas as pd
import pytest
import sqlite3

from src.validation import execute_query, validate_read_only_query, QueryValidationError


@pytest.mark.parametrize('texto', ['drop', 'update', 'a;b', 'antes--depois', '/* literal */'])
def test_palavras_e_pontuacao_em_literal_sao_dados(texto):
    with sqlite3.connect(':memory:') as con:
        result = execute_query(con, f"SELECT '{texto}' AS texto;")
    assert result.loc[0, 'texto'] == texto


def test_comentario_nao_oculta_segundo_comando():
    with pytest.raises(QueryValidationError):
        validate_read_only_query('SELECT 1; -- comentário\nDROP TABLE clientes')


def test_limite_de_linhas_e_query_longa():
    with sqlite3.connect(':memory:') as con:
        result = execute_query(con, 'WITH RECURSIVE n(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM n WHERE x<10000) SELECT x FROM n', max_rows=7)
    assert len(result) == 7


def test_limite_de_operacoes_interrompe_recursao_sem_fim():
    with sqlite3.connect(':memory:') as con:
        with pytest.raises(QueryValidationError, match='limite'):
            execute_query(con, 'WITH RECURSIVE n(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM n) SELECT sum(x) FROM n', max_operations=1000)
        assert execute_query(con, 'SELECT 1').iloc[0, 0] == 1


def test_limite_de_celula_e_restaurado_apos_erro():
    with sqlite3.connect(':memory:') as con:
        original = con.getlimit(sqlite3.SQLITE_LIMIT_LENGTH)
        with pytest.raises(QueryValidationError):
            execute_query(con, 'SELECT zeroblob(1000001)')
        assert con.getlimit(sqlite3.SQLITE_LIMIT_LENGTH) == original
        assert execute_query(con, 'SELECT 1').iloc[0, 0] == 1


def test_query_muito_longa_e_rejeitada():
    with pytest.raises(QueryValidationError, match='10000'):
        validate_read_only_query('SELECT 1' + ' ' * 10000)
