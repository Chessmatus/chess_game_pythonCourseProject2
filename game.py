import pygame
import os

from const import *
from board import Board
from dragger import Dragger
from sound import Sound


class Game:
    def __init__(self):
        self.board = Board()
        self.next_player = 'white'
        self.dragger = Dragger()
        self.move_sound = Sound(os.path.join('assets/sounds/move.wav'))
        self.capture_sound = Sound(os.path.join('assets/sounds/capture.wav'))

    def show_background(self, surface):
        for row in range(ROWS):
            for column in range(COLUMNS):
                if (row + column) % 2 == 0:
                    color = (255, 211, 155)
                else:
                    color = (139, 87, 66)

                rect = (column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

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
                        img_center = column * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                # color
                color = '#C86464' if (move.final.row + move.final.column) % 2 == 0 else '#C84646'
                # rect
                rect = (move.final.column * SQUARE_SIZE, move.final.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = (244, 247, 116) if (pos.row + pos.column) % 2 == 0 else (214, 207, 76)
                # rect
                rect = (pos.column * SQUARE_SIZE, pos.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def sound_effect(self, captured=False):
        if captured:
            self.capture_sound.play()
        else:
            self.move_sound.play()
