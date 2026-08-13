from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "preview.png"


def rounded_box(ax, x, y, width, height, face, edge="#263a52", radius=0.018):
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle=f"round,pad=0.008,rounding_size={radius}",
        linewidth=1.2,
        edgecolor=edge,
        facecolor=face,
    )
    ax.add_patch(patch)
    return patch


def main() -> None:
    plt.rcParams.update({"font.family": "DejaVu Sans"})
    figure = plt.figure(figsize=(16, 9), dpi=160, facecolor="#07111f")
    ax = figure.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.055, 0.92, "LABORATÓRIO INTERATIVO", color="#7dd3fc", fontsize=10, fontweight="bold")
    ax.text(0.055, 0.84, "SQL sem mistério.", color="#f8fafc", fontsize=32, fontweight="bold")
    ax.text(
        0.055,
        0.785,
        "Veja a tabela, execute a consulta e entenda o resultado.",
        color="#9fb1c7",
        fontsize=13,
    )

    steps = [
        ("1", "Veja a tabela"),
        ("2", "Leia a pergunta"),
        ("3", "Execute o SQL"),
        ("4", "Compare o resultado"),
    ]
    for index, (number, label) in enumerate(steps):
        x = 0.055 + index * 0.225
        rounded_box(ax, x, 0.675, 0.195, 0.073, "#0e1b2b")
        ax.text(x + 0.015, 0.714, number, color="#38bdf8", fontsize=12, fontweight="bold", va="center")
        ax.text(x + 0.046, 0.714, label, color="#e8f0f7", fontsize=10.5, fontweight="bold", va="center")

    rounded_box(ax, 0.055, 0.19, 0.49, 0.425, "#0b1727")
    ax.text(0.078, 0.575, "Consulta SQL", color="#7dd3fc", fontsize=10, fontweight="bold")
    code_lines = [
        ("SELECT", " a.ticker,"),
        ("       ", " COUNT(*) AS total_ordens,"),
        ("       ", " SUM(o.quantidade * o.preco) AS volume"),
        ("FROM", " ordens AS o"),
        ("JOIN", " ativos AS a ON o.ativo_id = a.ativo_id"),
        ("WHERE", " o.status = 'Executada'"),
        ("GROUP BY", " a.ticker"),
        ("ORDER BY", " volume DESC;"),
    ]
    y = 0.525
    for keyword, rest in code_lines:
        ax.text(0.078, y, keyword, color="#38bdf8", fontsize=10.5, family="monospace", fontweight="bold")
        ax.text(0.135, y, rest, color="#d8e5f1", fontsize=10.5, family="monospace")
        y -= 0.043

    rounded_box(ax, 0.57, 0.19, 0.375, 0.425, "#0b1727")
    ax.text(0.593, 0.575, "Resultado", color="#7dd3fc", fontsize=10, fontweight="bold")
    headers = ["ticker", "total_ordens", "volume"]
    x_positions = [0.595, 0.71, 0.835]
    for x, header in zip(x_positions, headers):
        ax.text(x, 0.525, header, color="#9fb1c7", fontsize=9.5, fontweight="bold")

    rows = [
        ("FLOG11", "36", "81.847,59"),
        ("FCOM11", "45", "75.448,12"),
        ("FCRI11", "35", "67.346,60"),
        ("IPCA1", "40", "34.873,56"),
        ("TECA3", "41", "29.480,09"),
    ]
    y = 0.48
    for row_index, row in enumerate(rows):
        if row_index % 2 == 0:
            rounded_box(ax, 0.588, y - 0.019, 0.335, 0.043, "#101f32", edge="#101f32", radius=0.006)
        for x, value in zip(x_positions, row):
            ax.text(x, y, value, color="#e2e8f0", fontsize=9.5, va="center")
        y -= 0.057

    ax.text(
        0.055,
        0.105,
        "SELECT escolhe  |  FROM busca  |  WHERE filtra  |  GROUP BY resume  |  JOIN conecta",
        color="#7dd3fc",
        fontsize=10.5,
        fontweight="bold",
    )
    ax.text(
        0.055,
        0.065,
        "Dados fictícios brasileiros  |  SQLite em memória  |  Streamlit  |  Consultas seguras",
        color="#71869e",
        fontsize=9.5,
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT, facecolor=figure.get_facecolor(), bbox_inches=None)
    plt.close(figure)
    print(f"Preview salvo em {OUTPUT}")


if __name__ == "__main__":
    main()
