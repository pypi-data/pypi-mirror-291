from .hex import Hex
from .base import *

from math import sqrt, pi, cos, sin


ORIENTACAO_HEX = {
    'pontudo': Orientacao(sqrt(3), sqrt(3) / 2, 0, 3 / 2, sqrt(3) / 3, -1 / 3, 0, 2 / 3, 0.5),
    'plano': Orientacao(3 / 2, 0, sqrt(3) / 2, sqrt(3), 2 / 3, 0, -1 / 3, sqrt(3) / 3, 0)
}

# FUNÇÕES DE AUXÍLIO
def _ponto_hex_em_px(hex: Hex, tipo_layout: str = 'pontudo', tamanho_hex: int = 50, origem: tuple = Coordenada(0, 0)):
    orientacao = ORIENTACAO_HEX[tipo_layout]

    x = (orientacao.f0 * hex.q + orientacao.f1 * hex.r) * tamanho_hex
    y = (orientacao.f2 * hex.q + orientacao.f3 * hex.r) * tamanho_hex

    return Coordenada(x + origem.x, y + origem.y)


def _desvio_quina_hex(ponto: int, tipo_layout: str = 'pontudo', tamanho_hex: int = 50):
    orientacao = ORIENTACAO_HEX[tipo_layout]
    angulo = 2 * pi * (orientacao.angulo_inicial - ponto) / 6

    return Coordenada(tamanho_hex * cos(angulo), tamanho_hex * sin(angulo))


# FUNÇÃO PARA AS COORDENADAS DOS VERTÍCES
def vertices_hex(hex: Hex, geometria_hex: str = 'pontudo', tamanho_hex: int = 50, origem: tuple = Coordenada(0, 0)):
    """
    Pega as coordenadas dos seis pontos de um hexagono, em pixels
    """
    vertices = []
    centro = _ponto_hex_em_px(hex, geometria_hex, tamanho_hex, origem)

    for i in range(6):
        desvio = _desvio_quina_hex(i, geometria_hex, tamanho_hex)
        vertices.append((centro.x + desvio.x, centro.y + desvio.y))

    return vertices


# FUNÇÕES PARA DESENHAR A GRID
def grid_hexagonal(tamanho_grid: int):
    """
    Desenha uma grid de hexágonos no formato hexagonal, ao redor do hexágono do meio
    """
    dist = tamanho_grid
    mapa = []

    for q in range(-dist, dist + 1):
        r1 = max(-dist, -q - dist)
        r2 = min(dist, -q + dist)

        for r in range(r1, r2 + 1):
            mapa.append(Hex(q, r, -q-r))

    return mapa


def grid_retangular(qtd_horizontal: int, qtd_vertical: int, tipo_layout: str = 'pontudo'):
    """Desenha uma grid de hexágonos no formato retângular, tradicional"""
    topo, direita, baixo, esquerda = 0, qtd_horizontal, qtd_vertical, 0
    mapa = []

    if tipo_layout == 'pontudo':
        for r in range(topo, baixo + 1):
            r_margem = r // 2

            for q in range(esquerda - r_margem, direita - r_margem + 1):
                mapa.append(Hex(q, r, -q-r))

    if tipo_layout == 'plano':
        for q in range(esquerda, direita + 1):
            q_margem = q // 2

            for r in range(topo - q_margem, baixo - q_margem + 1):
                mapa.append(Hex(q, r, -q-r))

    return mapa


# FUNÇÃO PARA A ENCONTRAR UM HEXÁGONO NA GRID
def filtra_hex(grid: list, id: tuple):
    """Encontra um hexágono dentro da lista, com um valor específico, se houver"""
    lista = list(filter(lambda hex: hex.id == id, grid))

    return lista[0] if len(lista) > 0 else None

