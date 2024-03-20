from packaging.version import Version
from modules.UpdateUi import UpdateUi
from modules import proxy
import customtkinter
import requests
import logging
import json
import os

version = "1.2"

# set image path
image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
theme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "themes")

# Create a handler to display log messages in the GUI


class TkinterHandler(logging.Handler):
    """
    A logging handler that outputs logs to a Tkinter Text widget.

    Args:
        text_widget (customtkinter.CTkTextbox): The Text widget to output logs to.
    """

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
        self.text_widget.update()


class RootApp(customtkinter.CTk):
    """
    The main class for the application, which sets up the Tkinter GUI and handles all related functionality.
    """

    def __init__(self):
        super().__init__()

        # set up title and bitmap
        self.title("Proxy Settings")
        self.wm_iconbitmap(os.path.join(image_path, "verbindung.ico"))

        # set theme
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme(
            os.path.join(theme_path, "lavender.json"))
        self.geometry("330x330")
        self.resizable(False, False)

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

        # Create the main frame for widgets
        self.frame = customtkinter.CTkFrame(
            master=self, fg_color="transparent")
        self.frame.pack(pady=15, padx=15, fill="both", expand=True)

        self.horizontal_frame = customtkinter.CTkFrame(
            master=self.frame, fg_color="transparent")
        self.horizontal_frame.grid(
            row=0, column=0, sticky="ew", padx=5, pady=5)
        self.frame.grid_columnconfigure(
            0, weight=1)

        # Proxy Address Entry
        self.entry_ip = customtkinter.CTkEntry(
            self.horizontal_frame, width=75, justify="center", placeholder_text="Proxy ip-address")
        self.entry_ip.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.entry_ip.insert(0, proxy.fill_in_ip())
        self.entry_ip.bind("<Return>", command=self.proxy_changer)

        # Proxy Port Entry
        self.entry_port = customtkinter.CTkEntry(
            self.horizontal_frame, width=50, justify="center", placeholder_text="Proxy port")
        self.entry_port.grid(row=0, column=1, sticky="ew", padx=(0, 5))
        self.entry_port.insert(0, proxy.fill_in_port())
        self.entry_port.bind("<Return>", command=self.proxy_changer)

        # Apply Button
        self.button = customtkinter.CTkButton(
            self.horizontal_frame, width=50, text="Apply", command=self.proxy_changer)
        self.button.grid(row=0, column=2, sticky="ew")

        # Configure horizontal frame's columns to distribute space
        self.horizontal_frame.grid_columnconfigure(
            0, weight=3)
        self.horizontal_frame.grid_columnconfigure(
            1, weight=1)
        self.horizontal_frame.grid_columnconfigure(
            2, weight=1)

        # Proxy ON/OFF Switch
        self.switch = customtkinter.CTkSwitch(
            master=self.frame, text="Turn Proxy ON/OFF", progress_color="green", command=self.proxy_toggle)
        self.switch.grid(row=1, column=0, sticky="w", padx=5, pady=(10, 0))

        # Status Label
        self.label = customtkinter.CTkLabel(
            master=self.frame, text="Disabled", text_color="red")
        self.label.grid(row=1, column=0, sticky="e", padx=15, pady=(10, 0))

        # check for software update
        self.check_update()

        # check current settings and set switch/label
        if proxy.status_check():
            self.switch.select()
            self.label.configure(text="Enabled", text_color="green")
        proxy.server_check()

    def proxy_changer(self, event=None):
        """
        Changes the proxy address to the value entered in the Tkinter Entry widget.

        Args:
            event (Event, optional): The event that triggered this method. Defaults to None.
        """
        proxy.change_address(f"{self.entry_ip.get()}:{self.entry_port.get()}")

    def proxy_toggle(self):
        """
        Toggles the proxy on or off based on the value of the switch.
        If the switch is off, the proxy is deactivated and the label text changes to 'Disabled' in red.
        If the switch is on, the proxy is activated and the label text changes to 'Enabled' in green.
        """
        if self.switch.get() == 0:
            if proxy.deactivate():
                self.label.configure(text="Disabled", text_color="red")
            else:
                self.switch.select()
            return

        if self.switch.get() == 1:
            if proxy.activate():
                self.label.configure(text="Enabled", text_color="green")
            else:
                self.switch.deselect()
            return

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
