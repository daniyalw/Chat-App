from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import ui
from darkdetect import isDark
from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import *

class Client:
    def __init__(self):
        # set variables
        self.remote_ip = "70.64.1.9"
        self.remote_port = 33000
        self.logged = False
        self.username = ""
        self.addr = (self.remote_ip, self.remote_port)

        # socket creation
        self.client_socket = socket(AF_INET, SOCK_STREAM)

        # gui
        self.root = Tk()
        self.root.title("App")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.onopen = ui.LoadingFrame(self.root, self.go_login, self.go_signup)
        self.signup_page = ui.SignupFrame(self.root, self.signup, self.from_signup)
        self.login_page = ui.LoginFrame(self.root, self.login, self.from_login)
        self.loading_ui = ui.LoadingUI(self.root)
        self.chat_ui = ui.ChatUI(self.root, self._send, self.from_chat, self.new)
        self.main_page = ui.MainUI(self.root, self.to_chat)

        self.onopen.pack()

    def new(self, name):
        formatted = f"new:{name}".encode('utf-8')
        self.client_socket.send(formatted)

    def to_chat(self):
        self.switch(self.main_page, self.chat_ui)

    def from_chat(self):
        self.switch(self.chat_ui, self.main_page)

    def _send(self, formatted):
        formatted = f"to:{formatted}"
        formatted = formatted.encode("utf-8")
        self.client_socket.send(formatted)

    def switch(self, frame1, frame2):
        frame1.pack_forget()
        frame2.pack()

    def from_signup(self):
        self.switch(self.signup_page, self.onopen)

    def from_login(self):
        self.switch(self.login_page, self.onopen)

    def go_login(self):
        self.switch(self.onopen, self.login_page)

    def go_signup(self):
        self.switch(self.onopen, self.signup_page)

    def receive(self):
        # main loop
        while True:
            try:
                msg = self.client_socket.recv(1024).decode("utf8")
            except OSError:
                break

            if msg.startswith("signup"):
                result = msg.split(':')[1]
                if result == "True":
                    self.switch(self.loading_ui, self.main_page)
                else:
                    self.username = ""
                    self.switch(self.loading_ui, self.signup_page)

            elif msg.startswith("login"):
                result = msg.split(':')[1]
                if result == "True":
                    self.switch(self.loading_ui, self.main_page)
                else:
                    self.username = ""
                    self.switch(self.loading_ui, self.login_page)

            if msg.startswith("content"):
                msg = str(msg[9:])
                messages = eval(msg)
                msgs = messages

                for person in msgs:
                    for x, i in enumerate(msgs[person]):
                        messages[person][x] = i

                self.chat_ui.set(messages, self.username)

            if msg.startswith("new"):
                result = msg.split(':')[2]
                name = msg.split(':')[1]
                if result == "True":
                    result = True
                else:
                    result = False
                if result:
                    self.chat_ui._insert(name)

    def str_insert(self, string, location, sub):
        return string[:location] + sub + string[location:]

    def signup(self):
        self.username, password = self.signup_page.get()
        self.switch(self.signup_page, self.loading_ui)
        formatted = f"signup:username:{self.username}:password:{password}".encode("utf-8")
        self.client_socket.send(formatted)

    def login(self):
        self.username, password = self.login_page.get()
        self.switch(self.login_page, self.loading_ui)
        formatted = f"login:username:{self.username}:password:{password}".encode("utf-8")
        self.client_socket.send(formatted)

    def on_closing(self, event=None):
        self.client_socket.close()
        self.root.destroy()

    def start(self):
        try:
            self.client_socket.connect(self.addr)
        except:
            showerror("Error", "Unable to connect to server.")

        receive_thread = Thread(target=self.receive)
        receive_thread.start()
        self.root.mainloop()

if __name__ == "__main__":
    client = Client()
    client.start()
