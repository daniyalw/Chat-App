import socket
from threading import Thread
import back

class Server:
    def __init__(self):
        self.ip = "10.0.0.199"
        self.port = 33000
        self.addr = (self.ip, self.port)
        self.clients = {}
        self.auth = back.Auth("accounts.json")
        self.messages = back.Messages()

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

    def handle_client(self, client):
        while True:
            try:
                msg = client.recv(1024).decode('utf-8')
            except OSError:
                del self.clients[client]
                return

            if msg.startswith("login"):
                username = msg.split(':')[2]
                password = msg.split(':')[4]
                result = self.auth.login(username, password)
                message = "login:" + str(result)
                message = message.encode("utf-8")
                self.send(message, client)

                if result:
                    self.clients[client]['username'] = username
                    messages = self.messages.get()
                    message = "contents:" + str(messages[username])
                    message = message.encode("utf-8")
                    self.send(message, client)

            elif msg.startswith("signup"):
                username = msg.split(':')[2]
                password = msg.split(':')[4]
                result = self.auth.signup(username, password)
                message = "signup:" + str(result)
                message = message.encode("utf-8")
                self.send(message, client)

                if result:
                    self.clients[client]['username'] = username
                    messages = self.messages.get()
                    messages[username] = {}
                    self.messages.set(messages)

            if msg.startswith("to"):
                to = msg.split(':')[1].strip()
                _from = self.clients[client]['username'].strip()
                message = msg.split(':')[2].strip()

                clients = self.clients

                contents = self.messages.get()
                if to in contents:
                    if _from not in contents[to]:
                        contents[to][_from] = []
                    contents[to][_from].append(f'{_from}:{message}')
                if _from in contents:
                    if to not in contents[_from]:
                        contents[_from][to] = []
                    contents[_from][to].append(f'{_from}:{message}')
                self.messages.set(contents)

                contents = self.messages.get()

                for c in clients: # loop through current connections
                    if self.clients[c]['username'] == to:
                        self.clients[c]['client'].send(("contents:" + str(contents[_from])).encode('utf-8'))
                        sent = True

            if msg.startswith("new"):
                name = msg.split(':')[1]
                result = self.auth.check(name)

                if result:
                    formatted = f"new:{name}:True".encode("utf-8")
                    client.send(formatted)
                else:
                    formatted = f"new:{name}:False".encode("utf-8")
                    client.send(formatted)

    def send(self, msg, sock):
        sock.send(msg)

    def broadcast(self, msg):
        for sock in self.clients:
            sock.send(msg)

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
