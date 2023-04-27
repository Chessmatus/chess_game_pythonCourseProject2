from const import *
from square import Square


class Board:

    def __init__(self):
        self.squares = []

    def _create(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for column in range(COLUMNS)]
        print(self.squares)

    def _add_pieces(self, color):
        pass
