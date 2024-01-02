from Database import Database


class User:
    def __init__(self, name, username, password, email):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.is_logged_in = False
        self.database = Database()

    def login(self, emailusername, password):
        user_data = self.database.get_user_data(emailusername)
        if user_data and user_data["password"] == password:
            self.is_logged_in = True
            self.name = user_data["name"]
            self.username = user_data["username"]
            self.email = user_data["email"]
            self.balance = user_data["balance"]
            self.pemasukan_list = user_data["keuangan"]["pemasukan_list"]
            self.pengeluaran_list = user_data["keuangan"]["pengeluaran_list"]
            return True
        return False

    def register(self, name, username, password, email):
        if self.database.get_user_data(username):
            return False
        return self.database.register_user(name, username, password, email)
