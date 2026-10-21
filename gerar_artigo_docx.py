"""
Gera o artigo científico limpo (sem caracteres * ou #) em formato Word (.docx) e
Texto Puro (.txt), baseado no modelo de C:\\jones e fundamentado nos 4 arquivos
científicos da pasta C:\\altomatos:
1. CORREIA et al. (2011) - Fungos associados ao declínio da videira no Nordeste do Brasil (UFRPE/Embrapa).
2. NASCIMENTO; MARIANO (2004) - Cancro bacteriano da videira: etiologia, epidemiologia e medidas de controle (UFRPE/UNEB).
3. PEIXOTO (2005) - Sistemas Dinâmicos e Controladores Fuzzy: um Estudo da Dispersão da Morte Súbita dos Citros em São Paulo (UNICAMP).
4. RODRIGUES (2011) - Transmissão vertical e horizontal de parasitas usando autômatos celulares probabilísticos (UFPB).
"""

import copy
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
    "Simulação da Propagação de Fitopatógenos e Barreira de Contenção em Plantação de Uvas "
    "por Autômatos Celulares Probabilísticos em Ambiente Python"
)

AUTOR = "Edson José de Amorim Oliveira1"
AFILIACAO = (
    "1Departamento de Estatística e Informática\n"
    "Universidade Federal Rural de Pernambuco – Recife, PE – Brasil"
)
EMAIL = "edson.amorim@ufrpe.br"

RESUMO_CORPO = (
    "O Brasil destaca-se na produção mundial de uvas de mesa, concentrando na região Nordeste "
    "quase a totalidade das exportações nacionais, sobretudo no Vale do São Francisco. Todavia, "
    "enfermidades fitossanitárias como o declínio da videira associado a fungos fitopatogênicos "
    "(Correia et al., 2011) e o cancro bacteriano causado por Xanthomonas campestris pv. viticola "
    "(Nascimento; Mariano, 2004) representam severos desafios à viticultura. Este trabalho apresenta "
    "o desenvolvimento de um modelo computacional baseado em Autômatos Celulares Probabilísticos "
    "(Peixoto, 2005; Rodrigues, 2011), implementado em Python e validado por Desenvolvimento "
    "Orientado a Testes (TDD com Pytest), para analisar a transmissão horizontal por contágio a "
    "partir de parreiras contaminadas sobre parreiras próximas e sua posterior recuperação atuando "
    "como barreira de contenção fitossanitária. A simulação foi executada ao longo de 50 ciclos "
    "temporais em uma grade de 50 por 50 parreiras, modelando a vizinhança de Moore e o bloqueio "
    "espacial promovido pelo manejo protetor. Os resultados incluem a análise da curva epidemiológica, "
    "validação automatizada por testes unitários e relatórios em formato .txt adaptados para "
    "acessibilidade via leitores de tela."
)

SEC1_TITULO = "1. Introdução"
SEC1_P1 = (
    "A viticultura possui expressiva relevância socioeconômica no Brasil, especialmente nos polos "
    "irrigados do Nordeste, como o Vale do São Francisco e o Vale do Siriji em Pernambuco e o Vale "
    "do Assú no Rio Grande do Norte, responsáveis por cerca de 99% da exportação brasileira de uvas "
    "de mesa (Correia et al., 2011). Entretanto, a intensificação do cultivo de videira (Vitis vinifera) "
    "em áreas contínuas favorece a disseminação de fitopatógenos severos, a exemplo do complexo de "
    "fungos causadores do declínio da videira, como Lasiodiplodia theobromae (Correia et al., 2011), "
    "e do cancro bacteriano causado por Xanthomonas campestris pv. viticola, cuja transmissão dentro "
    "do parreiral ocorre rapidamente entre plantas próximas por respingos de chuva, irrigação e "
    "tratos culturais (Nascimento; Mariano, 2004)."
)
SEC1_P2 = (
    "Para investigar o avanço espaço-temporal de epidemias agrícolas em pomares e talhões, os "
    "Autômatos Celulares (AC) constituem um arcabouço discreto no tempo, no espaço e no estado "
    "altamente eficaz, no qual cada planta é representada por um sítio do reticulado cujas interações "
    "locais determinam o padrão macroscópico emergente (Peixoto, 2005). Sob a ótica da transmissão "
    "horizontal por contágio em redes bidimensionais, os Autômatos Celulares Probabilísticos permitem "
    "incorporar a estocasticidade inerente ao contato infeccioso entre hospedeiros vizinhos (Rodrigues, "
    "2011). O objetivo deste trabalho é formalizar e testar via TDD (Pytest) um modelo de AC em Python "
    "capaz de simular a contaminação entre parreiras próximas e demonstrar como a recuperação das "
    "plantas tratadas passa a atuar como barreira física e biológica de contenção no vinhedo."
)

