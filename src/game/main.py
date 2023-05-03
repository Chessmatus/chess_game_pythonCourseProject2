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
        self.results = [0, 0, 0]
        self.altered_result = False
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = None
        self.move_sound = Sound(os.path.join('assets/sounds/move.wav'))
        self.capture_sound = Sound(os.path.join('assets/sounds/capture.wav'))
        self.btns = []
        self.btns.append(Button("RESIGN", 4 * DIFF + COLUMNS * SQUARE_SIZE,
                                DIFF + SQUARE_SIZE + SQUARE_SIZE // 2, (255, 0, 0), 100, 75, 20))
        self.btns.append(Button("DRAW", 4 * DIFF + COLUMNS * SQUARE_SIZE,
                                DIFF + 3 * SQUARE_SIZE + SQUARE_SIZE // 2, (0, 255, 0), 100, 75, 20))
        self.btns.append(Button("EXIT", 4 * DIFF + COLUMNS * SQUARE_SIZE,
                                DIFF + 5 * SQUARE_SIZE + SQUARE_SIZE // 2, (0, 0, 255), 100, 75, 20))
        self.btns.append(Button("BACK", 4 * DIFF + COLUMNS * SQUARE_SIZE,
                                DIFF + 3 * SQUARE_SIZE + SQUARE_SIZE // 2, (0, 0, 255), 100, 75, 20))

    def menu_screen(self):
        run = True
        clock = pygame.time.Clock()
        btns = []
        btns.append(Button("PLAY", WIDTH // 3 - 100, HEIGHT // 2 - 25, (255, 0, 0), 200, 50, 20))
        btns.append(Button("RESULTS", 2 * WIDTH // 3 - 100, HEIGHT // 2 - 25, (255, 0, 0), 200, 50, 20))

        while run:
            clock.tick(60)
            self.screen.fill((128, 128, 128))
            btns[0].draw(self.screen)
            btns[1].draw(self.screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btns[0].click(event.pos):
                        run = False
                    if btns[1].click(event.pos):
                        self.get_results()
        try:
            self.mainloop()
        except:
            pass

    def get_results(self):
        run = True
        font = pygame.font.SysFont("arial", 40)
        text_wins = font.render(f"WINS: {self.results[0]}", True, WHITE)
        text_draws = font.render(f"DRAWS: {self.results[1]}", True, WHITE)
        text_loses = font.render(f"LOSES: {self.results[2]}", True, WHITE)
        back_btn = Button("BACK", WIDTH // 2 - text_wins.get_width() // 2,
                          HEIGHT // 2 - text_wins.get_height() // 2 + 200, (0, 255, 0), 175, 75, 40)

        while run:
            self.screen.fill((128, 128, 128))
            self.screen.blit(text_wins, (WIDTH // 2 - text_wins.get_width() // 2,
                                         HEIGHT // 2 - text_wins.get_height() // 2 - 100))
            self.screen.blit(text_draws, (WIDTH // 2 - text_wins.get_width() // 2,
                                          HEIGHT // 2 - text_wins.get_height() // 2))
            self.screen.blit(text_loses, (WIDTH // 2 - text_wins.get_width() // 2,
                                          HEIGHT // 2 - text_wins.get_height() // 2 + 100))
            back_btn.draw(self.screen)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_btn.click(event.pos):
                        run = False

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
        self.altered_result = False

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
            try:
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
            except:
                run = False

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
                        elif self.btns[0].click(event.pos):
                            self.game.result = 'Lost'
                        elif self.btns[1].click(event.pos):
                            self.game.draw_offered_you = True
                        elif self.btns[2].click(event.pos):
                            run = False

                    # mouse motion
                    elif event.type == pygame.MOUSEMOTION:
                        self.mouse_motion(event.pos)

                    # click release
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.mouse_release(event.pos)

                elif self.game.connected():
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        if self.btns[2].click(event.pos):
                            run = False

                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        if self.btns[3].click(event.pos):
                            run = False

                # quit app
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False

            if self.game.result and not self.altered_result:
                if self.game.result == 'Won':
                    self.results[0] += 1
                elif self.game.result == 'Lost':
                    self.results[2] += 1
                else:
                    self.results[1] += 1

                self.altered_result = True

            if run:
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
while True:
    try:
        main.menu_screen()
    except:
        break
