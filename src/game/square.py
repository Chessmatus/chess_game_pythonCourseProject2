class Square:

    def __init__(self, row, column, piece=None):
        self.row = row
        self.column = column
        self.piece = piece

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def __str__(self):
        return str(self.row) + " " + str(self.column)

    def has_piece(self):
        return self.piece is not None

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True

    def isempty_or_rival(self, color):
        return self.isempty() or self.has_rival_piece(color)

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def isempty(self):
        return not self.has_piece()

    def has_rival_piece(self, color):
        return self.has_piece() and self.piece.color != color