SEC2_TITULO = "2. Detalhamento do Modelo Computacional"
SEC2_P1 = (
    "O modelo foi construído em Python utilizando matrizes bidimensionais (NumPy e Matplotlib/Tkinter) "
    "e verificado por testes unitários automatizados com Pytest. Seguindo a formulação espacial para "
    "talhões agrícolas descrita por Peixoto (2005) e a atualização síncrona em redes quadradas "
    "abordada por Rodrigues (2011), o parreiral é definido como um reticulado discreto de dimensões "
    "50 por 50."
)
SEC2_P2 = (
    "A grade abriga um total de N = 2.500 células, onde cada sítio representa uma parreira localizada "
    "na posição (i, j) no instante discreto t com estado E(i, j, t) pertencente ao conjunto {S, I, R}, "
    "adaptado do modelo epidemiológico espacial SIR:"
)
SEC2_B1 = (
    "Saudável / Suscetível (S): Parreira sadia, produtiva e vulnerável à transmissão horizontal "
    "por contágio a partir de parreiras adjacentes infectadas na vizinhança de Moore (8 vizinhos "
    "mais próximos de raio 1, conforme Peixoto, 2005). Representada graficamente pelo caractere . "
    "no relatório impresso."
)
SEC2_B2 = (
    "Contaminada / Infectada (I): Parreira colonizada pelo patógeno (como X. campestris pv. viticola "
    "ou fungos de declínio) que transmite a infecção horizontalmente para suas vizinhas próximas "
    "com probabilidade p durante seu ciclo infeccioso (Rodrigues, 2011). Representada pelo caractere X."
)
SEC2_B3 = (
    "Recuperada / Barreira de Contenção (R): Parreira que, após o período infeccioso (T_rec = 3 ciclos), "
    "passou por intervenção fitossanitária recomendada pela literatura — tal como poda drástica de "
    "ramos sintomáticos, pincelamento de cortes com pasta cúprica e aplicação de fungicidas cúpricos "
    "ou tiocarbamatos que formam uma película protetora bacteriostática no filoplano, associada a "
    "barreiras quebra-vento (Nascimento; Mariano, 2004). No autômato, essa parreira recuperada "
    "torna-se imune e atua como barreira mecânica e biológica de contenção, bloqueando a passagem "
    "do contágio para as parreiras saudáveis adjacentes. Representada pelo caractere O."
)

SEC3_TITULO = "3. Resultados e Discussão"
SEC3_P1 = (
    "Para avaliar a estabilidade do modelo computacional, a consistência das regras locais validadas "
    "via TDD (Pytest) e a dinâmica de transmissão horizontal e contenção na grade de 2.500 parreiras, "
    "foram executadas três replicações independentes da simulação sob as mesmas condições iniciais "
    "(1% de focos primários, p = 0,35 e T_rec = 3), durante um horizonte temporal fixado em T = 50 ciclos."
)
SEC3_P2 = (
    "Os dados empíricos obtidos revelaram uma convergência para o estado livre de doença (extinção "
    "da fase infectada I = 0, conforme Rodrigues, 2011) com preservação de parreiras sadias:"
)
SEC3_P3 = (
    "Encerramento do surto: Em todas as simulações, o ciclo epidemiológico atingiu a extinção "
    "(ausência de novas parreiras na condição Contaminada) entre os ciclos 21 e 24, comprovando "
    "a contenção espacial."
)
SEC3_B1 = "Ensaio 1: A propagação encerrou-se no 21º ciclo (341 parreiras saudáveis preservadas e 2.159 recuperadas em barreira)."
SEC3_B2 = "Ensaio 2: A propagação encerrou-se no 22º ciclo (368 parreiras saudáveis preservadas e 2.132 recuperadas em barreira)."
SEC3_B3 = "Ensaio 3: A propagação encerrou-se no 24º ciclo (388 parreiras saudáveis preservadas e 2.112 recuperadas em barreira)."
SEC3_TAB_TITULO = "Resumo dos Ensaios da Simulação (T = 50 ciclos)"
SEC3_P4 = (
    "A interrupção da transmissão horizontal — ocorrida antes da metade do horizonte temporal "
    "estipulado — evidencia o papel determinante da transição para o estado Recuperada / Barreira "
    "de Contenção (R) combinada à topologia de Moore (Peixoto, 2005). Conforme preconizado no "
    "manejo integrado da videira por Nascimento e Mariano (2004), a detecção precoce dos focos "
    "iniciais seguida pela proteção química cúprica e isolamento cultural impede que o patógeno "
    "alcance a totalidade do pomar. No reticulado discreto, as parreiras que transitaram para o "
    "estado R formaram cinturões protetores que encapsularam as manchas de infecção (I), "
    "preservando entre 341 e 388 parreiras Suscetíveis (S) livres de contaminação."
)

