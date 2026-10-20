"""
Gera o artigo científico em formato Word (.docx) utilizando diretamente o arquivo
modelo localizado em C:\\jones:
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


def substituir_texto_paragrafo(p_elem: ET.Element, novo_texto: str, preservar_tab: bool = False) -> None:
    """Substitui o texto de um parágrafo mantendo a formatação original do modelo."""
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
    """Mantém o 'Resumo. ' em negrito/itálico e atualiza o texto do resumo."""
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
    """Atualiza os dados da tabela de Resumo dos Ensaios da Simulação (T = 50 ciclos)."""
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


def gerar_docx_artigo() -> None:
    arquivos_modelo = glob.glob(r"C:\jones\Simula*Python.docx")
    if not arquivos_modelo:
        raise FileNotFoundError("Arquivo modelo .docx não encontrado em C:\\jones.")
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

    # Child 00: Título (Heading1)
    substituir_texto_paragrafo(
        filhos[0],
        "Simulação da Propagação de Pragas e Barreira de Contenção em Plantação de Uvas por Autômatos Celulares em Ambiente Python",
    )

    # Child 05: Resumo
    preencher_resumo(
        filhos[5],
        "O controle fitossanitário em vinhedos representa um dos desafios mais complexos para a viticultura contemporânea. A modelagem computacional in silico tem se consolidado como uma ferramenta essencial para a compreensão dos mecanismos de disseminação fitopatogênica e da contenção de pragas agrícolas. Este trabalho apresenta o desenvolvimento de um modelo computacional baseado em Autômatos Celulares (AC), implementado na linguagem Python, para analisar a dinâmica de contágio e propagação espacial de uma parreira contaminada sobre uma plantação de parreiras sadias e sua posterior recuperação atuando como barreira de contenção. A simulação foi executada ao longo de 50 ciclos temporais, modelando as transições de estado, a mecânica da vizinhança espacial de Moore e o impacto do tempo de recuperação das parreiras na formação da barreira. Os resultados incluem a análise quantitativa da curva epidemiológica e relatórios em formato .txt adaptados para acessibilidade via leitores de tela.",
    )

    # Child 06: 1. Introdução
    substituir_texto_paragrafo(filhos[6], "1. Introdução")

    # Child 07: Parágrafo 1 da Introdução
    substituir_texto_paragrafo(
        filhos[7],
        "A disseminação de fitopatógenos e a progressão de pragas em plantações de uvas (Vitis vinifera) envolvem processos biológicos e espaciais altamente complexos, nos quais parreiras contaminadas interagem diretamente com o microambiente e com as videiras ao seu redor. O estudo da dinâmica espacial de contaminação entre parreiras próximas fornece insights valiosos sobre como focos locais de infecção se propagam e afetam o parreiral como um todo.",
        preservar_tab=True,
    )

    # Child 08: Parágrafo 2 da Introdução
    substituir_texto_paragrafo(
        filhos[8],
        "Nesse contexto, os Autômatos Celulares (AC) constituem um arcabouço matemático e computacional discreto ideal para simular sistemas agrícolas em que regras locais determinam o comportamento emergente global. O objetivo deste trabalho é formalizar um modelo de AC capaz de simular a mecânica de contágio entre parreiras contaminadas e sadias, avaliando o papel do raio de vizinhança, das taxas de propagação e da formação de recuperação fitossanitária atuando como barreira de contenção contra o avanço da praga na plantação.",
        preservar_tab=True,
    )

    # Child 09: 2. Detalhamento do Modelo Computacional
    substituir_texto_paragrafo(filhos[9], "2. Detalhamento do Modelo Computacional")

    # Child 10: Parágrafo 1 do Modelo
    substituir_texto_paragrafo(
        filhos[10],
        "O modelo foi construído em Python e utiliza matrizes bidimensionais (biblioteca NumPy e visualização com Matplotlib/Tkinter) para representar a estrutura espacial da plantação de uvas. A grade espacial é definida como um reticulado discreto de dimensões 50 x 50.",
        preservar_tab=True,
    )

    # Child 11: Parágrafo 2 do Modelo
    substituir_texto_paragrafo(
        filhos[11],
        "A grade abriga um total de 2.500 células (parreiras de uva). Cada parreira localizada na posição (i, j) no instante de tempo t possui um estado E(i, j, t) pertencente a {S, I, R}, baseado em uma adaptação do modelo epidemiológico SIR:",
        preservar_tab=True,
    )

    # Child 12: Bullet 1 - Saudável / Suscetível (S)
    substituir_texto_paragrafo(
        filhos[12],
        "Saudável / Suscetível (S): Parreira sadia, produtiva e suscetível à contaminação induzida por parreiras adjacentes infectadas na vizinhança de Moore. Representada graficamente pelo caractere . no relatório impresso.",
    )

    # Child 13: Bullet 2 - Contaminada / Infectada (I)
    substituir_texto_paragrafo(
        filhos[13],
        "Contaminada / Infectada (I): Parreira infectada que expressa o vetor de contágio, capaz de transmitir a praga para as parreiras vizinhas próximas durante seu ciclo infeccioso. Representada pelo caractere X.",
    )

    # Child 14: Bullet 3 - Recuperada / Barreira de Contenção (R)
    substituir_texto_paragrafo(
        filhos[14],
        "Recuperada / Barreira de Contenção (R): Parreira que completou seu período infeccioso e recuperou-se, tornando-se imune e atuando como barreira mecânica e biológica de contenção que bloqueia o avanço da contaminação. Representada pelo caractere O.",
    )

    # Child 15: 3. Resultados e Discussão
    substituir_texto_paragrafo(filhos[15], "3. Resultados e Discussão")

    # Child 16: Parágrafo 1 de Resultados
    substituir_texto_paragrafo(
        filhos[16],
        "Para avaliar a estabilidade do modelo computacional e a dinâmica de propagação do contágio e formação de barreira na plantação de uvas, foram executadas três replicações independentes da simulação sob as mesmas condições iniciais, durante um horizonte temporal fixado em T = 50 ciclos.",
        preservar_tab=True,
    )

    # Child 17: Parágrafo 2 de Resultados
    substituir_texto_paragrafo(
        filhos[17],
        "Os dados empíricos obtidos revelaram uma convergência no comportamento dinâmico do sistema:",
        preservar_tab=True,
    )

    # Child 18: Encerramento do surto
    substituir_texto_paragrafo(
        filhos[18],
        "Encerramento do surto: Em todas as simulações, o ciclo epidemiológico atingiu a extinção (ausência de novas parreiras na condição Contaminada) entre os ciclos 21 e 24.",
    )

    # Child 19, 20, 21: Bullets dos 3 Ensaios
    substituir_texto_paragrafo(
        filhos[19],
        "Ensaio 1: A propagação encerrou-se no 21º ciclo (341 parreiras saudáveis preservadas e 2.159 recuperadas em barreira).",
    )
    substituir_texto_paragrafo(
        filhos[20],
        "Ensaio 2: A propagação encerrou-se no 22º ciclo (368 parreiras saudáveis preservadas e 2.132 recuperadas em barreira).",
    )
    substituir_texto_paragrafo(
        filhos[21],
        "Ensaio 3: A propagação encerrou-se no 24º ciclo (388 parreiras saudáveis preservadas e 2.112 recuperadas em barreira).",
    )

    # Child 22: Título da Tabela
    substituir_texto_paragrafo(
        filhos[22],
        "Resumo dos Ensaios da Simulação (T = 50 ciclos)",
    )

    # Child 23: Tabela
    atualizar_tabela_ensaios(filhos[23])

    # Child 24: Discussão pós-tabela
    substituir_texto_paragrafo(
        filhos[24],
        "A interrupção da contaminação — ocorrida na primeira metade do tempo total estipulado — evidencia o papel determinante da taxa de transição para o estado Recuperada / Barreira de Contenção (R) e da vizinhança espacial. As parreiras que transitaram para o estado R passaram a atuar como barreiras físicas e topológicas no reticulado discreto da plantação, bloqueando as vias de contágio das parreiras no estado Contaminada (I) e impedindo a infecção total da população de parreiras Suscetíveis (S).",
        preservar_tab=True,
    )

    # Child 25: 4. Conclusão
    substituir_texto_paragrafo(filhos[25], "4. Conclusão")

    # Child 26: Parágrafo 1 da Conclusão
    substituir_texto_paragrafo(
        filhos[26],
        "O modelo desenvolvido em Python demonstrou eficácia ao representar a dinâmica de contaminação entre parreiras de uva e sua posterior recuperação atuando como barreira de contenção por meio da abordagem de Autômatos Celulares baseada na topologia de Moore. A consistência observada nas replicações experimentais confirma que a transição para o estado recuperado/barreira limita significativamente a expansão da praga no vinhedo, delimitando a duração da fase infecciosa ao intervalo entre 21 e 24 ciclos.",
    )

    # Child 27: Parágrafo 2 da Conclusão
    substituir_texto_paragrafo(
        filhos[27],
        "Além do aporte teórico-computacional e da visualização gráfica, a geração de relatórios descritivos e matriciais em formato de texto simples (.txt) assegura a acessibilidade do software a leitores de tela, promovendo o uso inclusivo da ferramenta. Trabalhos futuros poderão explorar a influência da direção do vento entre as fileiras do parreiral e diferentes estratégias de manejo fitossanitário preventivo.",
    )

    novo_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)

    with zipfile.ZipFile(caminho_saida_projeto, "w", zipfile.ZIP_DEFLATED) as zout:
        zout.writestr("word/document.xml", novo_xml)
        for nome_arq, conteudo in outros_arquivos.items():
            zout.writestr(nome_arq, conteudo)

    shutil.copy2(caminho_saida_projeto, caminho_saida_jones)
    shutil.copy2(caminho_saida_projeto, caminho_saida_downloads)
    print(f"[OK] Artigo .docx gerado a partir de C:\\jones em:\n  1) {caminho_saida_projeto}\n  2) {caminho_saida_jones}\n  3) {caminho_saida_downloads}")


if __name__ == "__main__":
    gerar_docx_artigo()
