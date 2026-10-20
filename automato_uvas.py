"""
Autômato Celular: Dinâmica de Contaminação e Barreira de Contenção em Plantação de Uvas
=======================================================================================

Estados de cada célula (parreira de uva):
- 0: VAZIO (Corredor / Solo sem parreira)
- 1: SAUDÁVEL (Parreira produtiva suscetível à praga/fungo)
- 2: CONTAMINADA (Parreira infectada que transmite a doença para parreiras próximas)
- 3: RECUPERADA / BARREIRA (Parreira que se recuperou após tratamento/ciclo e agora
     atua como barreira de contenção, impedindo a passagem e reinfecção)

Regras de Transição (a cada passo de tempo t -> t+1):
1. Uma parreira SAUDÁVEL (1) com pelo menos uma parreira vizinha CONTAMINADA (2)
   tem probabilidade `p` de ser contaminada a cada vizinho infectado:
   P(infectar) = 1 - (1 - p)^k, onde k é o número de vizinhos contaminados.
2. Uma parreira CONTAMINADA (2) permanece infectada por `tempo_recuperacao` ciclos.
   Durante esse período, ela pode contaminar as parreiras próximas.
3. Após cumprir `tempo_recuperacao` ciclos, a parreira CONTAMINADA (2) se recupera
   e passa para o estado RECUPERADA / BARREIRA DE CONTENÇÃO (3).
4. Uma parreira RECUPERADA / BARREIRA (3) é imune e bloqueia a propagação da praga,
   protegendo as parreiras saudáveis ao seu redor (efeito de contenção em anel).
"""

import argparse
import random
import time
from dataclasses import dataclass, field
from enum import IntEnum
from typing import List, Tuple


class EstadoParreira(IntEnum):
    VAZIO = 0
    SAUDAVEL = 1
    CONTAMINADA = 2
    BARREIRA_RECUPERADA = 3


