import json


class Database:
    def __init__(self, filename="database.json"):
        self.filename = filename
        self.users_data = self.load_data()

    def load_data(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                for user in data["users"]:
                    balance = 0
                    for pemasukan in user["keuangan"]["pemasukan_list"]:
                        balance += pemasukan["jumlah"]
                    for pengeluaran in user["keuangan"]["pengeluaran_list"]:
                        balance -= pengeluaran["jumlah"]
                    user["balance"] = balance
                return data
        except FileNotFoundError:
            return {"users": []}

    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.users_data, file, indent=2)

    def get_user_data(self, username):
        for user in self.users_data["users"]:
            if user["username"] == username:
                return user
        return None

    def keuangan(self, username, pemasukan=None, pengeluaran=None):
        user_data = self.get_user_data(username)
        if user_data:
            if pemasukan:
                user_data["keuangan"]["pemasukan_list"].append(pemasukan)
            if pengeluaran:
                user_data["keuangan"]["pengeluaran_list"].append(pengeluaran)
            self.save_data()
            balance = 0
            for pemasukan in user_data["keuangan"]["pemasukan_list"]:
                balance += pemasukan["jumlah"]
            for pengeluaran in user_data["keuangan"]["pengeluaran_list"]:
                balance -= pengeluaran["jumlah"]
            user_data["balance"] = balance
            return True

        return False

    def register_user(self, name, username, password, email):
        new_user = {
            "name": name,
            "username": username,
            "password": password,
            "email": email,
            "balance": 0,
            "keuangan": {
                "pemasukan_list": [],
                "pengeluaran_list": []
            }
        }
        self.users_data["users"].append(new_user)
        self.save_data()
        return True
