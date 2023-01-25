from packaging.version import Version
from modules.UpdateUi import UpdateUi
from modules import proxy
import customtkinter
import requests
import logging
import json
import os

version = "1.1"

# set image path
image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

# Create a handler to display log messages in the GUI


class TkinterHandler(logging.Handler):
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget
        self.text_widget.configure(state='disabled')
        self.log_format = logging.Formatter('%(levelname)s: %(message)s\n')

    def emit(self, record):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(
            customtkinter.END, self.log_format.format(record))
        self.text_widget.see(customtkinter.END)
        self.text_widget.configure(state='disabled')
        self.text_widget.update()  # Refresh the widget


class RootApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # set up title and bitmap
        self.title("Proxy Settings")
        self.wm_iconbitmap(os.path.join(image_path, "verbindung.ico"))

        # set theme
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.geometry("325x330")

        self.version_label = customtkinter.CTkLabel(
            self, text=f"version {version}", text_color="grey", font=("Arial", 10))
        self.version_label.pack(side=customtkinter.BOTTOM)

        # Set up the log output widget
        self.log_output = customtkinter.CTkTextbox(self)
        self.log_output.pack(side=customtkinter.BOTTOM,
                             fill=customtkinter.BOTH, expand=True, padx=5)

        # Set up the logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        # Add the TkinterHandler to the logger
        self.handler = TkinterHandler(self.log_output)
        self.logger.addHandler(self.handler)

        # create frame for entry and button
        self.frame = customtkinter.CTkFrame(
            master=self, fg_color="transparent")
        self.frame.pack(anchor="n", pady=15, padx=15, side=customtkinter.TOP)

        self.vertical_frame_1 = customtkinter.CTkFrame(
            master=self.frame, fg_color="transparent")
        self.vertical_frame_1.grid(padx=7.5, column=0, row=0, sticky="n")

        self.vertical_frame_2 = customtkinter.CTkFrame(
            master=self.frame, fg_color="transparent")
        self.vertical_frame_2.grid(padx=7.5, column=1, row=0, sticky="n")

        self.entry = customtkinter.CTkEntry(
            self.vertical_frame_1, width=150, placeholder_text="Enter new Proxy address")
        self.entry.grid(column=0, row=0, sticky="w", pady=(0, 7.5))
        self.entry.insert(0, proxy.fill_in())

        self.button = customtkinter.CTkButton(
            self.vertical_frame_2, width=75, text="Apply")
        self.button.grid(column=1, row=0, pady=(0, 7.5))
        self.button.bind("<Button-1>", command=self.proxy_changer)

        self.switch = customtkinter.CTkSwitch(
            self.vertical_frame_1, text="Turn Proxy ON/OFF", progress_color="green", command=self.proxy_toggle)
        self.switch.grid(column=0, row=1, sticky="w", pady=(7.5, 0))

        self.label = customtkinter.CTkLabel(
            self.vertical_frame_2, text="Disabled", text_color="red")
        self.label.grid(column=1, row=1, pady=(7.5, 0))

        # check for software update
        self.check_update()

        # check current settings and set switch/label
        if proxy.status_check():
            self.switch.select()
            self.label.configure(text="Enabled", text_color="green")
        proxy.server_check()

    def proxy_changer(self, event=None):
        proxy.change_address(self.entry.get())

    def proxy_toggle(self):
        if self.switch.get() == 0:
            proxy.deactivate()
            self.label.configure(text="Disabled", text_color="red")
        if self.switch.get() == 1:
            proxy.activate()
            self.label.configure(text="Enabled", text_color="green")

    def check_update(self, version=version):
        """Checks for new releases on Github. If a new release is available, it downloads and 'installs' it.
        Args:
            version (_type_, optional): The current version of the software. This parameter is used to check if a new version is available.
            Defaults to the version of the software that is currently running.
        """

        url = "https://api.github.com/repos/infinitel8p/proxy-settings/releases"
        self.version = version

        try:
            # Send a get request to the GitHub releases api
            releases_response = requests.get(url)
            releases_data = json.loads(releases_response.text)
            # Get the latest release versions
            self.version = Version(self.version.replace("v", ""))
            self.latest_version = Version(
                releases_data[0]["tag_name"].replace("v", ""))
            logging.info(
                f"Current version: {self.version} | Latest release: {self.latest_version}")
            if self.latest_version > self.version:
                # if update available show update gui
                update = UpdateUi(self)
                update.grab_set()
                self.wait_window(update)
                # check if update has been started
                if update.updating:
                    self.destroy()
                    import sys
                    sys.exit()
        except (KeyError, IndexError):
            # If there is an error in the response, print an error message
            logging.info(
                "Error: Failed to retrieve version information from GitHub.")
        except requests.exceptions.HTTPError as errh:
            logging.info(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            logging.info(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            logging.info(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            logging.info(f"Something Else: {err}")
        except Exception as e:
            logging.info(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    root = RootApp()
    root.mainloop()
