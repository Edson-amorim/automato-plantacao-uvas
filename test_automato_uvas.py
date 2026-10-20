"""
Suíte de Testes Orientada a Comportamento / TDD com Pytest
==========================================================
Valida as regras de transição do Autômato Celular da plantação de uvas:
1. Inicialização do reticulado 50x50 (2.500 parreiras) e conservação populacional (S + I + R = N).
2. Contágio espacial entre parreiras próximas na vizinhança de Moore.
3. Recuperação da parreira após o período infeccioso (TEMPO_RECUPERACAO).
4. Atuação das parreiras recuperadas como barreira de contenção (imunidade e bloqueio).
5. Geração de representações textuais ('.', 'X', 'O') e descrições acessíveis para leitores de tela.
"""

import numpy as np
import pytest

import index
from automato_uvas import AutomatoPlantacaoUvas, EstadoParreira


# ============================================================================
# Testes TDD para o módulo principal de simulação matricial (index.py)
# ============================================================================

def test_inicializacao_grade_50x50_e_conservacao():
    """Garante que a plantação inicia com 50x50 (2.500 parreiras) e soma S + I + R = 2500."""
    grade, tempo_infeccao = index.inicializar_plantacao(semente=18)
    assert grade.shape == (50, 50)
    assert tempo_infeccao.shape == (50, 50)

    s, i, r = index.contar_estados(grade)
    assert s + i + r == 2500
    assert i > 0, "Deve haver ao menos uma parreira inicialmente contaminada com a semente 18"
    assert r == 0, "Nenhuma parreira deve iniciar no estado recuperado no ciclo 0"


def test_transicao_contaminada_para_recuperada_barreira():
    """
    Verifica se uma parreira contaminada se recupera exatamente após TEMPO_RECUPERACAO ciclos
    e passa para o estado RECUPERADA_BARREIRA.
    """
    grade = np.full((index.TAMANHO, index.TAMANHO), index.SAUDAVEL, dtype=int)
    tempo_infeccao = np.zeros((index.TAMANHO, index.TAMANHO), dtype=int)

    # Isola o teste de recuperação fixando probabilidade de contágio zero temporariamente
    prob_original = index.PROB_CONTAGIO
    index.PROB_CONTAGIO = 0.0
    try:
        grade[25, 25] = index.CONTAMINADA
        for ciclo in range(1, index.TEMPO_RECUPERACAO):
            index.atualizar(grade, tempo_infeccao)
            assert grade[25, 25] == index.CONTAMINADA, (
                f"A parreira ainda deveria estar contaminada no ciclo {ciclo}"
            )

        # No ciclo igual a TEMPO_RECUPERACAO, deve se recuperar e virar barreira
        index.atualizar(grade, tempo_infeccao)
        assert grade[25, 25] == index.RECUPERADA_BARREIRA
        assert tempo_infeccao[25, 25] == 0
    finally:
        index.PROB_CONTAGIO = prob_original


def test_barreira_de_contencao_imune_e_bloqueia_contagio():
    """
    Verifica que parreiras no estado RECUPERADA_BARREIRA:
    1) São imunes (não voltam ao estado CONTAMINADA).
    2) Bloqueiam a contaminação de uma parreira saudável quando há >= 3 vizinhas em barreira.
    """
    grade = np.full((index.TAMANHO, index.TAMANHO), index.SAUDAVEL, dtype=int)
    tempo_infeccao = np.zeros((index.TAMANHO, index.TAMANHO), dtype=int)

    # Parreira saudável em (10, 10) protegida por 3 parreiras recuperadas (barreira)
    grade[10, 10] = index.SAUDAVEL
    grade[9, 9] = index.RECUPERADA_BARREIRA
    grade[9, 10] = index.RECUPERADA_BARREIRA
    grade[9, 11] = index.RECUPERADA_BARREIRA

    # Mesmo com uma parreira contaminada adjacente em (11, 10) e probabilidade 100%,
    # a barreira de contenção ao redor deve proteger a parreira (10, 10)
    grade[11, 10] = index.CONTAMINADA

    prob_original = index.PROB_CONTAGIO
    index.PROB_CONTAGIO = 1.0
    try:
        index.atualizar(grade, tempo_infeccao)
        # As parreiras da barreira permanecem intactas (imunes)
        assert grade[9, 9] == index.RECUPERADA_BARREIRA
        assert grade[9, 10] == index.RECUPERADA_BARREIRA
        assert grade[9, 11] == index.RECUPERADA_BARREIRA
        # A parreira saudável protegida pela barreira não foi contaminada
        assert grade[10, 10] == index.SAUDAVEL
    finally:
        index.PROB_CONTAGIO = prob_original


