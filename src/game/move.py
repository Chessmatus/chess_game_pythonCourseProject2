from square import Square


class Move:

    def __init__(self, initial, final):
        self.initial = initial
        self.final = final

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final

    def __str__(self):
        return str(self.initial) + " " + str(self.final)


class StraightLineMoves:

    def __init__(self, board, piece, row, column, incrs, bool=True):
        for incr in incrs:
            row_incr, col_incr = incr
            possible_move_row = row + row_incr
            possible_move_col = column + col_incr

            while True:
                if Square.in_range(possible_move_row, possible_move_col):

                    initial = Square(row, column)
                    final_piece = board.squares[possible_move_row][possible_move_col].piece
                    final = Square(possible_move_row, possible_move_col, final_piece)
                    move = Move(initial, final)

                    # empty
                    if board.squares[possible_move_row][possible_move_col].isempty():
                        if bool:
                            if not board.in_check(piece, move):
                                # append move
                                piece.add_move(move)
                        else:
                            # append move
                            piece.add_move(move)

                    # has rival piece
                    elif board.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        if bool:
                            if not board.in_check(piece, move):
                                # append move
                                piece.add_move(move)
                        else:
                            # append move
                            piece.add_move(move)
                        break

                    # has team piece
                    elif board.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                        break

                # not in range
                else:
                    break

                possible_move_row += row_incr
                possible_move_col += col_incr
