import socket
from _thread import *
import pickle

from board import Board


server = "10.55.131.80"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)
print("Waiting to connection, Server Started")

boards = [Board(), Board()]
player = 0


def threaded_client(conn, pl):
    conn.send(pickle.dumps(str(pl)))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048 * 6))
            boards[pl] = data

            if not data:
                print("Waiting for move...")
                break
            else:
                if pl == 1:
                    reply = boards[0]
                else:
                    reply = boards[1]
                # print(pl, ": Received: ", data.last_move())
                # print(pl, ": Sending: ", reply.last_move())

            conn.sendall(pickle.dumps(reply))

        except:
            break

    print("Lost Connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, player))
    player += 1
