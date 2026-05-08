# ✈️ SQL no Aeroporto de Dados

> Um guia visual e interativo de SQL para iniciantes, usando um sistema de voos como exemplo prático do mundo real.

<br>

![SQL Badge](https://img.shields.io/badge/SQL-Guia%20Visual-1a6bdc?style=for-the-badge&logo=postgresql&logoColor=white)
![Level Badge](https://img.shields.io/badge/Nível-Iniciante-1d9e75?style=for-the-badge)
![HTML Badge](https://img.shields.io/badge/Formato-HTML%20Interativo-ef9f27?style=for-the-badge&logo=html5&logoColor=white)
![License Badge](https://img.shields.io/badge/Licença-MIT-7f77dd?style=for-the-badge)

<br>

## 📌 Sobre o projeto

Este repositório contém um **guia visual e interativo de SQL**, criado para quem está começando na área de dados e quer entender os comandos mais importantes de forma clara, prática e memorável.

A ideia surgiu de uma observação simples: a maioria dos materiais de SQL para iniciantes é muito técnica, cheia de jargão e sem contexto do mundo real. Este guia resolve isso usando uma **analogia com um aeroporto** — cada comando SQL é explicado como uma ferramenta que um controlador de tráfego aéreo usaria para gerenciar voos, passageiros e companhias aéreas.

> **"SQL não é só código. É lógica — e lógica se aprende com bons exemplos."**

<br>

## 🎯 Para quem é este guia?

| Perfil | Este guia é útil? |
|--------|-------------------|
| Nunca usou SQL antes | ✅ Sim, começa aqui |
| Sabe o básico mas quer fixar os fundamentos | ✅ Sim, ótima revisão |
| Quer um material de referência rápida | ✅ Sim, use como consulta |
| Já é desenvolvedor SQL sênior | ⚠️ Talvez muito básico |

<br>

## 📚 O que você vai aprender

O guia cobre **8 seções completas**, cada uma com exemplos visuais, tabelas de resultado e código comentado:

### 1. `SELECT` — O painel de informações do aeroporto
Aprenda a escolher quais colunas você quer visualizar. Cobre `SELECT *`, seleção de colunas específicas, uso de `AS` para criar aliases e `SELECT DISTINCT` para eliminar duplicatas.

### 2. `WHERE` — O filtro do controlador de tráfego
Filtre apenas os registros que atendem a uma condição. Cobre operadores de comparação (`=`, `!=`, `>`, `<`, `>=`), operadores lógicos (`AND`, `OR`, `NOT`), `IN`, `BETWEEN`, `LIKE` e tratamento de `NULL`.

### 3. `JOIN` — Conectando terminais diferentes
Una informações de duas ou mais tabelas. Cobre `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN` e `FULL OUTER JOIN`, com exemplos visuais mostrando quais linhas são incluídas ou excluídas em cada tipo.

### 4. `GROUP BY` — O relatório por companhia aérea
Agrupe registros e calcule totais por categoria. Cobre a regra de ouro do GROUP BY, uso de `HAVING` para filtrar grupos e a diferença fundamental entre `WHERE` e `HAVING`.

### 5. `ORDER BY` — A fila de embarque organizada
Ordene os resultados como quiser. Cobre `ASC`, `DESC`, ordenação por múltiplas colunas e combinação com `LIMIT` para obter os "top N" registros.

### 6. Funções de Agregação — As ferramentas do gestor
Calcule estatísticas sobre conjuntos de dados com `COUNT()`, `SUM()`, `AVG()`, `MAX()` e `MIN()`. Inclui a diferença entre `COUNT(*)` e `COUNT(coluna)`.

### 7. Subqueries — Uma consulta dentro da outra
Escreva consultas aninhadas para responder perguntas mais complexas. Cobre subqueries no `WHERE`, subqueries no `FROM` (tabelas derivadas) e quando usar CTEs (`WITH`) no lugar de subqueries.

### 8. Boas Práticas — Como escrever SQL de qualidade
O que diferencia um analista júnior de um sênior. Cobre formatação e legibilidade, performance, checklist do analista e a **ordem real de execução** do SQL (que é diferente da ordem de escrita!).

<br>

## 🗂️ Estrutura do repositório

```
sql-guia-visual/
│
├── README.md                          ← Você está aqui
├── sql-guia-visual-bruno.html         ← Guia interativo completo (abra no navegador)
│
├── exemplos/                          ← Scripts SQL prontos para rodar
│   ├── 01_select.sql
│   ├── 02_where.sql
│   ├── 03_join.sql
│   ├── 04_group_by.sql
│   ├── 05_order_by.sql
│   ├── 06_funcoes_agregacao.sql
│   ├── 07_subqueries.sql
│   └── 08_boas_praticas.sql
│
└── dados/
    └── aeroporto_sample.sql           ← Script para criar e popular as tabelas de exemplo
```

<br>

## 🚀 Como usar

### Opção 1 — Abrir direto no navegador (mais fácil)
1. Baixe o arquivo `sql-guia-visual-bruno.html`
2. Dê dois cliques no arquivo
3. Ele abrirá no seu navegador — Chrome, Firefox ou Edge funcionam perfeitamente
4. Navegue pelas abas na parte superior

### Opção 2 — Acessar via GitHub Pages
Acesse o guia online sem precisar baixar nada:

```
https://bruno-dsn.github.io/sql-guia-visual/
```

### Opção 3 — Clonar o repositório
```bash
git clone https://github.com/bruno-dsn/sql-guia-visual.git
cd sql-guia-visual
# Abra o arquivo HTML no navegador
open sql-guia-visual-bruno.html       # macOS
start sql-guia-visual-bruno.html      # Windows
xdg-open sql-guia-visual-bruno.html  # Linux
```

### Opção 4 — Praticar com o banco de dados de exemplo
```bash
# Com PostgreSQL instalado:
psql -U seu_usuario -d seu_banco -f dados/aeroporto_sample.sql

# Com MySQL:
mysql -u seu_usuario -p seu_banco < dados/aeroporto_sample.sql

# Com SQLite:
sqlite3 aeroporto.db < dados/aeroporto_sample.sql
```

<br>

## 🗺️ Mapa visual do guia

```
┌─────────────────────────────────────────────────────────────────┐
│                    SQL NO AEROPORTO DE DADOS                    │
├─────────────┬──────────────────────────────────────────────────-┤
│  SELECT     │  Escolhe quais colunas exibir no painel           │
│  WHERE      │  Filtra só os voos que atendem a condição         │
│  JOIN       │  Conecta tabelas de passageiros e voos            │
│  GROUP BY   │  Agrupa e conta voos por companhia                │
│  ORDER BY   │  Organiza a fila de embarque por horário          │
│  Funções    │  Calcula médias, totais e máximos                 │
│  Subquery   │  Pergunta dentro de pergunta                      │
│  Práticas   │  Checklist do analista de dados                   │
└─────────────┴────────────────────────────────────────────────────┘
```

<br>

## 💡 Por que o tema aeroporto?

A escolha do tema foi intencional. Um aeroporto é um sistema de dados rico e familiar para qualquer pessoa:

- **Tabela `voos`** → registros com destino, horário, status, gate
- **Tabela `passageiros`** → registros com nome, assento, voo associado
- **Tabela `companhias`** → registros com nome, código, hub

Isso cria exemplos naturais para todos os comandos: filtrar voos atrasados (`WHERE`), contar voos por companhia (`GROUP BY`), unir passageiro ao seu voo (`JOIN`), listar pelo maior atraso (`ORDER BY DESC`).

<br>

## 🛠️ Tecnologias utilizadas

| Tecnologia | Uso |
|------------|-----|
| HTML5 | Estrutura do guia |
| CSS3 | Estilização, animações e layout responsivo |
| JavaScript (vanilla) | Navegação entre seções e barra de progresso |
| Google Fonts | Tipografia (Syne + JetBrains Mono) |

Nenhuma dependência externa. Nenhum framework. Um único arquivo HTML que funciona em qualquer navegador.

<br>

## 📖 Conceitos abordados — referência rápida

```sql
-- SELECT: escolher colunas
SELECT destino, companhia, hora FROM voos;

-- WHERE: filtrar linhas
SELECT * FROM voos WHERE status = 'Atrasado';

-- JOIN: unir tabelas
SELECT p.nome, v.destino
FROM passageiros p
JOIN voos v ON p.voo_id = v.id;

-- GROUP BY: agrupar e contar
SELECT companhia, COUNT(*) AS total_voos
FROM voos
GROUP BY companhia;

-- ORDER BY: ordenar resultados
SELECT destino, hora FROM voos ORDER BY hora ASC;

-- Funções de agregação
SELECT COUNT(*), AVG(atraso_min), MAX(atraso_min) FROM voos;

-- Subquery
SELECT destino FROM voos
WHERE atraso_min > (SELECT AVG(atraso_min) FROM voos);
```

<br>

## 🔗 Recursos complementares

Quer continuar aprendendo? Aqui estão alguns recursos gratuitos e de qualidade:

- 📘 [SQLZoo](https://sqlzoo.net) — exercícios interativos no navegador
- 📘 [Mode SQL Tutorial](https://mode.com/sql-tutorial) — focado em análise de dados
- 📘 [W3Schools SQL](https://www.w3schools.com/sql) — referência rápida de sintaxe
- 📘 [LeetCode — Database](https://leetcode.com/problemset/database/) — desafios práticos
- 📘 [PostgreSQL Documentation](https://www.postgresql.org/docs/) — documentação oficial

<br>

## 🤝 Contribuindo

Encontrou um erro? Tem uma sugestão de melhoria? Quer adicionar um novo exemplo?

1. Faça um fork do repositório
2. Crie uma branch: `git checkout -b feature/minha-melhoria`
3. Commit suas mudanças: `git commit -m 'Adiciona exemplo de CTE'`
4. Push para a branch: `git push origin feature/minha-melhoria`
5. Abra um Pull Request

Toda contribuição é bem-vinda! ⭐

<br>

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

Você pode usar, copiar, modificar e distribuir este material livremente — desde que mantenha os créditos.

<br>

## 👤 Autor

**Bruno da Silva Nunes**
Analista de Dados · 2026

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Bruno%20da%20Silva%20Nunes-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/bruno-dsnunes/)
[![GitHub](https://img.shields.io/badge/GitHub-bruno--dsn-181717?style=flat&logo=github&logoColor=white)](https://github.com/bruno-dsn)

<br>

---

<div align="center">

**Se este guia te ajudou, deixa uma ⭐ no repositório!**

*Feito com ☕ e muito SQL por Bruno da Silva Nunes*

</div>
