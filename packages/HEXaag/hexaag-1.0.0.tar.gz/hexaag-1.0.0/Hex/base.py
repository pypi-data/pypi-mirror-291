from collections import namedtuple

# TUPLAS COM NOME
Orientacao = namedtuple("Orientação", ['f0', 'f1', 'f2', 'f3', 'b0', 'b1', 'b2', 'b3', 'angulo_inicial'])
Coordenada = namedtuple("Coordenada", ['x', 'y'])
Medida = namedtuple("Medida", ['largura', 'altura'])
