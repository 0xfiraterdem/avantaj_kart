import socket


class Communication:
    def __init__(self, IP=None, PORT=None):
        self.TCP = "TCP"
        self.IP = IP
        self.PORT = PORT
        self.socket = None
        self.last_data = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.IP, self.PORT))

    def listen(self):
        data = self.socket.recv(1024)
        self.last_data = data.hex()
        if data.hex()[6:8] != "04":
            self.last_data = data.hex()

    def send(self, data):
        self.socket.sendall(data)

    def close(self):
        self.socket.close()
