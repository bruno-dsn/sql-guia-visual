# Modelo de dados

O laboratório usa um cenário financeiro inteiramente fictício. O objetivo é
ensinar relações entre tabelas sem depender de credenciais, APIs ou um servidor
de banco de dados.

## Relacionamentos

```text
clientes 1 ---- N contas 1 ---- N ordens N ---- 1 ativos
```

- `clientes.cliente_id` identifica cada cliente;
- `contas.cliente_id` liga uma conta ao seu titular;
- `ordens.conta_id` identifica a conta que enviou a ordem;
- `ordens.ativo_id` identifica o ativo negociado.

## Tabela clientes

| Coluna | Significado |
|---|---|
| cliente_id | Identificador inteiro do cliente |
| nome | Nome fictício |
| cidade | Município de residência |
| uf | Unidade federativa |
| perfil_investidor | Conservador, Moderado ou Arrojado |
| data_cadastro | Data fictícia de entrada |

## Tabela contas

| Coluna | Significado |
|---|---|
| conta_id | Identificador da conta |
| cliente_id | Chave que aponta para clientes |
| tipo_conta | Investimentos, Digital ou Previdência |
| saldo | Saldo fictício em reais |
| status | Ativa ou Inativa |

## Tabela ativos

| Coluna | Significado |
|---|---|
| ativo_id | Identificador do ativo |
| ticker | Código fictício de negociação |
| nome_ativo | Nome fictício do produto |
| tipo_ativo | Ação, FII, Renda fixa ou Fundo |
| setor | Classificação simplificada |

## Tabela ordens

| Coluna | Significado |
|---|---|
| ordem_id | Identificador da ordem |
| conta_id | Chave que aponta para contas |
| ativo_id | Chave que aponta para ativos |
| lado | Compra ou Venda |
| quantidade | Quantidade fictícia negociada |
| preco | Preço unitário fictício em reais |
| data_ordem | Data fictícia da operação |
| status | Executada, Cancelada ou Pendente |

