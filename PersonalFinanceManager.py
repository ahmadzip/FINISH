import datetime
import random
from User import User
from Database import Database


class PersonalFinanceManager(User):
    def __init__(self, name, username, password, email):
        super().__init__(name, username, password, email)
        self.balance = 0
        self.pemasukan_list = []
        self.pengeluaran_list = []
        self.database = Database()
        self.username = username

    def sync_data(self, username):
        self.username = username
        user_data = self.database.get_user_data(username)
        if user_data and "balance" in user_data:
            self.balance = user_data["balance"]
            self.pemasukan_list = user_data["keuangan"]["pemasukan_list"]
            self.pengeluaran_list = user_data["keuangan"]["pengeluaran_list"]
            return True
        return False

    def pemasukan_keuangan(self, jumlah, deskripsi_deposit, username):
        self.username = username
        if self.is_logged_in:
            self.balance += jumlah
            pemasukan_data = {"jumlah": jumlah, "deskripsi": deskripsi_deposit,
                              "tanggal": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            self.database.keuangan(username, pemasukan=pemasukan_data)
            return True
        return False

    def pengeluaran_harian(self, jumlah, deskripsi_pengeluaran, username):
        self.username = username
        if self.is_logged_in and self.balance >= jumlah:
            self.balance -= jumlah
            pengeluaran_data = {"jumlah": jumlah, "deskripsi": deskripsi_pengeluaran,
                                "tanggal": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            self.database.keuangan(username, pengeluaran=pengeluaran_data)
            return True
        return False

    def get_data_pemasukan(self):
        self.pemasukan_list = []
        for pemasukan in self.database.get_user_data(self.username)["keuangan"]["pemasukan_list"]:
            self.pemasukan_list.append(pemasukan)
        return self.pemasukan_list

    def get_data_pengeluaran_harian(self):
        self.pengeluaran_list = []
        for pengeluaran in self.database.get_user_data(self.username)["keuangan"]["pengeluaran_list"]:
            if pengeluaran["tanggal"].split(" ")[0] == datetime.datetime.now().strftime("%Y-%m-%d"):
                self.pengeluaran_list.append(pengeluaran)
        return self.pengeluaran_list

    def get_saldo(self, username):
        self.username = username
        user_data = self.database.get_user_data(username)

        if user_data and "balance" in user_data:
            self.balance = user_data["balance"]
            return self.balance
        else:
            return 0

    def delete_pemasukan(self, data1, data2, data3, username):
        strrrr = [data1, data3, data2]
        self.username = username
        getdata = self.database.get_user_data(username)
        for i in range(len(getdata["keuangan"]["pemasukan_list"])):
            if getdata["keuangan"]["pemasukan_list"][i]["tanggal"] == strrrr[2]:
                getdata["keuangan"]["pemasukan_list"].pop(i)
                self.database.save_data()
                return True

        for i in range(len(self.pemasukan_list)):
            if self.pemasukan_list[i]["tanggal"] == strrrr[2]:
                self.pemasukan_list.pop(i)
                self.database.save_data()
                return True
        return False

    def delete_pengeluaran(self, data1, data2, data3, username):
        strrrr = [data1, data3, data2]
        self.username = username
        getdata = self.database.get_user_data(username)
        for i in range(len(getdata["keuangan"]["pengeluaran_list"])):
            if getdata["keuangan"]["pengeluaran_list"][i]["tanggal"] == strrrr[2]:
                getdata["keuangan"]["pengeluaran_list"].pop(i)
                self.database.save_data()
                return True

        for i in range(len(self.pengeluaran_list)):
            if self.pengeluaran_list[i]["tanggal"] == strrrr[2]:
                self.pengeluaran_list.pop(i)
                self.database.save_data()
                return True
        return False
