# Contagem de Veículos Utilizando Visão Clássica

A solução com visão clássica consiste em um programa que é capaz de contar veículos a partir de imagens de câmeras de segurança. Ela utiliza um algoritmo de remoção de plano de fundo de imagens além de alguns filtros para a separação dos componentes representados por retângulos que representam os veículos. A partir disso, são utilizadas algumas heurísticas para relacionar os componentes encontrados em diferentes frames do vídeo e realizar a classificação desses componentes como veículos.

Essa solução ainda não é capaz de identificar os modelos dos veículos, mas apresenta uma forma de relacionar os veículos encontrados em diferentes frames de um vídeo e remover a necessidade de definir linhas verticais às rodovias para realizar a contagem. Dessa forma, ela pode ser utilizada para a contagem dos modelos de veículos a partir de uma solução com redes neurais.
