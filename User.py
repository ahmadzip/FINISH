class User:
    def __init__(self, name="manzip", username="1", password="1", email="ahamdzipmail@gmail.com"):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.is_logged_in = False

    def login(self, emailusername, password):
        if self.email == emailusername or self.username == emailusername and self.password == password:
            self.is_logged_in = True
            return True
        return False

    def register(self, name, username, password, email):
        if not self.is_logged_in:
            self.name = name
            self.username = username
            self.password = password
            self.email = email
            return True
        return False