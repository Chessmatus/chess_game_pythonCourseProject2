import socket


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
            return 'white' if self.client.recv(2048).decode() == '0' else 'black'
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)


