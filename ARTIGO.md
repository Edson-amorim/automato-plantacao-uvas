# Simulação da Propagação de Pragas e Barreira de Contenção em Plantações de Uvas por Autômatos Celulares em Ambiente Python

**Edson José de Amorim Oliveira¹**

¹Departamento de Estatística e Informática  
Universidade Federal Rural de Pernambuco – Recife, PE – Brasil  
`edson.amorim@ufrpe.br`

---

**Resumo.** *O controle fitossanitário em vinhedos representa um dos desafios mais estratégicos para a viticultura moderna, visto que patógenos fúngicos e pragas agrícolas propagam-se rapidamente entre parreiras adjacentes. A modelagem computacional in silico tem se consolidado como uma ferramenta essencial para a compreensão da disseminação espacial de doenças em cultivos perenes e para o planejamento de barreiras de manejo. Este trabalho apresenta o desenvolvimento de um modelo computacional baseado em Autômatos Celulares (AC), implementado na linguagem Python, para analisar a dinâmica de contaminação espacial a partir de uma parreira infectada sobre as parreiras próximas e sua posterior recuperação atuando como barreira de contenção. A simulação foi executada ao longo de 50 ciclos temporais ($T = 50$), modelando as transições probabilísticas de estado, a mecânica da vizinhança espacial de Moore e o efeito protetor das parreiras recuperadas na contenção do surto. Os resultados incluem visualização gráfica interativa, análise quantitativa da curva epidemiológica e relatórios em formato `.txt` adaptados para acessibilidade via leitores de tela.*

---

## 1. Introdução

A disseminação de fitopatógenos em plantações de uvas (*Vitis vinifera*), como o míldio (*Plasmopara viticola*) e o oídio (*Erysiphe necator*), envolve processos biológicos e espaciais altamente dinâmicos, nos quais uma parreira contaminada interage diretamente com as parreiras próximas por meio da dispersão local de esporos e contato foliar. O estudo da dinâmica espacial de contaminação no parreiral fornece subsídios valiosos sobre como focos primários de infecção se alastram e como o manejo localizado pode proteger o vinhedo como um todo.

Nesse contexto, os Autômatos Celulares (AC) constituem um arcabouço matemático e computacional discreto ideal para simular sistemas agrícolas em que regras locais de interação entre plantas vizinhas determinam o comportamento epidemiológico emergente global. O objetivo deste trabalho é formalizar e implementar em Python um modelo de AC capaz de simular a mecânica de contaminação entre parreiras infectadas e saudáveis, avaliando o papel do raio de vizinhança de Moore, da taxa probabilística de contágio e da recuperação induzida das parreiras, que passam a atuar como verdadeiras barreiras físicas e biológicas de contenção contra o avanço da praga.

---

## 2. Detalhamento do Modelo Computacional

O modelo foi construído em Python (disponibilizado em repositório público com modos de execução em interface gráfica Tkinter, Matplotlib e terminal) e utiliza matrizes bidimensionais para representar a disposição espacial das fileiras do vinhedo. A grade espacial dos ensaios padrão é definida como um reticulado discreto de dimensões $20 \times 20$ (expansível para $30 \times 42$ na interface interativa).

A grade de ensaio abriga um total de $N = 400$ parreiras de uva. Cada célula localizada na posição $(i, j)$ no instante de tempo discreto $t$ possui um estado $E_{i,j}(t) \in \{S, I, R\}$, baseado em uma adaptação espacial do modelo epidemiológico SIR com formação de barreira:

* **Parreira Saudável / Suscetível ($S$):** Parreira sadia, produtiva e suscetível à contaminação induzida por parreiras adjacentes infectadas na vizinhança de Moore ($8$ vizinhas). A probabilidade de contágio em cada passo é dada por $P = 1 - (1 - p)^k$, onde $p = 0,16$ é a taxa base de transmissão por contato e $k$ é o número de parreiras próximas contaminadas. Representada graficamente pelo caractere `.` no relatório impresso (`.txt`) e pela cor verde na simulação visual.
* **Parreira Contaminada / Infectada ($I$):** Parreira acometida pelo patógeno que expressa o vetor de contágio durante $T_{\text{rec}} = 2$ ciclos infecciosos, sendo capaz de contaminar as parreiras próximas adjacentes. Representada pelo caractere `X` no relatório acessível e pela cor vermelha na interface gráfica.
* **Parreira Recuperada / Barreira de Contenção ($R$):** Parreira que completou seu período infeccioso ($T_{\text{rec}}$) e se recuperou após resposta fisiológica ou intervenção fitossanitária, tornando-se imune à reinfecção e atuando como barreira mecânica e biológica de contenção que bloqueia a propagação para as parreiras saudáveis protegidas atrás dela. Representada pelo caractere `O` no relatório `.txt` e pela cor azul na interface visual.

