import customtkinter
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Message import Message
from User import User
from PersonalFinanceManager import PersonalFinanceManager
from Auth import Login, Registration
import tkinter as tk
from tkinter import ttk


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.user = User("", "", "", "")
        self.finance_manager = PersonalFinanceManager(self.user.name,
                                                      self.user.username, self.user.password, self.user.email)
        self.logged_in = False
        self.title("Aplikasi Management Keuangan Mahasiswa UTY Hebat")
        self.geometry("700x450")
        self.message = Message(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.income_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.expense_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent")

        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame, text="Dashboard", compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="> Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")
        self.income_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="> Pemasukan",
                                                     fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                     anchor="w", command=self.pemasukan_button_event)
        self.income_button.grid(row=2, column=0, sticky="ew")

        self.expense_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="> Pengeluaran",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.pengeluaran_button_event)
        self.expense_button.grid(row=3, column=0, sticky="ew")
        self.mode_label = customtkinter.CTkLabel(
            self.navigation_frame, text="Saldo: Rp. 0", compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.mode_label.grid(row=5, column=0, padx=20, pady=20)
        self.mode_button = customtkinter.CTkButton(self.navigation_frame, text="Light",
                                                   command=self.toggle_mode)
        self.mode_button.grid(row=6, column=0, padx=20, pady=20, sticky="s")
        self.home_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.registration_frame = Registration(self, app_instance=self)
        self.login_frame = Login(self, app_instance=self)
        self.login_frame.grid(row=0, column=1, sticky="nsew")
        self.select_frame_by_name("login")

    def update_saldo_label(self):
        saldo = self.finance_manager.get_saldo(self.user.username)
        self.mode_label.configure(text=f"Saldo: Rp. {saldo}")

    def create_graphs(self):
        self.update_saldo_label()
        self.finance_manager.sync_data(self.user.username)
        figure, (monthly_income_ax, monthly_expenses_ax) = plt.subplots(
            1, 2, figsize=(14, 4))

        income_data = self.finance_manager.get_data_pemasukan()
        expenses_data = self.finance_manager.get_data_pengeluaran_harian()
        monthly_income_data = self.aggregate_data_by_month(income_data)
        monthly_expenses_data = self.aggregate_data_by_month(expenses_data)
        monthly_income_ax.plot(monthly_income_data.keys(
        ), monthly_income_data.values(), marker='o', linestyle='-')
        monthly_income_ax.set_title("Pemasukan Bulanan")
        monthly_income_ax.set_xlabel("Bulan")
        monthly_income_ax.set_ylabel("Total Pemasukan")
        monthly_expenses_ax.plot(monthly_expenses_data.keys(
        ), monthly_expenses_data.values(), marker='o', linestyle='-')
        monthly_expenses_ax.set_title("Pengeluaran Bulanan")
        monthly_expenses_ax.set_xlabel("Bulan")
        monthly_expenses_ax.set_ylabel("Total Pengeluaran")
        canvas = FigureCanvasTkAgg(figure, master=self.home_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=1, column=0, padx=20, pady=20)

    def aggregate_data_by_month(self, data_list):
        monthly_data = {}
        for entry in data_list:
            date = datetime.datetime.strptime(
                entry["tanggal"], "%Y-%m-%d %H:%M:%S")
            month_year_key = date.strftime("%B %Y")
            if month_year_key not in monthly_data:
                monthly_data[month_year_key] = entry["jumlah"]
            else:
                monthly_data[month_year_key] += entry["jumlah"]
        return monthly_data

    def home_button_event(self):
        self.select_frame_by_name("home")
        self.select_frame_by_name("home")
        self.create_graphs()

    def hide_all_frames(self):
        self.login_frame.grid_forget()
        self.home_frame.grid_forget()
        self.registration_frame.grid_forget()
        self.income_frame.grid_forget()
        self.expense_frame.grid_forget()

    def select_frame_by_name(self, name):

        if not self.logged_in and name not in ["login", "register"]:
            self.message.show_error("Please login first")
            return
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.income_button.configure(
            fg_color=("gray75", "gray25") if name == "income" else "transparent")
        self.expense_button.configure(
            fg_color=("gray75", "gray25") if name == "expense" else "transparent")
        self.hide_all_frames()
        if name == "login":
            self.login_frame.grid(row=0, column=1, sticky="nsew")
        elif name == "register":
            self.registration_frame.grid(row=0, column=1, sticky="nsew")
        elif name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
            self.create_graphs()
            self.update_saldo_label()
            self.finance_manager.sync_data(self.user.username)
        elif name == "income":
            self.create_income_frame()
            self.income_frame.grid(row=0, column=1, sticky="nsew")
            self.update_saldo_label()
            self.finance_manager.sync_data(self.user.username)
        elif name == "expense":
            self.create_expense_frame()
            self.expense_frame.grid(row=0, column=1, sticky="nsew")
            self.update_saldo_label()
            self.finance_manager.sync_data(self.user.username)

    def toggle_mode(self):
        if customtkinter.get_appearance_mode() == "Dark":
            customtkinter.set_appearance_mode("Light")
            self.mode_button.configure(text="Dark")
        else:
            customtkinter.set_appearance_mode("Dark")
            self.mode_button.configure(text="Light")

    def home_button_event(self):
        self.select_frame_by_name("home")

    def pemasukan_button_event(self):
        self.select_frame_by_name("income")

    def pengeluaran_button_event(self):
        self.select_frame_by_name("expense")

    def create_income_frame(self):
        self.income_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.income_frame.grid_columnconfigure(0, weight=1)
        self.income_label = customtkinter.CTkLabel(
            self.income_frame, text="Input Pemasukan", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.income_label.grid(row=0, column=0, padx=20, pady=20)
        self.income_entry = customtkinter.CTkEntry(self.income_frame)
        self.income_entry.grid(row=1, column=0, padx=20, pady=10)
        self.income_entry.insert(0, "Jumlah")
        self.income_entry.bind(
            "<Button-1>", lambda event: self.income_entry.delete(0, "end"))
        self.description_entry = customtkinter.CTkEntry(self.income_frame)
        self.description_entry.grid(row=2, column=0, padx=20, pady=10)
        self.description_entry.insert(0, "Deskripsi")
        self.description_entry.bind(
            "<Button-1>", lambda event: self.description_entry.delete(0, "end"))
        self.submit_button = customtkinter.CTkButton(
            self.income_frame, text="Submit", command=self.submit_income)
        self.submit_button.grid(row=3, column=0, padx=20, pady=10)

        # table
        datafortable = self.finance_manager.get_data_pemasukan()
        self.table = ttk.Treeview(self.income_frame, columns=(
            "Jumlah", "Tanggal", "Deskripsi"))
        self.table.heading("#0", text="No")
        self.table.heading("Jumlah", text="Jumlah")
        self.table.heading("Tanggal", text="Tanggal")
        self.table.heading("Deskripsi", text="Deskripsi")
        self.table.column("#000", width=50)
        self.table.column("Jumlah", width=100)
        self.table.column("Tanggal", width=100)
        self.table.column("Deskripsi", width=100)
        self.table.grid(row=4, column=0, padx=20, pady=10)
        for i in range(len(datafortable)):
            self.table.insert(parent="", index="end", iid=i, text=i, values=(
                datafortable[i]["jumlah"], datafortable[i]["tanggal"], datafortable[i]["deskripsi"]))
        self.table.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        item = self.table.selection()[0]
        data = self.table.item(item, "values")
        result = self.finance_manager.delete_pemasukan(
            data[0], data[1], data[2], self.user.username)
        if result:
            self.message.show_checkmark("Pemasukan Berhasil Dihapus")
        else:
            self.message.show_error("Pemasukan Gagal Dihapus")
        self.table.delete(item)

    def submit_income(self):
        income = int(self.income_entry.get())
        description = self.description_entry.get()
        resin = self.finance_manager.pemasukan_keuangan(
            income, description, self.user.username)
        if resin:
            self.message.show_checkmark("Pemasukan Berhasil")
        else:
            self.message.show_error("Pemasukan Gagal")

    def create_expense_frame(self):
        self.expense_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.expense_frame.grid_columnconfigure(0, weight=1)
        self.expense_label = customtkinter.CTkLabel(
            self.expense_frame, text="Input Pengeluaran", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.expense_label.grid(row=0, column=0, padx=20, pady=20)
        self.expense_entry = customtkinter.CTkEntry(self.expense_frame)
        self.expense_entry.grid(row=1, column=0, padx=20, pady=10)
        self.expense_entry.insert(0, "Jumlah")
        self.expense_entry.bind(
            "<Button-1>", lambda event: self.expense_entry.delete(0, "end"))
        self.description_entry = customtkinter.CTkEntry(self.expense_frame)
        self.description_entry.grid(row=2, column=0, padx=20, pady=10)
        self.description_entry.insert(0, "Deskripsi")
        self.description_entry.bind(
            "<Button-1>", lambda event: self.description_entry.delete(0, "end"))
        self.submit_button = customtkinter.CTkButton(
            self.expense_frame, text="Submit", command=self.submit_expense)
        self.submit_button.grid(row=3, column=0, padx=20, pady=10)

        # table
        datafortable = self.finance_manager.get_data_pengeluaran_harian()
        self.table = ttk.Treeview(self.expense_frame, columns=(
            "Jumlah", "Tanggal", "Deskripsi"))
        self.table.heading("#0", text="No")
        self.table.heading("Jumlah", text="Jumlah")
        self.table.heading("Tanggal", text="Tanggal")
        self.table.heading("Deskripsi", text="Deskripsi")
        self.table.column("#000", width=50)
        self.table.column("Jumlah", width=100)
        self.table.column("Tanggal", width=100)
        self.table.column("Deskripsi", width=100)
        self.table.grid(row=4, column=0, padx=20, pady=10)

        for i in range(len(datafortable)):
            self.table.insert(parent="", index="end", iid=i, text=i, values=(
                datafortable[i]["jumlah"], datafortable[i]["tanggal"], datafortable[i]["deskripsi"]))
        self.table.bind("<Double-1>", self.on_double_click1)

    def on_double_click1(self, event):
        item = self.table.selection()[0]
        data = self.table.item(item, "values")
        result = self.finance_manager.delete_pengeluaran(
            data[0], data[1], data[2], self.user.username)
        if result:
            self.message.show_checkmark("Pengeluaran Berhasil Dihapus")
        else:
            self.message.show_error("Pengeluaran Gagal Dihapus")
        self.table.delete(item)

    def submit_expense(self):
        expense = int(self.expense_entry.get())
        description = self.description_entry.get()
        retult = self.finance_manager.pengeluaran_harian(
            expense, description, self.user.username)
        if retult:
            self.message.show_checkmark("Pengeluaran Berhasil")
        else:
            self.message.show_error("Pengeluaran Gagal")


if __name__ == "__main__":
    app = App()
    app.mainloop()
