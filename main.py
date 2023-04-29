import pygame
import sys

from const import *
from game import Game


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):

        dragger = self.game.dragger
        board = self.game.board

        while True:
            # show methods
            self.game.show_background(self.screen)
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
                        board.calc_moves(piece, clicked_row, clicked_column)
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)
                        # show methods
                        self.game.show_background(self.screen)
                        self.game.show_moves(self.screen)
                        self.game.show_pieces(self.screen)


                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        self.game.show_background(self.screen)
                        self.game.show_moves(self.screen)
                        self.game.show_pieces(self.screen)
                        dragger.update_blit(self.screen)

                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()

                # quit app
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.mainloop()
