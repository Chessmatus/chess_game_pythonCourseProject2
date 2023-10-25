import pygame

from const import *
from board import Board
from dragger import Dragger


class Game:
    def __init__(self):
        self.board = Board()
        self.player_color = None
        self.dragger = Dragger()
        self.result = None
        self.draw_offered_opp = False
        self.draw_offered_you = False
        self.ready = False
        self.game_id = None

    def connected(self):
        return self.ready

    def show_game(self, surface, btns, release=False):
        if not self.connected():
            self.show_board_background(surface)
            self.show_out_of_board_back(surface, btns)
            self.show_coordinates(surface)
            self.show_pieces(surface)

        else:
            self.show_board_background(surface)
            self.show_out_of_board_back(surface, btns)
            self.show_coordinates(surface)
            self.show_last_move(surface)
            if not release:
                self.show_moves(surface)
            self.show_pieces(surface)

    def show_board_background(self, surface):
        for row in range(ROWS):
            for column in range(COLUMNS):
                if (row + column) % 2 == 0:
                    color = (255, 211, 155)
                else:
                    color = (139, 87, 66)

                rect = (column * SQUARE_SIZE + DIFF, row * SQUARE_SIZE + DIFF, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_out_of_board_back(self, surface, btns, connected=False):
        rect_back = (ROWS * SQUARE_SIZE + 2 * DIFF, 0, WIDTH - BOARD_SIDE - 2 * DIFF, HEIGHT)
        pygame.draw.rect(surface, (51, 51, 51), rect_back)

        f = pygame.font.SysFont('arial', 15)
        text_you = f.render('YOU', True, WHITE)
        text_opp = f.render('OPPONENT', True, WHITE)
        text_you_won = f.render('YOU(WON)', True, WHITE)
        text_you_lost = f.render('YOU(LOST)', True, WHITE)
        text_opp_lost = f.render('OPPONENT(LOST)', True, WHITE)
        text_opp_won = f.render('OPPONENT(WON)', True, WHITE)
        text_opp_draw = f.render('OPPONENT(DRAW)', True, WHITE)
        text_you_draw = f.render('YOU(DRAW)', True, WHITE)
        text_waiting = f.render("WAITING FOR OPPONENT...", True, WHITE)
        text_off_opp_draw = f.render("(OFFERED DRAW)", True, WHITE)
        text_off_you_draw = f.render("YOU(OFFERED DRAW)", True, WHITE)
        center_waiting = [(6 * DIFF + (COLUMNS * SQUARE_SIZE), DIFF + SQUARE_SIZE // 2),
                          (6 * DIFF + (COLUMNS * SQUARE_SIZE), DIFF + SQUARE_SIZE // 2 + 7 * SQUARE_SIZE)]

        if self.connected():
            for i in range(3):
                btns[i].draw(surface)
            center = [(6 * DIFF + (COLUMNS * SQUARE_SIZE), DIFF + SQUARE_SIZE // 2),
                      (6 * DIFF + (COLUMNS * SQUARE_SIZE), DIFF + SQUARE_SIZE // 2 + 7 * SQUARE_SIZE)]

            if self.result:
                if self.result == 'Lost':
                    pos_lost = text_you_lost.get_rect(center=center[0]) if self.player_color == 'black' \
                        else text_you_lost.get_rect(center=center[1])
                    pos_won = text_opp_won.get_rect(center=center[0]) if self.player_color == 'white' \
                        else text_opp_won.get_rect(center=center[1])
                    surface.blit(text_opp_won, pos_won)
                    surface.blit(text_you_lost, pos_lost)

                elif self.result == 'Won':
                    pos_lost = text_opp_lost.get_rect(center=center[0]) if self.player_color == 'white' \
                        else text_opp_lost.get_rect(center=center[1])
                    pos_won = text_you_won.get_rect(center=center[0]) if self.player_color == 'black' \
                        else text_you_won.get_rect(center=center[1])
                    surface.blit(text_you_won, pos_won)
                    surface.blit(text_opp_lost, pos_lost)

                else:
                    pos_draw_1 = text_opp_draw.get_rect(center=center[0]) if self.player_color == 'white' \
                        else text_opp_draw.get_rect(center=center[1])
                    pos_draw_2 = text_you_draw.get_rect(center=center[0]) if self.player_color == 'black' \
                        else text_you_draw.get_rect(center=center[1])
                    surface.blit(text_you_draw, pos_draw_2)
                    surface.blit(text_opp_draw, pos_draw_1)

            elif self.draw_offered_you or self.draw_offered_opp:
                if self.draw_offered_you:
                    pos_you = text_off_you_draw.get_rect(center=center[0]) if self.player_color == 'black' \
                        else text_off_you_draw.get_rect(center=center[1])
                    surface.blit(text_off_you_draw, pos_you)
                    pos_opp = text_opp.get_rect(center=center[0]) if self.player_color == 'white' \
                        else text_opp.get_rect(center=center[1])
                    surface.blit(text_opp, pos_opp)
                if self.draw_offered_opp:
                    pos_you = text_you.get_rect(center=center[0]) if self.player_color == 'black' \
                        else text_you.get_rect(center=center[1])
                    surface.blit(text_you, pos_you)
                    pos_opp = text_off_opp_draw.get_rect(center=center[0]) if self.player_color == 'white' \
                        else text_off_opp_draw.get_rect(center=center[1])
                    surface.blit(text_off_opp_draw, pos_opp)

            else:
                pos_you = text_you.get_rect(center=center[0]) if self.player_color == 'black' \
                    else text_you.get_rect(center=center[1])
                surface.blit(text_you, pos_you)
                pos_opp = text_opp.get_rect(center=center[0]) if self.player_color == 'white' \
                    else text_opp.get_rect(center=center[1])
                surface.blit(text_opp, pos_opp)

        else:
            pos_waiting = text_waiting.get_rect(center=center_waiting[0]) if self.player_color == 'white' \
                else text_waiting.get_rect(center=center_waiting[1])
            surface.blit(text_waiting, pos_waiting)
            pos_you = text_you.get_rect(center=center_waiting[0]) if self.player_color == 'black' \
                else text_you.get_rect(center=center_waiting[1])
            surface.blit(text_you, pos_you)
            btns[3].draw(surface)

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
