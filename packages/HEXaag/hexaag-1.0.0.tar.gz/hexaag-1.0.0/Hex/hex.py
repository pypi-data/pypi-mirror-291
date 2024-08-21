# CLASSE COORDENADA
# A entidade de Hex
class Hex:
    def __init__(self, q: int, r: int, s: int):
        assert not (int(q) + int(r) + int(s) !=
                    0), "a soma de 'q', 'r' e 's' deve ser 0"
        self.q = q
        self.r = r
        self.s = s
        self.id = (q, r, s)

        # As direções dos vizinhos, iniciando de cima, horário
        self._direcoes = [
            (0, -1, 1),
            (1, -1, 0),
            (1, 0, -1),
            (0, 1, -1),
            (-1, 1, 0),
            (-1, 0, 1),
        ]

    def __str__(self):
        return f'{self.id}'

    def __repr__(self):
        return f'<Hexágono({int(self.q)}, {int(self.r)}, {int(self.s)})>'

    def __eq__(self, other):
        return (self.q, self.r, self.s) == (other.q, other.r, other.s)

    def __add__(self, other):
        return Hex(self.q + other.q, self.r + other.r, self.s + other.s)

    def __sub__(self, other):
        return Hex(self.q - other.q, self.r - other.r, self.s - other.s)

    def __mul__(self, valor):
        return Hex(self.q * valor, self.r * valor, self.s * valor)

    def __truediv__(self, valor):
        return Hex(self.q / valor, self.r / valor, self.s / valor)

    # PROPRIEDADES
    @property
    def comprimento(self):
        return int((abs(self.q) + abs(self.r) + abs(self.s))/2)

    # MÉTODOS
    def _direcao(self, direcao: int):
        assert direcao in range(6), 'a direção deve estar entre 0 a 5'
        return self._direcoes[direcao]

    def distancia(self, other):
        novo_hex = self - other
        return novo_hex.comprimento

    def vizinho(self, index: int):
        return self + Hex(*self._direcao(index))
