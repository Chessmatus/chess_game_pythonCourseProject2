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
        while True:
            self.game.show_background(self.screen)
            self.game.show_pieces(self.screen)
            dragger = self.game.dragger
            board = self.game.board

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQUARE_SIZE
                    clicked_column = dragger.mouseX // SQUARE_SIZE

                    if board.squares[clicked_row][clicked_column].has_piece():
                        piece = board.squares[clicked_row][clicked_column].piece
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)

                # mouse motion
                if event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        pass

                # click release
                if event.type == pygame.MOUSEBUTTONUP:
                    pass

                # quit app
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.mainloop()
