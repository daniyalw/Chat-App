import json
import pickle

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

    def check(self, username):
        with open(self.path, 'r') as file:
            contents = json.load(file)

        if username in contents:
            return True
        else:
            return False

class Messages:
    def __init__(self):
        self.path = "messages.json"
        self.mode = "r"
        self.write = "w"

    def get(self):
        with open(self.path, self.mode) as f:
            contents = json.load(f)

        return contents

    def get_username(self, username):
        with open(self.path, self.mode) as f:
            contents = json.load(f)

        return contents[username] if username in contents else False

    def set(self, dictionary):
        with open(self.path, self.write) as f:
            json.dump(dictionary, f, indent=4)
