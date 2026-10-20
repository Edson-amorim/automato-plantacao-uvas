"""
Gera o artigo científico limpo (sem caracteres Markdown como * ou #) em formato
Word (.docx) e Texto Puro (.txt), baseado diretamente no arquivo modelo de C:\\jones:
'Simulação da Propagação de Células Infectadas por Autômatos Celulares em Ambiente Python.docx'
"""

import glob
import shutil
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace("w", NS_W)
ET.register_namespace("r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships")
ET.register_namespace("m", "http://schemas.openxmlformats.org/officeDocument/2006/math")
ET.register_namespace("wp", "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing")
ET.register_namespace("w14", "http://schemas.microsoft.com/office/word/2010/wordml")


TITULO = (
    "Simulação da Propagação de Pragas e Barreira de Contenção em Plantação de Uvas "
    "por Autômatos Celulares em Ambiente Python"
)

AUTOR = "Edson José de Amorim Oliveira1"
AFILIACAO = (
    "1Departamento de Estatística e Informática\n"
    "Universidade Federal Rural de Pernambuco – Recife, PE – Brasil"
)
EMAIL = "edson.amorim@ufrpe.br"

RESUMO_CORPO = (
    "As pragas agrícolas e doenças fúngicas em vinhedos representam um dos desafios mais "
    "complexos para a viticultura contemporânea. A modelagem computacional in silico tem se "
    "consolidado como uma ferramenta essencial para a compreensão dos mecanismos de disseminação "
    "fitopatogênica e da contenção espacial de surtos em cultivos perenes. Este trabalho apresenta "
    "o desenvolvimento de um modelo computacional baseado em Autômatos Celulares (AC), implementado "
    "na linguagem Python e validado por Desenvolvimento Orientado a Testes (TDD com Pytest), para "
    "analisar a dinâmica de contágio e propagação espacial de uma parreira contaminada sobre uma "
    "população de parreiras sadias, bem como sua posterior recuperação atuando como barreira de "
    "contenção. A simulação foi executada ao longo de 50 ciclos temporais, modelando as transições "
    "de estado, a mecânica da vizinhança espacial de Moore e o impacto do tempo de recuperação das "
    "parreiras na proteção do vinhedo. Os resultados incluem a análise quantitativa da curva "
    "epidemiológica, suíte de testes automatizados e relatórios em formato .txt adaptados para "
    "acessibilidade via leitores de tela."
)

SEC1_TITULO = "1. Introdução"
SEC1_P1 = (
    "A patogênese e a progressão de pragas e doenças fúngicas em plantações de uvas envolvem "
    "processos biológicos e espaciais altamente complexos, nos quais parreiras contaminadas "
    "interagem diretamente com o microambiente e com as videiras próximas ao seu redor. O estudo "
    "da dinâmica espacial de contaminação no parreiral fornece informações valiosas sobre como "
    "os focos iniciais de infecção se propagam para as plantas adjacentes e afetam a plantação "
    "como um todo."
)
SEC1_P2 = (
    "Nesse contexto, os Autômatos Celulares (AC) constituem um arcabouço matemático e "
    "computacional discreto ideal para simular sistemas agrícolas em que regras locais de "
    "proximidade determinam o comportamento emergente global. O objetivo deste trabalho é "
    "formalizar um modelo de AC em Python capaz de simular a mecânica de contágio entre "
    "parreiras contaminadas e sadias, avaliando o papel do raio de vizinhança de Moore, das "
    "taxas de propagação, da validação automatizada via TDD com Pytest e da recuperação das "
    "parreiras, que passam a atuar como barreira de contenção contra o avanço da praga."
)

SEC2_TITULO = "2. Detalhamento do Modelo Computacional"
SEC2_P1 = (
    "O modelo foi construído em Python e utiliza matrizes bidimensionais para representar a "
    "estrutura espacial da plantação de uvas, contando com verificação automatizada de regras "
    "por meio do framework Pytest (TDD). A grade espacial é definida como um reticulado discreto "
    "de dimensões 50 por 50."
)
SEC2_P2 = (
    "A grade abriga um total de 2.500 células (parreiras). Cada parreira localizada na posição "
    "(i, j) no instante de tempo t possui um estado E(i, j, t) pertencente ao conjunto {S, I, R}, "
    "baseado em uma adaptação do modelo epidemiológico SIR:"
)
SEC2_B1 = (
    "Saudável / Suscetível (S): Parreira sadia, produtiva e suscetível à contaminação induzida "
    "por parreiras próximas infectadas. Representada graficamente pelo caractere . no relatório impresso."
)
SEC2_B2 = (
    "Contaminada / Infectada (I): Parreira infectada que expressa o vetor de contágio, capaz de "
    "transmitir a praga para suas vizinhas diretas na vizinhança de Moore. Representada pelo caractere X."
)
SEC2_B3 = (
    "Recuperada / Barreira de Contenção (R): Parreira que completou seu período infeccioso e "
    "se recuperou, tornando-se imune e atuando como barreira mecânica e biológica de contenção "
    "que impede a passagem da infecção para as parreiras sadias adjacentes. Representada pelo caractere O."
)

