import socket
import pickle


def get_self_hostname():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    hostname = s.getsockname()[0]
    s.close()
    return hostname


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = get_self_hostname()
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player_color = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return 'white' if pickle.loads(self.client.recv(2048)) == '0' else 'black'
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048 * 8))
        except socket.error as e:
            print(e)


