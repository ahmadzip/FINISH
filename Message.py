from CTkMessagebox import CTkMessagebox

class Message:
    def __init__(self, app):
        self.app = app

    def show_info(self, message):
        CTkMessagebox(title="Info", message=message)

    def show_checkmark(self, message):
        CTkMessagebox(message=message, icon="check", option_1="Thanks")

    def show_error(self, message):
        CTkMessagebox(title="Error", message=message, icon="cancel")

    def show_warning(self, message):
        msg = CTkMessagebox(title="Warning Message!", message=message,
                            icon="warning", option_1="Cancel", option_2="Retry")
        if msg.get() == "Retry":
            self.show_warning(message)

    def ask_question(self, message):
        msg = CTkMessagebox(title="Exit?", message=message, icon="question",
                            option_1="Cancel", option_2="No", option_3="Yes")
        response = msg.get()
        if response == "Yes":
            self.app.destroy()
        else:
            print("Click 'Yes' to exit!")
