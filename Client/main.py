import socket
from socket import AF_INET, SOCK_STREAM
from os.path import exists

HOST = "localhost"
PORT = 50009


class Client:
    def __init__(self):
        self.session_id = str()
        self.socket = socket.socket(AF_INET, SOCK_STREAM)
        self.socket.connect((HOST, PORT))

    # def connect(self): Not needed
    #     self.socket.connect((HOST, PORT))

    def load_session_id(self):
        if exists("session_id.dat"):
            with open("session_id.dat", 'r') as f:
                self.session_id = f.readline()

    def save_session_id(self):
        with open("session_id.dat", 'w') as f:
            f.write(self.session_id)

    def log_in(self):
        self.socket.sendall("_login_".encode("utf8"))

        print(self.socket.recv(1024).decode("utf8"))
        username = input(">>")
        self.socket.sendall(username.encode("utf8"))

        print(self.socket.recv(1024).decode("utf8"))
        password = input(">>")
        self.socket.sendall(password.encode("utf8"))

        data = self.socket.recv(1024).decode("utf8")
        if data != "_false_":
            self.session_id = data
            self.save_session_id()
            print("login successfull", self.session_id)
        else:
            print("epic fail")

    def send_msg(self, msg: str):
        self.socket.sendall(msg.encode("utf8"))
        data = self.socket.recv(1024)
        print(data.decode("utf8"))

    def loop(self):
        self.load_session_id()

        with self.socket:
            while not self.session_id:
                try:
                    print("[1] login\n[2] register\n")
                    choice = input("Your choice: ")
                    match choice:
                        case '1':
                            self.log_in()
                        case '2':
                            pass
                        case _:
                            return
                except KeyboardInterrupt:
                    exit(0)
            while self.session_id:
                self.send_msg(input(">>"))


if __name__ == '__main__':
    client = Client()
    client.loop()