---

## 3. Resultados e Discussão

Para avaliar a estabilidade do modelo computacional, a dinâmica de contaminação entre parreiras próximas e a eficácia da formação da barreira de contenção na grade celular, foram executadas três replicações independentes da simulação (Ensaios 1, 2 e 3) sob o cenário de foco de infecção com linha de contenção, durante um horizonte temporal fixado em $T = 50$ ciclos.

Os dados empíricos obtidos revelaram uma forte convergência no comportamento dinâmico do parreiral e na contenção efetiva da praga:

**Encerramento do surto e proteção do vinhedo:** Em todas as simulações, o ciclo epidemiológico atingiu a extinção completa do patógeno (ausência de parreiras na condição Contaminada) entre os ciclos $20$ e $24$, preservando a maioria das parreiras saudáveis intactas.

* **Ensaio 1:** A propagação encerrou-se no $20^\circ$ ciclo, preservando $221$ parreiras saudáveis ($55,25\%$) protegidas por $179$ parreiras recuperadas em barreira ($44,75\%$).
* **Ensaio 2:** A propagação encerrou-se no $22^\circ$ ciclo, preservando $241$ parreiras saudáveis ($60,25\%$) protegidas por $159$ parreiras recuperadas em barreira ($39,75\%$).
* **Ensaio 3:** A propagação encerrou-se no $24^\circ$ ciclo, preservando $267$ parreiras saudáveis ($66,75\%$) protegidas por $133$ parreiras recuperadas em barreira ($33,25\%$).

**Resumo dos Ensaios da Simulação na Plantação de Uvas ($T = 50$ ciclos)**

| Ensaio | Ciclo de Extinção da Infecção | Duração do surto e Contenção Final |
| :--- | :--- | :--- |
| **Ensaio 1** | Ciclo 20 | 20 ciclos (221 saudáveis / 179 barreira) |
| **Ensaio 2** | Ciclo 22 | 22 ciclos (241 saudáveis / 159 barreira) |
| **Ensaio 3** | Ciclo 24 | 24 ciclos (267 saudáveis / 133 barreira) |

A interrupção da contaminação — ocorrida antes da metade do horizonte temporal estipulado ($T = 50$) — evidencia o papel determinante da transição para o estado Recuperada / Barreira de Contenção ($R$) combinada à topologia espacial de Moore. À medida que as primeiras parreiras contaminadas ($I$) completam seu ciclo e se recuperam, elas formam um cinturão contínuo de células no estado $R$ ao redor da frente de invasão. Essas parreiras recuperadas passam a atuar como barreiras físicas e topológicas no reticulado discreto, bloqueando as rotas de contágio das parreiras ainda no estado $I$ e impedindo que a praga alcance o restante da população de parreiras Saudáveis / Suscetíveis ($S$).

---

## 4. Conclusão

O modelo desenvolvido em Python demonstrou elevada eficácia ao representar a dinâmica espacial de contaminação fitopatogênica em uma plantação de uvas por meio da abordagem de Autômatos Celulares baseada na vizinhança de Moore. A consistência observada nas replicações experimentais confirma que a recuperação das parreiras e sua atuação como barreira de contenção limitam decisivamente a expansão da praga, extinguindo o surto entre $20$ e $24$ ciclos e preservando entre $55,25\%$ e $66,75\%$ do parreiral saudável.

Além da interface gráfica interativa e dos gráficos epidemiológicos, a geração automatizada de relatórios tabulares e mapas espaciais em formato de texto simples (`.txt`) assegura a plena acessibilidade do software a leitores de tela, promovendo o uso inclusivo da ferramenta científica. Trabalhos futuros poderão incorporar anisotropia induzida pela direção do vento entre as fileiras de parreiras e diferentes regimes de poda e pulverização preventiva.
