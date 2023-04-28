import pygame
from const import *


class Dragger:

    def __init__(self):
        self.piece = None
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_column = 0
        self.dragging = False

    def update_blit(self):
        pass

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos

    def save_initial(self, pos):
        self.initial_row = pos[1] // SQUARE_SIZE
        self.initial_column = pos[0] // SQUARE_SIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False