SEC4_TITULO = "4. Conclusão"
SEC4_P1 = (
    "O modelo desenvolvido em Python e validado por testes automatizados em TDD (Pytest) demonstrou "
    "eficácia ao representar a dinâmica espacial de contaminação horizontal em plantações de uvas "
    "e a formação de barreiras de contenção por parreiras recuperadas. Em consonância com os "
    "estudos fitopatológicos de Correia et al. (2011) e Nascimento e Mariano (2004), bem como "
    "com a teoria de Autômatos Celulares aplicada a sistemas agrícolas e epidemiológicos (Peixoto, "
    "2005; Rodrigues, 2011), verificou-se que a rápida recuperação e proteção das plantas ao redor "
    "dos focos limita a duração do surto ao intervalo entre 21 e 24 ciclos."
)
SEC4_P2 = (
    "Adicionalmente, a geração automatizada de relatórios descritivos e matrizes visuais em formato "
    "de texto simples (.txt) assegura a plena acessibilidade do software a leitores de tela, "
    "promovendo a inclusão científica. Trabalhos futuros poderão incorporar controladores baseados "
    "em lógica fuzzy para modelar a influência da velocidade e direção dos ventos na dispersão "
    "não-local do patógeno entre fileiras do parreiral, à semelhança da abordagem proposta por "
    "Peixoto (2005)."
)

SEC5_TITULO = "5. Referências"
REF_1 = (
    "CORREIA, K. C.; CÂMARA, M. P. S.; BARBOSA, M. A. G.; SALES JR., R.; AGUSTÍ-BRISACH, C.; "
    "GRAMAJE, D.; GARCÍA-JIMÉNEZ, J.; ABAD-CAMPOS, P.; ARMENGOL, J.; MICHEREFF, S. J. Fungos "
    "associados ao declínio da videira no Nordeste do Brasil. Tropical Plant Pathology, v. 36, "
    "Suplemento, p. 909, 2011."
)
REF_2 = (
    "NASCIMENTO, A. R. P.; MARIANO, R. L. R. Cancro bacteriano da videira: etiologia, "
    "epidemiologia e medidas de controle. Ciência Rural, Santa Maria, v. 34, n. 1, p. 301-307, "
    "jan.-fev. 2004."
)
REF_3 = (
    "PEIXOTO, M. S. Sistemas Dinâmicos e Controladores Fuzzy: um Estudo da Dispersão da Morte "
    "Súbita dos Citros em São Paulo. 2005. 189 f. Tese (Doutorado em Matemática Aplicada) – "
    "Instituto de Matemática, Estatística e Computação Científica, Universidade Estadual de "
    "Campinas (UNICAMP), Campinas, 2005."
)
REF_4 = (
    "RODRIGUES, L. L. F. Transmissão vertical e horizontal de parasitas usando autômatos "
    "celulares probabilísticos. 2011. 68 f. Dissertação (Mestrado em Física) – Centro de Ciências "
    "Exatas e da Natureza, Universidade Federal da Paraíba (UFPB), João Pessoa, 2011."
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
        "",
        SEC5_TITULO,
        REF_1,
        REF_2,
        REF_3,
        REF_4,
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
    substituir_texto_paragrafo(filhos[26], SEC4_P1, preservar_tab=True)
    substituir_texto_paragrafo(filhos[27], SEC4_P2, preservar_tab=True)

    # Adiciona a seção 5. Referências antes do sectPr final clonando o estilo Heading2 e parágrafos
    heading_ref = copy.deepcopy(filhos[25])
    substituir_texto_paragrafo(heading_ref, SEC5_TITULO, preservar_tab=False)

    idx_insercao = len(body) - 1  # Antes de w:sectPr
    body.insert(idx_insercao, heading_ref)
    idx_insercao += 1

    for ref_texto in (REF_1, REF_2, REF_3, REF_4):
        p_ref = copy.deepcopy(filhos[26])
        substituir_texto_paragrafo(p_ref, ref_texto, preservar_tab=False)
        body.insert(idx_insercao, p_ref)
        idx_insercao += 1

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
    (Path(r"C:\automato_plantacao_uvas") / "ARTIGO.md").write_text(texto_limpo, encoding="utf-8")
    print("[OK] Artigo atualizado com as 4 referências de C:\\altomatos (.docx, .txt e ARTIGO.md).")


if __name__ == "__main__":
    gerar_docx_artigo()
