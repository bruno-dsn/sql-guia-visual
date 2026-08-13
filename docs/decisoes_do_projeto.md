# Decisões do projeto

## Público

O aplicativo foi desenhado para pessoas que nunca consultaram um banco de
dados. Cada aula parte de uma pergunta, apresenta a tabela de origem, traduz as
cláusulas e exibe o resultado.

## SQLite em memória

O SQLite foi escolhido porque faz parte da biblioteca padrão do Python e não
exige servidor. Os CSVs são carregados em memória quando a aplicação começa.
Isso facilita a publicação no Streamlit Community Cloud e mantém a instalação
local simples.

## Consultas somente para leitura

O playground aceita uma única consulta iniciada por `SELECT` ou `WITH`. Comandos
que modificam tabelas são bloqueados. Essa decisão evita perda de dados e mantém
o ambiente previsível para iniciantes.

## Correção pelo resultado

Os desafios não exigem que o aluno copie uma consulta específica. A resposta é
executada e comparada ao resultado esperado. Duas consultas diferentes podem
ser aceitas quando retornam os mesmos dados na mesma estrutura e ordem.

## Dados sintéticos

Clientes, contas, ativos, preços e ordens são fictícios. O cenário brasileiro
foi escolhido para tornar exemplos de saldo, estado, perfil e investimento mais
familiares. O projeto não reproduz dados, regras ou sistemas internos da B3 nem
de qualquer instituição financeira.

## Escopo deliberado

O laboratório cobre fundamentos de consulta: `SELECT`, `FROM`, `WHERE`,
`ORDER BY`, `LIMIT`, agregações, `GROUP BY`, `JOIN` e `CASE WHEN`. Comandos de
administração de banco e escrita de dados ficaram fora do escopo inicial.

