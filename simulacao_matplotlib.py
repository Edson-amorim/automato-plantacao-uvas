"""
Visualização com Matplotlib do Autômato Celular da Plantação de Uvas.
Permite tanto exibir a animação ao vivo quanto gerar um painel ilustrativo (PNG)
mostrando a evolução da contaminação e a formação da barreira de contenção pelas
parreiras recuperadas.
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import matplotlib.animation as animation

from automato_uvas import AutomatoPlantacaoUvas, EstadoParreira


MAPA_CORES = ListedColormap([
    "#1e1e2e",  # 0: Vazio
    "#2e7d32",  # 1: Parreira Saudável (Verde)
    "#d32f2f",  # 2: Parreira Contaminada (Vermelho)
    "#1976d2",  # 3: Parreira Recuperada / Barreira de Contenção (Azul)
])


def salvar_painel_evolucao(caminho_saida: str = "evolucao_plantacao_uvas.png") -> None:
    """Executa a simulação e salva uma imagem com os estágios e curvas SIR."""
    automato = AutomatoPlantacaoUvas(
        linhas=35,
        colunas=45,
        prob_contagio=0.38,
        tempo_recuperacao=4,
        semente=101,
    )
    automato.reiniciar_plantacao("foco_com_barreira_parcial")

    geracoes_captura = [0, 5, 12, 25]
    grades_capturadas = {}

    for g in range(max(geracoes_captura) + 1):
        if g in geracoes_captura:
            grades_capturadas[g] = np.array(automato.grade, dtype=int)
        automato.avancar_geracao()

    fig = plt.figure(figsize=(14, 8), facecolor="#181825")
    fig.suptitle(
        "Autômato Celular: Contaminação e Barreira de Contenção em Plantação de Uvas",
        color="white",
        fontsize=15,
        fontweight="bold",
        y=0.97,
    )

    for idx, g in enumerate(geracoes_captura):
        ax = fig.add_subplot(2, 3, idx + 1 if idx < 2 else idx + 2)
        ax.imshow(grades_capturadas[g], cmap=MAPA_CORES, vmin=0, vmax=3)
        ax.set_title(f"Geração t = {g}", color="#cdd6f4", fontsize=11, fontweight="bold")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor("#45475a")

    # Gráfico de curvas ao longo das gerações
    ax_curva = fig.add_subplot(1, 3, 3)
    ax_curva.set_facecolor("#1e1e2e")
    tempos = list(range(len(automato.historico)))
    saudaveis = [h[0] for h in automato.historico]
    contaminadas = [h[1] for h in automato.historico]
    recuperadas = [h[2] for h in automato.historico]

    ax_curva.plot(tempos, saudaveis, label="Saudáveis", color="#4caf50", linewidth=2.5)
    ax_curva.plot(tempos, contaminadas, label="Contaminadas", color="#f44336", linewidth=2.5)
    ax_curva.plot(tempos, recuperadas, label="Recuperadas (Barreira)", color="#29b6f6", linewidth=2.5)
    ax_curva.set_title("Dinâmica Populacional das Parreiras", color="#cdd6f4", fontsize=11, fontweight="bold")
    ax_curva.set_xlabel("Geração (Ciclos de Tempo)", color="#cdd6f4")
    ax_curva.set_ylabel("Número de Parreiras", color="#cdd6f4")
    ax_curva.tick_params(colors="#cdd6f4")
    ax_curva.grid(True, linestyle="--", alpha=0.25, color="#cdd6f4")
    ax_curva.legend(facecolor="#252538", edgecolor="#45475a", labelcolor="white")
    for spine in ax_curva.spines.values():
        spine.set_edgecolor("#45475a")

    legenda_patches = [
        Patch(facecolor="#2e7d32", label="Parreira Saudável (Suscetível)"),
        Patch(facecolor="#d32f2f", label="Parreira Contaminada (Infecta Próximas)"),
        Patch(facecolor="#1976d2", label="Parreira Recuperada (Barreira de Contenção)"),
    ]
    fig.legend(
        handles=legenda_patches,
        loc="lower center",
        ncol=3,
        facecolor="#252538",
        edgecolor="#45475a",
        labelcolor="white",
        fontsize=10,
        bbox_to_anchor=(0.5, 0.01),
    )

    plt.tight_layout(rect=[0, 0.06, 1, 0.93])
    plt.savefig(caminho_saida, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Painel salvo com sucesso em: {caminho_saida}")


def animar_matplotlib() -> None:
    """Abre janela animada do Matplotlib com a grade e o gráfico em tempo real."""
    automato = AutomatoPlantacaoUvas(linhas=35, colunas=45, prob_contagio=0.38, tempo_recuperacao=4)
    automato.reiniciar_plantacao("foco_com_barreira_parcial")

    fig, (ax_grade, ax_curva) = plt.subplots(1, 2, figsize=(13, 5.5), facecolor="#181825")
    fig.suptitle(
        "Simulação em Tempo Real: Plantação de Uvas",
        color="white",
        fontsize=14,
        fontweight="bold",
    )

    img = ax_grade.imshow(np.array(automato.grade), cmap=MAPA_CORES, vmin=0, vmax=3)
    ax_grade.set_xticks([])
    ax_grade.set_yticks([])

    ax_curva.set_facecolor("#1e1e2e")
    linha_s, = ax_curva.plot([], [], color="#4caf50", lw=2, label="Saudáveis")
    linha_c, = ax_curva.plot([], [], color="#f44336", lw=2, label="Contaminadas")
    linha_r, = ax_curva.plot([], [], color="#29b6f6", lw=2, label="Recuperadas (Barreira)")
    ax_curva.set_xlim(0, 60)
    ax_curva.set_ylim(0, automato.linhas * automato.colunas)
    ax_curva.set_xlabel("Geração", color="white")
    ax_curva.set_ylabel("Quantidade de Parreiras", color="white")
    ax_curva.tick_params(colors="white")
    ax_curva.legend(facecolor="#252538", labelcolor="white")
    ax_curva.grid(True, alpha=0.2)

    def atualizar(_frame):
        if automato.contar_estados()[1] > 0:
            automato.avancar_geracao()
        img.set_data(np.array(automato.grade))
        s, c, r = automato.contar_estados()
        ax_grade.set_title(
            f"Geração {automato.geracao} | Saudáveis: {s} | Contaminadas: {c} | Barreira: {r}",
            color="white",
            fontsize=10,
        )
        t = list(range(len(automato.historico)))
        linha_s.set_data(t, [h[0] for h in automato.historico])
        linha_c.set_data(t, [h[1] for h in automato.historico])
        linha_r.set_data(t, [h[2] for h in automato.historico])
        if len(t) > ax_curva.get_xlim()[1]:
            ax_curva.set_xlim(0, len(t) + 15)
        return img, linha_s, linha_c, linha_r

    _anim = animation.FuncAnimation(fig, atualizar, interval=180, blit=False, cache_frame_data=False)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualização Matplotlib do Autômato de Uvas")
    parser.add_argument(
        "--salvar-imagem",
        action="store_true",
        help="Gera e salva o painel PNG da evolução da plantação.",
    )
    args = parser.parse_args()
    if args.salvar_imagem:
        salvar_painel_evolucao()
    else:
        animar_matplotlib()
