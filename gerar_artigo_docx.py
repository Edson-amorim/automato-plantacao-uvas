"""
Gera o artigo científico em formato Word (.docx) seguindo exatamente a formatação,
estilos, fontes e estrutura do arquivo modelo do autor:
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
    """Substitui o texto de um parágrafo mantendo a formatação (w:pPr e w:rPr do primeiro run)."""
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

    # Remove runs antigos
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

    # Run 1: "Resumo. " em negrito e itálico
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

    # Run 2: Corpo do resumo em itálico
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
        ["Ensaio", "Ciclo de Extinção da Infecção", "Duração do surto e Contenção Final"],
        ["Ensaio 1", "Ciclo 20", "20 ciclos (221 saudáveis / 179 barreira)"],
        ["Ensaio 2", "Ciclo 22", "22 ciclos (241 saudáveis / 159 barreira)"],
        ["Ensaio 3", "Ciclo 24", "24 ciclos (267 saudáveis / 133 barreira)"],
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
    arquivos_modelo = glob.glob(r"C:\Users\edson\Downloads\Simula*Python.docx")
    if not arquivos_modelo:
        raise FileNotFoundError("Arquivo modelo .docx não encontrado em Downloads.")
    caminho_modelo = arquivos_modelo[0]

    caminho_saida_projeto = Path(
        r"C:\automato_plantacao_uvas\Simulacao_Propagacao_Plantacao_Uvas_Automatos_Celulares_Python.docx"
    )
    caminho_saida_downloads = Path(
        r"C:\Users\edson\Downloads\Simulação da Propagação em Plantação de Uvas por Autômatos Celulares em Ambiente Python.docx"
    )

    shutil.copy2(caminho_modelo, caminho_saida_projeto)

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
        "Simulação da Propagação de Pragas e Barreira de Contenção em Plantações de Uvas por Autômatos Celulares em Ambiente Python",
    )

    # Child 01, 02, 03, 04: Autor, Filiação (UFRPE) e E-mail permanecem idênticos ao modelo

    # Child 05: Resumo
    preencher_resumo(
        filhos[5],
        "O controle fitossanitário em vinhedos representa um dos desafios mais estratégicos para a viticultura moderna, visto que patógenos fúngicos e pragas agrícolas propagam-se rapidamente entre parreiras adjacentes. A modelagem computacional in silico tem se consolidado como uma ferramenta essencial para a compreensão da disseminação espacial de doenças em cultivos perenes e para o planejamento de barreiras de manejo. Este trabalho apresenta o desenvolvimento de um modelo computacional baseado em Autômatos Celulares (AC), implementado na linguagem Python, para analisar a dinâmica de contaminação espacial a partir de uma parreira infectada sobre as parreiras próximas e sua posterior recuperação atuando como barreira de contenção. A simulação foi executada ao longo de 50 ciclos temporais (T = 50), modelando as transições probabilísticas de estado, a mecânica da vizinhança espacial de Moore e o efeito protetor das parreiras recuperadas na contenção do surto. Os resultados incluem visualização gráfica interativa, análise quantitativa da curva epidemiológica e relatórios em formato .txt adaptados para acessibilidade via leitores de tela.",
    )

    # Child 06: 1. Introdução
    substituir_texto_paragrafo(filhos[6], "1. Introdução")

    # Child 07: Parágrafo 1 da Introdução
    substituir_texto_paragrafo(
        filhos[7],
        "A disseminação de fitopatógenos em plantações de uvas (Vitis vinifera), como o míldio (Plasmopara viticola) e o oídio (Erysiphe necator), envolve processos biológicos e espaciais altamente dinâmicos, nos quais uma parreira contaminada interage diretamente com as parreiras próximas por meio da dispersão local de esporos e contato foliar. O estudo da dinâmica espacial de contaminação no parreiral fornece subsídios valiosos sobre como focos primários de infecção se alastram e como o manejo localizado pode proteger o vinhedo como um todo.",
        preservar_tab=True,
    )

    # Child 08: Parágrafo 2 da Introdução
    substituir_texto_paragrafo(
        filhos[8],
        "Nesse contexto, os Autômatos Celulares (AC) constituem um arcabouço matemático e computacional discreto ideal para simular sistemas agrícolas em que regras locais de interação entre plantas vizinhas determinam o comportamento epidemiológico emergente global. O objetivo deste trabalho é formalizar e implementar em Python um modelo de AC capaz de simular a mecânica de contaminação entre parreiras infectadas e saudáveis, avaliando o papel do raio de vizinhança de Moore, da taxa probabilística de contágio e da recuperação induzida das parreiras, que passam a atuar como verdadeiras barreiras físicas e biológicas de contenção contra o avanço da praga.",
        preservar_tab=True,
    )

    # Child 09: 2. Detalhamento do Modelo Computacional
    substituir_texto_paragrafo(filhos[9], "2. Detalhamento do Modelo Computacional")

    # Child 10: Parágrafo 1 do Modelo
    substituir_texto_paragrafo(
        filhos[10],
        "O modelo foi construído em Python (disponibilizado em repositório público com modos de execução em interface gráfica Tkinter, Matplotlib e terminal) e utiliza matrizes bidimensionais para representar a disposição espacial das fileiras do vinhedo. A grade espacial dos ensaios padrão é definida como um reticulado discreto de dimensões 20 x 20 (expansível para 30 x 42 na interface interativa).",
        preservar_tab=True,
    )

    # Child 11: Parágrafo 2 do Modelo
    substituir_texto_paragrafo(
        filhos[11],
        "A grade de ensaio abriga um total de N = 400 parreiras de uva. Cada célula localizada na posição (i, j) no instante de tempo discreto t possui um estado E(i, j, t) pertencente ao conjunto {S, I, R}, baseado em uma adaptação espacial do modelo epidemiológico SIR com formação de barreira:",
        preservar_tab=True,
    )

    # Child 12: Bullet 1 - Saudável / Suscetível (S)
    substituir_texto_paragrafo(
        filhos[12],
        "Parreira Saudável / Suscetível (S): Parreira sadia, produtiva e suscetível à contaminação induzida por parreiras adjacentes infectadas na vizinhança de Moore (8 vizinhas). A probabilidade de contágio em cada passo é dada por P = 1 - (1 - p)^k, onde p = 0,16 é a taxa base de transmissão por contato e k é o número de parreiras próximas contaminadas. Representada pelo caractere . no relatório impresso (.txt) e pela cor verde na simulação visual.",
    )

    # Child 13: Bullet 2 - Contaminada / Infectada (I)
    substituir_texto_paragrafo(
        filhos[13],
        "Parreira Contaminada / Infectada (I): Parreira acometida pelo patógeno que expressa o vetor de contágio durante T_rec = 2 ciclos infecciosos, sendo capaz de contaminar as parreiras próximas adjacentes. Representada pelo caractere X no relatório acessível e pela cor vermelha na interface gráfica.",
    )

    # Child 14: Bullet 3 - Recuperada / Barreira de Contenção (R)
    substituir_texto_paragrafo(
        filhos[14],
        "Parreira Recuperada / Barreira de Contenção (R): Parreira que completou seu período infeccioso (T_rec) e se recuperou após resposta fisiológica ou intervenção fitossanitária, tornando-se imune à reinfecção e atuando como barreira mecânica e biológica de contenção que bloqueia a propagação para as parreiras saudáveis protegidas atrás dela. Representada pelo caractere O no relatório .txt e pela cor azul na interface visual.",
    )

    # Child 15: 3. Resultados e Discussão
    substituir_texto_paragrafo(filhos[15], "3. Resultados e Discussão")

    # Child 16: Parágrafo 1 de Resultados
    substituir_texto_paragrafo(
        filhos[16],
        "Para avaliar a estabilidade do modelo computacional, a dinâmica de contaminação entre parreiras próximas e a eficácia da formação da barreira de contenção na grade celular, foram executadas três replicações independentes da simulação (Ensaios 1, 2 e 3) sob o cenário de foco de infecção com linha de contenção, durante um horizonte temporal fixado em T = 50 ciclos.",
        preservar_tab=True,
    )

    # Child 17: Parágrafo 2 de Resultados
    substituir_texto_paragrafo(
        filhos[17],
        "Os dados empíricos obtidos revelaram uma forte convergência no comportamento dinâmico do parreiral e na contenção efetiva da praga:",
        preservar_tab=True,
    )

    # Child 18: Encerramento do surto
    substituir_texto_paragrafo(
        filhos[18],
        "Encerramento do surto e proteção do vinhedo: Em todas as simulações, o ciclo epidemiológico atingiu a extinção completa do patógeno (ausência de parreiras na condição Contaminada) entre os ciclos 20 e 24, preservando a maioria das parreiras saudáveis intactas.",
    )

    # Child 19, 20, 21: Bullets dos 3 Ensaios
    substituir_texto_paragrafo(
        filhos[19],
        "Ensaio 1: A propagação encerrou-se no 20º ciclo, preservando 221 parreiras saudáveis (55,25%) protegidas por 179 parreiras recuperadas em barreira (44,75%).",
    )
    substituir_texto_paragrafo(
        filhos[20],
        "Ensaio 2: A propagação encerrou-se no 22º ciclo, preservando 241 parreiras saudáveis (60,25%) protegidas por 159 parreiras recuperadas em barreira (39,75%).",
    )
    substituir_texto_paragrafo(
        filhos[21],
        "Ensaio 3: A propagação encerrou-se no 24º ciclo, preservando 267 parreiras saudáveis (66,75%) protegidas por 133 parreiras recuperadas em barreira (33,25%).",
    )

    # Child 22: Título da Tabela
    substituir_texto_paragrafo(
        filhos[22],
        "Resumo dos Ensaios da Simulação na Plantação de Uvas (T = 50 ciclos)",
    )

    # Child 23: Tabela
    atualizar_tabela_ensaios(filhos[23])

    # Child 24: Discussão pós-tabela
    substituir_texto_paragrafo(
        filhos[24],
        "A interrupção da contaminação — ocorrida antes da metade do horizonte temporal estipulado (T = 50) — evidencia o papel determinante da transição para o estado Recuperada / Barreira de Contenção (R) combinada à topologia espacial de Moore. À medida que as primeiras parreiras contaminadas (I) completam seu ciclo e se recuperam, elas formam um cinturão contínuo de células no estado R ao redor da frente de invasão. Essas parreiras recuperadas passam a atuar como barreiras físicas e topológicas no reticulado discreto, bloqueando as rotas de contágio das parreiras ainda no estado I e impedindo que a praga alcance o restante da população de parreiras Saudáveis / Suscetíveis (S).",
        preservar_tab=True,
    )

    # Child 25: 4. Conclusão
    substituir_texto_paragrafo(filhos[25], "4. Conclusão")

    # Child 26: Parágrafo 1 da Conclusão
    substituir_texto_paragrafo(
        filhos[26],
        "O modelo desenvolvido em Python demonstrou elevada eficácia ao representar a dinâmica espacial de contaminação fitopatogênica em uma plantação de uvas por meio da abordagem de Autômatos Celulares baseada na vizinhança de Moore. A consistência observada nas replicações experimentais confirma que a recuperação das parreiras e sua atuação como barreira de contenção limitam decisivamente a expansão da praga, extinguindo o surto entre 20 e 24 ciclos e preservando entre 55,25% e 66,75% do parreiral saudável.",
    )

    # Child 27: Parágrafo 2 da Conclusão
    substituir_texto_paragrafo(
        filhos[27],
        "Além da interface gráfica interativa e dos gráficos epidemiológicos, a geração automatizada de relatórios tabulares e mapas espaciais em formato de texto simples (.txt) assegura a plena acessibilidade do software a leitores de tela, promovendo o uso inclusivo da ferramenta científica. Trabalhos futuros poderão incorporar anisotropia induzida pela direção do vento entre as fileiras de parreiras e diferentes regimes de poda e pulverização preventiva.",
    )

    novo_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)

    with zipfile.ZipFile(caminho_saida_projeto, "w", zipfile.ZIP_DEFLATED) as zout:
        zout.writestr("word/document.xml", novo_xml)
        for nome_arq, conteudo in outros_arquivos.items():
            zout.writestr(nome_arq, conteudo)

    shutil.copy2(caminho_saida_projeto, caminho_saida_downloads)
    print(f"Artigo .docx gerado com sucesso em:\n  1) {caminho_saida_projeto}\n  2) {caminho_saida_downloads}")


if __name__ == "__main__":
    gerar_docx_artigo()