SEC3_TITULO = "3. Resultados e Discussão"
SEC3_P1 = (
    "Para avaliar a estabilidade do modelo computacional, a exatidão das regras verificadas "
    "pelos testes em TDD (Pytest) e a dinâmica de propagação do contágio na grade celular da "
    "plantação de uvas, foram executadas três replicações independentes da simulação sob as "
    "mesmas condições iniciais, durante um horizonte temporal fixado em T = 50 ciclos."
)
SEC3_P2 = (
    "Os dados empíricos obtidos revelaram uma convergência no comportamento dinâmico do sistema:"
)
SEC3_P3 = (
    "Encerramento do surto: Em todas as simulações, o ciclo epidemiológico atingiu a extinção "
    "(ausência de novas parreiras na condição Contaminada) entre os ciclos 21 e 24, consolidando "
    "a barreira de contenção."
)
SEC3_B1 = "Ensaio 1: A propagação encerrou-se no 21º ciclo (341 parreiras saudáveis preservadas e 2.159 recuperadas em barreira)."
SEC3_B2 = "Ensaio 2: A propagação encerrou-se no 22º ciclo (368 parreiras saudáveis preservadas e 2.132 recuperadas em barreira)."
SEC3_B3 = "Ensaio 3: A propagação encerrou-se no 24º ciclo (388 parreiras saudáveis preservadas e 2.112 recuperadas em barreira)."
SEC3_TAB_TITULO = "Resumo dos Ensaios da Simulação (T = 50 ciclos)"
SEC3_P4 = (
    "A interrupção da contaminação — ocorrida na primeira metade do tempo total estipulado — "
    "evidencia o papel determinante da taxa de transição para o estado Recuperada / Barreira de "
    "Contenção (R) e da vizinhança mecânica de Moore. As parreiras que transitaram para o estado "
    "R passaram a atuar como barreiras físicas e topológicas no reticulado discreto, bloqueando "
    "as vias de contágio das parreiras no estado Contaminada (I) e impedindo a infecção total da "
    "população de parreiras Suscetíveis (S). Esse comportamento também foi comprovado "
    "deterministicamente pela suíte de testes automatizados em Pytest, na qual um anel fechado "
    "de parreiras recuperadas isola integralmente um foco central de infecção."
)

SEC4_TITULO = "4. Conclusão"
SEC4_P1 = (
    "O modelo desenvolvido em Python demonstrou eficácia ao representar a dinâmica de "
    "contaminação entre parreiras próximas e sua posterior recuperação atuando como barreira "
    "de contenção por meio da abordagem de Autômatos Celulares baseada na topologia de Moore. "
    "A consistência observada nas replicações experimentais e nos testes automatizados via TDD "
    "(Pytest) confirma que a transição para o estado recuperado limita significativamente a "
    "expansão da praga na plantação de uvas, delimitando a duração da fase infecciosa ao "
    "intervalo entre 21 e 24 ciclos."
)
SEC4_P2 = (
    "Além do aporte teórico-computacional e dos gráficos gerados, a emissão de relatórios "
    "tabulares e descritivos em formato de texto simples (.txt) assegura a acessibilidade do "
    "software a leitores de tela, promovendo o uso inclusivo da ferramenta. Trabalhos futuros "
    "poderão explorar a variação probabilística induzida pela ação do vento entre as fileiras "
    "do vinhedo e diferentes protocolos de manejo preventivo."
)


