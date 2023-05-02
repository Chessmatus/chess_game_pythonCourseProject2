import copy
import sys
import pygame
import pickle

from const import *
from game import Game
from square import Square
from move import Move

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
        self.game = Game()

    def mainloop(self):

        n = Network()
        self.game.player_color = n.player_color
        print(self.game.player_color)
        dragger = self.game.dragger
        clock = pygame.time.Clock()

        while True:
            # show methods
            clock.tick(FPS)
            self.game.show_board_background(self.screen)
            self.game.show_out_of_board_back(self.screen)
            self.game.show_coordinates(self.screen)
            self.game.show_last_move(self.screen)
            self.game.show_moves(self.screen)
            self.game.show_pieces(self.screen)

            board = n.send(self.game.board)
            if board.last_move() and correct_move(board, self.game.player_color) != \
                    correct_move(self.game.board, self.game.player_color):
                print(board.last_move(), " : ", self.game.board.last_move())
                self.game.board = board
                print("-- ", board.last_move(), " : ", self.game.board.last_move())
            # print(type(self.game.board))
            '''last_move = n.send(self.game.board.last_move())
            print(last_move, ": ", self.game.board.last_move())
            if last_move != self.game.board.last_move():
                self.game.get_move_on_board(self.screen, last_move)'''

            if dragger.dragging:
                dragger.update_blit(self.screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = (dragger.mouseY - DIFF) // SQUARE_SIZE
                    clicked_column = (dragger.mouseX - DIFF) // SQUARE_SIZE

                    if Square.in_range(clicked_row, clicked_column):
                        self.mouse_down_board(clicked_row, clicked_column, event.pos)


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
                self.game.show_board_background(self.screen)
                self.game.show_out_of_board_back(self.screen)
                self.game.show_coordinates(self.screen)
                self.game.show_last_move(self.screen)
                self.game.show_moves(self.screen)
                self.game.show_pieces(self.screen)

    def mouse_motion(self, pos):
        dragger = self.game.dragger
        if dragger.dragging:
            dragger.update_mouse(pos)
            # show methods
            self.game.show_board_background(self.screen)
            self.game.show_out_of_board_back(self.screen)
            self.game.show_coordinates(self.screen)
            self.game.show_last_move(self.screen)
            self.game.show_moves(self.screen)
            self.game.show_pieces(self.screen)
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
                self.game.sound_effect(captured)
                # show methods
                self.game.show_board_background(self.screen)
                self.game.show_out_of_board_back(self.screen)
                self.game.show_coordinates(self.screen)
                self.game.show_last_move(self.screen)
                self.game.show_pieces(self.screen)
                # next turn
                self.game.next_turn()
            dragger.piece.clear_moves()

        dragger.undrag_piece()


main = Main()
main.mainloop()

# print(read_last_move("3 3 4 4"))
