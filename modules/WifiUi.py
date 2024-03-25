import customtkinter


class WifiUi(customtkinter.CTkFrame):
    def __init__(self, parent):

        # Main Frame
        super().__init__(master=parent)
        self.configure(fg_color="transparent")
        self.root = parent

        # Color of ToolTip bg and fg
        if customtkinter.get_appearance_mode() in ["Dark", "System"]:
            self.bg = "#2b2b2b"
            self.fg = "white"
        if customtkinter.get_appearance_mode() == "Light":
            self.bg = "#dbdbdb"
            self.fg = "black"

        # search qnumber label
        self.qnumber_text = customtkinter.CTkLabel(
            master=self, text="Test", wraplength=150, font=("Arial", 12))
        self.qnumber_text.pack(anchor="center")
