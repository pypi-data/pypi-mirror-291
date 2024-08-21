# Hexagonos
Ferramenta para gerar grid de hexágonos regulares, para a criação de mapas de RPG.

Classe criada com base [nesse artigo](https://www.redblobgames.com/grids/hexagons/implementation.html)

- [Changelog](#changelog)
- [Como criar um mapa hexágonal](#como-criar-um-mapa-hexágonal)
- [Classe Hex](#hex)
- [Coordenada](#coordenada)
- [Medida](#medida)
- [Vértices](#vertices_hex)
- [Localizar hexágno em uma lista](#filtrar_hex)

## Changelog
- **1.0.0** - Lançamento

## Como criar um mapa hexágonal
1. O primeiro passo é escolher a orientação do hexágono:
- `pontudo`: o vértice fica na parte superior
- `plano`: a parte superior é um dos lado
[Veja a diferença entre eles no artigo original](https://www.redblobgames.com/grids/hexagons/#basics).

2. Determine o tipo de layout que pode ser [hexágonal](#grid_hexagonal) ou [retangular](#grid_retangular). Passe o tamanho do mapa.

Esses dois passos vai retornar uma lista com os hexágonos.

### Desenhando a grid
Agora é preciso determinar mais dois parâmetros:
- a medida em pixels de cada hexágono
- qual a coordenada de início do mapa (lembrando que o centro do hexágono será essa coordenada, se colocar `0, 0` fará com que parte do hexágono não apareça).

Faça um loop na lista com a grid usando `vertices_hex` para obter os pontos a serem desenhados.

## Hex
A classe para criar o hexágono. Ela recebe três parâmetros, que indica as coordenadas cúbicas `q`, `r` e `s`, conforme descritas [aqui](https://www.redblobgames.com/grids/hexagons/#coordinates-cube).

### distancia(outro_hex)
Esse método vai medir a distância entre dois hexágonos, retornando um valor inteiro. Um hexágono que esteja encostado no outro vai ter a medida 1.

### vizinho(index)
Retorna um hexágono lateral entre os seis possíveis.

### id
Essa propriedade é a tupla com as coordenadas e pode ser usado para identificar o hexágono dentro da guia.

## Coordenada
Uma tupla nomeada, com `x` e `y` (se estiver fazendo uso do pygame pode ser substituída pelo `Vector2` que conta com diversos métodos de manipulação).

## Medida
Uma tupla nomeada com `largura` e `altura`.

## vertices_hex
Essa função retorna uma lista com as [coordenadas](#coordenada) em pixels de cada um dos seis pontos do hexágono.

## grid_hexagonal
Essa função retorna uma lista com os [hexágonos](#hex) para montar um mapa em formato hexagonal. O `tamanho_grid` é o raio do círculo formado ao redor do hexágono central (um grid de tamanho `4` vai ter 4 hexágnos à esquerda, 4 ao topo, 4 abaixo e 4 à direita do hexágono central).

## grid_retangular
Essa função retorna uma lista com os [hexágonos](#hex) para montar um mapa em formato retângular. O tamanho da grid é medido por `qtd_horizontal` e `qtd_vertical`, que determina a quantidade de retângulos nesses eixos.

## filtrar_hex
Essa função retorna um hexágono pelo [id](#id) dentro de uma grid de hexágonos. Se não houver um hexágono com esse id, retornar `None`.