def substituir_texto_paragrafo(p_elem: ET.Element, novo_texto: str, preservar_tab: bool = False) -> None:
    runs = p_elem.findall(f"{{{NS_W}}}r")
    if not runs:
        r = ET.SubElement(p_elem, f"{{{NS_W}}}r")
        t = ET.SubElement(r, f"{{{NS_W}}}t")
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        t.text = novo_texto
        return

    primeiro_run = runs[0]
    rPr = primeiro_run.find(f"{{{NS_W}}}rPr")
    tem_tab = primeiro_run.find(f"{{{NS_W}}}tab") is not None

    for r in runs:
        p_elem.remove(r)

    novo_r = ET.SubElement(p_elem, f"{{{NS_W}}}r")
    if rPr is not None:
        novo_r.append(rPr)
    if preservar_tab or tem_tab:
        ET.SubElement(novo_r, f"{{{NS_W}}}tab")
    novo_t = ET.SubElement(novo_r, f"{{{NS_W}}}t")
    novo_t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    novo_t.text = novo_texto


def preencher_resumo(p_elem: ET.Element, texto_corpo_resumo: str) -> None:
    runs = p_elem.findall(f"{{{NS_W}}}r")
    for r in runs:
        p_elem.remove(r)

    r1 = ET.SubElement(p_elem, f"{{{NS_W}}}r")
    rPr1 = ET.SubElement(r1, f"{{{NS_W}}}rPr")
    ET.SubElement(rPr1, f"{{{NS_W}}}rFonts", {
        f"{{{NS_W}}}ascii": "Times",
        f"{{{NS_W}}}cs": "Times",
        f"{{{NS_W}}}eastAsia": "Times",
        f"{{{NS_W}}}hAnsi": "Times",
    })
    ET.SubElement(rPr1, f"{{{NS_W}}}b", {f"{{{NS_W}}}val": "1"})
    ET.SubElement(rPr1, f"{{{NS_W}}}i", {f"{{{NS_W}}}val": "1"})
    t1 = ET.SubElement(r1, f"{{{NS_W}}}t", {"{http://www.w3.org/XML/1998/namespace}space": "preserve"})
    t1.text = "Resumo. "

    r2 = ET.SubElement(p_elem, f"{{{NS_W}}}r")
    rPr2 = ET.SubElement(r2, f"{{{NS_W}}}rPr")
    ET.SubElement(rPr2, f"{{{NS_W}}}rFonts", {
        f"{{{NS_W}}}ascii": "Times",
        f"{{{NS_W}}}cs": "Times",
        f"{{{NS_W}}}eastAsia": "Times",
        f"{{{NS_W}}}hAnsi": "Times",
    })
    ET.SubElement(rPr2, f"{{{NS_W}}}i", {f"{{{NS_W}}}val": "1"})
    t2 = ET.SubElement(r2, f"{{{NS_W}}}t", {"{http://www.w3.org/XML/1998/namespace}space": "preserve"})
    t2.text = texto_corpo_resumo


def atualizar_tabela_ensaios(tbl_elem: ET.Element) -> None:
    dados_linhas = [
        ["Ensaio", "Ciclo de Extinção da Infecção", "Duração do surto"],
        ["Ensaio 1", "Ciclo 21", "21 ciclos"],
        ["Ensaio 2", "Ciclo 22", "22 ciclos"],
        ["Ensaio 3", "Ciclo 24", "24 ciclos"],
    ]
    linhas_xml = tbl_elem.findall(f"{{{NS_W}}}tr")
    for idx_l, tr in enumerate(linhas_xml):
        if idx_l >= len(dados_linhas):
            break
        celulas_xml = tr.findall(f"{{{NS_W}}}tc")
        for idx_c, tc in enumerate(celulas_xml):
            if idx_c >= len(dados_linhas[idx_l]):
                break
            p = tc.find(f"{{{NS_W}}}p")
            if p is not None:
                substituir_texto_paragrafo(p, dados_linhas[idx_l][idx_c], preservar_tab=False)


def montar_texto_limpo() -> str:
    """Retorna o texto integral do artigo completamente limpo, sem * ou #."""
    blocos = [
        TITULO,
        "",
        AUTOR,
        AFILIACAO,
        EMAIL,
        "",
        f"Resumo. {RESUMO_CORPO}",
        "",
        SEC1_TITULO,
        SEC1_P1,
        SEC1_P2,
        "",
        SEC2_TITULO,
        SEC2_P1,
        SEC2_P2,
        f"- {SEC2_B1}",
        f"- {SEC2_B2}",
        f"- {SEC2_B3}",
        "",
        SEC3_TITULO,
        SEC3_P1,
        SEC3_P2,
        SEC3_P3,
        f"- {SEC3_B1}",
        f"- {SEC3_B2}",
        f"- {SEC3_B3}",
        "",
        SEC3_TAB_TITULO,
        "Ensaio | Ciclo de Extinção da Infecção | Duração do surto",
        "Ensaio 1 | Ciclo 21 | 21 ciclos",
        "Ensaio 2 | Ciclo 22 | 22 ciclos",
        "Ensaio 3 | Ciclo 24 | 24 ciclos",
        "",
        SEC3_P4,
        "",
        SEC4_TITULO,
        SEC4_P1,
        SEC4_P2,
    ]
    return "\n".join(blocos) + "\n"


