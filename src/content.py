from __future__ import annotations


LESSONS = {
    "1. SELECT e FROM": {
        "title": "Escolha o que deseja enxergar",
        "level": "Fundamentos",
        "analogy": (
            "Imagine uma planilha grande. SELECT escolhe as colunas que você quer "
            "ver e FROM informa em qual planilha os dados estão."
        ),
        "table": "clientes",
        "query": """SELECT cliente_id, nome, cidade, uf
FROM clientes
LIMIT 10;""",
        "question": "Quais são os dez primeiros clientes cadastrados?",
        "tip": "Troque as colunas depois de SELECT e execute novamente.",
    },
    "2. WHERE": {
        "title": "Filtre apenas o que importa",
        "level": "Fundamentos",
        "analogy": (
            "WHERE funciona como o filtro de uma planilha. As linhas que não "
            "atendem à condição ficam fora do resultado."
        ),
        "table": "clientes",
        "query": """SELECT nome, cidade, uf, perfil_investidor
FROM clientes
WHERE uf = 'SP' AND perfil_investidor = 'Moderado'
ORDER BY nome;""",
        "question": "Quais clientes de São Paulo têm perfil moderado?",
        "tip": "Experimente trocar SP por RJ, MG ou PR.",
    },
    "3. ORDER BY e LIMIT": {
        "title": "Organize e reduza o resultado",
        "level": "Fundamentos",
        "analogy": (
            "ORDER BY coloca os valores em ordem. DESC traz os maiores primeiro "
            "e LIMIT define quantas linhas você quer receber."
        ),
        "table": "contas",
        "query": """SELECT conta_id, cliente_id, tipo_conta, saldo
FROM contas
WHERE status = 'Ativa'
ORDER BY saldo DESC
LIMIT 10;""",
        "question": "Quais são as dez contas ativas com maior saldo?",
        "tip": "Troque DESC por ASC para inverter a ordem.",
    },
    "4. GROUP BY": {
        "title": "Transforme linhas em indicadores",
        "level": "Análise",
        "analogy": (
            "GROUP BY cria grupos antes do cálculo. Assim, COUNT conta linhas, "
            "SUM soma valores e AVG calcula médias dentro de cada grupo."
        ),
        "table": "ordens",
        "query": """SELECT lado,
       COUNT(*) AS quantidade_ordens,
       ROUND(AVG(preco * quantidade), 2) AS valor_medio
FROM ordens
WHERE status = 'Executada'
GROUP BY lado
ORDER BY valor_medio DESC;""",
        "question": "Quantas compras e vendas foram executadas e qual o valor médio?",
        "tip": "Toda coluna sem agregação no SELECT deve aparecer no GROUP BY.",
    },
    "5. JOIN": {
        "title": "Conecte tabelas relacionadas",
        "level": "Análise",
        "analogy": (
            "JOIN funciona como uma procura por código. O cliente está em uma "
            "tabela e a conta em outra; o cliente_id conecta as duas."
        ),
        "table": "clientes",
        "query": """SELECT c.nome,
       c.uf,
       ct.tipo_conta,
       ct.saldo
FROM clientes AS c
JOIN contas AS ct ON c.cliente_id = ct.cliente_id
WHERE ct.status = 'Ativa'
ORDER BY ct.saldo DESC
LIMIT 12;""",
        "question": "Quem são os clientes das contas ativas com maior saldo?",
        "tip": "c e ct são apelidos usados para deixar a consulta mais curta.",
    },
    "6. CASE WHEN": {
        "title": "Crie regras de negócio",
        "level": "Análise",
        "analogy": (
            "CASE WHEN representa uma decisão: se uma condição for verdadeira, "
            "use uma categoria; caso contrário, use outra."
        ),
        "table": "contas",
        "query": """SELECT conta_id,
       saldo,
       CASE
           WHEN saldo >= 50000 THEN 'Alta disponibilidade'
           WHEN saldo >= 15000 THEN 'Média disponibilidade'
           ELSE 'Baixa disponibilidade'
       END AS faixa_saldo
FROM contas
WHERE status = 'Ativa'
ORDER BY saldo DESC;""",
        "question": "Como classificar as contas ativas por faixa de saldo?",
        "tip": "A ordem das condições importa: o SQL testa de cima para baixo.",
    },
}


CHALLENGES = [
    {
        "title": "Clientes do Rio de Janeiro",
        "difficulty": "Inicial",
        "prompt": (
            "Mostre nome, cidade e perfil_investidor dos clientes do estado RJ, "
            "ordenados pelo nome."
        ),
        "starter": """SELECT nome, cidade, perfil_investidor
FROM clientes
WHERE
ORDER BY nome;""",
        "solution": """SELECT nome, cidade, perfil_investidor
FROM clientes
WHERE uf = 'RJ'
ORDER BY nome;""",
        "hint": "A condição compara a coluna uf com o texto 'RJ'.",
    },
    {
        "title": "Saldo médio por tipo de conta",
        "difficulty": "Intermediário",
        "prompt": (
            "Calcule o saldo médio das contas ativas por tipo_conta. Nomeie o "
            "cálculo como saldo_medio e arredonde para duas casas."
        ),
        "starter": """SELECT tipo_conta,
       ROUND(AVG(saldo), 2) AS saldo_medio
FROM contas
WHERE status = 'Ativa'
GROUP BY
ORDER BY saldo_medio DESC;""",
        "solution": """SELECT tipo_conta,
       ROUND(AVG(saldo), 2) AS saldo_medio
FROM contas
WHERE status = 'Ativa'
GROUP BY tipo_conta
ORDER BY saldo_medio DESC;""",
        "hint": "O agrupamento deve usar a mesma categoria exibida no SELECT.",
    },
    {
        "title": "Volume negociado por ativo",
        "difficulty": "Avançado",
        "prompt": (
            "Combine ordens e ativos. Para ordens executadas, mostre ticker e a "
            "soma de quantidade * preco como volume_total. Ordene do maior para o menor."
        ),
        "starter": """SELECT a.ticker,
       ROUND(SUM(o.quantidade * o.preco), 2) AS volume_total
FROM ordens AS o
JOIN ativos AS a ON
WHERE o.status = 'Executada'
GROUP BY a.ticker
ORDER BY volume_total DESC;""",
        "solution": """SELECT a.ticker,
       ROUND(SUM(o.quantidade * o.preco), 2) AS volume_total
FROM ordens AS o
JOIN ativos AS a ON o.ativo_id = a.ativo_id
WHERE o.status = 'Executada'
GROUP BY a.ticker
ORDER BY volume_total DESC;""",
        "hint": "As duas tabelas possuem a coluna ativo_id.",
    },
]

