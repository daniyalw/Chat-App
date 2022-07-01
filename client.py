from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

from tkinter import *
from tkinter.scrolledtext import *
from tkinter.commondialog import *
from tkinter.simpledialog import *
from tkinter.messagebox import *
from tkinter.ttk import *

import sys

class BeginningUI(Frame):
    def __init__(self, root, login, signup):
        self.root = root
        Frame.__init__(self, root)

        self.login_btn = Button(self, text="Login", command=login)
        self.signup_btn = Button(self, text="Signup", command=signup)

        self.login_btn.grid(row=0, column=0, padx=10, pady=10)
        self.signup_btn.grid(row=1, column=0, padx=10, pady=10)

class LoginUI(Frame):
    def __init__(self, root, login, back):
        self.root = root
        Frame.__init__(self, root)

        self.utext = Label(self, text="Username: ")
        self.ptext = Label(self, text="Password: ")

        self.uentry = Entry(self)
        self.pentry = Entry(self, show="*")

        self.submit_b = Button(self, text="Submit", command=login)
        self.back_b = Button(self, text="Back", command=back)
        self.message = Label(self)

        self.utext.grid(row=0, column=0, padx=10, pady=10)
        self.uentry.grid(row=0, column=1, padx=10, pady=10)
        self.ptext.grid(row=1, column=0, padx=10, pady=10)
        self.pentry.grid(row=1, column=1, padx=10, pady=10)
        self.submit_b.grid(row=3, column=1, padx=10, pady=10)
        self.back_b.grid(row=3, column=0, padx=10, pady=10)
        self.message.grid(row=5, column=0, padx=10, pady=10)

    def get(self):
        username = self.uentry.get()
        password = self.pentry.get()
        return username, password

    def message_config(self, message):
        self.message.config(text=message)

    def delete_all_from_entry(self):
        self.uentry.delete(0, END)
        self.pentry.delete(0, END)

class SignupUI(Frame):
    def __init__(self, root, signup, back):
        self.root = root
        Frame.__init__(self, root)

        self.utext = Label(self, text="Username: ")
        self.ptext = Label(self, text="Password: ")

        self.uentry = Entry(self)
        self.pentry = Entry(self, show="*")

        self.submit_b = Button(self, text="Submit", command=signup)
        self.back_b = Button(self, text="Back", command=back)
        self.message = Label(self)

        self.utext.grid(row=0, column=0, padx=10, pady=10)
        self.uentry.grid(row=0, column=1, padx=10, pady=10)
        self.ptext.grid(row=1, column=0, padx=10, pady=10)
        self.pentry.grid(row=1, column=1, padx=10, pady=10)
        self.submit_b.grid(row=3, column=1, padx=10, pady=10)
        self.back_b.grid(row=3, column=0, padx=10, pady=10)
        self.message.grid(row=5, column=0, padx=10, pady=10)

    def get(self):
        username = self.uentry.get()
        password = self.pentry.get()
        return username, password

    def message_config(self, message):
        self.message.config(text=message)

    def delete_all_from_entry(self):
        self.uentry.delete(0, END)
        self.pentry.delete(0, END)

class JoinServerUI(Frame):
    def __init__(self, root, join_chatroom):
        self.root = root
        Frame.__init__(self, root)

        # for joining a server
        self.jntext = Label(self, text="Join server name: ")
        self.jname = Entry(self)

        self.jptext = Label(self, text="Join server pswd: ")
        self.jpswd = Entry(self)

        self.jerr = Label(self)
        self.jbtn = Button(self, text="Submit", command=join_chatroom)

        self.jntext.grid(row=0, column=0, padx=10, pady=10)
        self.jname.grid(row=0, column=1, padx=10, pady=10)
        self.jptext.grid(row=1, column=0, padx=10, pady=10)
        self.jpswd.grid(row=1, column=1, padx=10, pady=10)
        self.jerr.grid(row=2, column=0, padx=10, pady=10)
        self.jbtn.grid(row=2, column=1, padx=10, pady=10)

    def get(self):
        return self.jname.get(), self.jpswd.get()

    def delete_all_from_entry(self):
        self.jname.delete(0, END)
        self.jpswd.delete(0, END)