def test_formatacao_acessivel_para_leitores_de_tela():
    """Valida a representação textual ('.', 'X', 'O') e o resumo narrativo acessível."""
    grade = np.full((index.TAMANHO, index.TAMANHO), index.SAUDAVEL, dtype=int)
    grade[0, 0] = index.CONTAMINADA
    grade[0, 1] = index.RECUPERADA_BARREIRA

    texto_grade = index.grade_para_texto(grade)
    primeira_linha = texto_grade.splitlines()[0]
    assert primeira_linha.startswith("XO.")

    desc_crescimento = index.gerar_descricao_acessivel(1, 2400, 80, 20, i_anterior=30)
    assert "cresceu" in desc_crescimento

    desc_recuo = index.gerar_descricao_acessivel(2, 2350, 40, 110, i_anterior=80)
    assert "recuou" in desc_recuo

    desc_fim = index.gerar_descricao_acessivel(21, 341, 0, 2159, i_anterior=5)
    assert "Surto encerrado" in desc_fim


# ============================================================================
# Testes TDD para a classe AutomatoPlantacaoUvas (automato_uvas.py)
# ============================================================================

@pytest.mark.parametrize("moore,esperado", [(True, 8), (False, 4)])
def test_vizinhanca_moore_vs_von_neumann(moore, esperado):
    """Testa a contagem de vizinhos contaminados nas topologias de Moore (8) e Von Neumann (4)."""
    automato = AutomatoPlantacaoUvas(linhas=5, colunas=5, vizinhanca_moore=moore)
    for l in range(5):
        for c in range(5):
            automato.grade[l][c] = EstadoParreira.CONTAMINADA
    automato.grade[2][2] = EstadoParreira.SAUDAVEL

    assert automato.contar_vizinhos_contaminados(2, 2) == esperado


def test_anel_barreira_isola_foco_central():
    """
    Prova por TDD que um anel fechado de parreiras recuperadas (BARREIRA_RECUPERADA)
    isola 100% um foco de contaminação central, impedindo qualquer vazamento para o vinhedo externo.
    """
    automato = AutomatoPlantacaoUvas(
        linhas=9,
        colunas=9,
        prob_contagio=1.0,  # Mesmo com 100% de chance de contágio
        tempo_recuperacao=3,
        vizinhanca_moore=True,
    )
    # Limpa toda a plantação como saudável
    for l in range(9):
        for c in range(9):
            automato.grade[l][c] = EstadoParreira.SAUDAVEL
            automato.tempo_infeccao[l][c] = 0

    # Foco contaminado no centro (4, 4)
    automato.infectar_parreira(4, 4)

    # Anel de parreiras recuperadas (barreira de contenção) cercando o centro
    for dl in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if (dl, dc) != (0, 0):
                automato.definir_barreira(4 + dl, 4 + dc)

    saudaveis_iniciais, _, _ = automato.contar_estados()

    # Avança 10 gerações até a extinção completa do foco central
    for _ in range(10):
        automato.avancar_geracao()

    saudaveis_finais, contaminadas_finais, recuperadas_finais = automato.contar_estados()

    assert contaminadas_finais == 0, "O foco central deve ter se recuperado completamente"
    assert saudaveis_finais == saudaveis_iniciais, (
        "Nenhuma parreira externa ao anel de contenção pode ter sido contaminada"
    )
    assert recuperadas_finais == 9, "As 8 parreiras da barreira + 1 central recuperada devem somar 9"
