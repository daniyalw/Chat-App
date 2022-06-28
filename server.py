import socket
from threading import Thread
import json

class Auth:
    def __init__(self, path):
        self.path = path

    def login(self, username, password):
        with open(self.path, "r") as file:
            contents = json.load(file)

        if username in contents:
            if str(hash(password)) == contents[username]:
                return True
        return False

    def signup(self, username, password):
        with open(self.path, "r") as file:
            contents = json.load(file)

        if username in contents:
            return False

        contents[username] = str(hash(password))

        with open(self.path, "w") as file:
            json.dump(contents, file, indent=4)

        return True

class Server:
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 33000
        self.addr = (self.ip, self.port)
        self.clients = {}
        self.auth = Auth("pswd.json")

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))

    def accept_incoming_connections(self):
        while True:
            client, client_address = self.server.accept()

            print(f"{client_address} has connected.")

            self.clients[client] = {
                'address':client_address,
                'client':client,
                'username':None
            }

            Thread(target=self.handle_client, args=(client,)).start()

    def send(self, msg, sock):
        sock.send(msg)

    def send_all(self, msg):
        for sock in self.clients:
            sock.send(msg)

    def broadcast_msg(self, msg):
        for sock in self.clients:
            if self.clients[sock]['username'] != None:
                sock.send(msg)

    def handle_client(self, client):
        while True:
            try:
                msg = client.recv(1024).decode('utf-8')
            except OSError:
                break

            if msg.startswith("login:"):
                if self.clients[client]['username'] != None:
                    del self.clients[client]
                    break

                uname = msg.split(":")[1]
                pswd = msg.split(":")[2]

                result = self.auth.login(uname, pswd)

                message = "login:" + str(result)
                message = message.encode("utf-8")
                self.send(message, client)

                if result:
                    self.clients[client]['username'] = uname

                    fmt = f"msg:SERVER:{uname} connected"
                    fmt = fmt.encode("utf-8")
                    self.broadcast_msg(fmt)
            elif msg.startswith("signup:"):
                if self.clients[client]['username'] != None:
                    del self.clients[client]
                    return

                uname = msg.split(":")[1]
                pswd = msg.split(":")[2]

                result = self.auth.signup(uname, pswd)

                message = "signup:" + str(result)
                message = message.encode("utf-8")
                self.send(message, client)

                if result:
                    self.clients[client]['username'] = uname

                    fmt = f"msg:SERVER:{uname} connected"
                    fmt = fmt.encode("utf-8")
                    self.broadcast_msg(fmt)
            elif msg.startswith("msg:"):
                if self.clients[client]['username'] == None:
                    del self.clients[client]
                    return

                text = msg.split(":")[1]
                fmt = f"msg:{self.clients[client]['username']}:{text}"
                fmt = fmt.encode("utf-8")

                self.broadcast_msg(fmt)
            elif msg.startswith("end"):
                fmt = ""
                to_send_fmt = False

                if self.clients[client]['username'] != None:
                    fmt = f"msg:SERVER:{self.clients[client]['username']} left"
                    fmt = fmt.encode("utf-8")
                    to_send_fmt = True

                del self.clients[client]

                if to_send_fmt:
                    self.broadcast_msg(fmt)
            elif msg.startswith("logout"):
                fmt = ""
                to_send_fmt = False

                if self.clients[client]['username'] != None:
                    fmt = f"msg:SERVER:{self.clients[client]['username']} left"
                    fmt = fmt.encode("utf-8")
                    to_send_fmt = True

                self.clients[client]['username'] = None

                if to_send_fmt:
                    self.broadcast_msg(fmt)

    def close(self):
        self.server.close()

    def start(self, listen=5):
        self.server.listen(listen)
        accept = Thread(target=self.accept_incoming_connections)
        accept.start()
        accept.join()

if __name__ == "__main__":
    server = Server()
    server.start()