@dataclass
class AutomatoPlantacaoUvas:
    linhas: int = 30
    colunas: int = 40
    prob_contagio: float = 0.38
    tempo_recuperacao: int = 4
    vizinhanca_moore: bool = True  # True = 8 vizinhos, False = 4 vizinhos (Von Neumann)
    semente: int | None = None

    grade: List[List[int]] = field(init=False)
    tempo_infeccao: List[List[int]] = field(init=False)
    geracao: int = field(default=0, init=False)
    historico: List[ Tuple[int, int, int] ] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if self.semente is not None:
            random.seed(self.semente)
        self.reiniciar_plantacao()

    def reiniciar_plantacao(self, cenario: str = "foco_central") -> None:
        """Inicializa a plantação de uvas de acordo com o cenário escolhido."""
        self.geracao = 0
        self.grade = [
            [EstadoParreira.SAUDAVEL for _ in range(self.colunas)]
            for _ in range(self.linhas)
        ]
        self.tempo_infeccao = [
            [0 for _ in range(self.colunas)]
            for _ in range(self.linhas)
        ]

        meio_l = self.linhas // 2
        meio_c = self.colunas // 2

        if cenario == "foco_central":
            # Parreira inicial contaminada no centro da plantação
            self.infectar_parreira(meio_l, meio_c)

        elif cenario == "foco_com_barreira_parcial":
            # Foco de contaminação à esquerda e um anel parcial de parreiras já recuperadas/barreira
            foco_l, foco_c = meio_l, self.colunas // 4
            self.infectar_parreira(foco_l, foco_c)
            self.infectar_parreira(foco_l + 1, foco_c)
            # Cria uma linha de contenção prévia de parreiras recuperadas com uma pequena brecha
            col_barreira = self.colunas // 2
            for l in range(2, self.linhas - 2):
                if l not in (meio_l, meio_l + 1):
                    self.grade[l][col_barreira] = EstadoParreira.BARREIRA_RECUPERADA
                    self.grade[l][col_barreira + 1] = EstadoParreira.BARREIRA_RECUPERADA

        elif cenario == "multiplos_focos":
            for _ in range(3):
                l = random.randint(3, self.linhas - 4)
                c = random.randint(3, self.colunas - 4)
                self.infectar_parreira(l, c)

        self.historico = [self.contar_estados()]

    def infectar_parreira(self, l: int, c: int) -> None:
        if 0 <= l < self.linhas and 0 <= c < self.colunas:
            self.grade[l][c] = EstadoParreira.CONTAMINADA
            self.tempo_infeccao[l][c] = 1

    def definir_barreira(self, l: int, c: int) -> None:
        if 0 <= l < self.linhas and 0 <= c < self.colunas:
            self.grade[l][c] = EstadoParreira.BARREIRA_RECUPERADA
            self.tempo_infeccao[l][c] = 0

    def contar_vizinhos_contaminados(self, l: int, c: int) -> int:
        """Conta quantas parreiras próximas estão contaminadas."""
        deslocamentos = [
            (-1, 0), (1, 0), (0, -1), (0, 1)
        ]
        if self.vizinhanca_moore:
            deslocamentos.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])

        contaminados = 0
        for dl, dc in deslocamentos:
            nl, nc = l + dl, c + dc
            if 0 <= nl < self.linhas and 0 <= nc < self.colunas:
                if self.grade[nl][nc] == EstadoParreira.CONTAMINADA:
                    contaminados += 1
        return contaminados

    def avancar_geracao(self) -> bool:
        """
        Executa um passo do autômato celular.
        Retorna True se ainda houver parreiras contaminadas ativas, False se estabilizou.
        """
        nova_grade = [linha[:] for linha in self.grade]
        novo_tempo = [linha[:] for linha in self.tempo_infeccao]

        for l in range(self.linhas):
            for c in range(self.colunas):
                estado_atual = self.grade[l][c]

                if estado_atual == EstadoParreira.SAUDAVEL:
                    vizinhos_inf = self.contar_vizinhos_contaminados(l, c)
                    if vizinhos_inf > 0:
                        # Probabilidade acumulada de contaminação pelos vizinhos próximos
                        prob_infectar = 1.0 - ((1.0 - self.prob_contagio) ** vizinhos_inf)
                        if random.random() < prob_infectar:
                            nova_grade[l][c] = EstadoParreira.CONTAMINADA
                            novo_tempo[l][c] = 1

                elif estado_atual == EstadoParreira.CONTAMINADA:
                    if self.tempo_infeccao[l][c] >= self.tempo_recuperacao:
                        # A parreira se recupera e passa a atuar como barreira de contenção!
                        nova_grade[l][c] = EstadoParreira.BARREIRA_RECUPERADA
                        novo_tempo[l][c] = 0
                    else:
                        novo_tempo[l][c] = self.tempo_infeccao[l][c] + 1

                elif estado_atual == EstadoParreira.BARREIRA_RECUPERADA:
                    # Permanece como barreira de contenção (imune, bloqueia contágio)
                    pass

        self.grade = nova_grade
        self.tempo_infeccao = novo_tempo
        self.geracao += 1
        saudaveis, contaminadas, recuperadas = self.contar_estados()
        self.historico.append((saudaveis, contaminadas, recuperadas))
        return contaminadas > 0

    def contar_estados(self) -> Tuple[int, int, int]:
        """Retorna (saudáveis, contaminadas, recuperadas/barreira)."""
        saudaveis = 0
        contaminadas = 0
        recuperadas = 0
        for l in range(self.linhas):
            for c in range(self.colunas):
                est = self.grade[l][c]
                if est == EstadoParreira.SAUDAVEL:
                    saudaveis += 1
                elif est == EstadoParreira.CONTAMINADA:
                    contaminadas += 1
                elif est == EstadoParreira.BARREIRA_RECUPERADA:
                    recuperadas += 1
        return saudaveis, contaminadas, recuperadas


