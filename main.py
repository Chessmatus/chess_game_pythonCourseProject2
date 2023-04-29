import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):

        dragger = self.game.dragger
        board = self.game.board
        # clock = pygame.time.Clock()

        while True:
            # show methods
            # clock.tick(FPS)
            self.game.show_background(self.screen)
            self.game.show_last_move(self.screen)
            self.game.show_moves(self.screen)
            self.game.show_pieces(self.screen)

            if dragger.dragging:
                dragger.update_blit(self.screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQUARE_SIZE
                    clicked_column = dragger.mouseX // SQUARE_SIZE

                    if board.squares[clicked_row][clicked_column].has_piece():
                        piece = board.squares[clicked_row][clicked_column].piece
                        # valid piece (color)
                        if piece.color == self.game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_column, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods
                            self.game.show_background(self.screen)
                            self.game.show_last_move(self.screen)
                            self.game.show_moves(self.screen)
                            self.game.show_pieces(self.screen)


                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        self.game.show_background(self.screen)
                        self.game.show_last_move(self.screen)
                        self.game.show_moves(self.screen)
                        self.game.show_pieces(self.screen)
                        dragger.update_blit(self.screen)

                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        release_row = dragger.mouseY // SQUARE_SIZE
                        release_column = dragger.mouseX // SQUARE_SIZE

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_column)
                        final = Square(release_row, release_column)
                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            # normal capture
                            captured = board.squares[release_row][release_column].has_piece()

                            board.move(dragger.piece, move)
                            board.set_false_en_passant(dragger.piece)
                            # sound
                            self.game.sound_effect(captured)
                            # show methods
                            self.game.show_background(self.screen)
                            self.game.show_last_move(self.screen)
                            self.game.show_pieces(self.screen)
                            # next turn
                            self.game.next_turn()

                    dragger.undrag_piece()

                # quit app
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.mainloop()
