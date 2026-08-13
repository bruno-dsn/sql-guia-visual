from __future__ import annotations

import re


CLAUSE_EXPLANATIONS = {
    "WITH": "Cria um resultado temporário para organizar uma consulta maior.",
    "SELECT": "Escolhe quais colunas ou cálculos aparecerão no resultado.",
    "FROM": "Indica a tabela onde a busca começa.",
    "JOIN": "Combina informações que estão em tabelas diferentes.",
    "ON": "Define como as linhas das tabelas se relacionam.",
    "WHERE": "Mantém somente as linhas que atendem a uma condição.",
    "GROUP BY": "Reúne linhas com o mesmo valor para criar resumos.",
    "HAVING": "Filtra grupos depois que os cálculos foram feitos.",
    "ORDER BY": "Organiza o resultado em ordem crescente ou decrescente.",
    "LIMIT": "Restringe quantas linhas serão exibidas.",
    "CASE": "Cria categorias ou regras condicionais dentro da consulta.",
}


def explain_query(query: str) -> list[dict[str, str]]:
    """Traduz as cláusulas mais comuns de SQL na ordem em que aparecem."""
    normalized = re.sub(r"\s+", " ", query.strip())
    if not normalized:
        return []

    matches: list[tuple[int, str]] = []
    for clause in CLAUSE_EXPLANATIONS:
        pattern = r"\b" + re.escape(clause).replace(r"\ ", r"\s+") + r"\b"
        match = re.search(pattern, normalized, flags=re.IGNORECASE)
        if match:
            matches.append((match.start(), clause))

    matches.sort()
    explanations = []
    for index, (start, clause) in enumerate(matches):
        end = matches[index + 1][0] if index + 1 < len(matches) else len(normalized)
        fragment = normalized[start:end].strip()
        explanations.append(
            {
                "clause": clause,
                "fragment": fragment,
                "meaning": CLAUSE_EXPLANATIONS[clause],
            }
        )
    return explanations

