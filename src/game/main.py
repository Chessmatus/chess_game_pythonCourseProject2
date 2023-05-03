import sys
import os
import pygame

from const import *
from buttons import Button
from square import Square
from move import Move
from sound import Sound

from network import Network


def correct_move(board, color):
    return board.last_move_b if color == 'white' else board.last_move_w


def next_color(color):
    return 'black' if color == 'white' else 'white'


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = None
        self.move_sound = Sound(os.path.join('assets/sounds/move.wav'))
        self.capture_sound = Sound(os.path.join('assets/sounds/capture.wav'))
        self.btns = []
        self.btns.append(Button("RESIGN", 4 * DIFF + COLUMNS * SQUARE_SIZE, DIFF + 3 * SQUARE_SIZE, (255, 0, 0)))
        self.btns.append(Button("DRAW", 4 * DIFF + COLUMNS * SQUARE_SIZE, DIFF + 4 * SQUARE_SIZE, (0, 255, 0)))

    def sound_effect(self, captured=False):
        if captured:
            self.capture_sound.play()
        else:
            self.move_sound.play()

    def mainloop(self):
        clock = pygame.time.Clock()
        n = Network()
        run = True
        connecting = True
        player_color = n.player_color

        while run:
            # show methods
            clock.tick(FPS)
            if connecting:
                try:
                    game = n.send("get")
                    self.game = game
                    self.game.player_color = player_color
                    dragger = self.game.dragger
                    if self.game.connected():
                        connecting = False
                except:
                    run = False
                    print("Couldn't get game")
                    break

            self.game.show_game(self.screen, self.btns)

            board_res_off = n.send((self.game.board, self.game.result,
                                    self.game.draw_offered_you, self.game.draw_offered_opp))
            if board_res_off[1] == 'Lost':
                self.game.result = 'Won'
            elif board_res_off[1] == 'Draw':
                self.game.result = 'Draw'
            elif board_res_off[2] and not self.game.draw_offered_you:
                self.game.draw_offered_opp = True
            elif board_res_off[2] and self.game.draw_offered_you:
                self.game.result = 'Draw'
            if board_res_off[0].last_move() and correct_move(board_res_off[0], self.game.player_color) != \
                    correct_move(self.game.board, self.game.player_color):
                self.game.board = board_res_off[0]
                if self.game.board.is_mate():
                    self.game.result = 'Lost'
                elif self.game.board.is_stalemate() or self.game.board.not_enough_pieces():
                    self.game.result = 'Draw'

            if self.game.connected() and not self.game.result:

                if dragger.dragging:
                    dragger.update_blit(self.screen)

            for event in pygame.event.get():
                if self.game.connected() and not self.game.result:

                    # click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse(event.pos)

                        clicked_row = (dragger.mouseY - DIFF) // SQUARE_SIZE
                        clicked_column = (dragger.mouseX - DIFF) // SQUARE_SIZE

                        if Square.in_range(clicked_row, clicked_column):
                            self.mouse_down_board(clicked_row, clicked_column, event.pos)
                        elif self.btns[0].click((dragger.mouseX, dragger.mouseY)):
                            self.game.result = 'Lost'
                        elif self.btns[1].click((dragger.mouseX, dragger.mouseY)):
                            self.game.draw_offered_you = True

                    # mouse motion
                    elif event.type == pygame.MOUSEMOTION:
                        self.mouse_motion(event.pos)

                    # click release
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.mouse_release(event.pos)

                # quit app
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def mouse_down_board(self, clicked_row, clicked_column, pos):
        board = self.game.board
        dragger = self.game.dragger
        if board.squares[clicked_row][clicked_column].has_piece():
            piece = board.squares[clicked_row][clicked_column].piece
            # valid piece (color)
            if piece.color == self.game.board.next_player and piece.color == self.game.player_color:
                board.calc_moves(piece, clicked_row, clicked_column, bool=True)
                dragger.save_initial(pos)
                dragger.drag_piece(piece)
                # show methods
                self.game.show_game(self.screen, self.btns)

    def mouse_motion(self, pos):
        dragger = self.game.dragger
        if dragger.dragging:
            dragger.update_mouse(pos)
            # show methods
            self.game.show_game(self.screen, self.btns)
            dragger.update_blit(self.screen)

    def mouse_release(self, pos):
        dragger = self.game.dragger
        board = self.game.board
        if dragger.dragging:
            dragger.update_mouse(pos)

            release_row = (dragger.mouseY - DIFF) // SQUARE_SIZE
            release_column = (dragger.mouseX - DIFF) // SQUARE_SIZE

            # create possible move
            initial = Square(dragger.initial_row, dragger.initial_column)
            final = Square(release_row, release_column)
            move = Move(initial, final)

            if board.valid_move(dragger.piece, move):
                captured = board.squares[release_row][release_column].has_piece()
                board.move(dragger.piece, move)
                # sound
                self.sound_effect(captured)
                # show methods
                self.game.show_game(self.screen, self.btns, release=True)
                # next turn
                self.game.next_turn()
                dragger.piece.clear_moves()
                if self.game.board.is_mate():
                    self.game.result = 'Won'
                elif self.game.board.is_stalemate() or self.game.board.not_enough_pieces():
                    self.game.result = 'Draw'
            dragger.piece.clear_moves()

        dragger.undrag_piece()


main = Main()
main.mainloop()
