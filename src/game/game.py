from const import *
from board import Board
from dragger import Dragger
from sound import Sound

import os
import pygame


class Game:
    def __init__(self):
        self.board = Board()
        self.player_color = None
        self.dragger = Dragger()
        self.move_sound = Sound(os.path.join('assets/sounds/move.wav'))
        self.capture_sound = Sound(os.path.join('assets/sounds/capture.wav'))
        self.result = None

    def show_board_background(self, surface):
        for row in range(ROWS):
            for column in range(COLUMNS):
                if (row + column) % 2 == 0:
                    color = (255, 211, 155)
                else:
                    color = (139, 87, 66)

                rect = (column * SQUARE_SIZE + DIFF, row * SQUARE_SIZE + DIFF, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_out_of_board_back(self, surface):
        rect_back = (ROWS * SQUARE_SIZE + 2 * DIFF, 0, WIDTH - BOARD_SIDE - 2 * DIFF, HEIGHT)
        pygame.draw.rect(surface, (51, 51, 51), rect_back)

        f = pygame.font.SysFont('arial', 15)
        text_you = f.render('YOU:', True, WHITE)
        text_opp = f.render('OPPONENT:', True, WHITE)
        text_won = f.render('WON', True, WHITE)
        text_lost = f.render('LOST', True, WHITE)
        text_draw = f.render('DRAW', True, WHITE)

        center = [(4 * DIFF + (COLUMNS * SQUARE_SIZE), DIFF + SQUARE_SIZE // 2),
                  (4 * DIFF + (COLUMNS * SQUARE_SIZE), DIFF + SQUARE_SIZE // 2 + 7 * SQUARE_SIZE)]
        pos_you = text_you.get_rect(center=center[0]) if self.player_color == 'black' \
            else text_you.get_rect(center=center[1])
        pos_opp = text_opp.get_rect(center=center[0]) if self.player_color == 'white' \
            else text_opp.get_rect(center=center[1])
        surface.blit(text_you, pos_you)
        surface.blit(text_opp, pos_opp)

        if self.result:
            center_1 = [(7 * DIFF + (COLUMNS * SQUARE_SIZE), DIFF + SQUARE_SIZE // 2),
                      (7 * DIFF + (COLUMNS * SQUARE_SIZE), DIFF + SQUARE_SIZE // 2 + 7 * SQUARE_SIZE)]
            if self.result == 'Lost':
                pos_lost = text_lost.get_rect(center=center_1[0]) if self.player_color == 'black' \
                    else text_lost.get_rect(center=center_1[1])
                pos_won = text_won.get_rect(center=center_1[0]) if self.player_color == 'white' \
                    else text_won.get_rect(center=center_1[1])
                surface.blit(text_won, pos_won)
                surface.blit(text_lost, pos_lost)

            elif self.result == 'Won':
                pos_lost = text_lost.get_rect(center=center_1[0]) if self.player_color == 'white' \
                    else text_lost.get_rect(center=center_1[1])
                pos_won = text_won.get_rect(center=center_1[0]) if self.player_color == 'black' \
                    else text_won.get_rect(center=center_1[1])
                surface.blit(text_won, pos_won)
                surface.blit(text_lost, pos_lost)

            else:
                pos_draw_1 = text_draw.get_rect(center=center_1[0])
                pos_draw_2 = text_draw.get_rect(center=center_1[1])
                surface.blit(text_draw, pos_draw_1)
                surface.blit(text_draw, pos_draw_2)



        color_frame = (139,71,38)
        rect_up = (0, 0, BOARD_SIDE + 2 * DIFF, DIFF)
        rect_left = (0, DIFF, DIFF, BOARD_SIDE + DIFF)
        rect_down = (DIFF, BOARD_SIDE + DIFF, BOARD_SIDE + DIFF, DIFF)
        rect_right = (BOARD_SIDE + DIFF, DIFF, DIFF, BOARD_SIDE)
        pygame.draw.rect(surface, color_frame, rect_up)
        pygame.draw.rect(surface, color_frame, rect_left)
        pygame.draw.rect(surface, color_frame, rect_down)
        pygame.draw.rect(surface, color_frame, rect_right)

    def show_coordinates(self, surface):
        f = pygame.font.SysFont('arial', 12)
        cols = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        rows = ('8', '7', '6', '5', '4', '3', '2', '1')
        for col in range(COLUMNS):
            text = f.render(cols[col], True, WHITE)
            center = DIFF + (col * SQUARE_SIZE + SQUARE_SIZE // 2), DIFF + ROWS * SQUARE_SIZE + DIFF // 2
            pos = text.get_rect(center=center)
            surface.blit(text, pos)

        for row in range(ROWS):
            text = f.render(rows[row], True, WHITE)
            center = DIFF // 2, DIFF + (row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pos = text.get_rect(center=center)
            surface.blit(text, pos)

        rect_white = (DIFF + COLUMNS * SQUARE_SIZE + (DIFF // 2 - MOVE_BTN_SIZE // 2),
                      DIFF + ROWS * SQUARE_SIZE + (DIFF // 2 - MOVE_BTN_SIZE // 2),
                      MOVE_BTN_SIZE, MOVE_BTN_SIZE)
        rect_black = (DIFF + COLUMNS * SQUARE_SIZE + (DIFF // 2 - MOVE_BTN_SIZE // 2), (DIFF // 2 - MOVE_BTN_SIZE // 2),
                      MOVE_BTN_SIZE, MOVE_BTN_SIZE)
        if self.board.next_player == 'black':
            pygame.draw.rect(surface, BLACK, rect_black)
        else:
            pygame.draw.rect(surface, WHITE, rect_white)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for column in range(COLUMNS):
                # piece ?
                if self.board.squares[row][column].has_piece():
                    piece = self.board.squares[row][column].piece

                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture).convert_alpha()
                        img_center = column * SQUARE_SIZE + SQUARE_SIZE // 2 + DIFF,\
                            row * SQUARE_SIZE + SQUARE_SIZE // 2 + DIFF
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                # color
                color = '#C86464' if (move.final.row + move.final.column) % 2 == 0 else '#C84646'
                # rect
                rect = (move.final.column * SQUARE_SIZE + DIFF,
                        move.final.row * SQUARE_SIZE + DIFF, SQUARE_SIZE, SQUARE_SIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        if self.board.last_move():
            initial = self.board.last_move().initial
            final = self.board.last_move().final

            for pos in [initial, final]:
                # color
                color = (244, 247, 116) if (pos.row + pos.column) % 2 == 0 else (214, 207, 76)
                # rect
                rect = (pos.column * SQUARE_SIZE + DIFF,
                        pos.row * SQUARE_SIZE + DIFF, SQUARE_SIZE, SQUARE_SIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def next_turn(self):
        self.board.next_player = 'white' if self.board.next_player == 'black' else 'black'

    def sound_effect(self, captured=False):
        if captured:
            self.capture_sound.play()
        else:
            self.move_sound.play()

    def get_move_on_board(self, surface, move):
        if self.board.squares[move.initial.row][move.initial.column].has_piece() and \
                self.board.squares[move.initial.row][move.initial.column].piece.color == self.board.next_player:
            piece = self.board.squares[move.initial.row][move.initial.column].piece
            self.board.calc_moves(piece, move.initial.row, move.initial.column)
            if self.board.valid_move(piece, move):
                captured = self.board.squares[move.final.row][move.final.column].has_piece()
                self.board.move(piece, move)
                # sound
                self.sound_effect(captured)
                # show methods
                self.show_board_background(surface)
                self.show_out_of_board_back(surface)
                self.show_coordinates(surface)
                self.show_last_move(surface)
                self.show_pieces(surface)
                # next turn
                self.next_turn()
            piece.clear_moves()
