from const import *
from square import Square
from piece import *
from move import Move
import copy
from sound import Sound
import os


class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for column in range(COLUMNS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

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

        def pawn_moves():
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][column].isempty():
                        # create initial and final move squares
                        initial_position = Square(row, column)
                        final_position = Square(move_row, column)
                        # create a new move
                        move = Move(initial_position, final_position)
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append move
                                piece.add_move(move)
                        else:
                            # append move
                            piece.add_move(move)
                    # blocked
                    else:
                        break
                # not in range
                else:
                    break

            # diagonal moves
            move_row = row + piece.dir
            move_column = [column - 1, column + 1]
            for possible_col in move_column:
                if Square.in_range(move_row, possible_col):
                    if self.squares[move_row][possible_col].has_rival_piece(piece.color):
                        # create initial and final move squares
                        initial_position = Square(row, column)
                        final_piece = self.squares[move_row][possible_col].piece
                        final_position = Square(move_row, possible_col, final_piece)
                        # create a new move
                        move = Move(initial_position, final_position)
                        if bool:
                            if not self.in_check(piece, move):
                                # append move
                                piece.add_move(move)
                        else:
                            # append move
                            piece.add_move(move)

            # en_passant move
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            # left en_passant
            if Square.in_range(column - 1) and row == r:
                if self.squares[row][column - 1].has_rival_piece(piece.color):
                    p = self.squares[row][column - 1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial_position = Square(row, column)
                            final_position = Square(fr, column - 1, p)
                            # create a new move
                            move = Move(initial_position, final_position)
                            if bool:
                                if not self.in_check(piece, move):
                                    # append move
                                    piece.add_move(move)
                            else:
                                # append move
                                piece.add_move(move)

            # right en_passant
            if Square.in_range(column + 1) and row == r:
                if self.squares[row][column + 1].has_rival_piece(piece.color):
                    p = self.squares[row][column + 1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial_position = Square(row, column)
                            final_position = Square(fr, column + 1, p)
                            # create a new move
                            move = Move(initial_position, final_position)
                            if bool:
                                if not self.in_check(piece, move):
                                    # append move
                                    piece.add_move(move)
                            else:
                                # append move
                                piece.add_move(move)

        def knight_moves():
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
                    if self.squares[possible_move_row][possible_move_column].isempty_or_rival(piece.color):
                        # create squares of the new move
                        initial = Square(row, column)
                        final_piece = self.squares[possible_move_row][possible_move_column].piece
                        final = Square(possible_move_row, possible_move_column, final_piece)   # piece=piece
                        # create new move
                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                # append move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            # append move
                            piece.add_move(move)

        def straight_line_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = column + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):

                        initial = Square(row, column)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)

                        # empty
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            if bool:
                                if not self.in_check(piece, move):
                                    # append move
                                    piece.add_move(move)
                            else:
                                # append move
                                piece.add_move(move)

                        # has rival piece
                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            if bool:
                                if not self.in_check(piece, move):
                                    # append move
                                    piece.add_move(move)
                            else:
                                # append move
                                piece.add_move(move)
                            break

                        # has team piece
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    # not in range
                    else:
                        break

                    possible_move_row += row_incr
                    possible_move_col += col_incr

        def king_moves():
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
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        # create squares of the new move
                        initial = Square(row, column)
                        final = Square(possible_move_row, possible_move_col)  # piece=piece
                        # create new move
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                # append move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            # append move
                            piece.add_move(move)

            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for col in range(1, 4):
                            if self.squares[row][col].has_piece():
                                break

                            if col == 3:
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                move_r = Move(initial, final)

                                # king move
                                initial = Square(row, column)
                                final = Square(row, 2)
                                move_k = Move(initial, final)

                                if bool:
                                    if not self.in_check(piece, move_k) and not self.in_check(left_rook, move_r):
                                        # append move rook
                                        left_rook.add_move(move_r)
                                        # append move king
                                        piece.add_move(move_k)
                                else:
                                    # append move rook
                                    left_rook.add_move(move_r)
                                    # append move king
                                    piece.add_move(move_k)

                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for col in range(5, 7):
                            if self.squares[row][col].has_piece():
                                break

                            if col == 6:
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                move_r = Move(initial, final)

                                # king move
                                initial = Square(row, column)
                                final = Square(row, 6)
                                move_k = Move(initial, final)

                                if bool:
                                    if not self.in_check(piece, move_k) and not self.in_check(right_rook, move_r):
                                        # append move rook
                                        right_rook.add_move(move_r)
                                        # append move king
                                        piece.add_move(move_k)
                                else:
                                    # append move rook
                                    right_rook.add_move(move_r)
                                    # append move king
                                    piece.add_move(move_k)

        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straight_line_moves([(-1, 1), (-1, -1), (1, -1), (1, 1)])

        elif isinstance(piece, Rook):
            straight_line_moves([(-1, 0), (0, 1), (1, 0), (0, -1)])

        elif isinstance(piece, Queen):
            straight_line_moves([(-1, 1), (-1, -1), (1, -1), (1, 1), (-1, 0), (0, 1), (1, 0), (0, -1)])

        elif isinstance(piece, King):
            king_moves()

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
        self.last_move = move

    def castling(self, initial, final):
        return abs(initial.column - final.column) == 2

    def set_false_en_passant(self, piece):
        if not isinstance(piece, Pawn):
            return

        for row in range(ROWS):
            for column in range(COLUMNS):
                if isinstance(self.squares[row][column].piece, Pawn):
                    self.squares[row][column].piece.en_passant = False

        piece.en_passant = True

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)

        for row in range(ROWS):
            for column in range(COLUMNS):
                if temp_board.squares[row][column].has_rival_piece(piece.color):
                    p = temp_board.squares[row][column].piece
                    temp_board.calc_moves(p, row, column, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True

        return False

    def valid_move(self, piece, move):
        return move in piece.moves
