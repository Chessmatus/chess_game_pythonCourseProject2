from const import *
from piece import *
import copy
from sound import Sound
import os


class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for column in range(COLUMNS)]
        self.next_player = 'white'
        self.last_move_w = None
        self.last_move_b = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def last_move(self):
        return self.last_move_w if self.next_player == 'black' else self.last_move_b

    def _create(self):
        for row in range(ROWS):
            for column in range(COLUMNS):
                self.squares[row][column] = Square(row, column)

    def _add_pieces(self, color):
        if color == 'white':
            row_pawn, row_other = (6, 7)
        else:
            row_pawn, row_other = (1, 0)

        # pawns
        for column in range(COLUMNS):
            self.squares[row_pawn][column] = Square(row_pawn, column, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))

    def calc_moves(self, piece, row, column, bool=True):
        # calculates all the possible moves of a specific piece on a specific position

        if isinstance(piece, Pawn):
            piece.pawn_moves(self, row, column, bool)

        elif isinstance(piece, Knight):
            piece.knight_moves(self, row, column, bool)

        elif isinstance(piece, Bishop):
            piece.bishop_move(self, row, column, bool)

        elif isinstance(piece, Rook):
            piece.rook_move(self, row, column, bool)

        elif isinstance(piece, Queen):
            piece.queen_move(self, row, column, bool)

        elif isinstance(piece, King):
            piece.king_moves(self, row, column, bool)

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.column].piece = Queen(piece.color)

    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.row][final.column].isempty()

        # console move update
        self.squares[initial.row][initial.column].piece = None
        self.squares[final.row][final.column].piece = piece

        if isinstance(piece, Pawn):
            # en_passant capture
            diff = final.column - initial.column
            if diff != 0 and en_passant_empty:
                # console move update
                self.squares[initial.row][initial.column + diff].piece = None
                self.squares[final.row][final.column].piece = piece
                if not testing:
                    sound = Sound(os.path.join('assets/sounds/capture.wav'))
                    sound.play()

            else:
                # pawn promotion
                self.check_promotion(piece, final)

        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.column - initial.column
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # move
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # remember last move
        if self.next_player == 'white':
            self.last_move_w = move
        else:
            self.last_move_b = move

    def castling(self, initial, final):
        return abs(initial.column - final.column) == 2

    def in_check(self, piece=None, move=None):
        temp_board = copy.deepcopy(self)
        color = self.next_player
        if move and piece:
            temp_piece = copy.deepcopy(piece)
            temp_board.move(temp_piece, move, testing=True)
            color = piece.color

        for row in range(ROWS):
            for column in range(COLUMNS):
                if temp_board.squares[row][column].has_rival_piece(color):
                    p = temp_board.squares[row][column].piece
                    temp_board.calc_moves(p, row, column, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True

        return False

    def valid_move(self, piece, move):
        return move in piece.moves

    def is_mate(self):
        if self.in_check():
            for row in range(ROWS):
                for col in range(COLUMNS):
                    if isinstance(self.squares[row][col].piece, King) and \
                            self.squares[row][col].piece.color == self.next_player:
                        self.calc_moves(self.squares[row][col].piece, row, col)
                        if not self.squares[row][col].piece.can_be_moved:
                            return True

        return False

    def is_stalemate(self):
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.squares[row][col].has_piece() and self.squares[row][col].piece.color == self.next_player:
                    piece = self.squares[row][col].piece
                    self.calc_moves(piece, row, col)
                    if self.squares[row][col].piece.can_be_moved:
                        return False

        return True

    def not_enough_pieces(self):
        num_of_pieces = [0, 0]
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.squares[row][col].has_piece():
                    piece = self.squares[row][col].piece
                    if isinstance(piece, Pawn):
                        return False

                    elif isinstance(piece, Knight):
                        num_of_pieces[0] += 1

                    elif isinstance(piece, Bishop):
                        num_of_pieces[1] += 1

                    elif isinstance(piece, Rook):
                        return False

                    elif isinstance(piece, Queen):
                        return False

        return True if num_of_pieces[0] + num_of_pieces[1] <= 1 else False

