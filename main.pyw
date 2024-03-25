from packaging.version import Version
from modules.UpdateUi import UpdateUi
from modules.WifiUi import WifiUi
from modules.ProxyUi import ProxyUi
from modules import proxy
import customtkinter
import requests
import logging
import json
import os

version = "1.3"

# set image path
image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
theme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "themes")

# Create a handler to display log messages in the GUI


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
        self.geometry("350x330")
        self.resizable(False, False)

        # Create Tabview
        self.tabview = customtkinter.CTkTabview(self, fg_color="transparent")
        self.tabview.pack(fill="both", expand=True)
        self.tabview.add("Proxy Settings")
        self.tabview.add("Wifi Settings")

        self.proxy_ui = ProxyUi(self.tabview.tab("Proxy Settings"), version)
        self.proxy_ui.pack(fill="both", expand=True)

        self.wifi_ui = WifiUi(self.tabview.tab("Wifi Settings"))
        self.wifi_ui.pack(fill="both", expand=True)

        # check for software update
        self.check_update()

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