def executar_modo_terminal(linhas: int = 15, colunas: int = 30, passos: int = 25, intervalo: float = 0.15) -> None:
    """Executa uma demonstração do autômato diretamente no terminal."""
    simbolos = {
        EstadoParreira.VAZIO: " . ",
        EstadoParreira.SAUDAVEL: "🍇",
        EstadoParreira.CONTAMINADA: "🦠",
        EstadoParreira.BARREIRA_RECUPERADA: "🛡️",
    }
    automato = AutomatoPlantacaoUvas(
        linhas=linhas,
        colunas=colunas,
        prob_contagio=0.40,
        tempo_recuperacao=3,
        semente=42,
    )
    automato.reiniciar_plantacao("foco_com_barreira_parcial")

    print("=" * 72)
    print(" AUTÔMATO CELULAR - PLANTAÇÃO DE UVAS E BARREIRA DE CONTENÇÃO")
    print(" Legenda: 🍇 Saudável | 🦠 Contaminada | 🛡️ Recuperada (Barreira)")
    print("=" * 72)

    for _ in range(passos):
        saudaveis, contaminadas, recuperadas = automato.contar_estados()
        print(f"\nGeração {automato.geracao:02d} | 🍇 Saudáveis: {saudaveis} | 🦠 Contaminadas: {contaminadas} | 🛡️ Barreira/Recuperadas: {recuperadas}")
        for l in range(automato.linhas):
            linha_str = "".join(simbolos[automato.grade[l][c]] for c in range(automato.colunas))
            print(linha_str)

        if not automato.avancar_geracao():
            saudaveis, contaminadas, recuperadas = automato.contar_estados()
            print(f"\nGeração {automato.geracao:02d} (Estabilizado - Praga Contida!)")
            print(f"Resultado Final -> 🍇 Saudáveis protegidas: {saudaveis} | 🦠 Contaminadas: {contaminadas} | 🛡️ Recuperadas (Barreira): {recuperadas}")
            break
        time.sleep(intervalo)


