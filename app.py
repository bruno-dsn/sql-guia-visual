from __future__ import annotations

import html
from pathlib import Path

import pandas as pd
import streamlit as st

from src.content import CHALLENGES, LESSONS
from src.database import create_database, list_tables, table_columns, table_preview
from src.explainer import explain_query
from src.validation import QueryValidationError, execute_query, same_result


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

TABLE_DESCRIPTIONS = {
    "clientes": "Uma linha por pessoa cadastrada na instituição fictícia.",
    "contas": "Contas vinculadas aos clientes por cliente_id.",
    "ativos": "Catálogo fictício de produtos de investimento.",
    "ordens": "Compras e vendas vinculadas a contas e ativos.",
}


st.set_page_config(
    page_title="SQL sem Mistério",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 82% 8%, rgba(56, 189, 248, 0.12), transparent 25%),
            radial-gradient(circle at 15% 22%, rgba(129, 140, 248, 0.10), transparent 28%),
            #07111f;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1625 0%, #08121e 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.16);
    }
    .block-container {
        max-width: 1280px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }
    .eyebrow {
        color: #7dd3fc;
        font-size: 0.76rem;
        font-weight: 750;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 0.55rem;
    }
    .hero-title {
        color: #f8fafc;
        font-size: clamp(2.35rem, 5vw, 4.8rem);
        line-height: 0.98;
        letter-spacing: -0.055em;
        font-weight: 820;
        max-width: 900px;
        margin: 0;
    }
    .hero-subtitle {
        color: #a9bad0;
        font-size: 1.08rem;
        line-height: 1.65;
        max-width: 780px;
        margin-top: 1.1rem;
    }
    .lesson-card, .schema-card, .clause-card, .metric-card {
        border: 1px solid rgba(148, 163, 184, 0.17);
        background: rgba(14, 27, 43, 0.76);
        border-radius: 16px;
        padding: 1.05rem 1.15rem;
        height: 100%;
        box-shadow: 0 14px 40px rgba(0, 0, 0, 0.14);
    }
    .card-label {
        color: #7dd3fc;
        font-size: 0.72rem;
        font-weight: 750;
        letter-spacing: 0.11em;
        text-transform: uppercase;
    }
    .card-title {
        color: #f1f5f9;
        font-size: 1.02rem;
        font-weight: 720;
        margin-top: 0.35rem;
    }
    .card-copy {
        color: #a9bad0;
        font-size: 0.9rem;
        line-height: 1.5;
        margin-top: 0.35rem;
    }
    .sql-flow {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.7rem;
        margin: 1.2rem 0;
    }
    .sql-step {
        border-top: 3px solid #38bdf8;
        background: rgba(15, 30, 48, 0.86);
        border-radius: 10px;
        padding: 0.85rem;
    }
    .sql-step strong { color: #f8fafc; display: block; }
    .sql-step span { color: #93a6bc; font-size: 0.82rem; }
    .status-ok {
        border-left: 4px solid #2dd4bf;
        background: rgba(45, 212, 191, 0.09);
        color: #ccfbf1;
        padding: 0.9rem 1rem;
        border-radius: 8px;
    }
    .small-note { color: #8093aa; font-size: 0.82rem; line-height: 1.5; }
    div[data-testid="stMetric"] {
        border: 1px solid rgba(148, 163, 184, 0.17);
        background: rgba(14, 27, 43, 0.72);
        padding: 0.8rem 1rem;
        border-radius: 14px;
    }
    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
    }
    @media (max-width: 800px) {
        .sql-flow { grid-template-columns: 1fr 1fr; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_connection():
    return create_database(DATA_DIR)


connection = get_connection()

if "completed_lessons" not in st.session_state:
    st.session_state.completed_lessons = set()
if "solved_challenges" not in st.session_state:
    st.session_state.solved_challenges = set()


def page_header(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(f'<div class="eyebrow">{html.escape(eyebrow)}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<p class="hero-subtitle">{html.escape(subtitle)}</p>', unsafe_allow_html=True)


def show_result(frame: pd.DataFrame) -> None:
    first, second = st.columns(2)
    first.metric("Linhas retornadas", f"{len(frame):,}".replace(",", "."))
    second.metric("Colunas no resultado", len(frame.columns))
    st.dataframe(frame, width="stretch", hide_index=True)
    if len(frame) == 500:
        st.caption("Exibição limitada às primeiras 500 linhas para manter o laboratório leve.")


def show_explanation(query: str) -> None:
    explanations = explain_query(query)
    if not explanations:
        st.caption("Escreva uma consulta para ver a tradução das cláusulas.")
        return

    st.markdown("#### O que cada parte está fazendo")
    for item in explanations:
        with st.expander(f"{item['clause']}: {item['meaning']}"):
            st.code(item["fragment"], language="sql")


def run_editor(default_query: str, key: str) -> None:
    query = st.text_area(
        "Consulta SQL",
        value=default_query,
        height=210,
        key=f"editor_{key}",
        help="Você pode modificar a consulta e executar quantas vezes quiser.",
    )
    show_explanation(query)
    if st.button("Executar consulta", type="primary", key=f"run_{key}"):
        try:
            result = execute_query(connection, query)
        except QueryValidationError as error:
            st.error(str(error))
        except Exception as error:
            st.error(f"O banco não conseguiu executar a consulta: {error}")
        else:
            st.session_state.completed_lessons.add(key)
            show_result(result)


def render_home() -> None:
    st.markdown('<div class="eyebrow">Laboratório interativo</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">SQL sem mistério.</h1>', unsafe_allow_html=True)
    st.markdown(
        """
        <p class="hero-subtitle">
        Aprenda a consultar dados olhando o antes, executando o comando e entendendo
        o depois. Sem instalação de banco, sem cadastro e sem conhecimento prévio.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sql-flow">
            <div class="sql-step"><strong>1. Veja a tabela</strong><span>Conheça os dados disponíveis.</span></div>
            <div class="sql-step"><strong>2. Leia a pergunta</strong><span>Entenda o objetivo da consulta.</span></div>
            <div class="sql-step"><strong>3. Execute o SQL</strong><span>Edite e teste o comando.</span></div>
            <div class="sql-step"><strong>4. Compare</strong><span>Observe o resultado produzido.</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Comece por aqui")
    columns = st.columns(3)
    cards = [
        ("Fundamentos", "SELECT, FROM e WHERE", "Aprenda a escolher colunas e filtrar linhas."),
        ("Análise", "GROUP BY e JOIN", "Crie indicadores e combine tabelas relacionadas."),
        ("Prática", "Desafios corrigidos", "Resolva tarefas e valide o resultado da consulta."),
    ]
    for column, (label, title, copy) in zip(columns, cards):
        column.markdown(
            f"""
            <div class="lesson-card">
                <div class="card-label">{label}</div>
                <div class="card-title">{title}</div>
                <div class="card-copy">{copy}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### O banco que usaremos")
    st.write(
        "O cenário representa uma instituição brasileira fictícia. Os nomes, valores, "
        "ativos e operações são sintéticos e existem apenas para aprendizagem."
    )
    schema_columns = st.columns(4)
    for column, table_name in zip(schema_columns, ["clientes", "contas", "ordens", "ativos"]):
        count = connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        column.markdown(
            f"""
            <div class="schema-card">
                <div class="card-label">Tabela</div>
                <div class="card-title">{table_name}</div>
                <div class="card-copy">{TABLE_DESCRIPTIONS[table_name]}<br><br>{count} linhas</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Uma primeira consulta")
    st.code(
        """SELECT nome, cidade
FROM clientes
WHERE uf = 'SP'
ORDER BY nome;""",
        language="sql",
    )
    st.info(
        "Leitura em português: mostre o nome e a cidade da tabela clientes, "
        "mantenha apenas quem está em SP e organize os nomes em ordem alfabética."
    )


def render_data_map() -> None:
    page_header(
        "Antes da consulta",
        "Conheça o banco de dados",
        "SQL consulta tabelas. Antes de escrever comandos, veja quais informações existem e como elas se conectam.",
    )

    st.markdown("### Relacionamentos")
    st.markdown(
        """
        <div class="sql-flow">
            <div class="sql-step"><strong>clientes</strong><span>cliente_id identifica uma pessoa.</span></div>
            <div class="sql-step"><strong>contas</strong><span>cliente_id aponta para o titular.</span></div>
            <div class="sql-step"><strong>ordens</strong><span>conta_id identifica quem negociou.</span></div>
            <div class="sql-step"><strong>ativos</strong><span>ativo_id identifica o produto.</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Relação principal: clientes 1:N contas 1:N ordens N:1 ativos.")

    selected = st.selectbox("Escolha uma tabela", list_tables(connection))
    st.markdown(f"**O que ela representa:** {TABLE_DESCRIPTIONS[selected]}")
    st.markdown("**Colunas:** " + ", ".join(table_columns(connection, selected)))
    st.dataframe(table_preview(connection, selected, 12), width="stretch", hide_index=True)


def render_lesson(lesson_name: str) -> None:
    lesson = LESSONS[lesson_name]
    page_header(lesson["level"], lesson_name, lesson["title"])

    left, right = st.columns([1.25, 1])
    with left:
        st.markdown("#### Ideia principal")
        st.write(lesson["analogy"])
        st.markdown("#### Pergunta que vamos responder")
        st.info(lesson["question"])
    with right:
        st.markdown(f"#### Tabela de partida: `{lesson['table']}`")
        st.dataframe(
            table_preview(connection, lesson["table"], 6),
            width="stretch",
            hide_index=True,
        )

    st.divider()
    run_editor(lesson["query"], lesson_name)
    st.caption("Dica: " + lesson["tip"])


def render_challenges() -> None:
    page_header(
        "Hora de praticar",
        "Desafios com correção",
        "Complete a consulta. A validação compara o resultado, então soluções SQL diferentes também podem estar corretas.",
    )

    titles = [f"{item['difficulty']} | {item['title']}" for item in CHALLENGES]
    selected_title = st.selectbox("Escolha um desafio", titles)
    challenge_index = titles.index(selected_title)
    challenge = CHALLENGES[challenge_index]

    st.markdown("#### Objetivo")
    st.write(challenge["prompt"])
    with st.expander("Preciso de uma dica"):
        st.write(challenge["hint"])

    answer = st.text_area(
        "Sua solução",
        value=challenge["starter"],
        height=240,
        key=f"challenge_{challenge_index}",
    )
    show_explanation(answer)

    if st.button("Verificar resposta", type="primary"):
        try:
            actual = execute_query(connection, answer)
            expected = execute_query(connection, challenge["solution"])
        except QueryValidationError as error:
            st.error(str(error))
        except Exception as error:
            st.error(f"Ainda há algo para ajustar na consulta: {error}")
        else:
            if same_result(actual, expected):
                st.session_state.solved_challenges.add(challenge_index)
                st.markdown(
                    '<div class="status-ok">Resultado correto. A consulta respondeu exatamente ao desafio.</div>',
                    unsafe_allow_html=True,
                )
                show_result(actual)
            else:
                st.warning(
                    "A consulta executou, mas o resultado ainda difere do esperado. "
                    "Confira colunas, filtros, agrupamento e ordenação."
                )
                show_result(actual)

    with st.expander("Mostrar uma solução possível"):
        st.code(challenge["solution"], language="sql")


def render_playground() -> None:
    page_header(
        "Exploração livre",
        "Playground SQL",
        "Escreva consultas SELECT usando qualquer uma das quatro tabelas. O banco é recriado em memória e não pode ser alterado.",
    )
    with st.expander("Consultar tabelas e colunas"):
        for table_name in list_tables(connection):
            st.markdown(f"**{table_name}:** " + ", ".join(table_columns(connection, table_name)))

    default = """SELECT a.ticker,
       COUNT(*) AS total_ordens,
       ROUND(SUM(o.quantidade * o.preco), 2) AS volume_total
FROM ordens AS o
JOIN ativos AS a ON o.ativo_id = a.ativo_id
WHERE o.status = 'Executada'
GROUP BY a.ticker
ORDER BY volume_total DESC;"""
    run_editor(default, "playground")


lesson_total = len(LESSONS)
completed_total = len(st.session_state.completed_lessons.intersection(LESSONS.keys()))
challenge_total = len(CHALLENGES)
solved_total = len(st.session_state.solved_challenges)

st.sidebar.markdown("### SQL sem Mistério")
st.sidebar.caption("Aprenda consultando dados")
page = st.sidebar.radio(
    "Navegação",
    ["Início", "Mapa dos dados", *LESSONS.keys(), "Desafios", "Playground"],
    label_visibility="collapsed",
)
st.sidebar.divider()
st.sidebar.markdown("**Progresso desta sessão**")
st.sidebar.progress((completed_total + solved_total) / (lesson_total + challenge_total))
st.sidebar.caption(
    f"{completed_total}/{lesson_total} aulas executadas | "
    f"{solved_total}/{challenge_total} desafios resolvidos"
)
st.sidebar.markdown(
    '<p class="small-note">Os dados são fictícios e o progresso existe somente enquanto esta sessão estiver aberta.</p>',
    unsafe_allow_html=True,
)

if page == "Início":
    render_home()
elif page == "Mapa dos dados":
    render_data_map()
elif page in LESSONS:
    render_lesson(page)
elif page == "Desafios":
    render_challenges()
else:
    render_playground()