class CreateServerUI(Frame):
    def __init__(self, root, create_room):
        self.root = root
        Frame.__init__(self, root)

        # for creating a server
        self.cntext = Label(self, text="Create server name: ")
        self.cname = Entry(self)

        self.cptext = Label(self, text="Create server pswd: ")
        self.cpswd = Entry(self)

        self.cerr = Label(self)
        self.cbtn = Button(self, text="Submit", command=create_room)

        self.cntext.grid(row=0, column=0, padx=10, pady=10)
        self.cname.grid(row=0, column=1, padx=10, pady=10)
        self.cptext.grid(row=1, column=0, padx=10, pady=10)
        self.cpswd.grid(row=1, column=1, padx=10, pady=10)
        self.cerr.grid(row=2, column=0, padx=10, pady=10)
        self.cbtn.grid(row=2, column=1, padx=10, pady=10)

    def get(self):
        return self.cname.get(), self.cpswd.get()

    def delete_all_from_entry(self):
        self.cname.delete(0, END)
        self.cpswd.delete(0, END)

class SelectChoiceRoom(Frame):
    def __init__(self, root, create_ui, join_ui):
        self.root = root
        Frame.__init__(self, root)

        self.cbtn = Button(self, text="Create", command=create_ui)
        self.jbtn = Button(self, text="Join", command=join_ui)

        self.cbtn.grid(row=0, column=0, padx=10, pady=10)
        self.jbtn.grid(row=1, column=0, padx=10, pady=10)

class ChatUI(Frame):
    def __init__(self, root, _send, logout, name):
        self.root = root
        Frame.__init__(self, root)

        self._send = _send
        self.name = name

        self.lgt_btn = Button(self, text="Logout", command=logout)
        self.lgt_btn.grid(row=0, column=4, sticky='nsew')

        self.text = ScrolledText(self) # the messages widget
        self.text.config(highlightbackground="white")
        self.text.config(state='disabled')
        self.text.grid(row=1, rowspan=3, columnspan=4, column=1, sticky='nsew')

        self.content_entry = Text(self, height=2, width=50) # the widget to enter a new messages
        self.content_entry.config(highlightbackground=self.content_entry['highlightcolor'])
        self.content_entry.grid(row=4, column=1, sticky='nsew')

        self.send_b = Button(self, text="Send", command=self.send)
        self.send_b.grid(row=4, column=2, sticky='nsew', padx=20, pady=20)

    def display_new_msg(self, msg, _from):
        self.text.config(state='normal')

        if _from == self.name:
            self.text.insert(END, f"Me: {msg}\n")
        else:
            self.text.insert(END, f"{_from}: {msg}\n")

        self.text.config(state='disabled')

    def send(self):
        content = self.content_entry.get('1.0', 'end-1c')

        if content.strip() == "":
            return

        fmt = f"msg:{content}"

        self.content_entry.delete('1.0', END)

        self._send(fmt)

    def change_my_name(self, new_name):
        self.name = new_name

    def delete_all_from_entry(self):
        self.text.config(state='normal')
        self.text.delete('1.0', END)
        self.text.config(state='disabled')

        self.content_entry.delete('1.0', END)

class LoadingUI(Frame):
    def __init__(self, root):
        self.root = root
        Frame.__init__(self, root)

        self.label = Label(self, text="Loading...");
        self.label.pack()

