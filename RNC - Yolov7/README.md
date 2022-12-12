# Reconhecimento de Modelos de Veículos com Yolov7

O reconhecimento de modelos de veículos em câmeras de segurança é problemático de várias formas: 

- Alguns veículos de diferentes modelos são muito semelhantes devido ao aproveitamento de peças, seguimento de um padrão ou versão (hatch ou sedan);
- Facelift apresentam mudanças estéticas consideráveis mas que não podem ser visualizadas dependendo do ponto de vista;
- A qualidade das imagens das câmeras de segurança é ruim;
- Câmeras de segurança diferentes capturam as imagens dos veículos em ângulos diferentes;
- Existe uma quantidade muito grande de modelos de veículos

Devido a esses fatores, seria necessário um dataset muito grande para identificar qualquer modelo de veículo, além da necessidade de possuir imagens de diferentes ângulos e diferentes qualidades, uma abordagem com Reinforcement Learning para aperfeiçoar o aprendizado a partir das imagens capturadas das câmeras de segurança pode ser uma alternativa viável para tornar o sistema mais preciso.

A aplicação web Roboflow foi utilizada para gerar os datasets no formato necessário do Yolov7. Os projetos estão disponíveis no link <https://app.roboflow.com/vehiclemodeldetection>.

## Criação do Dataset

O primeiro passo é a criação do dataset, que foi feito a partir de um web scraping do Google imagens pesquisando pelos modelos de veículos desejados. O código para essa solução automatizada é encontrado no arquivo download-images.ipynb. Para utilizá-lo, é necessário possuir o Google Chrome e o plugin chromedriver, além do pacote selenium. Foram selecionadas de 100 a 150 imagens de cada modelo de veículo desejado.

Após obter as imagens, elas foram anotadas na aplicação do Roboflow, para ser baixada no formato adequado posteriormente.

## Treinamento da Rede

O treinamento da rede foi feito por meio do notebook yolov7.ipynb, disponível no próprio blog do Roboflow (<https://blog.roboflow.com/yolov7-custom-dataset-training-tutorial/>), que também apresenta um tutorial e uma videoaula. O treinamento foi feito utilizando os ambientes do Google Colab, que possuem máquinas com GPUs dedicadas.

## Resultados

Foram feitos testes com apenas um veículo (fiat uno), dois veículos (fiat uno + jeep compass), três veículos (fiat uno + jeep compass + fiat strada) e vários veículos (gm astra sedan + jeep compass + ford eco sport + ford fiesta hatch + vw gol + hyundai hb20 hatch + nissan kicks + vw saveiro + fiat strada + fiat uno). Os resultados encontram-se na pasta "Resultados", percebe-se que há uma poluição muito grande à medida que são consideradas mais classes de veículos para o dataset, entretanto, boa parte dos veículos são identificados corretamente.