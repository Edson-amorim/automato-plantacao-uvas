import numpy as np
import matplotlib.pyplot as plt

TAMANHO = 50  # Grade 50x50 (2500 parreiras de uva)
PROB_INICIAL = 0.01  # 1% de chance de uma parreira começar contaminada
PROB_CONTAGIO = 0.35  # Probabilidade de contaminação pelas parreiras próximas
TEMPO_RECUPERACAO = 3  # Ciclos até a parreira se recuperar e virar barreira de contenção
NUM_FRAMES = 50  # Quantidade de ciclos a simular (T = 50)

SAUDAVEL = 0
CONTAMINADA = 1
RECUPERADA_BARREIRA = 2

SIMBOLOS = {SAUDAVEL: '.', CONTAMINADA: 'X', RECUPERADA_BARREIRA: 'O'}


def inicializar_plantacao(semente=None):
    if semente is not None:
        np.random.seed(semente)
    grade = np.random.choice(
        [SAUDAVEL, CONTAMINADA],
        size=(TAMANHO, TAMANHO),
        p=[1 - PROB_INICIAL, PROB_INICIAL],
    )
    tempo_infeccao = np.zeros((TAMANHO, TAMANHO), dtype=int)
    return grade, tempo_infeccao


def atualizar(grade, tempo_infeccao):
    nova_grade = grade.copy()
    for i in range(TAMANHO):
        for j in range(TAMANHO):
            if grade[i, j] == CONTAMINADA:
                tempo_infeccao[i, j] += 1
                if tempo_infeccao[i, j] >= TEMPO_RECUPERACAO:
                    # A parreira contaminada se recupera e passa a atuar como barreira de contenção
                    nova_grade[i, j] = RECUPERADA_BARREIRA
                    tempo_infeccao[i, j] = 0
            elif grade[i, j] == SAUDAVEL:
                vizinhos = grade[max(0, i - 1):min(TAMANHO, i + 2), max(0, j - 1):min(TAMANHO, j + 2)]
                total_contaminadas = np.sum(vizinhos == CONTAMINADA)
                total_barreira = np.sum(vizinhos == RECUPERADA_BARREIRA)
                # Parreiras recuperadas ao redor atuam como barreira de contenção bloqueando o contágio
                if total_contaminadas >= 1 and total_barreira < 3:
                    if np.random.rand() < PROB_CONTAGIO:
                        nova_grade[i, j] = CONTAMINADA
    grade[:] = nova_grade[:]
    return grade


def contar_estados(grade):
    saudaveis = int(np.sum(grade == SAUDAVEL))
    contaminadas = int(np.sum(grade == CONTAMINADA))
    recuperadas = int(np.sum(grade == RECUPERADA_BARREIRA))
    return saudaveis, contaminadas, recuperadas


def grade_para_texto(grade):
    linhas = []
    for i in range(TAMANHO):
        linha = ''.join(SIMBOLOS[celula] for celula in grade[i])
        linhas.append(linha)
    return '\n'.join(linhas)


def gerar_descricao_acessivel(frame, s, i, r, i_anterior):
    """Gera um resumo narrativo claro para ser lido com facilidade por leitores de tela."""
    total = s + i + r
    perc_s = (s / total) * 100
    perc_i = (i / total) * 100
    perc_r = (r / total) * 100
    descricao = f"Ciclo {frame}: "
    descricao += f"{s} parreiras saudáveis ({perc_s:.1f}%), "
    descricao += f"{i} contaminadas ({perc_i:.1f}%) e "
    descricao += f"{r} recuperadas atuando como barreira de contenção ({perc_r:.1f}%). "
    if i_anterior is not None:
        diferenca = i - i_anterior
        if diferenca > 0:
            descricao += f"A contaminação cresceu: mais {diferenca} novas parreiras contaminadas."
        elif diferenca < 0:
            descricao += f"A contaminação recuou: menos {abs(diferenca)} parreiras contaminadas em relação ao ciclo anterior."
        else:
            descricao += "O número de parreiras contaminadas permaneceu estável."
    if i == 0 and frame > 0:
        descricao += " Surto encerrado (não há mais parreiras contaminadas; barreira de contenção consolidada)."
    return descricao


def executar_simulacao(semente=18, caminho_txt='saida_altomato.txt', caminho_png='grafico_epidemia.png'):
    grade, tempo_infeccao = inicializar_plantacao(semente)
    historico_s = []
    historico_i = []
    historico_r = []
    i_anterior = None
    ciclo_extincao = None

    with open(caminho_txt, 'w', encoding='utf-8') as arquivo:
        arquivo.write('============================================================\n')
        arquivo.write(' SIMULAÇÃO DE AUTÔMATO CELULAR - PLANTAÇÃO DE UVAS (SIR)\n')
        arquivo.write('============================================================\n')
        arquivo.write(f'Dimensões da plantação: {TAMANHO} por {TAMANHO} ({TAMANHO*TAMANHO} parreiras no total).\n')
        arquivo.write(f'Total de ciclos simulados: {NUM_FRAMES}.\n')
        arquivo.write('Legenda visual da grade:\n')
        arquivo.write('  . = Parreira Saudável | X = Parreira Contaminada | O = Recuperada (Barreira de Contenção)\n')
        arquivo.write('------------------------------------------------------------\n\n')

        for frame in range(NUM_FRAMES):
            s, i, r = contar_estados(grade)
            historico_s.append(s)
            historico_i.append(i)
            historico_r.append(r)
            if i == 0 and frame > 0 and ciclo_extincao is None:
                ciclo_extincao = frame

            descricao = gerar_descricao_acessivel(frame, s, i, r, i_anterior)
            arquivo.write(f'=== CICLO {frame} ===\n')
            arquivo.write(f'RESUMO DESCRITIVO: {descricao}\n\n')
            arquivo.write('MATRIZ VISUAL:\n')
            arquivo.write(grade_para_texto(grade))
            arquivo.write('\n\n' + '-' * 60 + '\n\n')

            i_anterior = i
            grade = atualizar(grade, tempo_infeccao)

    print(f'[OK] Relatório salvo em: {caminho_txt} (Extinção no Ciclo {ciclo_extincao})')

    if caminho_png:
        plt.figure(figsize=(10, 6))
        plt.plot(historico_s, label='Parreiras Saudáveis (S)', color='#2b5c8f', linewidth=2.5)
        plt.plot(historico_i, label='Parreiras Contaminadas (I)', color='#d9381e', linewidth=2.5)
        plt.plot(historico_r, label='Recuperadas / Barreira de Contenção (R)', color='#2d8a4e', linewidth=2.5)
        plt.title('Evolução Temporal da Contaminação e Barreira na Plantação de Uvas (Modelo SIR)', fontsize=13, fontweight='bold')
        plt.xlabel('Ciclos de Tempo', fontsize=12)
        plt.ylabel('Número de Parreiras', fontsize=12)
        plt.legend(fontsize=11)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig(caminho_png, dpi=300)
        plt.close()
        print(f'[OK] Gráfico colorido salvo em: {caminho_png}')


if __name__ == '__main__':
    # Executa os 3 ensaios independentes (T = 50 ciclos) e gera os relatórios .txt e o gráfico
    executar_simulacao(semente=18, caminho_txt='teste_01.txt', caminho_png='grafico_epidemia.png')
    executar_simulacao(semente=5, caminho_txt='teste_02.txt', caminho_png=None)
    executar_simulacao(semente=14, caminho_txt='teste_03.txt', caminho_png=None)
    executar_simulacao(semente=18, caminho_txt='saida_altomato.txt', caminho_png=None)
