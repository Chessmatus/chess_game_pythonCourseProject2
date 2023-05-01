import socket
from _thread import *
import sys

from move import Move
from square import Square


server = "10.55.131.80"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)
print("Waiting to connection, Server Started")


def read_last_move(string):
    if string:
        lis = string.split(" ")
        move = Move(Square(int(lis[0]), int(lis[1])), Square(int(lis[2]), int(lis[3])))
    else:
        move = ""
    return move


def make_last_move(move):
    return str(move.initial.row) + " " + str(move.initial.column) + " " + \
        str(move.final.row) + " " + str(move.final.column) if move else ""


player = 0
last_move = [None, None]


def threaded_client(conn, pl):
    conn.send(str.encode(str(pl)))
    reply = ""
    while True:
        try:
            data = read_last_move(conn.recv(2048).decode())
            last_move[pl] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = last_move[0]
                else:
                    reply = last_move[1]
                # print("Received: ", data)
                # print("Sending: ", reply)

            conn.sendall(str.encode(make_last_move(reply)))

        except:
            break

    print("Lost Connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, player))
    player += 1
