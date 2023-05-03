import socket
import pickle


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.55.131.80"
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


