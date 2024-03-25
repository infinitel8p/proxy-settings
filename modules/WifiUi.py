import customtkinter


class WifiUi(customtkinter.CTkFrame):
    def __init__(self, parent):

        # Main Frame
        super().__init__(master=parent)
        self.configure(fg_color="transparent")
        self.root = parent

        self.qnumber_text = customtkinter.CTkLabel(
            master=self, text="Test", wraplength=150, font=("Arial", 12))
        self.qnumber_text.pack(anchor="center")
