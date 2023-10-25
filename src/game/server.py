import socket
from _thread import *
import pickle

from game import Game


def get_self_hostname():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    hostname = s.getsockname()[0]
    s.close()
    return hostname


host = get_self_hostname()
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((host, port))
except socket.error as e:
    print(e)

s.listen(4)
print("Waiting to connection, Server Started")
games = {}
id_count = 0


def threaded_client(conn, pl, g_id):
    global id_count
    conn.send(pickle.dumps(str(pl)))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048 * 8))
            if g_id in games:

                if not data:
                    break
                else:
                    if data != 'get':
                        games[g_id][pl].board = data[0]
                        games[g_id][pl].result = data[1]
                        games[g_id][pl].draw_offered_you = data[2]
                        games[g_id][pl].draw_offered_opp = data[3]
                        if pl == 1:
                            reply = (games[g_id][0].board, games[g_id][0].result,
                                     games[g_id][0].draw_offered_you, games[g_id][0].draw_offered_opp)
                        else:
                            reply = (games[g_id][1].board, games[g_id][1].result,
                                     games[g_id][1].draw_offered_you, games[g_id][1].draw_offered_opp)

                    else:
                        reply = games[g_id][pl]

                conn.sendall(pickle.dumps(reply))

            else:
                break

        except:
            break

    print("Lost Connection: ", pl)
    try:
        del games[g_id]
        print("Closing Game", g_id)
    except:
        pass
    id_count -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    id_count += 1
    player = 0
    game_id = (id_count - 1) // 2
    if id_count % 2 == 1:
        games[game_id] = (Game(), Game())
        games[game_id][player].game_id = game_id
    else:
        player = 1
        games[game_id][player].ready = True
        games[game_id][player - 1].ready = True
        games[game_id][player].game_id = game_id

    start_new_thread(threaded_client, (conn, player, game_id))
