import datetime
import random

from User import User


class PersonalFinanceManager(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.balance = 0
        self.pemasukan_list = []
        self.pengeluaran_list = []
        self.generate_fake_data()

    def generate_fake_data(self):
        for month in range(5, 13):
            fake_date = datetime.datetime(2023, month, 1, 6, 0, 0)
            self.pemasukan_list.append(
                {"jumlah": 2000000, "deskripsi": "Gaji", "tanggal": fake_date.strftime("%Y-%m-%d %H:%M:%S")})

        for month in range(5, 13):
            days_in_month = (datetime.datetime(2023, month %
                             12 + 1, 1) - datetime.datetime(2023, month, 1)).days
            for day in range(1, days_in_month + 1):
                daily_expense = {
                    "jumlah": random.randint(30000, 60000),
                    "tanggal": datetime.datetime(2023, month, day, 12, 0, 0).strftime("%Y-%m-%d %H:%M:%S")
                }
                categories = ["Makan", "Jajan", "Bensin"]
                category = random.choice(categories)
                daily_expense["deskripsi"] = category
                self.pengeluaran_list.append(daily_expense)

        print("Fake data generated")
        print(self.pemasukan_list)
        print(self.pengeluaran_list)

    def get_data_pemasukan(self):
        return self.pemasukan_list

    def get_data_pengeluaran_harian(self):
        return self.pengeluaran_list
