from tkinter import *
from tkinter.scrolledtext import *
from tkinter.commondialog import *
from tkinter.simpledialog import *
from tkinter.ttk import *

class LoadingUI(Frame):
    def __init__(self, root):
        self.root = root
        Frame.__init__(self, root)

        self.label = Label(self, text="Loading...")

        self.label.pack(anchor="c")

class LoadingFrame(Frame):
    def __init__(self, root, login, signup):
        self.root = root
        Frame.__init__(self, root)

        self.login_button = Button(self, text="Login", command=login)
        self.signup_button = Button(self, text="Signup", command=signup)

        self.login_button.grid(row=0, column=0, padx=10, pady=10)
        self.signup_button.grid(row=1, column=0, padx=10, pady=10)

class LoginFrame(Frame):
    def __init__(self, root, login, back):
        self.root = root
        Frame.__init__(self, root)
        self.login = login
        self.back = back
        self.create_widgets()

    def create_widgets(self):
        self.user_l = Label(self, text="Username: ")
        self.user_b = Entry(self)
        self.pswd_l = Label(self, text="Password: ")
        self.pswd_b = Entry(self, show="*")
        self.submit_b = Button(self, text="Submit", command=self.login)
        self.back_b = Button(self, text="Back", command=self.back)
        self.message = Label(self)

        self.user_l.grid(row=0, column=0, padx=10, pady=10)
        self.user_b.grid(row=0, column=1, padx=10, pady=10)
        self.pswd_l.grid(row=1, column=0, padx=10, pady=10)
        self.pswd_b.grid(row=1, column=1, padx=10, pady=10)
        self.submit_b.grid(row=3, column=1, padx=10, pady=10)
        self.back_b.grid(row=3, column=0, padx=10, pady=10)
        self.message.grid(row=5, column=0, padx=10, pady=10)

    def get(self):
        username = self.user_b.get()
        password = self.pswd_b.get()
        return username, password

    def message_config(self, message):
        self.message.config(text=message)

class SignupFrame(Frame):
    def __init__(self, root, signup, back):
        self.root = root
        Frame.__init__(self, root)
        self.signup = signup
        self.back = back
        self.create_widgets()

    def create_widgets(self):
        self.user_l = Label(self, text="Username: ")
        self.user_b = Entry(self)
        self.pswd_l = Label(self, text="Password: ")
        self.pswd_b = Entry(self, show="*")
        self.submit_b = Button(self, text="Submit", command=self.signup)
        self.back_b = Button(self, text="Back", command=self.back)
        self.message = Label(self)

        self.user_l.grid(row=0, column=0, padx=10, pady=10)
        self.user_b.grid(row=0, column=1, padx=10, pady=10)
        self.pswd_l.grid(row=1, column=0, padx=10, pady=10)
        self.pswd_b.grid(row=1, column=1, padx=10, pady=10)
        self.submit_b.grid(row=3, column=1, padx=10, pady=10)
        self.back_b.grid(row=3, column=0, padx=10, pady=10)
        self.message.grid(row=5, column=0, padx=10, pady=10)

    def get(self):
        username = self.user_b.get()
        password = self.pswd_b.get()
        return username, password

    def message_config(self, message):
        self.message.config(text=message)

class ChatUI(Frame):
    def __init__(self, root, send, back, new):
        self.root = root
        self.messages = None
        self.iid = 0
        self._send = send
        self.name = ""
        self._new = new
        self.to = ""
        self.load = True
        Frame.__init__(self, root)

        self.back_b = Button(self, text="Back", command=back)
        self.back_b.grid(row=0, column=0, sticky='nsew', pady=15)

        self.new_b = Button(self, text="New", command=self.new)
        self.new_b.grid(row=1, column=0, sticky='nsew', pady=15)

        self.tree = Treeview(self)
        self.tree.heading("#0", text="Messages")
        self.tree.bind("<<TreeviewSelect>>", self.select)
        self.tree.grid(rowspan=2, row=2, column=0, sticky='nsew')
        self.tree['height'] = 20

        self.text = ScrolledText(self)
        self.text['height'] += 4
        self.text.config(highlightbackground="white")
        self.text.config(state='disabled')
        self.text.grid(row=0, rowspan=3, columnspan=4, column=1, sticky='nsew')

        self.content_entry = Text(self, height=2, width=50)
        self.content_entry.config(highlightbackground=self.content_entry['highlightcolor'])
        self.content_entry.grid(row=3, column=1, sticky='nsew')

        self.send_b = Button(self, text="Send", command=self.send)
        self.send_b.grid(row=3, column=2, sticky='nsew', padx=20, pady=20)

    def new(self):
        name = askstring("New", "Enter name: ")
        self.content_entry.config(state='normal')
        self._new(name)

    def send(self):
        msg = self.content_entry.get('1.0', 'end-1c')

        if msg.strip() == "":
            return

        self.text.config(state='normal')
        self.to = self.get_name()
        formatted = f"{self.to}: {msg}"
        fmt = f"{self.name}: {msg}"
        self.text.insert(END, fmt+'\n')
        self.text.config(state='disabled')
        self._send(formatted)

    def get_name(self):
        selected = self.tree.focus()
        if not selected:
            return False

        name = self.tree.item(selected, "text")
        return name

    def select(self, event=None):
        selected = self.tree.focus()
        if not selected:
            return

        name = self.tree.item(selected, "text")
        if name in self.messages:
            self.text.config(state='normal')
            self.text.delete('1.0', END)

            messages = self.messages[name]
            for message in messages:
                self.text.insert(END, message+"\n")
            self.text.config(state='disabled')

            self.to = name

    def get(self):
        name = self.get_name()
        if not name:
            name = ""
        message = self.content_entry.get('end-1c')
        return name, message

    def reset(self):
        self.tree_clear()
        for person in self.messages:
            self._insert(person)

    def new_content(self, content):
        if self.get_name() != False:

            name = self.get_name()
            self.text.config(state='normal')
            self.text.delete('1.0', END)

            for message in content[self.name]:
                self.text.insert(END, message + "\n")

            self.text.config(state='disabled')

        self.reset()

    def _insert(self, name):
        self.tree.insert('', END, iid=self.iid, text=name)
        self.iid += 1

    def tree_clear(self):
        self.tree.delete(*self.tree.get_children())

    def set(self, messages, name):
        self.messages = messages
        self.name = name
        if self.load:
            self.reset()
            self.load = False
        else:
            self.new_content(messages)


class MainUI(Frame):
    def __init__(self, root, to_chat):
        self.root = root
        Frame.__init__(self, root)

        self.chat_button = Button(self, text="Chat", command=to_chat)
        self.chat_button.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
