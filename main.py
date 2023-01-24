import customtkinter
import proxy
import sys
import os

# set image path
image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")


class RootApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # set up title and bitmap
        self.title("Proxy Settings")
        self.wm_iconbitmap(os.path.join(image_path, "verbindung.ico"))

        # set theme
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        # create frame for entry and button
        self.frame_1 = customtkinter.CTkFrame(
            master=self, fg_color="transparent")
        self.frame_1.pack(anchor="n", pady=15, padx=15, side=customtkinter.TOP)

        self.entry = customtkinter.CTkEntry(
            self.frame_1, width=150, placeholder_text="Enter new Proxy address")
        self.entry.grid(column=0, row=0, padx=(
            0, 7.5), pady=(0, 15), sticky="w")
        self.entry.insert(0, proxy.fill_in())

        self.button = customtkinter.CTkButton(
            self.frame_1, width=75, text="Apply")
        self.button.grid(column=1, row=0, padx=(
            7.5, 0), pady=(0, 15), sticky="e")

        self.label = customtkinter.CTkLabel(
            self.frame_1, text="Turn Proxy ON/OFF:")
        self.label.grid(column=0, row=1, padx=(
            0, 7.5), pady=(0, 15), sticky="w")

        self.switch = customtkinter.CTkSwitch(
            self.frame_1, text="", progress_color="green")
        self.switch.grid(column=1, row=1, pady=(0, 15), sticky="e")


if __name__ == "__main__":
    root = RootApp()
    root.mainloop()
