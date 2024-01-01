import customtkinter
from Message import Message


class Registration(customtkinter.CTkFrame):
    def __init__(self, master, app_instance, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self.app_instance = app_instance
        self.message = Message(app_instance)
        self.grid_columnconfigure(0, weight=1)
        self.registration_label = customtkinter.CTkLabel(
            self, text="Registration", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.registration_label.grid(row=0, column=0, padx=20, pady=20)
        self.fullname_entry = customtkinter.CTkEntry(self)
        self.fullname_entry.grid(row=1, column=0, padx=20, pady=10)
        self.fullname_entry.insert(0, "Fullname")
        self.fullname_entry.bind(
            "<Button-1>", lambda event: self.fullname_entry.delete(0, "end"))
        self.username_entry = customtkinter.CTkEntry(self)
        self.username_entry.grid(row=2, column=0, padx=20, pady=10)
        self.username_entry.insert(0, "Username")
        self.username_entry.bind(
            "<Button-1>", lambda event: self.username_entry.delete(0, "end"))
        self.email_entry = customtkinter.CTkEntry(self)
        self.email_entry.grid(row=3, column=0, padx=20, pady=10)
        self.email_entry.insert(0, "Email")
        self.email_entry.bind(
            "<Button-1>", lambda event: self.email_entry.delete(0, "end"))
        self.password_entry = customtkinter.CTkEntry(
            self, show="*")
        self.password_entry.grid(row=4, column=0, padx=20, pady=10)
        self.password_entry.insert(0, "Password")
        self.register_button = customtkinter.CTkButton(
            self, text="Register", command=self.register_event)
        self.login_button = customtkinter.CTkButton(
            self, text="Login", command=self.login_event)
        self.register_button.grid(row=5, column=0, padx=20, pady=10)
        self.login_button.grid(row=6, column=0, padx=20, pady=10)

    def register_event(self):
        fullname = self.fullname_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        if not fullname or not username or not email or not password:
            self.message.show_error("Please fill all fields")
            return
        if not self.app_instance.user.is_logged_in and self.app_instance.user.register(fullname, username, password, email):
            self.message.show_checkmark("Registration successful")
            print(self.app_instance.user.username,
                  self.app_instance.user.password)
        else:
            self.message.show_error("Registration failed")
            self.app_instance.user = self.app_instance.user

    def login_event(self):
        self.app_instance.select_frame_by_name("login")


class Login(customtkinter.CTkFrame):
    def __init__(self, master, app_instance, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self.app_instance = app_instance
        self.message = Message(app_instance)
        self.grid_columnconfigure(0, weight=1)
        self.login_label = customtkinter.CTkLabel(
            self, text="Login", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=20, pady=20)
        self.username_entry = customtkinter.CTkEntry(self)
        self.username_entry.grid(row=1, column=0, padx=20, pady=10)
        self.username_entry.insert(0, "Username")
        self.username_entry.bind(
            "<Button-1>", lambda event: self.username_entry.delete(0, "end"))
        self.password_entry = customtkinter.CTkEntry(
            self, show="*")
        self.password_entry.grid(row=2, column=0, padx=20, pady=10)
        self.password_entry.insert(0, "Password")
        self.password_entry.bind(
            "<Button-1>", lambda event: self.password_entry.delete(0, "end"))
        self.login_button = customtkinter.CTkButton(
            self, text="Login", command=self.login_event)
        self.register_button = customtkinter.CTkButton(
            self, text="Register", command=self.register_event)
        self.login_button.grid(row=3, column=0, padx=20, pady=10)
        self.register_button.grid(row=4, column=0, padx=20, pady=10)

    def login_event(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            self.message.show_error("Please fill all fields")
            return
        if self.app_instance.user.login(username, password):
            self.message.show_checkmark("Login successful")
            self.app_instance.logged_in = True
            self.app_instance.finance_manager.is_logged_in = True
            self.app_instance.select_frame_by_name("home")
        else:
            self.message.show_error("Login failed")

    def register_event(self):
        self.app_instance.select_frame_by_name("register")
