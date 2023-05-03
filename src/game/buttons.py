import pygame

from const import *


class Button:
    def __init__(self, text, x, y, color, width, height, size):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.text_size = size

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("arial", self.text_size)
        text = font.render(self.text, True, WHITE)
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2),
                        self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
