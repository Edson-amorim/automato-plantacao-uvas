# Simulação da Propagação de Pragas e Barreira de Contenção em Plantação de Uvas por Autômatos Celulares em Ambiente Python

**Edson José de Amorim Oliveira¹**

¹Departamento de Estatística e Informática  
Universidade Federal Rural de Pernambuco – Recife, PE – Brasil  
`edson.amorim@ufrpe.br`

---

**Resumo.** *O controle fitossanitário em vinhedos representa um dos desafios mais complexos para a viticultura contemporânea. A modelagem computacional in silico tem se consolidado como uma ferramenta essencial para a compreensão dos mecanismos de disseminação fitopatogênica e da contenção de pragas agrícolas. Este trabalho apresenta o desenvolvimento de um modelo computacional baseado em Autômatos Celulares (AC), implementado na linguagem Python com desenvolvimento orientado a testes (TDD via Pytest), para analisar a dinâmica de contágio e propagação espacial de uma parreira contaminada sobre uma plantação de parreiras sadias e sua posterior recuperação atuando como barreira de contenção. A simulação foi executada ao longo de 50 ciclos temporais, modelando as transições de estado, a mecânica da vizinhança espacial de Moore e o impacto do tempo de recuperação das parreiras na formação da barreira. Os resultados incluem a análise quantitativa da curva epidemiológica, verificação automatizada por testes unitários e relatórios em formato `.txt` adaptados para acessibilidade via leitores de tela.*

---

## 1. Introdução

A disseminação de fitopatógenos e a progressão de pragas em plantações de uvas (*Vitis vinifera*) envolvem processos biológicos e espaciais altamente complexos, nos quais parreiras contaminadas interagem diretamente com o microambiente e com as videiras ao seu redor. O estudo da dinâmica espacial de contaminação entre parreiras próximas fornece insights valiosos sobre como focos locais de infecção se propagam e afetam o parreiral como um todo.

Nesse contexto, os Autômatos Celulares (AC) constituem um arcabouço matemático e computacional discreto ideal para simular sistemas agrícolas em que regras locais determinam o comportamento emergente global. O objetivo deste trabalho é formalizar um modelo de AC capaz de simular a mecânica de contágio entre parreiras contaminadas e sadias, avaliando o papel do raio de vizinhança, das taxas de propagação e da formação de recuperação fitossanitária atuando como barreira de contenção contra o avanço da praga na plantação.

---

## 2. Detalhamento do Modelo Computacional

O modelo foi construído em Python seguindo práticas de Desenvolvimento Orientado a Testes (TDD com o framework `pytest`) e utiliza matrizes bidimensionais (biblioteca NumPy e visualização com Matplotlib/Tkinter) para representar a estrutura espacial da plantação de uvas. A grade espacial é definida como um reticulado discreto de dimensões $50 \times 50$.

A grade abriga um total de $2.500$ células (parreiras de uva). Cada parreira localizada na posição $(i, j)$ no instante de tempo $t$ possui um estado $E_{i,j}(t) \in \{S, I, R\}$, baseado em uma adaptação do modelo epidemiológico SIR:

* **Saudável / Suscetível ($S$):** Parreira sadia, produtiva e suscetível à contaminação induzida por parreiras adjacentes infectadas na vizinhança de Moore. Representada graficamente pelo caractere `.` no relatório impresso.
* **Contaminada / Infectada ($I$):** Parreira infectada que expressa o vetor de contágio, capaz de transmitir a praga para as parreiras vizinhas próximas durante seu ciclo infeccioso. Representada pelo caractere `X`.
* **Recuperada / Barreira de Contenção ($R$):** Parreira que completou seu período infeccioso e recuperou-se, tornando-se imune e atuando como barreira mecânica e biológica de contenção que bloqueia o avanço da contaminação. Representada pelo caractere `O`.

---

## 3. Resultados e Discussão

Para avaliar a estabilidade do modelo computacional, a invariância das regras verificadas via TDD (`pytest`) e a dinâmica de propagação do contágio e formação de barreira na plantação de uvas, foram executadas três replicações independentes da simulação sob as mesmas condições iniciais, durante um horizonte temporal fixado em $T = 50$ ciclos.

Os dados empíricos obtidos revelaram uma convergência no comportamento dinâmico do sistema:

**Encerramento do surto:** Em todas as simulações, o ciclo epidemiológico atingiu a extinção (ausência de novas parreiras na condição Contaminada) entre os ciclos $21$ e $24$.

* **Ensaio 1:** A propagação encerrou-se no $21^\circ$ ciclo ($341$ parreiras saudáveis preservadas e $2.159$ recuperadas em barreira).
* **Ensaio 2:** A propagação encerrou-se no $22^\circ$ ciclo ($368$ parreiras saudáveis preservadas e $2.132$ recuperadas em barreira).
* **Ensaio 3:** A propagação encerrou-se no $24^\circ$ ciclo ($388$ parreiras saudáveis preservadas e $2.112$ recuperadas em barreira).

**Resumo dos Ensaios da Simulação ($T = 50$ ciclos)**

| Ensaio | Ciclo de Extinção da Infecção | Duração do surto |
| :--- | :--- | :--- |
| **Ensaio 1** | Ciclo 21 | 21 ciclos |
| **Ensaio 2** | Ciclo 22 | 22 ciclos |
| **Ensaio 3** | Ciclo 24 | 24 ciclos |

A interrupção da contaminação — ocorrida na primeira metade do tempo total estipulado — evidencia o papel determinante da taxa de transição para o estado Recuperada / Barreira de Contenção ($R$) e da vizinhança espacial. As parreiras que transitaram para o estado $R$ passaram a atuar como barreiras físicas e topológicas no reticulado discreto da plantação, bloqueando as vias de contágio das parreiras no estado Contaminada ($I$) e impedindo a infecção total da população de parreiras Suscetíveis ($S$).

---

## 4. Conclusão

O modelo desenvolvido em Python e validado por testes automatizados em TDD (`pytest`) demonstrou eficácia ao representar a dinâmica de contaminação entre parreiras de uva e sua posterior recuperação atuando como barreira de contenção por meio da abordagem de Autômatos Celulares baseada na topologia de Moore. A consistência observada nas replicações experimentais confirma que a transição para o estado recuperado/barreira limita significativamente a expansão da praga no vinhedo, delimitando a duração da fase infecciosa ao intervalo entre $21$ e $24$ ciclos.

Além do aporte teórico-computacional e da visualização gráfica, a geração de relatórios descritivos e matriciais em formato de texto simples (`.txt`) assegura a acessibilidade do software a leitores de tela, promovendo o uso inclusivo da ferramenta. Trabalhos futuros poderão explorar a influência da direção do vento entre as fileiras do parreiral e diferentes estratégias de manejo fitossanitário preventivo.