def iniciar_interface_grafica() -> None:
    """Inicia a interface gráfica interativa em Tkinter."""
    import tkinter as tk
    from tkinter import ttk

    CORES = {
        EstadoParreira.VAZIO: "#2b2b2b",
        EstadoParreira.SAUDAVEL: "#2e7d32",             # Verde parreira saudável
        EstadoParreira.CONTAMINADA: "#d32f2f",          # Vermelho parreira contaminada
        EstadoParreira.BARREIRA_RECUPERADA: "#1976d2",  # Azul/Ciano parreira recuperada (barreira)
    }

    root = tk.Tk()
    root.title("Autômato Celular - Plantação de Uvas (Contaminação e Barreira de Contenção)")
    root.geometry("1120x740")
    root.configure(bg="#1e1e2e")

    automato = AutomatoPlantacaoUvas(linhas=30, colunas=42, prob_contagio=0.36, tempo_recuperacao=4)
    automato.reiniciar_plantacao("foco_com_barreira_parcial")

    em_execucao = {"ativo": False}
    ferramenta_clique = tk.StringVar(value="contaminar")
    cenario_var = tk.StringVar(value="foco_com_barreira_parcial")
    prob_var = tk.DoubleVar(value=0.36)
    recup_var = tk.IntVar(value=4)
    velocidade_var = tk.IntVar(value=180)

    # Layout principal
    frame_esq = tk.Frame(root, bg="#1e1e2e", padx=12, pady=12)
    frame_esq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    frame_dir = tk.Frame(root, bg="#252538", width=320, padx=14, pady=14)
    frame_dir.pack(side=tk.RIGHT, fill=tk.Y)

    # Título e status no topo
    lbl_titulo = tk.Label(
        frame_esq,
        text="🍇 Autômato Celular: Parreiras de Uva & Barreira de Contenção",
        font=("Segoe UI", 15, "bold"),
        fg="#f8f8f2",
        bg="#1e1e2e",
    )
    lbl_titulo.pack(anchor="w", pady=(0, 6))

    lbl_status = tk.Label(
        frame_esq,
        text="",
        font=("Segoe UI", 11, "bold"),
        fg="#a6e3a1",
        bg="#1e1e2e",
    )
    lbl_status.pack(anchor="w", pady=(0, 8))

    # Canvas da plantação
    tam_celula = 18
    largura_canvas = automato.colunas * tam_celula
    altura_canvas = automato.linhas * tam_celula

    canvas = tk.Canvas(
        frame_esq,
        width=largura_canvas,
        height=altura_canvas,
        bg="#181825",
        highlightthickness=2,
        highlightbackground="#45475a",
    )
    canvas.pack(pady=4)

    # Canvas de gráfico de evolução temporal
    lbl_grafico = tk.Label(
        frame_esq,
        text="Evolução da Plantação ao Longo do Tempo (Saudáveis vs Contaminadas vs Recuperadas/Barreira):",
        font=("Segoe UI", 9, "bold"),
        fg="#cdd6f4",
        bg="#1e1e2e",
    )
    lbl_grafico.pack(anchor="w", pady=(8, 2))

    canvas_grafico = tk.Canvas(
        frame_esq,
        width=largura_canvas,
        height=95,
        bg="#181825",
        highlightthickness=1,
        highlightbackground="#45475a",
    )
    canvas_grafico.pack(pady=2)

    retangulos = [[None for _ in range(automato.colunas)] for _ in range(automato.linhas)]
    for l in range(automato.linhas):
        for c in range(automato.colunas):
            x1 = c * tam_celula
            y1 = l * tam_celula
            x2 = x1 + tam_celula
            y2 = y1 + tam_celula
            retangulos[l][c] = canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=CORES[automato.grade[l][c]],
                outline="#1e1e2e",
                width=1,
            )

    def desenhar_grade() -> None:
        for l in range(automato.linhas):
            for c in range(automato.colunas):
                estado = automato.grade[l][c]
                cor = CORES[estado]
                # Destaca parreiras recém-contaminadas vs prestes a se recuperar
                if estado == EstadoParreira.CONTAMINADA:
                    t = automato.tempo_infeccao[l][c]
                    if t >= automato.tempo_recuperacao:
                        cor = "#ff9800"  # Laranja: prestes a virar barreira de contenção
                canvas.itemconfig(retangulos[l][c], fill=cor)

        saudaveis, contaminadas, recuperadas = automato.contar_estados()
        total = automato.linhas * automato.colunas
        lbl_status.config(
            text=(
                f"Geração: {automato.geracao:03d}   |   "
                f"🟢 Saudáveis: {saudaveis} ({saudaveis*100//total}%)   |   "
                f"🔴 Contaminadas: {contaminadas} ({contaminadas*100//total}%)   |   "
                f"🔵 Recuperadas (Barreira): {recuperadas} ({recuperadas*100//total}%)"
            )
        )
        desenhar_grafico()

    def desenhar_grafico() -> None:
        canvas_grafico.delete("all")
        hist = automato.historico[-120:]
        if len(hist) < 2:
            return
        total = automato.linhas * automato.colunas
        w = largura_canvas
        h = 95
        passo_x = w / max(len(hist) - 1, 1)

        pts_saud = []
        pts_cont = []
        pts_rec = []
        for idx, (s, c, r) in enumerate(hist):
            x = idx * passo_x
            pts_saud.extend([x, h - (s / total) * (h - 10) - 5])
            pts_cont.extend([x, h - (c / total) * (h - 10) - 5])
            pts_rec.extend([x, h - (r / total) * (h - 10) - 5])

        canvas_grafico.create_line(*pts_saud, fill="#4caf50", width=2)
        canvas_grafico.create_line(*pts_cont, fill="#f44336", width=2)
        canvas_grafico.create_line(*pts_rec, fill="#29b6f6", width=2)

    def ao_clicar_canvas(evento) -> None:
        c = evento.x // tam_celula
        l = evento.y // tam_celula
        if 0 <= l < automato.linhas and 0 <= c < automato.colunas:
            modo = ferramenta_clique.get()
            if modo == "contaminar":
                automato.infectar_parreira(l, c)
            elif modo == "barreira":
                automato.definir_barreira(l, c)
            elif modo == "saudavel":
                automato.grade[l][c] = EstadoParreira.SAUDAVEL
                automato.tempo_infeccao[l][c] = 0
            desenhar_grade()

    canvas.bind("<Button-1>", ao_clicar_canvas)
    canvas.bind("<B1-Motion>", ao_clicar_canvas)

    def ciclo_simulacao() -> None:
        if not em_execucao["ativo"]:
            return
        automato.prob_contagio = prob_var.get()
        automato.tempo_recuperacao = recup_var.get()
        ainda_ativo = automato.avancar_geracao()
        desenhar_grade()
        if ainda_ativo:
            root.after(velocidade_var.get(), ciclo_simulacao)
        else:
            em_execucao["ativo"] = False
            btn_iniciar.config(text="▶ Iniciar Simulação", bg="#2e7d32")

    def alternar_execucao() -> None:
        if em_execucao["ativo"]:
            em_execucao["ativo"] = False
            btn_iniciar.config(text="▶ Continuar Simulação", bg="#2e7d32")
        else:
            em_execucao["ativo"] = True
            btn_iniciar.config(text="⏸ Pausar Simulação", bg="#f57c00")
            ciclo_simulacao()

    def avancar_um_passo() -> None:
        em_execucao["ativo"] = False
        btn_iniciar.config(text="▶ Continuar Simulação", bg="#2e7d32")
        automato.prob_contagio = prob_var.get()
        automato.tempo_recuperacao = recup_var.get()
        automato.avancar_geracao()
        desenhar_grade()

    def reiniciar() -> None:
        em_execucao["ativo"] = False
        btn_iniciar.config(text="▶ Iniciar Simulação", bg="#2e7d32")
        automato.prob_contagio = prob_var.get()
        automato.tempo_recuperacao = recup_var.get()
        automato.reiniciar_plantacao(cenario_var.get())
        desenhar_grade()

    # Painel de Controles à Direita
    tk.Label(
        frame_dir, text="Painel de Controle", font=("Segoe UI", 13, "bold"),
        fg="#ffffff", bg="#252538"
    ).pack(anchor="w", pady=(0, 10))

    btn_iniciar = tk.Button(
        frame_dir, text="▶ Iniciar Simulação", font=("Segoe UI", 11, "bold"),
        bg="#2e7d32", fg="white", relief=tk.FLAT, pady=6, command=alternar_execucao
    )
    btn_iniciar.pack(fill=tk.X, pady=4)

    btn_passo = tk.Button(
        frame_dir, text="⏭ Avançar 1 Geração", font=("Segoe UI", 10),
        bg="#3b3b54", fg="white", relief=tk.FLAT, pady=5, command=avancar_um_passo
    )
    btn_passo.pack(fill=tk.X, pady=4)

    btn_reset = tk.Button(
        frame_dir, text="🔄 Reiniciar Plantação", font=("Segoe UI", 10),
        bg="#45475a", fg="white", relief=tk.FLAT, pady=5, command=reiniciar
    )
    btn_reset.pack(fill=tk.X, pady=(4, 14))

    # Cenários
    tk.Label(
        frame_dir, text="Cenário Inicial:", font=("Segoe UI", 10, "bold"),
        fg="#cdd6f4", bg="#252538"
    ).pack(anchor="w")

    cenarios = [
        ("Foco + Barreira de Contenção", "foco_com_barreira_parcial"),
        ("Foco Central Único", "foco_central"),
        ("Múltiplos Focos Aleatórios", "multiplos_focos"),
    ]
    for texto, valor in cenarios:
        tk.Radiobutton(
            frame_dir, text=texto, variable=cenario_var, value=valor,
            bg="#252538", fg="#cdd6f4", selectcolor="#1e1e2e",
            activebackground="#252538", activeforeground="#ffffff",
            command=reiniciar
        ).pack(anchor="w")

    # Sliders de parâmetros
    tk.Label(
        frame_dir, text="\nProbabilidade de Contágio (p):", font=("Segoe UI", 10, "bold"),
        fg="#cdd6f4", bg="#252538"
    ).pack(anchor="w")
    tk.Scale(
        frame_dir, from_=0.05, to=0.95, resolution=0.01, orient=tk.HORIZONTAL,
        variable=prob_var, bg="#252538", fg="#ffffff", highlightthickness=0
    ).pack(fill=tk.X)

    tk.Label(
        frame_dir, text="Ciclos até Recuperação (Barreira):", font=("Segoe UI", 10, "bold"),
        fg="#cdd6f4", bg="#252538"
    ).pack(anchor="w", pady=(8, 0))
    tk.Scale(
        frame_dir, from_=1, to=12, resolution=1, orient=tk.HORIZONTAL,
        variable=recup_var, bg="#252538", fg="#ffffff", highlightthickness=0
    ).pack(fill=tk.X)

    tk.Label(
        frame_dir, text="Intervalo entre Gerações (ms):", font=("Segoe UI", 10, "bold"),
        fg="#cdd6f4", bg="#252538"
    ).pack(anchor="w", pady=(8, 0))
    tk.Scale(
        frame_dir, from_=40, to=600, resolution=20, orient=tk.HORIZONTAL,
        variable=velocidade_var, bg="#252538", fg="#ffffff", highlightthickness=0
    ).pack(fill=tk.X)

    # Interação com o mouse
    tk.Label(
        frame_dir, text="\nClique/Arraste na Plantação para:", font=("Segoe UI", 10, "bold"),
        fg="#cdd6f4", bg="#252538"
    ).pack(anchor="w")
    opcoes_mouse = [
        ("🔴 Contaminar Parreira", "contaminar"),
        ("🔵 Criar Barreira Recuperada", "barreira"),
        ("🟢 Restaurar Parreira Saudável", "saudavel"),
    ]
    for texto, valor in opcoes_mouse:
        tk.Radiobutton(
            frame_dir, text=texto, variable=ferramenta_clique, value=valor,
            bg="#252538", fg="#cdd6f4", selectcolor="#1e1e2e",
            activebackground="#252538", activeforeground="#ffffff"
        ).pack(anchor="w")

    # Legenda explicativa
    quadro_legenda = tk.LabelFrame(
        frame_dir, text="Legenda de Estados", font=("Segoe UI", 9, "bold"),
        fg="#cdd6f4", bg="#252538", padx=8, pady=6
    )
    quadro_legenda.pack(fill=tk.X, pady=(14, 0))

    itens_legenda = [
        ("#2e7d32", "Parreira Saudável (Suscetível)"),
        ("#d32f2f", "Parreira Contaminada (Transmite)"),
        ("#ff9800", "Em Recuperação Final (Último ciclo)"),
        ("#1976d2", "Recuperada (Barreira de Contenção)"),
    ]
    for cor, desc in itens_legenda:
        f = tk.Frame(quadro_legenda, bg="#252538")
        f.pack(anchor="w", pady=2)
        tk.Frame(f, bg=cor, width=14, height=14).pack(side=tk.LEFT, padx=(0, 6))
        tk.Label(f, text=desc, font=("Segoe UI", 8), fg="#e0e0e0", bg="#252538").pack(side=tk.LEFT)

    desenhar_grade()
    root.mainloop()


