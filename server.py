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
        self.rooms = {}
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
                'username':None,
                'room':None
            }

            Thread(target=self.handle_client, args=(client,)).start()

    def create_room(self, name, pswd, sock):
        if self.clients[sock]['username'] == None:
            return

        if name in self.rooms:
            sock.send(f"room:room taken:create".encode("utf-8"))
            return

        self.rooms[name] = pswd
        self.clients[sock]['room'] = name
        sock.send(f"room:success:create".encode("utf-8"))
        sock.send(f"msg:SERVER:{self.clients[sock]['username']} connected".encode("utf-8"))

    def users_in_room(self, name):
        count = 0

        for sock in self.clients:
            if self.clients[sock]['room'] == name:
                count += 1

        return count

    def add_user_to_room(self, sock, room, pswd):
        if self.clients[sock]['username'] == None or self.clients[sock]['room'] != None:
            return "no username"

        if room not in self.rooms:
            return "non-existent room"

        if self.rooms[room] != pswd:
            return "incorrect password"

        self.clients[sock]['room'] = room
        return "correct"

    def del_room(self, name):
        if self.users_in_room(name) == 0:
            del self.rooms[name]

    def send(self, msg, sock):
        sock.send(msg)

    def send_all(self, msg):
        for sock in self.clients:
            sock.send(msg)

    def broadcast_msg(self, msg, room):
        for sock in self.clients:
            if self.clients[sock]['username'] != None and self.clients[sock]['room'] == room:
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
            elif msg.startswith("msg:"):
                if self.clients[client]['username'] == None:
                    del self.clients[client]
                    return

                if self.clients[client]['room'] == None:
                    del self.clients[client]
                    return

                text = msg.split(":")[1]
                fmt = f"msg:{self.clients[client]['username']}:{text}"
                fmt = fmt.encode("utf-8")

                self.broadcast_msg(fmt, self.clients[client]['room'])
            elif msg.startswith("end"):
                room = None

                if self.clients[client]['username'] != None and self.clients[client]['room'] != None:
                    fmt = f"msg:SERVER:{self.clients[client]['username']} left"
                    fmt = fmt.encode("utf-8")

                    room = self.clients[client]['room']
                    self.broadcast_msg(fmt, self.clients[client]['room'])

                del self.clients[client]

                # will delete room if no users left
                if room != None:
                    self.del_room(room)
            elif msg.startswith("logout"):
                room = None

                if self.clients[client]['username'] != None and self.clients[client]['room'] != None:
                    fmt = f"msg:SERVER:{self.clients[client]['username']} left"
                    fmt = fmt.encode("utf-8")

                    room = self.clients[client]['room']
                    self.broadcast_msg(fmt, self.clients[client]['room'])

                self.clients[client]['username'] = None
                self.clients[client]['room'] = None

                # will delete room if no users left
                if room != None:
                    self.del_room(room)
            elif msg.startswith("room:"):
                action = msg.split(":")[1]
                name = msg.split(":")[2]
                pswd = msg.split(":")[3]

                if action == "create":
                    self.create_room(name, pswd, client)
                elif action == "join":
                    ret = self.add_user_to_room(client, name, pswd)

                    if ret != "correct":
                        client.send(f"room:{ret}:join".encode("utf-8"))
                    else:
                        client.send(f"room:success:join".encode("utf-8"))
                        self.broadcast_msg(f"msg:SERVER:{self.clients[client]['username']} connected".encode("utf-8"), name)


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
