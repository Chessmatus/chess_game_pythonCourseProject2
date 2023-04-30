import os
from square import Square
from move import *


class Piece:

    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size=80):
        self.texture = os.path.join(f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

    def get_move(self, initial, final):
        move = Move(initial, final)
        self.add_move(move)


class Pawn(Piece):

    def __init__(self, color):
        if color == 'white':
            self.dir = -1
        else:
            self.dir = 1
        self.en_passant = False
        super().__init__('pawn', color, 1.0)

    def vertical_moves(self, board, row, column, steps):
        # vertical moves
        start = row + self.dir
        end = row + (self.dir * (1 + steps))
        for possible_move in range(start, end, self.dir):
            if Square.in_range(possible_move):
                if board.squares[possible_move][column].isempty():
                    self.get_move(Square(row, column), Square(possible_move, column))
                    '''if bool:
                        if not self.in_check(piece, move):
                            # append move
                            piece.add_move(move)
                    else:
                        # append move
                        piece.add_move(move)'''
                # blocked
                else:
                    break
            # not in range
            else:
                break

    def diagonal_moves(self, board, row, column):
        # diagonal moves
        move_row = row + self.dir
        move_column = [column - 1, column + 1]
        for possible_col in move_column:
            if Square.in_range(move_row, possible_col):
                if board.squares[move_row][possible_col].has_rival_piece(self.color):
                    final_piece = board.squares[move_row][possible_col].piece
                    self.get_move(Square(row, column), Square(move_row, possible_col, final_piece))
                    '''if bool:
                        if not self.in_check(piece, move):
                            # append move
                            piece.add_move(move)
                    else:
                        # append move
                        piece.add_move(move)'''

    def en_passant_move(self, board, row, column, direction):
        if direction == 'left':
            rival_piece_column = column - 1
        else:
            rival_piece_column = column + 1

        initial_row = 3 if self.color == 'white' else 4
        final_row = 2 if self.color == 'white' else 5

        if Square.in_range(rival_piece_column) and row == initial_row:
            if board.squares[row][rival_piece_column].has_rival_piece(self.color):
                p = board.squares[row][rival_piece_column].piece
                if isinstance(p, Pawn):
                    if board.last_move.initial == Square(initial_row - (p.dir * 2), rival_piece_column) and \
                       board.last_move.final == Square(initial_row, rival_piece_column):
                        self.get_move(Square(row, column), Square(final_row, rival_piece_column, p))
                        '''if bool:
                            if not self.in_check(piece, move):
                                # append move
                                piece.add_move(move)
                        else:
                            # append move
                            piece.add_move(move)'''

    def pawn_moves(self, board, row, column):
        steps = 1 if self.moved else 2

        self.vertical_moves(board, row, column, steps)
        self.diagonal_moves(board, row, column)
        # left en_passant
        self.en_passant_move(board, row, column, 'left')
        # right en_passant
        self.en_passant_move(board, row, column, 'right')


class Knight(Piece):

    def __init__(self, color):
        super().__init__('knight', color, 3.0)

    def knight_moves(self, board, row, column):
        # 8 possible moves
        possible_moves = ((row + 2, column + 1),
                          (row + 2, column - 1),
                          (row + 1, column + 2),
                          (row + 1, column - 2),
                          (row - 1, column + 2),
                          (row - 1, column - 2),
                          (row - 2, column - 1),
                          (row - 2, column + 1))
        for possible_move in possible_moves:
            possible_move_row, possible_move_column = possible_move

            if Square.in_range(possible_move_row, possible_move_column):
                if board.squares[possible_move_row][possible_move_column].isempty_or_rival(self.color):
                    final_piece = board.squares[possible_move_row][possible_move_column].piece
                    self.get_move(Square(row, column), Square(possible_move_row, possible_move_column, final_piece))
                    '''if bool:
                        if not self.in_check(piece, move):
                            # append move
                            piece.add_move(move)
                        else:
                            break
                    else:
                        # append move
                        piece.add_move(move)'''


class Bishop(Piece):

    def __init__(self, color):
        super().__init__('bishop', color, 3.001)

    def bishop_move(self, board, row, column):
        StraightLineMoves(board, self, row, column, [(-1, 1), (-1, -1), (1, -1), (1, 1)])


class Rook(Piece):

    def __init__(self, color):
        super().__init__('rook', color, 5.0)

    def rook_move(self, board, row, column):
        StraightLineMoves(board, self, row, column, [(-1, 0), (0, 1), (1, 0), (0, -1)])


class Queen(Piece):

    def __init__(self, color):
        super().__init__('queen', color, 9.0)

    def queen_move(self, board, row, column):
        StraightLineMoves(board, self, row, column, [(-1, 1), (-1, -1), (1, -1), (1, 1), (-1, 0), (0, 1), (1, 0), (0, -1)])


class King(Piece):

    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', color, 10000.0)

    def normal_moves(self, board, row, column):
        adjs = [(row - 1, column + 0),
                (row - 1, column + 1),
                (row - 1, column - 1),
                (row + 0, column + 1),
                (row + 0, column - 1),
                (row + 1, column + 0),
                (row + 1, column + 1),
                (row + 1, column - 1)
                ]

        for possible_move in adjs:
            possible_move_row, possible_move_col = possible_move
            if Square.in_range(possible_move_row, possible_move_col):
                if board.squares[possible_move_row][possible_move_col].isempty_or_rival(self.color):
                    self.get_move(Square(row, column), Square(possible_move_row, possible_move_col))
                    '''if bool:
                        if not self.in_check(piece, move):
                            # append move
                            piece.add_move(move)
                        else:
                            break
                    else:
                        # append move
                        piece.add_move(move)'''

    def long_castling(self, board, row, column):
        left_rook = board.squares[row][0].piece
        if isinstance(left_rook, Rook):
            if not left_rook.moved:
                for col in range(1, 4):
                    if board.squares[row][col].has_piece():
                        break

                    if col == 3:
                        self.left_rook = left_rook
                        # rook move
                        self.left_rook.get_move(Square(row, 0), Square(row, 3))
                        # king move
                        self.get_move(Square(row, column), Square(row, 2))
                        '''if bool:
                            if not self.in_check(piece, move_k) and not self.in_check(left_rook, move_r):
                                # append move rook
                                left_rook.add_move(move_r)
                                # append move king
                                piece.add_move(move_k)
                        else:
                            # append move rook
                            left_rook.add_move(move_r)
                            # append move king
                            piece.add_move(move_k)'''

    def short_castling(self, board, row, column):
        # king castling
        right_rook = board.squares[row][7].piece
        if isinstance(right_rook, Rook):
            if not right_rook.moved:
                for col in range(5, 7):
                    if board.squares[row][col].has_piece():
                        break

                    if col == 6:
                        self.right_rook = right_rook
                        # rook move
                        self.right_rook.get_move(Square(row, 7), Square(row, 5))
                        # king move
                        self.get_move(Square(row, column), Square(row, 6))
                        '''if bool:
                            if not self.in_check(piece, move_k) and not self.in_check(right_rook, move_r):
                                # append move rook
                                right_rook.add_move(move_r)
                                # append move king
                                piece.add_move(move_k)
                        else:
                            # append move rook
                            right_rook.add_move(move_r)
                            # append move king
                            piece.add_move(move_k)'''

    def king_moves(self, board, row, column):
        self.normal_moves(board, row, column)

        if not self.moved:
            self.long_castling(board, row, column)
            self.short_castling(board, row, column)