def gerar_docx_artigo() -> None:
    arquivos_modelo = glob.glob(r"C:\jones\Simula*C*lulas*Python.docx")
    if not arquivos_modelo:
        arquivos_modelo = glob.glob(r"C:\jones\Simula*Python.docx")
    caminho_modelo = arquivos_modelo[0]

    nome_arquivo_saida = "Simulação da Propagação em Plantação de Uvas por Autômatos Celulares em Ambiente Python.docx"
    caminho_saida_projeto = Path(r"C:\automato_plantacao_uvas") / nome_arquivo_saida
    caminho_saida_jones = Path(r"C:\jones") / nome_arquivo_saida
    caminho_saida_downloads = Path(r"C:\Users\edson\Downloads") / nome_arquivo_saida

    with zipfile.ZipFile(caminho_modelo, "r") as zin:
        xml_bytes = zin.read("word/document.xml")
        outros_arquivos = {
            item.filename: zin.read(item.filename)
            for item in zin.infolist()
            if item.filename != "word/document.xml"
        }

    root = ET.fromstring(xml_bytes)
    body = root.find(f"{{{NS_W}}}body")
    filhos = list(body)

    substituir_texto_paragrafo(filhos[0], TITULO)
    preencher_resumo(filhos[5], RESUMO_CORPO)

    substituir_texto_paragrafo(filhos[6], SEC1_TITULO)
    substituir_texto_paragrafo(filhos[7], SEC1_P1, preservar_tab=True)
    substituir_texto_paragrafo(filhos[8], SEC1_P2, preservar_tab=True)

    substituir_texto_paragrafo(filhos[9], SEC2_TITULO)
    substituir_texto_paragrafo(filhos[10], SEC2_P1, preservar_tab=True)
    substituir_texto_paragrafo(filhos[11], SEC2_P2, preservar_tab=True)
    substituir_texto_paragrafo(filhos[12], SEC2_B1)
    substituir_texto_paragrafo(filhos[13], SEC2_B2)
    substituir_texto_paragrafo(filhos[14], SEC2_B3)

    substituir_texto_paragrafo(filhos[15], SEC3_TITULO)
    substituir_texto_paragrafo(filhos[16], SEC3_P1, preservar_tab=True)
    substituir_texto_paragrafo(filhos[17], SEC3_P2, preservar_tab=True)
    substituir_texto_paragrafo(filhos[18], SEC3_P3)
    substituir_texto_paragrafo(filhos[19], SEC3_B1)
    substituir_texto_paragrafo(filhos[20], SEC3_B2)
    substituir_texto_paragrafo(filhos[21], SEC3_B3)
    substituir_texto_paragrafo(filhos[22], SEC3_TAB_TITULO)
    atualizar_tabela_ensaios(filhos[23])
    substituir_texto_paragrafo(filhos[24], SEC3_P4, preservar_tab=True)

    substituir_texto_paragrafo(filhos[25], SEC4_TITULO)
    substituir_texto_paragrafo(filhos[26], SEC4_P1)
    substituir_texto_paragrafo(filhos[27], SEC4_P2)

    novo_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)

    with zipfile.ZipFile(caminho_saida_projeto, "w", zipfile.ZIP_DEFLATED) as zout:
        zout.writestr("word/document.xml", novo_xml)
        for nome_arq, conteudo in outros_arquivos.items():
            zout.writestr(nome_arq, conteudo)

    shutil.copy2(caminho_saida_projeto, caminho_saida_jones)
    shutil.copy2(caminho_saida_projeto, caminho_saida_downloads)

    texto_limpo = montar_texto_limpo()
    (Path(r"C:\automato_plantacao_uvas") / "artigo_limpo.txt").write_text(texto_limpo, encoding="utf-8")
    (Path(r"C:\jones") / "artigo_limpo.txt").write_text(texto_limpo, encoding="utf-8")
    print("[OK] Artigo limpo (.docx e .txt) gerado com sucesso sem caracteres * ou #.")


if __name__ == "__main__":
    gerar_docx_artigo()