class Client:
    def __init__(self):
        self.remote_ip = "127.0.0.1"
        self.remote_port = 33000
        self.remote_addr = (self.remote_ip, self.remote_port)
        self.name = ""

        self.client_socket = socket(AF_INET, SOCK_STREAM)

        self.root = Tk()
        self.root.title("Chat App")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.first_ui = BeginningUI(self.root, self.from_first_to_login, self.from_first_to_signup)
        self.login_ui = LoginUI(self.root, self.login, self.from_login_to_first)
        self.signup_ui = SignupUI(self.root, self.signup, self.from_signup_to_first)
        self.select_ui = SelectChoiceRoom(self.root, self.from_select_to_create, self.from_select_to_join)
        self.join_ui = JoinServerUI(self.root, self.join_room)
        self.create_ui = CreateServerUI(self.root, self.create_room)
        self.chat_ui = ChatUI(self.root, self.send, self.logout, self.name)
        self.loading_ui = LoadingUI(self.root)

        self.first_ui.pack()

    def switch(self, frame1, frame2):
        frame1.pack_forget()
        frame2.pack()

    def from_first_to_login(self):
        self.switch(self.first_ui, self.login_ui)

    def from_login_to_first(self):
        self.switch(self.login_ui, self.first_ui)

    def from_first_to_signup(self):
        self.switch(self.first_ui, self.signup_ui)

    def from_signup_to_first(self):
        self.switch(self.signup_ui, self.first_ui)

    def from_login_to_chat(self):
        self.switch(self.login_ui, self.chat_ui)

    def from_signup_to_chat(self):
        self.switch(self.signup_ui, self.chat_ui)

    def from_loading_to_chat(self):
        self.switch(self.loading_ui, self.chat_ui)

    def from_select_to_create(self):
        self.switch(self.select_ui, self.create_ui)

    def from_select_to_join(self):
        self.switch(self.select_ui, self.join_ui)

    def send_msg(self, msg):
        msg = msg.encode("utf-8")
        self.client_socket.send(msg)

    def login(self):
        self.name, pswd = self.login_ui.get()
        fmt = f"login:{self.name}:{pswd}"
        self.switch(self.login_ui, self.loading_ui)
        self.send_msg(fmt)

    def signup(self):
        self.name, pswd = self.signup_ui.get()
        fmt = f"signup:{self.name}:{pswd}"
        self.switch(self.signup_ui, self.loading_ui)
        self.send_msg(fmt)

    def send(self, fmt):
        self.send_msg(fmt)

    def join_room(self):
        name, pswd = self.join_ui.get()
        self.switch(self.join_ui, self.loading_ui)
        self.send(f"room:join:{name}:{pswd}")

    def create_room(self):
        name, pswd = self.create_ui.get()
        self.switch(self.create_ui, self.loading_ui)
        self.send(f"room:create:{name}:{pswd}")

    def handler(self):
        while True:
            try:
                msg = self.client_socket.recv(1024).decode("utf8")
            except OSError:
                break

            if msg.startswith("login:"):
                result = msg.split(":")[1]

                if result.startswith("True"):
                    self.chat_ui.change_my_name(self.name)
                    self.switch(self.loading_ui, self.select_ui)
                else:
                    self.name = ""
                    self.switch(self.loading_ui, self.login_ui)
                    self.login_ui.message_config("Incorrect username/pswd.")
            elif msg.startswith("signup:"):
                result = msg.split(":")[1]

                if result == "True":
                    self.chat_ui.change_my_name(self.name)
                    self.switch(self.loading_ui, self.select_ui)
                else:
                    self.name = ""
                    self.switch(self.loading_ui, self.signup_ui)
                    self.signup_ui.message_config("Username taken.");
            elif msg.startswith("msg:"):
                _from = msg.split(":")[1]
                _msg = msg.split(":")[2]

                self.chat_ui.display_new_msg(_msg, _from)
            elif msg.startswith("room:"):
                succ = msg.split(":")[1]
                action = msg.split(":")[2]

                if succ == "success":
                    self.switch(self.loading_ui, self.chat_ui)
                else:
                    if action == "create":
                        self.create_ui.cerr.config(text=succ)
                        self.switch(self.loading_ui, self.create_ui)
                    else:
                        self.join_ui.jerr.config(text=succ)
                        self.switch(self.loading_ui, self.join_ui)

    def on_closing(self):
        self.send_msg("end")
        self.client_socket.close()
        self.root.destroy()

    def logout(self):
        self.name = ""
        self.chat_ui.change_my_name("")
        self.switch(self.chat_ui, self.first_ui)

        self.login_ui.delete_all_from_entry()
        self.signup_ui.delete_all_from_entry()
        self.join_ui.delete_all_from_entry()
        self.create_ui.delete_all_from_entry()
        self.chat_ui.delete_all_from_entry()

        self.send_msg("logout")

    def start(self):
        try:
            self.client_socket.connect(self.remote_addr)
        except:
            showerror("Error", "Unable to connect to server.")
            sys.exit(1)

        receive_thread = Thread(target=self.handler)
        receive_thread.start()
        self.root.mainloop()

if __name__ == "__main__":
    client = Client()
    client.start()