def gerar_relatorio_acessivel_txt(
    caminho_arquivo: str = "relatorio_plantacao_uvas.txt",
    linhas: int = 20,
    colunas: int = 20,
    horizonte_t: int = 50,
) -> None:
    """
    Executa 3 ensaios independentes da simulação em horizonte T=50 ciclos e
    gera um relatório tabular e visual em texto simples (.txt) adaptado para
    acessibilidade via leitores de tela (utilizando '.', 'X' e 'O').
    """
    simbolos_txt = {
        EstadoParreira.VAZIO: " ",
        EstadoParreira.SAUDAVEL: ".",
        EstadoParreira.CONTAMINADA: "X",
        EstadoParreira.BARREIRA_RECUPERADA: "O",
    }

    sementes_ensaios = [32, 1, 2]
    linhas_relatorio = []
    linhas_relatorio.append("=" * 76)
    linhas_relatorio.append(
        "RELATORIO ACESSIVEL DE SIMULACAO - AUTOMATO CELULAR (PLANTACAO DE UVAS)"
    )
    linhas_relatorio.append("=" * 76)
    linhas_relatorio.append(f"Dimensoes da Grade (Reticulado): {linhas} x {colunas} ({linhas * colunas} parreiras)")
    linhas_relatorio.append(f"Horizonte Temporal estipulado (T): {horizonte_t} ciclos")
    linhas_relatorio.append("Topologia de Vizinhanca: Vizinhanca de Moore (8 parreiras adjacentes)")
    linhas_relatorio.append("Legenda Acessivel de Estados:")
    linhas_relatorio.append("  [.] Saudavel / Suscetivel (S) : Parreira sadia e produtiva")
    linhas_relatorio.append("  [X] Contaminada / Infectada (I): Parreira infectada que transmite a praga")
    linhas_relatorio.append("  [O] Recuperada / Barreira (R) : Parreira recuperada que atua como barreira de contencao")
    linhas_relatorio.append("-" * 76)

    resumo_ensaios = []

    for idx_ensaio, semente in enumerate(sementes_ensaios, start=1):
        automato = AutomatoPlantacaoUvas(
            linhas=linhas,
            colunas=colunas,
            prob_contagio=0.16,
            tempo_recuperacao=2,
            vizinhanca_moore=True,
            semente=semente,
        )
        automato.reiniciar_plantacao("foco_com_barreira_parcial")

        ciclo_extincao = horizonte_t
        linhas_relatorio.append(f"\n>>> ENSAIO {idx_ensaio} (Semente Aleatoria = {semente}) <<<")
        linhas_relatorio.append("Ciclo | Saudaveis (S) | Contaminadas (I) | Recuperadas/Barreira (R)")
        linhas_relatorio.append("-" * 68)

        s0, c0, r0 = automato.contar_estados()
        linhas_relatorio.append(f"  {0:02d}  |      {s0:03d}      |       {c0:03d}        |           {r0:03d}")

        for ciclo in range(1, horizonte_t + 1):
            ainda_ativo = automato.avancar_geracao()
            s, c, r = automato.contar_estados()
            linhas_relatorio.append(f"  {ciclo:02d}  |      {s:03d}      |       {c:03d}        |           {r:03d}")
            if not ainda_ativo:
                ciclo_extincao = ciclo
                break

        s_fin, c_fin, r_fin = automato.contar_estados()
        resumo_ensaios.append((idx_ensaio, ciclo_extincao, s_fin, c_fin, r_fin))

        linhas_relatorio.append(
            f"\nEncerramento do surto no Ensaio {idx_ensaio}: Ciclo {ciclo_extincao} "
            f"(Parreiras Saudaveis preservadas: {s_fin}, Barreira formada: {r_fin})"
        )
        linhas_relatorio.append(f"Mapa Espacial Final da Plantacao (Ensaio {idx_ensaio} - Ciclo {ciclo_extincao}):")
        for l in range(automato.linhas):
            linha_mapa = " ".join(simbolos_txt[automato.grade[l][c]] for c in range(automato.colunas))
            linhas_relatorio.append("  " + linha_mapa)

    linhas_relatorio.append("\n" + "=" * 76)
    linhas_relatorio.append(f"RESUMO DOS ENSAIOS DA SIMULACAO (T = {horizonte_t} CICLOS)")
    linhas_relatorio.append("=" * 76)
    linhas_relatorio.append(
        "Ensaio   | Ciclo de Extincao | Duracao do Surto | Saudaveis (S) | Barreira (R)"
    )
    linhas_relatorio.append("-" * 76)
    for ensaio_id, extincao, s_fin, _c_fin, r_fin in resumo_ensaios:
        linhas_relatorio.append(
            f"Ensaio {ensaio_id} | Ciclo {extincao:02d}          | {extincao:02d} ciclos        | {s_fin:03d}           | {r_fin:03d}"
        )
    linhas_relatorio.append("=" * 76)

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_relatorio) + "\n")

    print(f"Relatório acessível gerado em: {caminho_arquivo}")
    for ensaio_id, extincao, s_fin, _c_fin, r_fin in resumo_ensaios:
        print(f"  Ensaio {ensaio_id}: Extinção no Ciclo {extincao} | Saudáveis: {s_fin} | Barreira: {r_fin}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Autômato Celular de Plantação de Uvas com Contaminação e Barreira de Contenção"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Executa a simulação no modo texto (terminal) em vez de abrir a janela gráfica.",
    )
    parser.add_argument(
        "--relatorio",
        action="store_true",
        help="Executa os 3 ensaios (T=50) e gera o relatório .txt acessível para leitores de tela.",
    )
    parser.add_argument(
        "--passos",
        type=int,
        default=25,
        help="Número máximo de gerações no modo --cli (padrão: 25).",
    )
    args = parser.parse_args()

    if args.relatorio:
        gerar_relatorio_acessivel_txt()
    elif args.cli:
        executar_modo_terminal(passos=args.passos, intervalo=0.05)
    else:
        iniciar_interface_grafica()

