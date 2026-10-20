Simulação da Propagação de Pragas e Barreira de Contenção em Plantação de Uvas por Autômatos Celulares em Ambiente Python

Edson José de Amorim Oliveira1

1Departamento de Estatística e Informática
Universidade Federal Rural de Pernambuco – Recife, PE – Brasil
edson.amorim@ufrpe.br

Resumo. As pragas agrícolas e doenças fúngicas em vinhedos representam um dos desafios mais complexos para a viticultura contemporânea. A modelagem computacional in silico tem se consolidado como uma ferramenta essencial para a compreensão dos mecanismos de disseminação fitopatogênica e da contenção espacial de surtos em cultivos perenes. Este trabalho apresenta o desenvolvimento de um modelo computacional baseado em Autômatos Celulares (AC), implementado na linguagem Python e validado por Desenvolvimento Orientado a Testes (TDD com Pytest), para analisar a dinâmica de contágio e propagação espacial de uma parreira contaminada sobre uma população de parreiras sadias, bem como sua posterior recuperação atuando como barreira de contenção. A simulação foi executada ao longo de 50 ciclos temporais, modelando as transições de estado, a mecânica da vizinhança espacial de Moore e o impacto do tempo de recuperação das parreiras na proteção do vinhedo. Os resultados incluem a análise quantitativa da curva epidemiológica, suíte de testes automatizados e relatórios em formato .txt adaptados para acessibilidade via leitores de tela.

1. Introdução

A patogênese e a progressão de pragas e doenças fúngicas em plantações de uvas envolvem processos biológicos e espaciais altamente complexos, nos quais parreiras contaminadas interagem diretamente com o microambiente e com as videiras próximas ao seu redor. O estudo da dinâmica espacial de contaminação no parreiral fornece informações valiosas sobre como os focos iniciais de infecção se propagam para as plantas adjacentes e afetam a plantação como um todo.

Nesse contexto, os Autômatos Celulares (AC) constituem um arcabouço matemático e computacional discreto ideal para simular sistemas agrícolas em que regras locais de proximidade determinam o comportamento emergente global. O objetivo deste trabalho é formalizar um modelo de AC em Python capaz de simular a mecânica de contágio entre parreiras contaminadas e sadias, avaliando o papel do raio de vizinhança de Moore, das taxas de propagação, da validação automatizada via TDD com Pytest e da recuperação das parreiras, que passam a atuar como barreira de contenção contra o avanço da praga.

2. Detalhamento do Modelo Computacional

O modelo foi construído em Python e utiliza matrizes bidimensionais para representar a estrutura espacial da plantação de uvas, contando com verificação automatizada de regras por meio do framework Pytest (TDD). A grade espacial é definida como um reticulado discreto de dimensões 50 por 50.

A grade abriga um total de 2.500 células (parreiras). Cada parreira localizada na posição (i, j) no instante de tempo t possui um estado E(i, j, t) pertencente ao conjunto {S, I, R}, baseado em uma adaptação do modelo epidemiológico SIR:

- Saudável / Suscetível (S): Parreira sadia, produtiva e suscetível à contaminação induzida por parreiras próximas infectadas. Representada graficamente pelo caractere . no relatório impresso.
- Contaminada / Infectada (I): Parreira infectada que expressa o vetor de contágio, capaz de transmitir a praga para suas vizinhas diretas na vizinhança de Moore. Representada pelo caractere X.
- Recuperada / Barreira de Contenção (R): Parreira que completou seu período infeccioso e se recuperou, tornando-se imune e atuando como barreira mecânica e biológica de contenção que impede a passagem da infecção para as parreiras sadias adjacentes. Representada pelo caractere O.

3. Resultados e Discussão

Para avaliar a estabilidade do modelo computacional, a exatidão das regras verificadas pelos testes em TDD (Pytest) e a dinâmica de propagação do contágio na grade celular da plantação de uvas, foram executadas três replicações independentes da simulação sob as mesmas condições iniciais, durante um horizonte temporal fixado em T = 50 ciclos.

Os dados empíricos obtidos revelaram uma convergência no comportamento dinâmico do sistema:

Encerramento do surto: Em todas as simulações, o ciclo epidemiológico atingiu a extinção (ausência de novas parreiras na condição Contaminada) entre os ciclos 21 e 24, consolidando a barreira de contenção.

- Ensaio 1: A propagação encerrou-se no 21º ciclo (341 parreiras saudáveis preservadas e 2.159 recuperadas em barreira).
- Ensaio 2: A propagação encerrou-se no 22º ciclo (368 parreiras saudáveis preservadas e 2.132 recuperadas em barreira).
- Ensaio 3: A propagação encerrou-se no 24º ciclo (388 parreiras saudáveis preservadas e 2.112 recuperadas em barreira).

Resumo dos Ensaios da Simulação (T = 50 ciclos)
Ensaio | Ciclo de Extinção da Infecção | Duração do surto
Ensaio 1 | Ciclo 21 | 21 ciclos
Ensaio 2 | Ciclo 22 | 22 ciclos
Ensaio 3 | Ciclo 24 | 24 ciclos

A interrupção da contaminação — ocorrida na primeira metade do tempo total estipulado — evidencia o papel determinante da taxa de transição para o estado Recuperada / Barreira de Contenção (R) e da vizinhança mecânica de Moore. As parreiras que transitaram para o estado R passaram a atuar como barreiras físicas e topológicas no reticulado discreto, bloqueando as vias de contágio das parreiras no estado Contaminada (I) e impedindo a infecção total da população de parreiras Suscetíveis (S). Esse comportamento também foi comprovado deterministicamente pela suíte de testes automatizados em Pytest, na qual um anel fechado de parreiras recuperadas isola integralmente um foco central de infecção.

4. Conclusão

O modelo desenvolvido em Python demonstrou eficácia ao representar a dinâmica de contaminação entre parreiras próximas e sua posterior recuperação atuando como barreira de contenção por meio da abordagem de Autômatos Celulares baseada na topologia de Moore. A consistência observada nas replicações experimentais e nos testes automatizados via TDD (Pytest) confirma que a transição para o estado recuperado limita significativamente a expansão da praga na plantação de uvas, delimitando a duração da fase infecciosa ao intervalo entre 21 e 24 ciclos.

Além do aporte teórico-computacional e dos gráficos gerados, a emissão de relatórios tabulares e descritivos em formato de texto simples (.txt) assegura a acessibilidade do software a leitores de tela, promovendo o uso inclusivo da ferramenta. Trabalhos futuros poderão explorar a variação probabilística induzida pela ação do vento entre as fileiras do vinhedo e diferentes protocolos de manejo preventivo.
