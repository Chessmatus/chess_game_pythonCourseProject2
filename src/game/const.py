import socket

WIDTH = 850
HEIGHT = 650

BOARD_SIDE = 600
DIFF = 25
FPS = 30

ROWS = 8
COLUMNS = 8

SQUARE_SIZE = BOARD_SIDE // COLUMNS
BUTTON_SIZE_L = 100
BUTTON_SIZE_W = 50

MOVE_BTN_SIZE = 12

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def get_self_hostname():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    hostname = s.getsockname()[0]
    s.close()
    return hostname


HOST = get_self_hostname()


